#!/usr/bin/env bash
# Kiểm sức khoẻ simplize.vn sau khi deploy production.
# Dùng: bash scripts/simplize-health.sh
# Mỗi dòng OK = đạt. Có dòng FAIL = cân nhắc lùi bản trên dashboard Vercel.

H=https://simplize.vn
UA='Mozilla/5.0'
fail=0

chk() { # chk <nhãn> <đường dẫn> <bytes tối thiểu> [chuỗi bắt buộc]
  local label="$1" path="$2" min="$3" must="$4"
  local body code size
  body=$(curl -s -A "$UA" --max-time 45 -w $'\n%{http_code}' "$H$path")
  code=${body##*$'\n'}
  body=${body%$'\n'*}
  size=$(printf '%s' "$body" | wc -c | tr -d ' ')

  if [ "$code" != "200" ]; then
    printf 'FAIL  %-26s HTTP %s\n' "$label" "$code"; fail=1; return
  fi
  if [ "$size" -lt "$min" ]; then
    printf 'FAIL  %-26s chỉ %sb (cần >%sb) — trang rỗng?\n' "$label" "$size" "$min"; fail=1; return
  fi
  if [ -n "$must" ] && ! printf '%s' "$body" | grep -qE "$must"; then
    printf 'FAIL  %-26s thiếu "%s"\n' "$label" "$must"; fail=1; return
  fi
  printf 'OK    %-26s 200  %sb\n' "$label" "$size"
}

echo "=== Trang chính ==="
chk "trang chủ"        /                  100000
chk "/co-phieu"        /co-phieu          200000 "<table"
chk "/gia-vang"        /gia-vang          200000
chk "/gia-vang/the-gioi" /gia-vang/the-gioi 100000
chk "/vi-mo"           /vi-mo              80000

echo
echo "=== Sitemap gửi Google (route sinh động — nhạy nhất) ==="
chk "sitemap.xml"      /sitemap.xml         800 "urlset|sitemapindex"
chk "sitemap gia-vang" /sitemap/gia-vang/sitemap_gia-vang.xml 10000 "urlset|sitemapindex"
chk "sitemap stock"    /sitemap/stock/sitemap_stock.xml      100000 "urlset|sitemapindex"
chk "RSS tin tức"      /rss/news/news-rss.xml                 10000 "<rss|<channel"

echo
echo "=== PR #6983 đã lên chưa (heading giả phải giảm 437 -> ~24) ==="
h6=$(curl -s -A "$UA" --max-time 45 "$H/co-phieu" | grep -o "<h6" | wc -l | tr -d ' ')
if [ "$h6" -lt 60 ]; then
  printf 'OK    %-26s H6=%s (đã áp dụng)\n' "heading /co-phieu" "$h6"
else
  printf 'CHƯA  %-26s H6=%s — bản mới chưa live, đợi thêm hoặc build fail\n' "heading /co-phieu" "$h6"
fi

echo
if [ "$fail" = "0" ]; then
  echo "✅ Không có FAIL. Còn 1 việc PHẢI tự thử bằng tay: ĐĂNG NHẬP Google/Facebook."
else
  echo "❌ Có FAIL ở trên → vào dashboard Vercel, Deployments, chọn bản 29/09, Instant Rollback."
fi
