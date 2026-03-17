from playwright.async_api import async_playwright


async def scrape_autoscout24(make: str, model: str, year_from: int = None,
                              year_to: int = None, price_max: int = None,
                              mileage_max: int = None) -> list[dict]:
    results = []

    url = f"https://www.autoscout24.de/lst/{make.lower()}/{model.lower()}?sort=age&desc=1"
    if year_from:
        url += f"&fregfrom={year_from}"
    if year_to:
        url += f"&fregto={year_to}"
    if price_max:
        url += f"&priceto={price_max}"
    if mileage_max:
        url += f"&kmto={mileage_max}"

    print(f"🔍 Парсим URL: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_extra_http_headers({"Accept-Language": "de-DE,de;q=0.9"})

        try:
            await page.goto(url, timeout=30000)
            await page.wait_for_selector("article", timeout=15000)

            cards = await page.query_selector_all("article")
            print(f"📋 Найдено карточек: {len(cards)}")

            for card in cards:
                try:
                    listing_id = await card.get_attribute("id")
                    if not listing_id:
                        continue

                    # Заголовок
                    title_el = await card.query_selector("h2")
                    title = await title_el.inner_text() if title_el else "—"

                    # Все текстовые элементы карточки
                    all_spans = await card.query_selector_all("span, p, div")

                    # Цена — ищем элемент с €
                    price = "—"
                    for span in all_spans:
                        text = await span.inner_text()
                        text = text.strip()
                        if "€" in text and len(text) < 20:
                            price = text
                            break

                    # Пробег — ищем элемент с km
                    mileage = "—"
                    for span in all_spans:
                        text = await span.inner_text()
                        text = text.strip()
                        if "km" in text.lower() and len(text) < 15:
                            mileage = text
                            break

                    # Год — на AutoScout24 формат "01/2018" или "2018"
                    year = "—"
                    import re
                    for span in all_spans:
                        text = await span.inner_text()
                        text = text.strip()
                        # Ищем формат MM/YYYY
                        match = re.search(r'\b(\d{2}/\d{4})\b', text)
                        if match:
                            year = match.group(1)
                            break
                        # Или просто YYYY
                        if len(text) == 4 and text.isdigit() and 1990 <= int(text) <= 2026:
                            year = text
                            break
                   # Ссылка — берём по ID объявления
                    full_url = f"https://www.autoscout24.de/angebote/{listing_id}"

                    results.append({
                        "id": listing_id,
                        "title": title.strip(),
                        "price": price,
                        "mileage": mileage,
                        "year": year,
                        "url": full_url,
                    })

                except Exception as e:
                    print(f"⚠️ Ошибка карточки: {e}")
                    continue

        except Exception as e:
            print(f"❌ Ошибка парсинга: {e}")

        finally:
            await browser.close()

    print(f"✅ Готово! Найдено объявлений: {len(results)}")
    return results