# digital-maturity-ai
AI agent za procjenu digitalne zrelosti kompanije (Streamlit app)
# AI Agent za procjenu digitalne zrelosti kompanije

Ovaj projekat predstavlja implementaciju AI agenta za procjenu digitalne zrelosti kompanije,
razvijen u okviru master studija na Univerzitetu Donja Gorica, Fakultet za informacione sisteme i tehnologije,
u sklopu predmeta **Alati i metode softverskog inženjerstva**.

Aplikacija omogućava interaktivnu procjenu digitalne zrelosti kompanije na osnovu unaprijed definisanih
dimenzija, automatsku evaluaciju rezultata, vizualni prikaz i generisanje preporuka za unapređenje.

---

## Funkcionalnosti

- Interaktivni upitnik za procjenu digitalne zrelosti
- Automatizovana evaluacija na osnovu rule-based AI agenta
- Klasifikacija nivoa digitalne zrelosti (početni, srednji, napredni)
- Vizualni prikaz rezultata (grafovi i tekstualni izvještaj)
- Generisanje preporuka za digitalnu transformaciju
- Mogućnost izvoza rezultata u PDF format
- Moderan i user-friendly GUI realizovan pomoću Streamlit-a

---

## Dimenzije procjene digitalne zrelosti

Procjena digitalne zrelosti zasniva se na sljedećim dimenzijama:

1. IT infrastruktura  
2. Automatizacija poslovnih procesa  
3. Upotreba podataka i analitike  
4. Cyber bezbjednost  
5. Digitalne kompetencije zaposlenih  

Svaka dimenzija se ocjenjuje numeričkom skalom, a ukupan rezultat se koristi za određivanje nivoa
digitalne zrelosti kompanije.

---

## Tehnologije i alati

- **Python**
- **Streamlit** – grafički korisnički interfejs
- **NumPy / Pandas** – obrada podataka
- **Matplotlib** – vizualizacija rezultata

---

## Struktura projekta

├── app.py # Streamlit aplikacija (ulazna tačka)
├── agent.py # Logika AI agenta i evaluacija digitalne zrelosti
├── recommendations.py # Generisanje preporuka na osnovu rezultata
├── pdf_utils.py # Izvoz rezultata u PDF format
├── requirements.txt # Spisak potrebnih Python paketa
├── README.md # Dokumentacija projekta
└── DejaVuSans.ttf # Font za PDF i grafički prikaz

---

## Kako pokrenuti aplikaciju

### 1. Kloniranje repozitorijuma
```bash
git clone https://github.com/nurudintivari/digital-maturity-ai.git
cd digital-maturity-ai
pip install -r requirements.txt
streamlit run app.py
```

```md
Aplikacija će se automatski otvoriti u web browseru na adresi:  
http://localhost:8501
```
---

## Napomena

Virtualno okruženje (`venv`) i automatski generisani fajlovi (`__pycache__`) nisu dio repozitorijuma,
u skladu sa Git best practices. Sve potrebne zavisnosti su navedene u `requirements.txt` fajlu.

---

## Akademski kontekst i dalji razvoj

Ovaj projekat predstavlja osnovu za dalju nadogradnju, uključujući:
- unapređenje korisničkog interfejsa
- proširenje upitnika i metodologije procjene
- integraciju mašinskog učenja
- povezivanje sa bazama podataka
- izradu i prijavu IEEE naučnog rada

---

## Autori

- Dijar Mujalović  
- Nurudin Tivari  

**Mentor:** Prof. dr Almir Badnjević  

Univerzitet Donja Gorica  
Fakultet za informacione sisteme i tehnologije



