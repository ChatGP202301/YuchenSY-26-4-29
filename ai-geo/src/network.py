from __future__ import annotations

import ipaddress
import socket
import threading
import time
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from urllib.robotparser import RobotFileParser

USER_AGENT = "Yuchen-AI-GEO-Audit/1.0 (+https://www.yuchensy.com/)"
MAX_BYTES = 512 * 1024
FETCH_SLOTS = threading.BoundedSemaphore(2)


def validate_public_https(url: str, resolver=socket.getaddrinfo) -> tuple[str, str]:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("only public HTTPS URLs without credentials are allowed")
    if parsed.port not in {None, 443}:
        raise ValueError("only port 443 is allowed")
    addresses = resolver(parsed.hostname, 443, type=socket.SOCK_STREAM)
    if not addresses:
        raise ValueError("DNS returned no addresses")
    for entry in addresses:
        ip = ipaddress.ip_address(entry[4][0])
        if not ip.is_global or ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
            raise ValueError(f"unsafe address: {ip}")
    return parsed.hostname.lower(), parsed.geturl()


class SafeRedirectHandler(HTTPRedirectHandler):
    def __init__(self, origin: str, resolver=socket.getaddrinfo):
        self.origin = origin
        self.resolver = resolver
        self.count = 0

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.count += 1
        if self.count > 5:
            raise ValueError("redirect limit exceeded")
        destination = urljoin(req.full_url, newurl)
        host, _ = validate_public_https(destination, self.resolver)
        if host != self.origin:
            raise ValueError("cross-origin redirect denied")
        return super().redirect_request(req, fp, code, msg, headers, destination)


def robots_allowed(url: str, resolver=socket.getaddrinfo) -> bool:
    parsed = urlsplit(url)
    robots_url = f"https://{parsed.hostname}/robots.txt"
    host, _ = validate_public_https(robots_url, resolver)
    opener = build_opener(SafeRedirectHandler(host, resolver))
    request = Request(robots_url, headers={"User-Agent":USER_AGENT}, method="GET")
    try:
        with opener.open(request, timeout=12) as response:
            payload = response.read(MAX_BYTES + 1)
    except Exception:
        return False
    if len(payload) > MAX_BYTES:
        return False
    return robots_text_allows(payload.decode("utf-8", errors="replace"), url, robots_url)


def robots_text_allows(payload: str, url: str, robots_url: str = "https://example.invalid/robots.txt") -> bool:
    parser = RobotFileParser()
    parser.set_url(robots_url)
    parser.parse(payload.splitlines())
    return parser.can_fetch(USER_AGENT, url)


def safe_get(url: str, resolver=socket.getaddrinfo, sleep=time.sleep) -> dict:
    host, normalized = validate_public_https(url, resolver)
    if not robots_allowed(normalized, resolver):
        raise PermissionError("robots.txt denies or could not safely confirm access")
    sleep(0.5)
    opener = build_opener(SafeRedirectHandler(host, resolver))
    request = Request(normalized, headers={"User-Agent":USER_AGENT, "Accept":"text/html,application/xhtml+xml"}, method="GET")
    with FETCH_SLOTS:
        with opener.open(request, timeout=12) as response:
            content_type = response.headers.get_content_type()
            if content_type not in {"text/html", "application/xhtml+xml", "text/plain"}:
                raise ValueError(f"unsupported content type: {content_type}")
            payload = response.read(MAX_BYTES + 1)
            if len(payload) > MAX_BYTES:
                raise ValueError("response exceeds byte limit")
            final_host, _ = validate_public_https(response.geturl(), resolver)
            if final_host != host:
                raise ValueError("cross-origin final URL denied")
            return {"url":response.geturl(), "status":response.status, "content_type":content_type, "text":payload.decode("utf-8", errors="replace")}
