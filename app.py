import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Půjčovna strojů", page_icon="🛠️", layout="centered")

# ================== CESTA K DB ==================
DB_PATH = Path(__file__).parent / "pujcovna.db"

# ================== AUTOVYTVOŘENÍ DB ==================
def ensure_db():
    """Vytvoří soubor DB + tabulky a naplní je daty (jen pokud chybí)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Tabulky
    c.execute("""
    CREATE TABLE IF NOT EXISTS klienti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazev_firmy TEXT,
        adresa TEXT,
        ico TEXT,
        sleva REAL,
        kontakt TEXT
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS stroje (
        id TEXT PRIMARY KEY,
        nazev TEXT,
        cena_den REAL
    )""")

    # Naplnění klientů (pouze při prázdné tabulce)
    c.execute("SELECT COUNT(*) FROM klienti")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO klienti VALUES (NULL, ?, ?, ?, ?, ?)", [
            ("BetonSy", "Svitavy, Poličská 58", "51216312", 7, "Jan Novák"),
            ("Stavmont s.r.o.", "Brno, Lidická 58", "12345678", 10, "Michal Malý"),
            ("BetonBau a.s.", "Praha, K Hájům 22", "87654321", 5, "Alena Nová"),
        ])

    # Naplnění strojů (pouze při prázdné tabulce)
    c.execute("SELECT COUNT(*) FROM stroje")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO stroje VALUES (?, ?, ?)", [
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
        ])

    conn.commit()
    conn.close()

def safe_read_sql(query: str) -> pd.DataFrame:
    """Provede SELECT; když chybí tabulky/DB, vytvoří je a dotaz zopakuje."""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except sqlite3.OperationalError:
        # Vytvoř DB/tabulky a zkus znovu
        ensure_db()
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

# Vytvoř DB (pro jistotu) hned po startu
ensure_db()

# ================== STYLY (zkrácené, stabilní) ==================
st.markdown("""
<style>
/* Tmavé inputy */
input, textarea { background:#151515 !important; color:#f5f5f5 !important; border-radius:10px !important; border:1px solid #333 !important; }
div[data-testid="stNumberInput"] input { background:#151515 !important; color:#f5f5f5 !important; border:1px solid #333 !important; font-weight:600 !important; }

/* Select / MultiSelect */
.stMultiSelect div[data-baseweb="select"] > div,
.stSelectbox   div[data-baseweb="select"] > div { background:#151515 !important; color:#f5f5f5 !important; border-radius:10px !important; border:1px solid #333 !important; }
.stMultiSelect div[data-baseweb="select"] span, .stSelectbox div[data-baseweb="select"] span { color:#f5f5f5 !important; }

/* TAGY v multiselectu (už žádná červená) */
.stApp .stMultiSelect div[data-baseweb="tag"]{ background:#06b6d4 !important; color:#ffffff !important; border:0 !important; border-radius:10px !important; box-shadow:0 2px 8px rgba(6,182,212,.35); }
.stApp .stMultiSelect div[data-baseweb="tag"]:hover{ background:#22d3ee !important; }
.stApp .stMultiSelect div[data-baseweb="tag"] svg, .stApp .stMultiSelect div[data-baseweb="tag"] path{ fill:#ffffff !important; color:#ffffff !important; }

/* Metriky */
[data-testid="stMetric"]{ background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.12); border-radius:12px; padding:.6rem .8rem; }

/* Pojistka: skryj případné progress/slidery */
div[role="slider"], div[role="progressbar"], input[type="range"], .stSlider, [data-testid="stSlider"], .stProgress, [data-testid="stProgress"], [data-testid="stProgressBar"]{ display:none !important; height:0 !important; opacity:0 !important; overflow:hidden !important; }
</style>
""", unsafe_allow_html=True)

# ================== DB LOADERS ==================
def nacti_klienty():
    return safe_read_sql("SELECT * FROM klienti")

def nacti_stroje():
    return safe_read_sql("SELECT * FROM stroje")

# ================== DATA ==================
klienti = nacti_klienty()
stroje  = nacti_stroje()

# ================== UI ==================
st.title("🛠️ Půjčovna strojů")
st.caption("Vyber klienta a stroje pro rychlý výpočet ceny pronájmu.")

st.markdown("### 👤 Výběr klienta")
klient = st.selectbox("Vyberte firmu", klienti["nazev_firmy"], label_visibility="collapsed")
sleva = float(klienti.loc[klienti["nazev_firmy"] == klient, "sleva"].values[0])

st.markdown("### 🔧 Výběr strojů")
vybrane_stroje = st.multiselect(
    "Vyberte stroje k pronájmu",
    stroje["nazev"].tolist(),
    help="Můžete vybrat více strojů najednou.",
    label_visibility="collapsed"
)

if vybrane_stroje:
    st.markdown("### ⏱️ Délka pronájmu")

    dny_dict = {}
    for stroj in vybrane_stroje:
        cena = float(stroje.loc[stroje["nazev"] == stroj, "cena_den"].values[0])
        col1, col2, col3 = st.columns([3, 2, 1], vertical_alignment="center")
        with col1:
            st.markdown(f"**{stroj}**")
        with col2:
            st.caption(f"{cena:,.2f} Kč / den")
        with col3:
            dny_dict[stroj] = st.number_input(
                "Počet dní", min_value=1, max_value=365, value=1, key=stroj, label_visibility="collapsed"
            )
        st.divider()

    if st.button("💰 Spočítat celkovou cenu", use_container_width=True):
        celkova = sum(float(stroje.loc[stroje["nazev"] == s, "cena_den"].values[0]) * dny
                      for s, dny in dny_dict.items())
        po_sleve = celkova * (1 - sleva/100)

        c1, c2 = st.columns(2)
        with c1: st.metric("💵 Cena bez slevy", f"{celkova:,.2f} Kč")
        with c2: st.metric("✅ Cena se slevou", f"{po_sleve:,.2f} Kč", delta=f"-{celkova - po_sleve:,.2f} Kč")
else:
    st.info("👆 Vyber alespoň jeden stroj pro výpočet ceny pronájmu.")
