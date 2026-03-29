import asyncio
import json
from playwright.async_api import async_playwright

async def fetch_all_ids():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.set_extra_http_headers({"Accept-Language": "de-DE,de;q=0.9"})

        print("🌐 Открываем Mobile.de...")
        await page.goto("https://suchen.mobile.de/fahrzeuge/detailsuche?vc=Car", timeout=30000)
        await page.wait_for_timeout(5000)

        # Берём первый select — это список марок
        selects = await page.query_selector_all("select")
        make_select = selects[0]
        options = await make_select.query_selector_all("option")

        # Сначала собираем все марки
        makes_raw = []
        for option in options:
            value = await option.get_attribute("value")
            text = await option.inner_text()
            text = text.strip()
            if not value or not value.isdigit():
                continue
            makes_raw.append({"name": text, "id": int(value)})

        print(f"📋 Найдено марок: {len(makes_raw)}")

        result = {}

        # Для каждой марки — выбираем её и собираем модели
        for make in makes_raw:
            print(f"🔍 Обрабатываем: {make['name']} (ID: {make['id']})...")

            try:
                # Выбираем марку в выпадающем списке
                selects = await page.query_selector_all("select")
                make_select = selects[0]
                await make_select.select_option(value=str(make["id"]))

                # Ждём пока загрузится список моделей
                await page.wait_for_timeout(1500)

                # Берём второй select — это список моделей
                selects = await page.query_selector_all("select")
                model_select = selects[1]
                model_options = await model_select.query_selector_all("option")

                models = {}
                for opt in model_options:
                    val = await opt.get_attribute("value")
                    txt = await opt.inner_text()
                    txt = txt.strip()
                    if not val or not val.isdigit():
                        continue
                    models[txt] = int(val)

                result[make["name"]] = {
                    "id": make["id"],
                    "models": models
                }

                print(f"   ✅ Моделей: {len(models)}")

            except Exception as e:
                print(f"   ⚠️ Ошибка: {e}")
                result[make["name"]] = {"id": make["id"], "models": {}}

        await browser.close()

    print(f"\n📦 Готово! Марок: {len(result)}")

    # Сохраняем в JSON
    with open("mobile_de_ids.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("💾 Сохранено в mobile_de_ids.json")

asyncio.run(fetch_all_ids())

