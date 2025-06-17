CATEGORY_KEYWORDS = {
    "food": {
        "color": "#f94144",
        "keywords": ["biedronka", "lidl", "kaufland", "żabka", "pizza", "kebab", "mc", "burger", "sushi", "carrefour", "lewiatan", "spożywcze"],
    },
    "transport": {
        "color": "#277da1",
        "keywords": ["uber", "bolt", "taxi", "bilet", "pkp", "pks", "bus", "komunikacja", "tramwaj", "paliwo", "orlen", "shell", "bp"],
    },
    "bills": {
        "color": "#f9c74f",
        "keywords": ["czynsz", "prąd", "gaz", "internet", "orange", "play", "plus", "tv", "media", "rachunek"],
    },
    "education": {
        "color": "#90be6d",
        "keywords": ["kurs", "szkoła", "uczelnia", "książka", "edukacja", "nauka", "platforma", "ebook", "udemy", "coursera", "szkolenie"],
    },
    "clothes": {
        "color": "#f3722c",
        "keywords": ["h&m", "reserved", "odzież", "buty", "spodnie", "koszulka", "sklep odzieżowy", "zara", "ccc", "cropp", "sneakersy"],
    },
    "electronics": {
        "color": "#4d908e",
        "keywords": ["media markt", "rtv", "agd", "komputer", "laptop", "elektronika", "telewizor", "x-kom", "morele", "tech"],
    },
    "entertainment": {
        "color": "#9c27b0",
        "keywords": ["kino", "teatr", "muzyka", "koncert", "spotify", "netflix", "hbo", "film", "serial", "rozrywka", "youtube", "gaming", "gry", "twitch"],
    },
    "health": {
        "color": "#4caf50",
        "keywords": ["apteka", "lekarz", "szpital", "medycyna", "wizyta", "badania", "leki", "dentysta", "fitness", "siłownia", "zdrowie", "rehabilitacja", "masaż"],
    }
}

def assign_category(title):
  title = title.lower()
  for category, data in CATEGORY_KEYWORDS.items():
    for keyword in data['keywords']:
      if keyword in title:
        return category
  return 'other'
