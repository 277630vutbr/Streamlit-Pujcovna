import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Půjčovna strojů", page_icon="🛠️", layout="centered")

# --------- VLASTNÍ STYLY (jen to, co theme neumí) ---------
st.markdown("""
<style>
/* tmavé inputy */
input, textarea {
  background-color:#151515 !important;
  color:#f5f5f5 !important;
  border-radius:10px !important;
  border:1px solid #333 !important;
}
div[data-testid="stNumberInput"] input {
  background-color:#151515 !important;
  color:#f5f5f5 !important;
  border:1px solid #333 !important;
  font-weight:600 !important;
}

/* select / multiselect */
.stMultiSelect div[data-baseweb="select"] > div,
.stSelectbox   div[data-baseweb="select"] > div {
  background-color:#151515 !important;
  color:#f5f5f5 !important;
  border-radius:10px !important;
  border:1px solid #333 !important;
}

/* TAGY v multiselectu – tyrkys, bílý text/křížek */
.stMultiSelect div[data-baseweb="tag"]{
  background:#06b6d4 !important;
  color:#ffffff !important;
  border:0 !important;
  border-radius:10px !important;
  box-shadow:0 2px 8px rgba(6,182,212,.35);
}
.stMultiSelect div[data-baseweb="tag"]:hover{ background:#22d3ee !important; }
.stMultiSelect div[data-baseweb="tag"] svg,
.stMultiSelect div[data-baseweb="tag"] path{ fill:#ffffff !important; color:#ffffff !important; }

/* metriky – lehké zvýraznění */
[data-testid="stMetric"]{
  background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.12);
  border-radius:12px; padding:.6rem .8rem;
}

/* (pojistka) schovej progress/slidery, kdyby je Streamlit vyrenderoval */
div[role="slider"], div[role="progressbar"], input[type="range"],
.stSlider, [data-testid="stSlider"], .stProgress, [data-testid="stProgress"], [data-testid="stProgressBar"]{
  display:none !important; height:0 !important; opacity:0 !important; overflow:hidden !important;
}
</style>
""", unsafe_allow_html=True)

# --------- DB HELPERS ---------
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

# --------- DATA ---------
klienti = nacti_klienty()
stroje  = nacti_stroje()

# --------- UI ---------
st.title("🛠️ Půjčovna strojů")
st.caption("Vítejte! Vyberte klienta a stroje pro rychlý výpočet ceny pronájmu.")

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
        with col1: st.markdown(f"**{stroj}**")
        with col2: st.caption(f"{cena:,.2f} Kč / den")
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
    st.info("👆 Vyberte alespoň jeden stroj pro výpočet ceny pronájmu.")

