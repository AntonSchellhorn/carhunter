# Параметры поиска — нормализованные для всех трёх сайтов
# Каждый параметр содержит:
# - значения для отображения пользователю
# - маппинг на параметры каждого сайта

# ─────────────────────────────────────────
# Тип кузова
# ─────────────────────────────────────────
BODY_TYPES = {
    "Limousine":    {"autoscout24": "sedan",   "mobile": "Limousine",  "kleinanzeigen": "Limousine"},
    "Kombi":        {"autoscout24": "estate",  "mobile": "Kombi",      "kleinanzeigen": "Kombi"},
    "SUV":          {"autoscout24": "suv",     "mobile": "SUV",        "kleinanzeigen": "SUV/Gelaendewagen"},
    "Cabrio":       {"autoscout24": "cabrio",  "mobile": "Cabrio",     "kleinanzeigen": "Cabrio/Roadster"},
    "Coupe":        {"autoscout24": "coupe",   "mobile": "Coupe",      "kleinanzeigen": "Coupe"},
    "Van":          {"autoscout24": "van",     "mobile": "Van/Minibus","kleinanzeigen": "Bus"},
    "Kleinwagen":   {"autoscout24": "small",   "mobile": "Kleinwagen", "kleinanzeigen": "Kleinwagen"},
    "Pick-up":      {"autoscout24": "pickup",  "mobile": "Pick-up",    "kleinanzeigen": "Pickup"},
    "Transporter":  {"autoscout24": "other",   "mobile": "Transporter","kleinanzeigen": "Transporter"},
}

# ─────────────────────────────────────────
# Тип топлива
# ─────────────────────────────────────────
FUEL_TYPES = {
    "Benzin":       {"autoscout24": "B",  "mobile": "PETROL",    "kleinanzeigen": "benzin"},
    "Diesel":       {"autoscout24": "D",  "mobile": "DIESEL",    "kleinanzeigen": "diesel"},
    "Elektro":      {"autoscout24": "E",  "mobile": "ELECTRIC",  "kleinanzeigen": "elektro"},
    "Hybrid":       {"autoscout24": "M",  "mobile": "HYBRID",    "kleinanzeigen": "hybrid"},
    "Plug-in Hybrid":{"autoscout24": "M", "mobile": "HYBRID_PLUG_IN", "kleinanzeigen": "hybrid"},
    "LPG/Autogas":  {"autoscout24": "L",  "mobile": "LPG",       "kleinanzeigen": "lpg"},
    "CNG/Erdgas":   {"autoscout24": "C",  "mobile": "CNG",       "kleinanzeigen": "cng"},
    "Wasserstoff":  {"autoscout24": "H",  "mobile": "HYDROGEN",  "kleinanzeigen": "wasserstoff"},
}

# ─────────────────────────────────────────
# Коробка передач
# ─────────────────────────────────────────
TRANSMISSION = {
    "Automatik":    {"autoscout24": "A", "mobile": "AUTOMATIC_GEAR", "kleinanzeigen": "automatik"},
    "Schaltgetriebe":{"autoscout24": "M","mobile": "MANUAL_GEAR",    "kleinanzeigen": "schaltgetriebe"},
}

# ─────────────────────────────────────────
# Количество дверей
# ─────────────────────────────────────────
DOORS = {
    "2/3":  {"autoscout24": "2",  "mobile": "DOORS_2_3", "kleinanzeigen": None},
    "4/5":  {"autoscout24": "5",  "mobile": "DOORS_4_5", "kleinanzeigen": None},
    "6/7":  {"autoscout24": "7",  "mobile": "DOORS_6_7", "kleinanzeigen": None},
}

# ─────────────────────────────────────────
# Количество мест
# ─────────────────────────────────────────
SEATS = {
    "2":  {"autoscout24": "2",  "mobile": "2",  "kleinanzeigen": None},
    "4":  {"autoscout24": "4",  "mobile": "4",  "kleinanzeigen": None},
    "5":  {"autoscout24": "5",  "mobile": "5",  "kleinanzeigen": None},
    "7":  {"autoscout24": "7",  "mobile": "7",  "kleinanzeigen": None},
    "8+": {"autoscout24": "8",  "mobile": "8",  "kleinanzeigen": None},
}

# ─────────────────────────────────────────
# Привод
# ─────────────────────────────────────────
DRIVE_TYPE = {
    "Frontantrieb": {"autoscout24": "F", "mobile": "FRONT_WHEEL_DRIVE",  "kleinanzeigen": None},
    "Heckantrieb":  {"autoscout24": "R", "mobile": "REAR_WHEEL_DRIVE",   "kleinanzeigen": None},
    "Allrad":       {"autoscout24": "A", "mobile": "ALL_WHEEL_DRIVE",    "kleinanzeigen": "allrad"},
}

# ─────────────────────────────────────────
# Состояние автомобиля
# ─────────────────────────────────────────
CONDITION = {
    "Neu":              {"autoscout24": "N", "mobile": "NEW",          "kleinanzeigen": None},
    "Gebraucht":        {"autoscout24": "U", "mobile": "USED",         "kleinanzeigen": None},
    "Jahreswagen":      {"autoscout24": "J", "mobile": "ANNUAL_CAR",   "kleinanzeigen": None},
    "Vorführfahrzeug":  {"autoscout24": "D", "mobile": "DEMONSTRATION","kleinanzeigen": None},
    "Oldtimer":         {"autoscout24": "O", "mobile": "OLDTIMER",     "kleinanzeigen": None},
}

# ─────────────────────────────────────────
# Количество владельцев (только AutoScout24 и Mobile.de)
# ─────────────────────────────────────────
OWNERS = {
    "1":    {"autoscout24": "1", "mobile": "1", "kleinanzeigen": None},
    "2":    {"autoscout24": "2", "mobile": "2", "kleinanzeigen": None},
    "3":    {"autoscout24": "3", "mobile": "3", "kleinanzeigen": None},
}

# ─────────────────────────────────────────
# Мощность двигателя (кВт)
# ─────────────────────────────────────────
POWER_RANGES = {
    "до 50 кВт":    {"autoscout24": {"powerto": 50},   "mobile": {"maxPowerKw": 50}},
    "50-100 кВт":   {"autoscout24": {"powerfrom": 50, "powerto": 100}, "mobile": {"minPowerKw": 50, "maxPowerKw": 100}},
    "100-150 кВт":  {"autoscout24": {"powerfrom": 100, "powerto": 150},"mobile": {"minPowerKw": 100, "maxPowerKw": 150}},
    "150-200 кВт":  {"autoscout24": {"powerfrom": 150, "powerto": 200},"mobile": {"minPowerKw": 150, "maxPowerKw": 200}},
    "200+ кВт":     {"autoscout24": {"powerfrom": 200}, "mobile": {"minPowerKw": 200}},
}

# ─────────────────────────────────────────
# Цвет кузова
# ─────────────────────────────────────────
COLORS = {
    "Schwarz":  {"autoscout24": "black",  "mobile": "BLACK"},
    "Weiß":     {"autoscout24": "white",  "mobile": "WHITE"},
    "Grau":     {"autoscout24": "grey",   "mobile": "GREY"},
    "Silber":   {"autoscout24": "silver", "mobile": "SILVER"},
    "Blau":     {"autoscout24": "blue",   "mobile": "BLUE"},
    "Rot":      {"autoscout24": "red",    "mobile": "RED"},
    "Grün":     {"autoscout24": "green",  "mobile": "GREEN"},
    "Braun":    {"autoscout24": "brown",  "mobile": "BROWN"},
    "Beige":    {"autoscout24": "beige",  "mobile": "BEIGE"},
    "Gold":     {"autoscout24": "gold",   "mobile": "GOLD"},
    "Orange":   {"autoscout24": "orange", "mobile": "ORANGE"},
    "Gelb":     {"autoscout24": "yellow", "mobile": "YELLOW"},
    "Violett":  {"autoscout24": "purple", "mobile": "PURPLE"},
}

# ─────────────────────────────────────────
# Параметры которых НЕТ на Kleinanzeigen
# (только AutoScout24 и Mobile.de)
# ─────────────────────────────────────────
NOT_AVAILABLE_ON_KLEINANZEIGEN = [
    "OWNERS",
    "DRIVE_TYPE",
    "DOORS",
    "SEATS",
    "POWER_RANGES",
]