import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from calcul_parc_eolian import calculeaza_energie

# Date despre turbine
turbine_data = {
    "Nordex N100 (2.5MW)": {"A": 7854, "N": 12},
    "Vestas V90 (3MW)": {"A": 6362, "N": 10},
    "Repower 5M (5MW)": {"A": 12469, "N": 6}
}

st.title("Analiza comparativă a producției de energie - Parc Eolian de 30 MW")

# Încărcăm automat vitezele
try:
    df = pd.read_excel("viteze.xlsx")
    

    if "v90" not in df.columns:
        st.error("❌ Fișierul trebuie să conțină o coloană numită 'v90'.")
    else:
        viteze = df["v90"].values

        rezultate = {}

        for nume_turbina, date in turbine_data.items():
            A = date["A"]
            N = date["N"]
            energie_totala = calculeaza_energie(viteze, A, N)
            rezultate[nume_turbina] = energie_totala

        # Afișăm energiile frumos cu puncte între mii
        st.subheader("📈 Energie totală anuală produsă de fiecare parc:")
        for turbina, energie in rezultate.items():
            energie_form = f"{energie:,.0f}".replace(",", ".")
            st.write(f"🔹 {turbina}: **{energie_form} MWh/an**")

        # Grafic comparativ
        fig, ax = plt.subplots()
        parc_nume = list(rezultate.keys())
        parc_valori = list(rezultate.values())
        ax.bar(parc_nume, parc_valori)
        ax.set_ylabel('Energie produsă (MWh/an)')
        ax.set_xlabel('Tip Turbină')
        ax.set_title('Comparație între tipurile de turbine')
        st.pyplot(fig)

        # Parc câștigător
        cea_mai_buna = max(rezultate, key=rezultate.get)
        energie_maxima = rezultate[cea_mai_buna]
        energie_maxima_form = f"{energie_maxima:,.0f}".replace(",", ".")

        st.success(f"🏆 Cea mai eficientă turbină: {cea_mai_buna}, cu o producție de {energie_maxima_form} MWh/an!")

        # 🔥 Concluzie detaliată
        st.subheader("📋 Concluzie finală:")
        st.write(f"""
După analiza comparativă a celor trei tipuri de turbine eoliene, s-a constatat că **{cea_mai_buna}** produce cea mai mare cantitate de energie anuală, atingând **{energie_maxima_form} MWh/an**.
Acest rezultat recomandă utilizarea modelului {cea_mai_buna} pentru optimizarea producției de energie într-un parc eolian de 30 MW.

Datele analizate sunt bazate pe viteze medii reale măsurate la 90m înălțime, pe o perioadă de un an.
""")

except FileNotFoundError:
    st.error("❌ Fișierul viteze.xlsx nu a fost găsit în folder. Te rog să îl adaugi în folderul aplicației.")

import streamlit as st
import pandas as pd
import joblib

st.header("Secțiunea AI pentru predicția energiei")

MODEL_FILE = 'model_turbina_castigatoare.pkl'

try:
    model = joblib.load(MODEL_FILE)
except Exception as e:
    st.error(f"Modelul ML nu a putut fi încărcat: {e}")
    model = None

uploaded_file = st.file_uploader("Încarcă fișier Excel cu viteze (.xlsx)", type=["xlsx"])

if uploaded_file is not None and model is not None:
    df = pd.read_excel(uploaded_file)
    if 'v90' in df.columns:
        viteze = df['v90'].values.reshape(-1, 1)
        if st.button("Calculează energia totală AI"):
            predictii = model.predict(viteze)
            energie_ai_mwh = predictii.sum() 
            energie_f = format(energie_ai_mwh, ',.2f').replace(',', 'X').replace('.', ',').replace('X', '.')
            st.write(f"Energie totală AI: {energie_f} MWh")

    else:
        st.error("Coloana 'viteza' nu există în fișier.")
else:
    st.info("Încarcă fișierul Excel pentru a vedea predicția AI.")
