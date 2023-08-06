# Copyright © 2019-2023 CZ.NIC, z. s. p. o.
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of dns-crawler.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import base64
import re
from itertools import takewhile
from urllib.parse import unquote, urljoin, urlparse
from time import time

import cert_human
from dns_crawler.geoip_utils import geoip_single
import icu
import idna
import requests
import urllib3
from forcediphttpsadapter.adapters import ForcedIPHTTPSAdapter
from requests_toolbelt.adapters.source import SourceAddressAdapter

from .certificate import parse_cert
from .ip_utils import is_valid_ipv6_address

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
cert_human.enable_urllib3_patch()

fallback_encodings = ["windows-1250", "iso-8859-2", "windows-1252"]

CHUNK_SIZE = 10240


class CrawlerAdapter(SourceAddressAdapter, ForcedIPHTTPSAdapter):
    pass


def create_request_headers(domain, user_agent, accept_language):
    if not domain:
        host = None
    elif is_valid_ipv6_address(domain):
        host = f"[{domain}]"
    else:
        try:
            host = idna.encode(domain).decode("ascii")
        except idna.core.InvalidCodepoint:
            host = domain
        except idna.core.IDNAError:
            host = None
    return {
        "Host": host,
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "Keep-Alive",
        "Accept-Language": accept_language,
    }


def parse_alt_svc(header):
    result = {}
    for pair in [i.split(";")[0].replace('"', "") for i in re.findall(r"[a-zA-Z0-9-]+=[^,]+", header)]:
        list = unquote(pair).split("=")
        result[list[0]] = list[1]
    return result


def parse_hsts(header):
    result = {}
    items = [i.lower() for i in re.split(r"; ?", header)]
    result["raw"] = header
    result["includeSubdomains"] = "includesubdomains" in items
    result["preload"] = "preload" in items
    try:
        result["max-age"] = [int("".join(takewhile(str.isdigit, re.split(r"[=:]", i)[1])))
                             for i in items if re.sub(r"['\"]", "", i).startswith("max-age")][0]
    except (IndexError, ValueError):
        pass
    return result


def parse_content_length(header):
    result = {}
    result["raw"] = header
    if not header:
        return result
    if not str.isdigit(header[0]):
        return result
    result["value"] = int("".join(takewhile(str.isdigit, header)))
    return result


header_parsers = {
    "alt-svc": parse_alt_svc,
    "strict-transport-security": parse_hsts,
    "content-length": parse_content_length
}


def emsg(e):
    if isinstance(e, (requests.exceptions.Timeout, requests.exceptions.ConnectTimeout)):
        msg = "timeout"
    else:
        msg = str(e)
    return msg


def autodetect_encoding(data, content_type=None, forced_encoding=None):
    if forced_encoding:
        encoding = forced_encoding
    else:
        try:
            encoding = icu.CharsetDetector(data).detect().getName()
        except AttributeError:
            encoding = "utf-8"
    try:
        data = str(data, encoding=encoding)
    except (UnicodeDecodeError, LookupError):
        if content_type and "charset" in content_type.lower():
            content_encoding = re.sub(r".*charset=", "", content_type, flags=re.IGNORECASE)
            return autodetect_encoding(data, forced_encoding=content_encoding)
        if not forced_encoding:
            return autodetect_encoding(data, forced_encoding=fallback_encodings[1])
        else:
            if fallback_encodings[-1] == forced_encoding:
                return (None, None)
            else:
                next_encoding = fallback_encodings[fallback_encodings.index(forced_encoding) + 1]
                return autodetect_encoding(data, forced_encoding=next_encoding)
    return (data, encoding)


def get_webserver_info(domain, ips, config, source_ip, geoip_dbs, path="/", ipv6=False, tls=False):
    if not ips or len(ips) < 1:
        return None
    http_timeout = (config["timeouts"]["http"], config["timeouts"]["http_read"])
    save_content = config["web"]["save_content"]
    save_binary = config["web"]["save_binary"]
    content_size_limit = config["web"]["content_size_limit"]
    max_redirects = config["web"]["max_redirects"]
    protocol = "https" if tls else "http"
    results = []
    ip_index = 0
    for entry in ips:
        ip_index += 1
        if config["web"]["max_ips_per_domain"] is not None and ip_index > config["web"]["max_ips_per_domain"]:
            break
        ip = entry["value"]
        if ip is None:
            continue
        s1 = requests.session()
        s2 = requests.session()
        s1.mount("https://", CrawlerAdapter(dest_ip=ip, source_address=source_ip))
        s2.mount("https://", SourceAddressAdapter(source_address=source_ip))
        s2.mount("http://", SourceAddressAdapter(source_address=source_ip))

        headers = create_request_headers(domain,
                                         config["web"]["user_agent"],
                                         config["web"]["accept_language"])
        first = {}
        try:
            content_bytes = []
            if protocol == "https":
                url = f"{protocol}://{domain}{path}"
                first["r"] = s1.get(url,
                                    allow_redirects=False,
                                    verify=False,
                                    stream=True,
                                    timeout=http_timeout,
                                    headers=headers)
                try:
                    first["ip"] = first["r"].raw._connection.sock.socket.getpeername()[0]
                except AttributeError:
                    first["ip"] = None
                try:
                    first["tls"] = {
                        "version": str(first["r"].raw._fp.fp.raw._sock.connection.get_protocol_version_name()),
                        "cipher_bits": int(first["r"].raw._fp.fp.raw._sock.connection.get_cipher_bits()),
                        "cipher_name": str(first["r"].raw._fp.fp.raw._sock.connection.get_cipher_name())
                    }
                except AttributeError:
                    pass
                chunk_len = 0
                start_time = time()
                for chunk in first["r"].iter_content(CHUNK_SIZE):
                    chunk_len += CHUNK_SIZE
                    content_bytes.append(chunk)
                    if chunk_len > content_size_limit or time() - start_time > config["timeouts"]["http_read"]:
                        first["r"].close()
            else:
                if ipv6:
                    host = f"[{ip}]"
                else:
                    host = ip
                url = f"{protocol}://{host}{path}"
                first["r"] = s2.get(url,
                                    allow_redirects=False,
                                    stream=True,
                                    timeout=http_timeout,
                                    headers=headers)
                try:
                    first["ip"] = first["r"].raw._connection.sock.socket.getpeername()[0]
                except AttributeError:
                    first["ip"] = None
                chunk_len = 0
                start_time = time()
                for chunk in first["r"].iter_content(CHUNK_SIZE):
                    chunk_len += CHUNK_SIZE
                    content_bytes.append(chunk)
                    if chunk_len > content_size_limit or time() - start_time > config["timeouts"]["http_read"]:
                        first["r"].close()
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout,
                ValueError, AttributeError, UnicodeDecodeError,
                requests.exceptions.ContentDecodingError,
                requests.exceptions.ChunkedEncodingError) as e:
            if isinstance(e, AttributeError):
                pass
            else:
                results.append({
                    "ip": ip,
                    "error": emsg(e)
                })
                continue
        first["url"] = url
        redirect_count = 0
        history = [first]
        while "r" in history[-1] and history[-1]["r"].is_redirect:
            content_bytes = []
            location = history[-1]["r"].headers["location"]
            url = urljoin(history[-1]["url"], location)
            h = {
                "url": url
            }
            if location == "":
                h["e"] = "Empty Location header in previous step"
            try:
                h["r"] = s1.get(url,
                                verify=False,
                                allow_redirects=False,
                                stream=True,
                                timeout=http_timeout,
                                headers=create_request_headers(urlparse(url).hostname,
                                                               config["web"]["user_agent"],
                                                               config["web"]["accept_language"])
                                )
                try:
                    h["ip"] = h["r"].raw._connection.sock.socket.getpeername()[0]
                except AttributeError:
                    h["ip"] = None
                try:
                    h["tls"] = {
                        "version": h["r"].raw._fp.fp.raw._sock.connection.get_protocol_version_name(),
                        "cipher_bits": h["r"].raw._fp.fp.raw._sock.connection.get_cipher_bits(),
                        "cipher_name": h["r"].raw._fp.fp.raw._sock.connection.get_cipher_name()
                    }
                except AttributeError:
                    h["tls"] = None
                chunk_len = 0
                start_time = time()
                for chunk in h["r"].iter_content(CHUNK_SIZE):
                    chunk_len += CHUNK_SIZE
                    content_bytes.append(chunk)
                    if chunk_len > content_size_limit or time() - start_time > config["timeouts"]["http_read"]:
                        h["r"].close()
            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout,
                    requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema,
                    requests.exceptions.ContentDecodingError, requests.exceptions.ChunkedEncodingError,
                    UnicodeError, ValueError) as e:
                h["e"] = emsg(e)
            except requests.exceptions.InvalidHeader as e:
                h["e"] = f"Invalid Location header in previous step. '{url}' - {emsg(e)}"
            except urllib3.exceptions.LocationParseError as e:
                h["e"] = emsg(e)
            history.append(h)
            redirect_count = redirect_count + 1
            if redirect_count >= max_redirects:
                break

        steps = []
        for (i, h) in enumerate(history):
            if i == 0:
                url = f"{protocol}://{domain}{path}"
            else:
                url = h["url"]
            if "e" in h:
                steps.append({
                    "url": url,
                    "error": h["e"]
                })
                continue
            step_tls = "r" in h and h["r"].url.startswith("https")
            step = {}
            if "r" in h:
                step["url"] = h["r"].url
                step["status"] = h["r"].status_code
                step["is_redirect"] = h["r"].is_redirect
            cookies = []
            for cookie in h["r"].cookies:
                cookies.append({
                    "domain": cookie.domain,
                    "name": cookie.name,
                    "value": cookie.value,
                    "secure": cookie.secure,
                    "expires": cookie.expires,
                    **cookie.__dict__["_rest"]
                })
            headers = {}
            for k, v in h["r"].headers.items():
                key = k.lower()
                if key == "set-cookie":
                    headers[key] = cookies
                elif key in header_parsers:
                    headers[key] = header_parsers[key](v)
                else:
                    headers[key] = v
            step["headers"] = headers
            if i == 0:
                step["ip"] = ip
            else:
                step["ip"] = h["ip"]
            step["geoip"] = geoip_single(step["ip"], geoip_dbs) if step["ip"] else None
            step["url"] = step["url"].replace(f"//{ip}/", f"//{domain}/").replace(f"//[{ip}]/", f"//{domain}/")
            if step_tls:
                if "tls" in h:
                    step["tls"] = h["tls"]
                if config["web"]["save_cert_chain"]:
                    if h["r"].raw.peer_cert_chain:
                        cert_chain = []
                        for cert in h["r"].raw.peer_cert_chain:
                            cert_chain.append(parse_cert(cert.to_cryptography()))
                        step["cert"] = cert_chain
                else:
                    if h["r"].raw.peer_cert:
                        step["cert"] = [parse_cert(h["r"].raw.peer_cert.to_cryptography())]
            if save_content:
                import magic
                detected_encoding = None
                content = b"".join(content_bytes)
                f = magic.Magic(uncompress=True, mime=True, mime_encoding=True)
                mimetype = f.from_buffer(content).split("; ")
                content_is_binary = mimetype[1] == "charset=binary"

                try:
                    if content_is_binary:
                        if save_binary:
                            content = f"data:{mimetype[0]};base64,"\
                                      f"{base64.b64encode(content).decode()}"
                    else:
                        try:
                            content, detected_encoding = autodetect_encoding(content)
                        except (requests.exceptions.ChunkedEncodingError,
                                requests.exceptions.ContentDecodingError) as e:
                            results.append({
                                "ip": ip,
                                "error": emsg(e)
                            })
                            continue
                except requests.exceptions.ConnectionError:
                    content = None
                if content == "":
                    content = None
                if content is None:
                    detected_encoding = None
                step["content"] = content
                if content_is_binary:
                    step["content_is_binary"] = True
                if detected_encoding is not None:
                    step["detected_encoding"] = detected_encoding.lower()
                step["detected_mimetype"] = mimetype[0]
            h["r"].close()
            steps.append(step)

        result = {
            "ip": ip,
            "redirect_count": redirect_count
        }

        if config["web"]["save_intermediate_steps"]:
            result["steps"] = steps
        else:
            if len(steps) > 0:
                result["final_step"] = steps[-1]
            else:
                result["final_step"] = None
        results.append(result)

        s1.close()
        s2.close()
    if len(results) == 0:
        return None
    return results
