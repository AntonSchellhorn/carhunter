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
- [x] Bot command menu via code (without BotFather)
- [ ] New user onboarding:
  - [x] Language selection keyboard (RU / DE / EN)
  - [x] /start shows language selection on first launch
  - [x] Translation system — locales.py (all texts in 3 languages)
  - [x] Complete car makes/models database — makes.py (100+ brands)
  - [x] Search parameters normalization — search_params.py (all 3 sites)
  - [x] Search sites selection (AutoScout24 / Mobile.de / Kleinanzeigen)
  - [x] Check interval setting (1 min — 24 h, default 30 min)
  - [x] Make and model selection from list (no manual input)
  - [x] Search parameters (year from/to, max mileage, max price)
  - [x] Search by radius from city (zip code + km)
  - [ ] Filter by photo availability (with photos only)
- [x] Server-side price filtering (discard listings above price_max)
- [x] Server-side mileage filtering (discard listings above mileage_max)
- [x] Server-side year filtering (discard listings outside year range)
- [x] Clear seen listings history on new search
- [x] Fixed URL encoding for models with spaces (Golf Plus → golf-plus)
- [x] Language column added to database (default: DE)
- [x] ⚙️ Menu button under each listing
- [x] Settings menu (language / sites / interval / parameters / status)

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
- [ ] Remove all debug print() statements

## Phase 6 — Monetization 🔧
- [ ] Free / Pro subscription system
- [ ] Free tier limits (1 search, 1 site, min. 30 min interval)
- [ ] Payments via Telegram Stars
- [ ] Free plan — minimum interval 30 min (ban protection)
- [ ] Pro plan — minimum interval 5 min

## Phase 7 — Scaling 🔧
- [ ] Migrate from SQLite to PostgreSQL
- [ ] Task queue for parser
- [ ] Auto-cleanup of old searches and listings
- [ ] Load testing
- [ ] Server monitoring
- [ ] Task queue (Celery/RQ) for 10000+ users
- [ ] Proxy rotation for scraping
- [ ] Delays between requests to sites