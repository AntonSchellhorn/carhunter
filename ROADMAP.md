# 📍 CarHunter — Roadmap

## Phase 0 — Environment Setup ✅
- [x] Install VSCode
- [x] Install Python 3.11.9
- [x] Create project folder carhunter
- [x] Create virtual environment venv
- [x] Install libraries (aiogram, playwright, apscheduler, aiosqlite)
- [x] Create GitHub repository
- [x] Initial commit

## Phase 1 — Telegram Bot (Skeleton) ✅
- [x] Create bot via @BotFather
- [x] Basic commands /start /search /stop /status
- [x] Accept search parameters from user
- [x] Save settings to SQLite

## Phase 2 — AutoScout24 Parser ✅
- [x] Parse listings via Playwright
- [x] Extract price, mileage, year, URL
- [x] Deduplication — never send the same listing twice
- [x] Scheduler — run every 30 minutes
- [x] Immediate check on search launch
- [x] Inline control buttons under each listing
- [x] Restart notification with control buttons

## Phase 3 — UX & Controls 🔧
- [ ] Bot command menu via code (without BotFather)
- [ ] New user onboarding:
  - [x] Language selection keyboard (RU / DE / EN)
  - [x] Translation system — locales.py (all texts in 3 languages)
  - [x] Complete car makes/models database — makes.py (100+ brands)
  - [x] Search parameters normalization — search_params.py (all 3 sites)
  - [ ] Search sites selection (AutoScout24 / Mobile.de / eBay)
  - [ ] Check interval setting (1 min — 24 h, default 30 min)
  - [ ] Make and model selection from list (no manual input)
  - [ ] Search parameters (year from/to, max mileage, max price)
- [x] Server-side price filtering (discard listings above price_max)
- [x] Server-side mileage filtering (discard listings above mileage_max)
- [x] Server-side year filtering (discard listings outside year range)
- [x] Clear seen listings history on new search
- [x] Fixed URL encoding for models with spaces (Golf Plus → golf-plus)
- [x] Language column added to database (default: DE)
- [ ] ⚙️ Menu button under each listing
- [ ] Settings menu (language / sites / interval / parameters / status)

## Phase 4 — Multi-Platform Coverage 🔧
- [ ] Parameter normalization across sites
- [ ] Show listing publication time
- [ ] Mobile.de parser
- [ ] eBay Kleinanzeigen parser
- [ ] User-selectable search sites

## Phase 5 — Production Deployment 🔧
- [ ] Docker container
- [ ] Deploy to Hetzner VPS (24/7 uptime)
- [ ] GitHub Actions CI/CD

## Phase 6 — Monetization 🔧
- [ ] Free / Pro subscription system
- [ ] Free tier limits (1 search, 1 site, min. 30 min interval)
- [ ] Payments via Telegram Stars

## Phase 7 — Scaling 🔧
- [ ] Migrate from SQLite to PostgreSQL
- [ ] Task queue for parser
- [ ] Auto-cleanup of old searches and listings
- [ ] Load testing
- [ ] Server monitoring