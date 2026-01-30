def get_recommendations(nivo):
    if nivo == "Početni nivo":
        return [
            "Uspostaviti osnovnu IT infrastrukturu.",
            "Standardizovati ključne poslovne procese.",
            "Definisati osnovne cyber bezbjednosne politike.",
            "Pokrenuti programe digitalne obuke zaposlenih."
        ]
    elif nivo == "Srednji nivo":
        return [
            "Povećati stepen automatizacije procesa.",
            "Unaprijediti upravljanje podacima.",
            "Ojačati sigurnosne kontrole.",
            "Razviti jasnu digitalnu strategiju."
        ]
    else:
        return [
            "Primijeniti naprednu analitiku i AI.",
            "Optimizovati procese kroz digitalne platforme.",
            "Kontinuirano testirati cyber otpornost.",
            "Podsticati digitalne inovacije."
        ]
