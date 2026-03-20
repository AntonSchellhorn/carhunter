# Все тексты бота на трёх языках
TEXTS = {
    "ru": {
        # Приветствие
        "welcome": "🚗 Привет! Я <b>CarHunter Bot</b>!\n\nЯ ищу автомобили на автомобильных сайтах Германии 24/7 и сообщаю, когда нахожу выгодное предложение.",
        "choose_language": "🌍 Выбери язык / Sprache wählen / Choose language:",

        # Главное меню
        "main_menu": "⚙️ <b>Главное меню</b>\n\nВыбери что хочешь настроить:",
        "btn_search": "🔍 Новый поиск",
        "btn_sites": "🌐 Сайты поиска",
        "btn_interval": "⏱ Интервал проверки",
        "btn_language": "🌍 Язык",
        "btn_status": "📊 Статус",
        "btn_stop": "⛔ Стоп",

        # Поиск
        "search_step_make_letter": "🔍 Шаг 1 — Выбери первую букву марки:",
        "search_step_make": "Выбери марку:",
        "search_step_series": "Выбери серию или пропусти:",
        "search_step_model": "Выбери модель:",
        "search_step_body": "Выбери тип кузова или пропусти:",
        "search_step_fuel": "Выбери тип топлива или пропусти:",
        "search_step_year_from": "📅 Введи год выпуска <b>от</b>:\n<i>Например: 2018</i>",
        "search_step_year_to": "📅 Введи год выпуска <b>до</b>:\n<i>Например: 2022</i>",
        "search_step_price_max": "💶 Введи максимальную цену (€):\n<i>Например: 20000</i>",
        "search_step_price_min": "💶 Введи минимальную цену (€) или пропусти:",
        "search_step_mileage_max": "🛣 Введи максимальный пробег (км):\n<i>Например: 150000</i>",

        # Кнопки
        "btn_skip": "⏭ Пропустить",
        "btn_back": "◀️ Назад",
        "btn_all": "📋 Все",
        "btn_confirm": "✅ Запустить поиск",
        "btn_restart": "🔄 Начать заново",
        "btn_refresh": "🔄 Обновить сейчас",
        "btn_new_search": "🔍 Новый поиск",
        "btn_menu": "⚙️ Меню",

        # Подтверждение поиска
        "search_summary": "✅ <b>Параметры поиска:</b>\n\n"
                         "🚘 Марка:     <b>{make}</b>\n"
                         "🔖 Модель:    <b>{model}</b>\n"
                         "📅 Год от:    <b>{year_from}</b>\n"
                         "📅 Год до:    <b>{year_to}</b>\n"
                         "💶 Цена до:   <b>{price_max} €</b>\n"
                         "🛣 Пробег до: <b>{mileage_max} км</b>\n"
                         "⛽ Топливо:   <b>{fuel}</b>\n"
                         "🏠 Кузов:     <b>{body}</b>",

        # Запуск поиска
        "search_started": "🚀 <b>Поиск запущен!</b>\n\nБуду следить за сайтами и пришлю уведомление как только найду подходящее объявление.\n\nОстановить: /stop",
        "search_stopped": "⛔ <b>Поиск остановлен.</b>\n\nНастройки сохранены — запустить снова: /search",

        # Уведомление о новом объявлении
        "new_listing": "🚗 <b>Новое объявление!</b>\n\n"
                      "📌 {title}\n"
                      "💶 Цена: <b>{price}</b>\n"
                      "🛣 Пробег: <b>{mileage}</b>\n"
                      "📅 Год: <b>{year}</b>\n"
                      "🌐 Сайт: <b>{site}</b>\n\n"
                      "🔗 <a href='{url}'>Открыть объявление</a>",

        # Рестарт бота
        "bot_restarted": "🟢 <b>Бот перезапущен!</b>\n\nТвой поиск активен:\n🚘 {make} {model}\n\nСледующая проверка запустится автоматически.",

        # Статус
        "status_active": "🟢 Активен",
        "status_stopped": "🔴 Остановлен",
        "status_message": "<b>Статус поиска: {status}</b>\n\n"
                         "🚘 Марка:     <b>{make}</b>\n"
                         "🔖 Модель:    <b>{model}</b>\n"
                         "📅 Год от:    <b>{year_from}</b>\n"
                         "📅 Год до:    <b>{year_to}</b>\n"
                         "💶 Цена до:   <b>{price_max} €</b>\n"
                         "🛣 Пробег до: <b>{mileage_max} км</b>\n"
                         "⏱ Интервал:  <b>{interval} мин</b>",
        "no_search": "📭 У тебя ещё нет настроек поиска.\nИспользуй /search чтобы начать.",

        # Сайты
        "choose_sites": "🌐 Выбери сайты для поиска:\n(можно выбрать несколько)",
        "sites_saved": "✅ Сайты сохранены!",

        # Интервал
        "choose_interval": "⏱ Выбери интервал проверки:",
        "interval_saved": "✅ Интервал сохранён: каждые <b>{interval}</b>",
        "interval_custom": "Введи интервал в минутах (1-1440):",

        # Ошибки
        "error_number": "⚠️ Введи число, например: <b>{example}</b>",
        "error_year": "⚠️ Введи корректный год, например: <b>2018</b>",
    },

    "de": {
        # Begrüßung
        "welcome": "🚗 Hallo! Ich bin <b>CarHunter Bot</b>!\n\nIch suche rund um die Uhr nach Autos auf deutschen Autobörsen und benachrichtige dich, wenn ich ein gutes Angebot finde.",
        "choose_language": "🌍 Wyбери язык / Sprache wählen / Choose language:",

        # Hauptmenü
        "main_menu": "⚙️ <b>Hauptmenü</b>\n\nWas möchtest du einstellen?",
        "btn_search": "🔍 Neue Suche",
        "btn_sites": "🌐 Suchportale",
        "btn_interval": "⏱ Prüfintervall",
        "btn_language": "🌍 Sprache",
        "btn_status": "📊 Status",
        "btn_stop": "⛔ Stopp",

        # Suche
        "search_step_make_letter": "🔍 Schritt 1 — Wähle den ersten Buchstaben der Marke:",
        "search_step_make": "Marke wählen:",
        "search_step_series": "Serie wählen oder überspringen:",
        "search_step_model": "Modell wählen:",
        "search_step_body": "Karosserietyp wählen oder überspringen:",
        "search_step_fuel": "Kraftstoffart wählen oder überspringen:",
        "search_step_year_from": "📅 Baujahr <b>von</b> eingeben:\n<i>Beispiel: 2018</i>",
        "search_step_year_to": "📅 Baujahr <b>bis</b> eingeben:\n<i>Beispiel: 2022</i>",
        "search_step_price_max": "💶 Höchstpreis eingeben (€):\n<i>Beispiel: 20000</i>",
        "search_step_price_min": "💶 Mindestpreis eingeben (€) oder überspringen:",
        "search_step_mileage_max": "🛣 Maximale Kilometerleistung eingeben:\n<i>Beispiel: 150000</i>",

        # Schaltflächen
        "btn_skip": "⏭ Überspringen",
        "btn_back": "◀️ Zurück",
        "btn_all": "📋 Alle",
        "btn_confirm": "✅ Suche starten",
        "btn_restart": "🔄 Neu beginnen",
        "btn_refresh": "🔄 Jetzt aktualisieren",
        "btn_new_search": "🔍 Neue Suche",
        "btn_menu": "⚙️ Menü",

        # Suchzusammenfassung
        "search_summary": "✅ <b>Suchparameter:</b>\n\n"
                         "🚘 Marke:      <b>{make}</b>\n"
                         "🔖 Modell:     <b>{model}</b>\n"
                         "📅 Jahr von:   <b>{year_from}</b>\n"
                         "📅 Jahr bis:   <b>{year_to}</b>\n"
                         "💶 Preis bis:  <b>{price_max} €</b>\n"
                         "🛣 KM bis:     <b>{mileage_max} km</b>\n"
                         "⛽ Kraftstoff: <b>{fuel}</b>\n"
                         "🏠 Karosserie: <b>{body}</b>",

        # Suche starten
        "search_started": "🚀 <b>Suche gestartet!</b>\n\nIch überwache die Portale und benachrichtige dich, sobald ich ein passendes Angebot finde.\n\nStoppen: /stop",
        "search_stopped": "⛔ <b>Suche gestoppt.</b>\n\nEinstellungen gespeichert — neu starten: /search",

        # Neue Anzeige
        "new_listing": "🚗 <b>Neue Anzeige!</b>\n\n"
                      "📌 {title}\n"
                      "💶 Preis: <b>{price}</b>\n"
                      "🛣 Kilometerstand: <b>{mileage}</b>\n"
                      "📅 Jahr: <b>{year}</b>\n"
                      "🌐 Portal: <b>{site}</b>\n\n"
                      "🔗 <a href='{url}'>Anzeige öffnen</a>",

        # Bot-Neustart
        "bot_restarted": "🟢 <b>Bot neugestartet!</b>\n\nDeine Suche ist aktiv:\n🚘 {make} {model}\n\nDie nächste Prüfung startet automatisch.",

        # Status
        "status_active": "🟢 Aktiv",
        "status_stopped": "🔴 Gestoppt",
        "status_message": "<b>Suchstatus: {status}</b>\n\n"
                         "🚘 Marke:      <b>{make}</b>\n"
                         "🔖 Modell:     <b>{model}</b>\n"
                         "📅 Jahr von:   <b>{year_from}</b>\n"
                         "📅 Jahr bis:   <b>{year_to}</b>\n"
                         "💶 Preis bis:  <b>{price_max} €</b>\n"
                         "🛣 KM bis:     <b>{mileage_max} km</b>\n"
                         "⏱ Intervall:  <b>{interval} min</b>",
        "no_search": "📭 Du hast noch keine Sucheinstellungen.\nVerwende /search um zu beginnen.",

        # Portale
        "choose_sites": "🌐 Wähle die Suchportale:\n(Mehrfachauswahl möglich)",
        "sites_saved": "✅ Portale gespeichert!",

        # Intervall
        "choose_interval": "⏱ Prüfintervall wählen:",
        "interval_saved": "✅ Intervall gespeichert: alle <b>{interval}</b>",
        "interval_custom": "Intervall in Minuten eingeben (1-1440):",

        # Fehler
        "error_number": "⚠️ Bitte eine Zahl eingeben, z.B.: <b>{example}</b>",
        "error_year": "⚠️ Bitte ein gültiges Jahr eingeben, z.B.: <b>2018</b>",
    },

    "en": {
        # Greeting
        "welcome": "🚗 Hello! I'm <b>CarHunter Bot</b>!\n\nI search German car marketplaces 24/7 and notify you when I find a good deal.",
        "choose_language": "🌍 Выбери язык / Sprache wählen / Choose language:",

        # Main menu
        "main_menu": "⚙️ <b>Main Menu</b>\n\nWhat would you like to configure?",
        "btn_search": "🔍 New Search",
        "btn_sites": "🌐 Search Sites",
        "btn_interval": "⏱ Check Interval",
        "btn_language": "🌍 Language",
        "btn_status": "📊 Status",
        "btn_stop": "⛔ Stop",

        # Search
        "search_step_make_letter": "🔍 Step 1 — Choose the first letter of the brand:",
        "search_step_make": "Choose brand:",
        "search_step_series": "Choose series or skip:",
        "search_step_model": "Choose model:",
        "search_step_body": "Choose body type or skip:",
        "search_step_fuel": "Choose fuel type or skip:",
        "search_step_year_from": "📅 Enter year <b>from</b>:\n<i>Example: 2018</i>",
        "search_step_year_to": "📅 Enter year <b>to</b>:\n<i>Example: 2022</i>",
        "search_step_price_max": "💶 Enter maximum price (€):\n<i>Example: 20000</i>",
        "search_step_price_min": "💶 Enter minimum price (€) or skip:",
        "search_step_mileage_max": "🛣 Enter maximum mileage (km):\n<i>Example: 150000</i>",

        # Buttons
        "btn_skip": "⏭ Skip",
        "btn_back": "◀️ Back",
        "btn_all": "📋 All",
        "btn_confirm": "✅ Start Search",
        "btn_restart": "🔄 Start Over",
        "btn_refresh": "🔄 Refresh Now",
        "btn_new_search": "🔍 New Search",
        "btn_menu": "⚙️ Menu",

        # Search summary
        "search_summary": "✅ <b>Search Parameters:</b>\n\n"
                         "🚘 Brand:    <b>{make}</b>\n"
                         "🔖 Model:    <b>{model}</b>\n"
                         "📅 Year from:<b>{year_from}</b>\n"
                         "📅 Year to:  <b>{year_to}</b>\n"
                         "💶 Max price:<b>{price_max} €</b>\n"
                         "🛣 Max km:   <b>{mileage_max} km</b>\n"
                         "⛽ Fuel:     <b>{fuel}</b>\n"
                         "🏠 Body:     <b>{body}</b>",

        # Search start
        "search_started": "🚀 <b>Search started!</b>\n\nI'll monitor the sites and notify you as soon as I find a matching listing.\n\nStop: /stop",
        "search_stopped": "⛔ <b>Search stopped.</b>\n\nSettings saved — restart: /search",

        # New listing notification
        "new_listing": "🚗 <b>New listing!</b>\n\n"
                      "📌 {title}\n"
                      "💶 Price: <b>{price}</b>\n"
                      "🛣 Mileage: <b>{mileage}</b>\n"
                      "📅 Year: <b>{year}</b>\n"
                      "🌐 Site: <b>{site}</b>\n\n"
                      "🔗 <a href='{url}'>Open listing</a>",

        # Bot restart
        "bot_restarted": "🟢 <b>Bot restarted!</b>\n\nYour search is active:\n🚘 {make} {model}\n\nNext check will start automatically.",

        # Status
        "status_active": "🟢 Active",
        "status_stopped": "🔴 Stopped",
        "status_message": "<b>Search status: {status}</b>\n\n"
                         "🚘 Brand:    <b>{make}</b>\n"
                         "🔖 Model:    <b>{model}</b>\n"
                         "📅 Year from:<b>{year_from}</b>\n"
                         "📅 Year to:  <b>{year_to}</b>\n"
                         "💶 Max price:<b>{price_max} €</b>\n"
                         "🛣 Max km:   <b>{mileage_max} km</b>\n"
                         "⏱ Interval: <b>{interval} min</b>",
        "no_search": "📭 You have no search settings yet.\nUse /search to get started.",

        # Sites
        "choose_sites": "🌐 Choose search sites:\n(multiple selection allowed)",
        "sites_saved": "✅ Sites saved!",

        # Interval
        "choose_interval": "⏱ Choose check interval:",
        "interval_saved": "✅ Interval saved: every <b>{interval}</b>",
        "interval_custom": "Enter interval in minutes (1-1440):",

        # Errors
        "error_number": "⚠️ Please enter a number, e.g.: <b>{example}</b>",
        "error_year": "⚠️ Please enter a valid year, e.g.: <b>2018</b>",
    }
}


def t(lang: str, key: str, **kwargs) -> str:
    """
    Получить текст на нужном языке.
    Если язык не найден — используем русский.
    Если ключ не найден — возвращаем ключ.
    """
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text