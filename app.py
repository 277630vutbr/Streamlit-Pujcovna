import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Půjčovna strojů", page_icon="🛠️", layout="centered")

# ===== Funkce pro načtení dat =====
def nacti_klienty():
    conn = sqlite3.connect("pujcovna.db")
    df = pd.read_sql_query("SELECT * FROM klienti", conn)
    conn.close()
    return df

def nacti_stroje():
    conn = sqlite3.connect("pujcovna.db")
    df = pd.read_sql_query("SELECT * FROM stroje", conn)
    conn.close()
    return df

# ===== Načtení dat =====
klienti = nacti_klienty()
stroje = nacti_stroje()

# ===== Hlavní aplikace =====
st.title("🛠️ Půjčovna strojů")
st.markdown("Vyber klienta a stroje pro výpočet ceny půjčovného.")

# Výběr klienta (sleva se použije interně, ale není zobrazena)
klient = st.selectbox("Vyber klienta", klienti["nazev_firmy"])
sleva = float(klienti.loc[klienti["nazev_firmy"] == klient, "sleva"].values[0])

st.markdown("---")

# Výběr více strojů
vybrane_stroje = st.multiselect(
    "Vyber stroje k pronájmu",
    stroje["nazev"].tolist(),
    help="Můžeš vybrat více strojů najednou."
)

# Zadání dní pro každý stroj zvlášť
if vybrane_stroje:
    st.subheader("⏱️ Délka pronájmu pro jednotlivé stroje:")
    dny_dict = {}
    for stroj in vybrane_stroje:
        cena = float(stroje.loc[stroje["nazev"] == stroj, "cena_den"].values[0])
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**{stroj}** — {cena:,.2f} Kč / den")
        with col2:
            dny_dict[stroj] = st.number_input(
                f"Dny pro {stroj}", min_value=1, max_value=365, value=1, key=stroj
            )

    st.markdown("---")
    if st.button("💰 Spočítat cenu"):
        celkova_cena = 0
        for stroj, dny in dny_dict.items():
            cena_den = float(stroje.loc[stroje["nazev"] == stroj, "cena_den"].values[0])
            celkova_cena += cena_den * dny

        cena_po_sleve = celkova_cena * (1 - sleva / 100)
        st.success(f"💵 **Cena bez slevy:** {celkova_cena:,.2f} Kč")
        st.success(f"✅ **Celková cena po slevě klienta:** {cena_po_sleve:,.2f} Kč")

else:
    st.info("Vyber alespoň jeden stroj pro výpočet ceny.")
