import asyncio
from scraper import scrape_autoscout24


async def test():
    print("🧪 Тестируем парсер...")
    results = await scrape_autoscout24(
        make="BMW",
        model="X5",
        year_from=2018,
        price_max=50000,
    )

    if results:
        print(f"\n✅ Найдено объявлений: {len(results)}")
        print("\n--- Первое объявление ---")
        first = results[0]
        print(f"ID:     {first['id']}")
        print(f"Название: {first['title']}")
        print(f"Цена:   {first['price']}")
        print(f"Пробег: {first['mileage']}")
        print(f"Год:    {first['year']}")
        print(f"Ссылка: {first['url']}")
    else:
        print("❌ Ничего не найдено")


asyncio.run(test())