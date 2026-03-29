from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import re

async def scrape_autoscout24(make: str, model: str, year_from: int = None,
                              year_to: int = None, price_max: int = None,
                              mileage_max: int = None, zip_code: str = None,
                              radius: int = None) -> list[dict]:
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
    if zip_code and radius:
        url += f"&zip={zip_code}&zipr={radius}"    

    print(f"🔍 Парсим URL: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
           headless=True,
           args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
           user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
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
                    # Фильтрация по цене
                    if price_max and price != "—":
                        price_num = int(re.sub(r'[^\d]', '', price))
                        if price_num > price_max:
                            continue

                    # Фильтрация по пробегу
                    if mileage_max and mileage != "—":
                        mileage_num = int(re.sub(r'[^\d]', '', mileage))
                        if mileage_num > mileage_max:
                            continue
                    # Фильтрация по году
                    if year != "—":
                        # Извлекаем только год из формата "01/2018" или "2018"
                        year_num = int(year.split("/")[-1])
                        if year_from and year_num < year_from:
                            continue
                        if year_to and year_num > year_to:
                            continue
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
            await context.close()
            await browser.close()

    print(f"✅ Готово! Найдено объявлений: {len(results)}")
    return results

async def scrape_mobile_de(make: str, model: str, year_from: int = None,
                            year_to: int = None, price_max: int = None,
                            mileage_max: int = None, zip_code: str = None,
                            radius: int = None) -> list[dict]:
    import json
    import os

    results = []

    # Загружаем ID марок и моделей из файла
    ids_path = os.path.join(os.path.dirname(__file__), "mobile_de_ids.json")
    with open(ids_path, "r", encoding="utf-8") as f:
        mobile_ids = json.load(f)

    # Ищем марку (без учёта регистра)
    make_data = None
    for name, data in mobile_ids.items():
        if name.lower() == make.lower():
            make_data = data
            break

    if not make_data:
        print(f"⚠️ Mobile.de: марка '{make}' не найдена в базе")
        return []

    make_id = make_data["id"]

    # Ищем модель (без учёта регистра)
    model_id = ""
    for model_name, model_id_val in make_data["models"].items():
        if model_name.lower() == model.lower():
            model_id = str(model_id_val)
            break

    # Строим параметр ms=MAKE_ID;MODEL_ID;;
    ms = f"{make_id};{model_id};;"

    # Строим URL
    url = f"https://suchen.mobile.de/fahrzeuge/search.html?isSearchRequest=true&ms={ms}&s=Car&vc=Car&od=up"

    if price_max:
        url += f"&p=%3A{price_max}"
    if mileage_max:
        url += f"&ml=%3A{mileage_max}"
    if year_from and year_to:
        url += f"&fr={year_from}%3A{year_to}"
    elif year_from:
        url += f"&fr={year_from}%3A"
    elif year_to:
        url += f"&fr=%3A{year_to}"
    if zip_code and radius:
        url += f"&zip={zip_code}&zipr={radius}"

    print(f"🔍 Mobile.de URL: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        await page.set_extra_http_headers({"Accept-Language": "de-DE,de;q=0.9"})

        try:
            await page.goto(url, timeout=30000)
            await page.wait_for_timeout(5000)

            # Закрываем cookie-баннер если есть
            try:
                await page.click("button:has-text('Einverstanden')", timeout=5000)
                await page.wait_for_timeout(2000)
            except Exception:
                pass

            await page.evaluate("window.scrollBy(0, 800)")
            await page.wait_for_timeout(2000)

            # Собираем все ссылки на объявления
            links = await page.query_selector_all("a[href*='details.html']")
            print(f"📋 Найдено ссылок: {len(links)}")

            seen_ids = set()

            for link in links:
                try:
                    href = await link.get_attribute("href")
                    if not href:
                        continue

                    # Извлекаем ID из href
                    id_match = re.search(r'id=(\d+)', href)
                    if not id_match:
                        continue

                    listing_id = id_match.group(1)

                    # Пропускаем дубли (одна карточка = несколько ссылок)
                    if listing_id in seen_ids:
                        continue
                    seen_ids.add(listing_id)

                    text = await link.inner_text()
                    text = text.strip()

                    if not text or "€" not in text:
                        continue

                    lines = [l.strip() for l in text.split("\n") if l.strip()]

                    # Заголовок — первая строка
                    title = lines[0] if lines else "—"

                    # Цена — ищем строку с €
                    price = "—"
                    for line in lines:
                        if "€" in line and len(line) < 20:
                            price = line
                            break

                    # Год, пробег — ищем строку с EZ
                    year = "—"
                    mileage = "—"
                    for line in lines:
                        if "EZ" in line:
                            # Формат: EZ 08/2011 • 83.400 km • ...
                            year_match = re.search(r'EZ\s+(\d{2}/\d{4})', line)
                            if year_match:
                                year = year_match.group(1)
                            km_match = re.search(r'([\d\.]+)\s*km', line)
                            if km_match:
                                mileage = km_match.group(1) + " km"
                            break

                    full_url = f"https://suchen.mobile.de/fahrzeuge/details.html?id={listing_id}"

                    results.append({
                        "id": f"mobile_{listing_id}",
                        "title": title,
                        "price": price,
                        "mileage": mileage,
                        "year": year,
                        "url": full_url,
                    })

                except Exception as e:
                    print(f"⚠️ Ошибка ссылки: {e}")
                    continue

        except Exception as e:
            print(f"❌ Ошибка Mobile.de: {e}")

        finally:
            await browser.close()

    print(f"✅ Mobile.de: найдено объявлений: {len(results)}")
    return results