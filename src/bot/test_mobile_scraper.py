import asyncio
from scraper import scrape_mobile_de

async def test():
    results = await scrape_mobile_de(
        make="Volkswagen",
        model="Golf",
        year_from=2010,
        year_to=2015,
        price_max=5000
    )
    print(f"\n📊 Итого объявлений: {len(results)}")
    for r in results[:5]:
        print(f"\n  🚗 {r['title']}")
        print(f"     💶 {r['price']}")
        print(f"     📅 {r['year']}")
        print(f"     🛣 {r['mileage']}")
        print(f"     🔗 {r['url']}")

asyncio.run(test())

