import sqlite3
import os
import streamlit as st

# -----------------------------------------------------------
# 📦 1️⃣ Vytvoření a naplnění databáze
# -----------------------------------------------------------

DB_PATH = "pujcovna.db"

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Tabulka klientů
    c.execute("""
        CREATE TABLE IF NOT EXISTS klienti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazev_firmy TEXT,
            adresa TEXT,
            ico TEXT,
            sleva REAL,
            kontaktni_osoba TEXT
        )
    """)

    # Tabulka strojů
    c.execute("""
        CREATE TABLE IF NOT EXISTS stroje (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kod TEXT,
            nazev TEXT,
            popis TEXT,
            cena_za_den REAL
        )
    """)

    conn.commit()
    conn.close()


def insert_sample_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Pokud už jsou data vložená, nepřidávat znovu
    c.execute("SELECT COUNT(*) FROM klienti")
    if c.fetchone()[0] == 0:
        c.executemany("""
            INSERT INTO klienti (nazev_firmy, adresa, ico, sleva, kontaktni_osoba)
            VALUES (?, ?, ?, ?, ?)
        """, [
            ("BetonSy", "Svitavy, Poličská 58", "51216312", 0.07, "Jan Novák"),
            ("Stavmont s.r.o.", "Brno, Lidická 58", "12345678", 0.10, "Michal Malý"),
            ("BetonBau a.s.", "Praha, K Hájům 22", "87654321", 0.05, "Alena Nová")
        ])

    c.execute("SELECT COUNT(*) FROM stroje")
    if c.fetchone()[0] == 0:
        c.executemany("""
            INSERT INTO stroje (kod, nazev, popis, cena_za_den)
            VALUES (?, ?, ?, ?)
        """, [
            ("ST001", "Kladivo AKU vrtací 4 kg NURON", "Popis", 363.00),
            ("ST002", "Svářečka polyfúzní průměr 20–63 mm", "Popis", 278.30),
            ("ST003", "Kladivo AKU bourací 15 kg TE-SP 32,8 J NURON", "Popis", 834.90),
            ("ST004", "Vrtačka jádrová do průměru 350 mm", "Popis", 1694.00),
            ("ST005", "Šroubovák AKU sádrokartonářský NURON", "Popis", 242.00),
            ("ST006", "Hřebíkovačka plynová na dřevo HILTI GX 90-WF", "Popis", 532.40),
            ("ST007", "Nakladač čelní pevný 0,75 m3 KRAMER 5075L prodloužené rameno", "Popis", 4840.00),
            ("ST008", "Traktorbagr KOMATSU WB 93R-8", "Popis", 5082.00),
            ("ST009", "Nakladač smykový 4 t BOBCAT S 650", "Popis", 4235.00),
            ("ST010", "Bruska excentrická", "Popis", 260.15),
            ("ST011", "Hoblík tesařský šířka 110 mm", "Popis", 375.10),
            ("ST012", "Plošina nůžková elektrická 6 m LGMG DEK N06-07E", "Popis", 888.99),
            ("ST013", "Třídička sítová 230 V", "Popis", 2662.00),
            ("ST014", "Minirypadlo 1 t BOBCAT E10z LH", "Popis", 2783.00),
            ("ST015", "Vrták zemní benzínový STIHL BT 131", "Popis", 907.50)
        ])

    conn.commit()
    conn.close()


def get_klienti():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nazev_firmy, adresa, ico, sleva, kontaktni_osoba FROM klienti")
    rows = c.fetchall()
    conn.close()
    return rows


def get_stroje():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, kod, nazev, popis, cena_za_den FROM stroje")
    rows = c.fetchall()
    conn.close()
    return rows


# -----------------------------------------------------------
# 💻 2️⃣ Streamlit aplikace
# -----------------------------------------------------------

st.set_page_config(page_title="Půjčovna strojů", layout="wide")

# Inicializace databáze
if not os.path.exists(DB_PATH):
    create_tables()
    insert_sample_data()

st.title("🏗️ Půjčovna stavebních strojů")
st.markdown("Moderní evidence klientů a výpočet půjčovného")

# --- Načtení dat
klienti = get_klienti()
stroje = get_stroje()

# --- Evidence klientů
st.header("📋 Evidence klientů")
st.dataframe(
    [{
        "Název firmy": k[1],
        "Adresa": k[2],
        "IČO": k[3],
        "Sleva (%)": f"{k[4]*100:.0f}",
        "Kontaktní osoba": k[5]
    } for k in klienti],
    use_container_width=True
)

# --- Evidence strojů
st.header("🛠️ Seznam strojů")
st.dataframe(
    [{
        "Kód": s[1],
        "Název stroje": s[2],
        "Popis": s[3],
        "Cena/den (Kč)": f"{s[4]:.2f}"
    } for s in stroje],
    use_container_width=True
)

# --- Výpočet půjčovného
st.header("💰 Výpočet půjčovného")

selected_firma = st.selectbox(
    "Vyberte firmu:",
    [f"{k[1]} ({k[5]}) – sleva {k[4]*100:.0f}%" for k in klienti]
)
selected_stroj = st.selectbox(
    "Vyberte stroj:",
    [f"{s[1]} – {s[2]} ({s[4]} Kč/den)" for s in stroje]
)
pocet_dni = st.number_input("Počet dní:", min_value=1, value=1, step=1)

if st.button("Spočítat cenu"):
    klient = klienti[[f"{k[1]} ({k[5]}) – sleva {k[4]*100:.0f}%" for k in klienti].index(selected_firma)]
    stroj = stroje[[f"{s[1]} – {s[2]} ({s[4]} Kč/den)" for s in stroje].index(selected_stroj)]

    zakladni_cena = stroj[4] * pocet_dni
    celkova_cena = zakladni_cena * (1 - klient[4])

    st.success(f"Základní cena: **{zakladni_cena:.2f} Kč**")
    st.info(f"Sleva firmy: **{klient[4]*100:.0f}%**")
    st.subheader(f"💸 Celková cena: **{celkova_cena:.2f} Kč**")

st.markdown("---")
st.caption("© 2025 Půjčovna stavebních strojů • Python + Streamlit + SQLite")
