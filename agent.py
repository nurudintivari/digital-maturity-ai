def evaluate_digital_maturity(dimensions: dict):
    weights = {
        "IT infrastruktura": 0.20,
        "Procesna digitalizacija": 0.20,
        "Podaci i analitika": 0.20,
        "Cyber bezbjednost": 0.25,
        "Digitalne kompetencije": 0.15
    }

    indeks = sum(dimensions[d] * weights[d] for d in dimensions)

    if indeks < 2.5:
        nivo = "Početni nivo"
    elif indeks < 3.8:
        nivo = "Srednji nivo"
    else:
        nivo = "Napredni nivo"

    return round(indeks, 2), nivo
