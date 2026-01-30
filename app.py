import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from agent import evaluate_digital_maturity
from recommendations import get_recommendations
from pdf_utils import generate_pdf

st.set_page_config(
    page_title="Procjena digitalne zrelosti",
    layout="wide"
)
# ================= TEMA =================
tema = st.sidebar.radio("Tema prikaza", ["Svijetla", "Tamna"])

if tema == "Tamna":
    bg = "#0e1117"
    fg = "#ffffff"
    card = "#161b22"
else:
    bg = "#ffffff"
    fg = "#212529"
    card = "#f8f9fa"

st.markdown(f"""
<style>
body {{
    background-color: {bg};
    color: {fg};
}}
.card {{
    background-color: {card};
    padding: 1.2rem;
    border-radius: 12px;
    margin-bottom: 1rem;
}}
</style>
""", unsafe_allow_html=True)
# ================= NAVIGACIJA =================
stranica = st.sidebar.selectbox(
    "Navigacija",
    ["Procjena", "Metodologija"]
)
if stranica == "Metodologija":
    st.title("Metodologija procjene digitalne zrelosti")

    st.markdown("""
    Ova aplikacija koristi **model digitalne zrelosti zasnovan na sposobnostima**.

    ### Dimenzije procjene
    - IT infrastruktura  
    - Procesna digitalizacija  
    - Podaci i analitika  
    - Cyber bezbjednost  
    - Digitalne kompetencije  

    ### Skala ocjenjivanja
    1 – Ne postoji / ad-hoc  
    2 – Djelimično implementirano  
    3 – Implementirano, ali nekonzistentno  
    4 – Standardizovano i mjerljivo  
    5 – Optimizovano i kontinuirano unapređivano  

    ### Izračunavanje indeksa
    - Ocjena dimenzije = prosjek pitanja  
    - Konačni indeks = težinski zbir dimenzija  

    Cyber bezbjednost ima veću težinu zbog svoje ključne uloge u digitalnoj otpornosti.

    ### Izlaz
    - Indeks digitalne zrelosti  
    - Radar dijagram  
    - Histogrami po dimenzijama  
    - PDF izvještaj  
    """)
if stranica == "Procjena":

    st.title("Procjena digitalne zrelosti kompanije")
    st.write("Popunite upitnik kako biste dobili objektivnu procjenu digitalne zrelosti.")

    naziv_kompanije = st.sidebar.text_input(
        "Naziv kompanije",
        placeholder="Unesite naziv kompanije"
    )

    def pitanja(naslov, lista):
        st.sidebar.subheader(naslov)
        return [st.sidebar.radio(p, [1,2,3,4,5], horizontal=True) for p in lista]

    it = pitanja("IT infrastruktura", [
        "Centralizacija informacionih sistema",
        "Skalabilnost IT infrastrukture",
        "Pouzdanost mrežne infrastrukture",
        "Standardizacija IT arhitekture",
        "Postojanje IT razvojnog plana"
    ])

    pr = pitanja("Procesna digitalizacija", [
        "Digitalna podrška procesima",
        "Automatizacija toka podataka",
        "Integrisanost sistema",
        "Mjerenje performansi procesa",
        "Kontinuirano unapređenje procesa"
    ])

    da = pitanja("Podaci i analitika", [
        "Standardizacija podataka",
        "Kvalitet i konzistentnost podataka",
        "Operativna analitika",
        "Strateška analitika",
        "Data governance prakse"
    ])

    cy = pitanja("Cyber bezbjednost", [
        "Formalizovane sigurnosne politike",
        "Kontrola pristupa sistemima",
        "Spremnost za incidente",
        "Sigurnosna testiranja",
        "Integracija bezbjednosti"
    ])

    sk = pitanja("Digitalne kompetencije", [
        "Digitalna pismenost zaposlenih",
        "Programi obuke",
        "Spremnost za nove tehnologije",
        "Upotreba digitalnih alata",
        "Podrška menadžmenta"
    ])
    if st.sidebar.button("🔍 Pokreni procjenu"):

        dimenzije = {
            "IT infrastruktura": sum(it)/5,
            "Procesna digitalizacija": sum(pr)/5,
            "Podaci i analitika": sum(da)/5,
            "Cyber bezbjednost": sum(cy)/5,
            "Digitalne kompetencije": sum(sk)/5
        }

        indeks, nivo = evaluate_digital_maturity(dimenzije)

        st.markdown(
            f"<div class='card'><h2>Indeks digitalne zrelosti: {indeks}</h2><h3>{nivo}</h3></div>",
            unsafe_allow_html=True
        )

        radar_df = pd.DataFrame({
            "Dimenzija": list(dimenzije.keys()) + [list(dimenzije.keys())[0]],
            "Vrijednost": list(dimenzije.values()) + [list(dimenzije.values())[0]]
        })

        fig = px.line_polar(
            radar_df,
            r="Vrijednost",
            theta="Dimenzija",
            line_close=True,
            range_r=[0,5]
        )
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Detaljna analiza po dimenzijama")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**IT infrastruktura**")
            st.plotly_chart(px.histogram(it, nbins=5), use_container_width=True)

        with col2:
            st.markdown("**Procesna digitalizacija**")
            st.plotly_chart(px.histogram(pr, nbins=5), use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("**Podaci i analitika**")
            st.plotly_chart(px.histogram(da, nbins=5), use_container_width=True)

        with col4:
            st.markdown("**Cyber bezbjednost**")
            st.plotly_chart(px.histogram(cy, nbins=5), use_container_width=True)

        st.markdown("**Digitalne kompetencije**")
        st.plotly_chart(px.histogram(sk, nbins=5), use_container_width=True)
        st.subheader("Preporuke za unapređenje")
        for r in get_recommendations(nivo):
            st.write("-", r)

        pdf_fajl = generate_pdf(
            naziv_kompanije,
            indeks,
            nivo,
            dimenzije
        )

        with open(pdf_fajl, "rb") as f:
            st.download_button(
                "📄 Preuzmi PDF izvještaj",
                data=f,
                file_name=pdf_fajl,
                mime="application/pdf"
            )
