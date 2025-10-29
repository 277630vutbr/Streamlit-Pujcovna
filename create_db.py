import sqlite3

# Připojení (nebo vytvoření) databáze
conn = sqlite3.connect("pujcovna.db")
cursor = conn.cursor()

# Vytvoření tabulky klientů
cursor.execute("""
CREATE TABLE IF NOT EXISTS klienti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nazev_firmy TEXT,
    adresa TEXT,
    ico TEXT,
    sleva REAL,
    kontakt TEXT
)
""")

# Vytvoření tabulky strojů (bez popisu)
cursor.execute("""
CREATE TABLE IF NOT EXISTS stroje (
    id TEXT PRIMARY KEY,
    nazev TEXT,
    cena_den REAL
)
""")

# Vyčištění starých dat
cursor.execute("DELETE FROM klienti")
cursor.execute("DELETE FROM stroje")

# Vložení klientů
klienti = [
    ("BetonSy", "Svitavy, Poličská 58", "51216312", 7, "Jan Novák"),
    ("Stavmont s.r.o.", "Brno, Lidická 58", "12345678", 10, "Michal Malý"),
    ("BetonBau a.s.", "Praha, K Hájům 22", "87654321", 5, "Alena Nová"),
]
cursor.executemany("INSERT INTO klienti VALUES (NULL, ?, ?, ?, ?, ?)", klienti)

# Vložení strojů (bez popisu)
stroje = [
    ("ST001", "Kladivo AKU vrtací 4 kg NURON", 363.00),
    ("ST002", "Svářečka polyfúzní průměr 20–63 mm", 278.30),
    ("ST003", "Kladivo AKU bourací 15 kg TE-SP 32,8 J NURON", 834.90),
    ("ST004", "Vrtačka jádrová do průměru 350 mm", 1694.00),
    ("ST005", "Šroubovák AKU sádrokartonářský NURON", 242.00),
    ("ST006", "Hřebíkovačka plynová na dřevo HILTI GX 90-WF", 532.40),
    ("ST007", "Nakladač čelní pevný 0,75 m3 KRAMER 5075L", 4840.00),
    ("ST008", "Traktorbagr KOMATSU WB 93R-8", 5082.00),
    ("ST009", "Nakladač smykový 4 t BOBCAT S 650", 4235.00),
    ("ST010", "Bruska excentrická", 260.15),
    ("ST011", "Hoblík tesařský šířka 110 mm", 375.10),
    ("ST012", "Plošina nůžková elektrická 6 m LGMG DEK N06-07E", 888.99),
    ("ST013", "Třídička sítová 230 V", 2662.00),
    ("ST014", "Minirypadlo 1 t BOBCAT E10z LH", 2783.00),
    ("ST015", "Vrták zemní benzínový STIHL BT 131", 907.50),
]
cursor.executemany("INSERT INTO stroje VALUES (?, ?, ?)", stroje)

conn.commit()
conn.close()

print("✅ Databáze byla vytvořena a naplněna daty.")
