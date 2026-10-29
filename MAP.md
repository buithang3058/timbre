# MAP.md — Bản đồ dự án Timbre

> Đọc file này + `CLAUDE.md` đầu mỗi cuộc hội thoại.
> Cập nhật file này mỗi khi tạo, di chuyển, hoặc xoá file/thư mục.
> Cập nhật gần nhất: 2026-10-21.

## Timbre là gì
Hệ thống AI-assisted "voice-first" để xây website/thương hiệu cá nhân:
chiến lược → nội dung → phân phối → lặp. Chạy như một bộ Claude Code slash
command (skills). Chi tiết: `README.md`, `PROJECT_CONTEXT.md`.

## Tìm thông tin ở đâu / Lưu thông tin ở đâu

| Thư mục / File | Chứa gì | Dùng khi |
|---|---|---|
| `CLAUDE.md` | Tôi là ai, dự án làm gì, cách làm việc, quy tắc + cấu hình GBrain | Đọc đầu mỗi hội thoại |
| `MAP.md` | File này — bản đồ dự án | Đọc đầu mỗi hội thoại |
| `contexte/` | Mọi thứ học được lâu dài: quyết định, sở thích, info hữu ích (1 chủ đề/file). Có: `bing-webmaster-tools.md` | Ghi khi học được điều lâu dài |
| `livrables/` | Sản phẩm giao nộp cho user (báo cáo, phân tích, bàn giao) | Khi tạo output cho user |
| `sources/` | Tài liệu thô đầu vào (paper, export SEMrush/GSC, trang đối thủ, transcript) | Khi nạp nguồn để nghiên cứu |
| `skills/` | Các skill Timbre, mỗi skill 1 thư mục có `SKILL.md` | Phát triển/sửa skill |
| `projects/` | Dữ liệu vận hành từng dự án nội dung (`simplize/`, `tokemist/`, `motquacam/`) | Làm SEO/nội dung cho 1 dự án |
| `voices/` | Voice DNA của tác giả (author layer) | Hiệu chỉnh giọng viết |
| `references/` | Tài liệu tham chiếu dùng chung (vd `eeat-framework.md`) | Tra khung lý thuyết SEO/nội dung |
| `templates/` | Mẫu dùng lại | Khởi tạo nội dung theo mẫu |
| `scripts/` | Script tiện ích: `gsc.py` (Google SC), `bing.py` (Bing WMT), `indexnow.py` (ping Bing crawl), `ga4.py`, `export-sheet.py`, `seo-cluster-audit.py` | Lấy dữ liệu SEO / chạy tác vụ |
| `planning/` | Ghi chú kế hoạch | Theo dõi kế hoạch đang chạy |
| `drafts/` | Bản nháp | — |
| `resources/`, `tests/` | Tài nguyên & test của plugin | — |
| `.claude-plugin/` | Manifest plugin Timbre | Đóng gói/phát hành plugin |
| `PROJECT_CONTEXT.md`, `IDEAS.md`, `TODOS.md` | Bối cảnh, ý tưởng, việc cần làm (cấp repo) | Nắm bối cảnh chung |
| `AGENTS.md` | Hướng dẫn dùng gstack + handoff cho Claude | Khi dùng workflow gstack |

## Ánh xạ cây harness tham chiếu → Timbre
Các mục trong cây tham chiếu đã có file tương đương nên **không tạo trùng**:
- `SPEC.md` → `PROJECT_CONTEXT.md` (dự án là gì, mục tiêu)
- `PLAN.md` → `TODOS.md` + `planning/`
- `.claude/skills/` + `.claude/workflows/` → `skills/` (skill = workflow của Timbre)
- `.claude/agents/` → `.agents/skills/` (symlink) ; `.mcp.json`/MCP → cấu hình user-scope (gbrain…)
- `.claude/agent-memory/` → `~/.claude/projects/.../memory/` + `contexte/`
Cố ý **chưa tạo** (tạo khi có nhu cầu thật): `CLAUDE.local.md`, `.worktreeinclude`,
`.claude/{rules,output-styles}/`, `docs/`, `.github/workflows/`.

## Ghi chú
- GBrain đã cấu hình (xem `CLAUDE.md`). Ưu tiên `gbrain search/query` cho truy
  vấn ngữ nghĩa; Grep cho chuỗi/regex chính xác.
- Riêng tư (gitignored, local-only): `CLAUDE.md`, `contexte/`, `livrables/`,
  `sources/`, `PROJECT_CONTEXT.md`, `TODOS.md`, `IDEAS.md`, `AGENTS.md`, `drafts/`,
  `resources/`, `voices/<brand>/`, `.env`. Plugin chỉ ship `skills/` + `scripts/`.
