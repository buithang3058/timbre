#!/usr/bin/env python3
"""
SEO cluster audit — quét 1 cụm trang cùng template và kiểm các cổng SEO cơ bản.

Dùng cho các cụm dùng chung template (giá hàng hoá, giá vàng, cổ phiếu…): thay vì
audit tay từng trang, chạy 1 lần ra bảng pass/warn/fail cho cả cụm. Chạy lại được
sau mỗi lần sửa để verify regression.

Usage:
  # Tự lấy slug từ hub /hang-hoa rồi audit cả cụm
  python3 scripts/seo-cluster-audit.py --hub https://simplize.vn/hang-hoa --prefix /hang-hoa

  # Cụm khác: đổi hub + prefix
  python3 scripts/seo-cluster-audit.py --hub https://simplize.vn/gia-vang --prefix /gia-vang

  # URL tự chỉ định
  python3 scripts/seo-cluster-audit.py --urls https://simplize.vn/hang-hoa/wti,https://simplize.vn/hang-hoa/gia-dong

  # Xuất JSON đầy đủ
  python3 scripts/seo-cluster-audit.py --hub https://simplize.vn/hang-hoa --prefix /hang-hoa --json out.json
"""

import argparse
import json
import re
import sys
import warnings
from urllib.parse import urljoin, urlparse

warnings.filterwarnings("ignore")
import requests

UA = "Mozilla/5.0 (compatible; SimplizeSEOAudit/1.0)"
TIMEOUT = 20

# Ngưỡng (điều chỉnh nếu cần)
TITLE_MAX = 60
META_MIN, META_MAX = 120, 160


def fetch(url):
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
        return r.status_code, r.text, r.url, len(r.history)
    except Exception as e:  # noqa: BLE001
        return None, f"__ERROR__ {e}", url, 0


def discover(hub_url, prefix):
    """Lấy danh sách URL con dạng <base><prefix>/<slug> từ trang hub."""
    base = "{u.scheme}://{u.netloc}".format(u=urlparse(hub_url))
    _, html, _, _ = fetch(hub_url)
    slugs = sorted(set(re.findall(re.escape(prefix) + r"/([a-z0-9-]+)", html)))
    return [urljoin(base + "/", prefix.strip("/") + "/" + s) for s in slugs]


def meta_content(html, prop):
    for attr in ("property", "name"):
        m = re.search(
            r'<meta[^>]+' + attr + r'="' + re.escape(prop) + r'"[^>]*content="([^"]*)"',
            html, re.I)
        if m:
            return m.group(1).strip()
    return ""


def link_href(html, rel):
    m = re.search(r'<link[^>]+rel="' + re.escape(rel) + r'"[^>]*href="([^"]*)"', html, re.I)
    return m.group(1).strip() if m else ""


def norm(u):
    return (u or "").rstrip("/")


def visible_text_len(html):
    h = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    return len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip())


def audit_page(url):
    status, html, final_url, n_redir = fetch(url)
    redirected = n_redir > 0 and norm(final_url) != norm(url)
    r = {"url": url, "final_url": final_url, "redirected": redirected,
         "status": status, "gates": {}, "data": {}}
    if status != 200:
        r["gates"]["status"] = "FAIL"
        r["data"]["error"] = html[:120] if isinstance(html, str) else ""
        return r
    r["gates"]["status"] = "redir" if redirected else "ok"

    title = ""
    m = re.search(r"<title[^>]*>([^<]*)</title>", html, re.I)
    if m:
        title = m.group(1).strip()
    desc = meta_content(html, "description")
    canon = link_href(html, "canonical")
    ogurl = meta_content(html, "og:url")
    h1 = len(re.findall(r"<h1[\s>]", html, re.I))
    # JSON-LD: chỉ tính block có nội dung (bỏ placeholder rỗng)
    ld_blocks = re.findall(
        r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S | re.I)
    ld_nonempty = sum(1 for b in ld_blocks if b.strip())
    has_intro = "Giới thiệu về" in html  # section mô tả (description) có render không
    vlen = visible_text_len(html)

    r["data"] = {
        "title": title, "title_len": len(title),
        "desc": desc, "desc_len": len(desc),
        "canonical": canon, "og_url": ogurl,
        "h1": h1, "ld_json": ld_nonempty, "has_intro": has_intro,
        "visible_len": vlen,
    }

    g = r["gates"]
    g["title"] = "ok" if title and len(title) <= TITLE_MAX else ("FAIL" if not title else "WARN")
    g["meta"] = "ok" if desc and META_MIN <= len(desc) <= META_MAX else ("FAIL" if not desc else "WARN")
    # cổng URL: so canonical == og:url == URL trang ĐÃ render (sau redirect).
    consistent = norm(canon) == norm(final_url) and norm(ogurl) == norm(final_url)
    g["url"] = "ok" if consistent else "FAIL"
    g["h1"] = "ok" if h1 == 1 else "WARN"
    g["schema"] = "ok" if ld_nonempty >= 1 else "FAIL"
    g["content"] = "ok" if has_intro else "WARN"
    return r


GLYPH = {"ok": "  ok  ", "WARN": " WARN ", "FAIL": " FAIL ", "redir": "redir "}


def short(url, prefix):
    p = urlparse(url).path
    return p


def main():
    ap = argparse.ArgumentParser(description="SEO cluster audit")
    ap.add_argument("--hub", help="URL hub để tự lấy slug (vd https://simplize.vn/hang-hoa)")
    ap.add_argument("--prefix", default="/hang-hoa", help="prefix path của cụm")
    ap.add_argument("--urls", help="danh sách URL, phân tách bằng dấu phẩy (bỏ qua --hub)")
    ap.add_argument("--limit", type=int, default=0, help="giới hạn số trang")
    ap.add_argument("--json", help="ghi kết quả đầy đủ ra file JSON")
    args = ap.parse_args()

    if args.urls:
        urls = [u.strip() for u in args.urls.split(",") if u.strip()]
    elif args.hub:
        urls = discover(args.hub, args.prefix)
    else:
        ap.error("cần --hub hoặc --urls")
    if args.limit:
        urls = urls[: args.limit]
    if not urls:
        print("Không tìm thấy URL nào.", file=sys.stderr)
        sys.exit(1)

    results = [audit_page(u) for u in urls]

    gates = ["status", "title", "meta", "url", "h1", "schema", "content"]
    hdr = f'{"PAGE":42} | ' + " | ".join(f"{g:^6}" for g in gates)
    print(hdr)
    print("-" * len(hdr))
    fails = {g: 0 for g in gates}
    warns = {g: 0 for g in gates}
    for r in results:
        row = f'{short(r["url"], args.prefix):42} | '
        cells = []
        for g in gates:
            v = r["gates"].get(g, "-")
            cells.append(GLYPH.get(v, f"{v:^6}"))
            if v == "FAIL":
                fails[g] += 1
            elif v == "WARN":
                warns[g] += 1
        print(row + "|".join(cells))
    print("-" * len(hdr))
    print(f"Tổng: {len(results)} trang")
    print("FAIL:", ", ".join(f"{g}={fails[g]}" for g in gates if fails[g]) or "0")
    print("WARN:", ", ".join(f"{g}={warns[g]}" for g in gates if warns[g]) or "0")

    # Liệt kê chi tiết trang FAIL để hành động
    problem = [r for r in results if "FAIL" in r["gates"].values()]
    if problem:
        print("\n--- Chi tiết trang có FAIL ---")
        for r in problem:
            bad = [g for g, v in r["gates"].items() if v == "FAIL"]
            d = r.get("data", {})
            extra = ""
            if "url" in bad:
                extra = f' (canonical={d.get("canonical","")} | og:url={d.get("og_url","")})'
            print(f'{short(r["url"], args.prefix)}: FAIL {",".join(bad)}{extra}')

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\nĐã ghi JSON: {args.json}")


if __name__ == "__main__":
    main()
