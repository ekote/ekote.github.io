#!/usr/bin/env python3
"""Builds every language version of ekote.github.io from one fact base.
Run: python3 build.py   (writes index.html, <lang>/index.html, sitemap.xml). Facts live here, never in the HTML."""
import json, html, os, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://ekote.github.io"
TODAY = datetime.date.today().isoformat()
VERIFY = '<meta name="google-site-verification" content="cSOWqrR3-ff1EmSCDMry0rZuk_c8wklIxxS-CFQkkfg" />'

LANGS = {  # code: (path, hreflang, og_locale, dir)
    "en": ("", "en-US", "en_US", "ltr"),
    "en-gb": ("en-gb/", "en-GB", "en_GB", "ltr"),
    "pl": ("pl/", "pl-PL", "pl_PL", "ltr"),
    "de": ("de/", "de-DE", "de_DE", "ltr"),
    "fr": ("fr/", "fr-FR", "fr_FR", "ltr"),
    "es": ("es/", "es-ES", "es_ES", "ltr"),
    "it": ("it/", "it-IT", "it_IT", "ltr"),
    "ar": ("ar/", "ar", "ar_AR", "rtl"),
}
SWITCH = [("en", "English (US)"), ("en-gb", "English (UK)"), ("pl", "Polski"), ("de", "Deutsch"), ("fr", "Français"), ("es", "Español"), ("it", "Italiano"), ("ar", "العربية")]

SAME_AS = [
    "https://orcid.org/0000-0001-8308-7129",
    "https://scholar.google.com/citations?user=wF7USzwAAAAJ",
    "https://www.researchgate.net/profile/Estera-Kot",
    "https://www.linkedin.com/in/esterakot/",
    "https://github.com/ekote",
    "https://x.com/estera_kot",
    "https://mvp.microsoft.com/en-US/MVP/profile/dee98064-3431-4a89-80f8-148643d8f705",
    "https://www.f6s.com/drkot",
]
LINKS = [  # hero: academic identity only
    ("https://orcid.org/0000-0001-8308-7129", "ORCID 0000-0001-8308-7129"),
    ("https://scholar.google.com/citations?user=wF7USzwAAAAJ", "Google Scholar"),
]
CV_LABEL = {"en": "Bio (PDF)", "en-gb": "Bio (PDF)", "pl": "Bio (PDF)", "de": "Bio (PDF)", "fr": "Bio (PDF)", "es": "Bio (PDF)", "it": "Bio (PDF)", "ar": "السيرة (PDF)"}
FOOTER_LINKS = [
    ("https://www.researchgate.net/profile/Estera-Kot", "ResearchGate"),
    ("https://www.linkedin.com/in/esterakot/", "LinkedIn"),
    ("https://github.com/ekote", "GitHub"),
    ("https://x.com/estera_kot", "X"),
    ("https://mvp.microsoft.com/en-US/MVP/profile/dee98064-3431-4a89-80f8-148643d8f705", "Microsoft MVP"),
]
UPDATED = {"en": "Last updated", "en-gb": "Last updated", "pl": "Ostatnia aktualizacja", "de": "Zuletzt aktualisiert", "fr": "Dernière mise à jour", "es": "Última actualización", "it": "Ultimo aggiornamento", "ar": "آخر تحديث"}
PUBS = [  # (year, kind, title, authors, venue, doi)
    (2024, "journal", "Semantic segmentation of the prostate based on onefold and joint multimodal medical images using YOLOv4 and U-Net", "E. Kot, T. Les, Z. Krawczyk-Borysiak, A. Vykhodtsev, K. Siwek", "Applied Sciences, 14(21), 9814, MDPI", "10.3390/app14219814"),
    (2021, "journal", "Deep learning-based framework for tumour detection and semantic segmentation", "E. Kot, Z. Krawczyk, K. Siwek, L. Królicki, P. Czwarnowski", "Bulletin of the Polish Academy of Sciences: Technical Sciences, e136750", "10.24425/bpasts.2021.136750"),
    (2020, "journal", "Architektura platformy korzystającej z metod uczenia maszynowego do przetwarzania obrazów biomedycznych w chmurze", "E. Kot, K. Siwek, E. Wińska", "Poznan University of Technology Academic Journals: Electrical Engineering, 104, 35-44", ""),
    (2019, "journal", "Algorytm segmentacji obrazów CT i PET do identyfikacji i wyznaczania objętości glejaka mózgu", "E. Kot, K. Siwek", "Poznan University of Technology Academic Journals: Electrical Engineering", ""),
    (2021, "conference", "U-Net training models for efficient brain tumour segmentation on multi-modality CT and PET images", "E. Kot, Z. Krawczyk, K. Siwek, K. Pleska, J. Rogalski, P. Czwarnowski", "22nd International Conference on Computational Problems of Electrical Engineering (CPEE), IEEE, 1-4", "10.1109/cpee54040.2021.9585272"),
    (2021, "conference", "Volumetric Modulated Arc Therapy dose distribution prediction for breast cancer patients: CNN approach", "Z. Krawczyk, R. Szmurło, P. Zawadzki, E. Kot, J. Starzyński, A. Zawadzka", "International Joint Conference on Neural Networks (IJCNN), IEEE, 1-10", "10.1109/ijcnn52387.2021.9533826"),
    (2021, "conference", "Reducing the uncertainty of agile software development using a random forest classification algorithm", "E. Wińska, E. Kot, W. Dąbrowski", "Lean and Agile Software Development (LASD 2021), Springer, 145-155", "10.1007/978-3-030-67084-9_9"),
    (2020, "conference", "U-Net and active contour methods for brain tumour segmentation and visualization", "E. Kot, Z. Krawczyk, K. Siwek, P. S. Czwarnowski", "International Joint Conference on Neural Networks (IJCNN), IEEE, 1-7", "10.1109/ijcnn48605.2020.9207572"),
    (2019, "conference", "Segmentation of brain biomedical images to compute the volume of gliomas", "E. Kot, K. Siwek", "ITM Web of Conferences, 28, EDP Sciences", "10.1051/itmconf/20192801016"),
    (2019, "conference", "Weryfikacja wyników obrazowania medycznego mózgu za pomocą testu na fantomie PET-CT", "E. Kot, K. Siwek", "XLII International Conference on Fundamentals of Electrotechnics and Circuit Theory (IC-SPETO 2019), Silesian University of Technology", ""),
    (2024, "thesis", "Multimodal medical image processing methods for computer-aided diagnosis support system of brain tumors", "E. Kot", "Ph.D. dissertation, Warsaw University of Technology, Institute of the Theory of Electrical Engineering, Measurement and Information Systems", ""),
    (2020, "other", "Brain tumour detection and segmentation using deep learning methods", "E. Kot, Z. Krawczyk, K. Siwek", "", ""),
    (2020, "other", "Improved Morphological Geodesic Active Contours algorithm for automated, voxel-wise segmentation of biomedical images", "E. Kot, Z. Krawczyk, K. Siwek", "", ""),
]

PUB_TITLE_EN = {
    "Architektura platformy korzystającej z metod uczenia maszynowego do przetwarzania obrazów biomedycznych w chmurze":
        "Architecture of a cloud platform using machine learning methods for biomedical image processing",
    "Algorytm segmentacji obrazów CT i PET do identyfikacji i wyznaczania objętości glejaka mózgu":
        "A CT and PET image segmentation algorithm for identifying and measuring the volume of brain glioma",
    "Weryfikacja wyników obrazowania medycznego mózgu za pomocą testu na fantomie PET-CT":
        "Verification of brain medical imaging results using a PET-CT phantom test",
}
PUB_IN_POLISH = {"en": "in Polish", "en-gb": "in Polish", "de": "auf Polnisch", "fr": "en polonais", "es": "en polaco", "it": "in polacco", "ar": "بالبولندية", "pl": ""}

# ---------------------------------------------------------------- texts
T = {}

T["en"] = dict(
    name="Dr. Estera Kot", page_title="Dr. Estera Kot",
    meta="Dr. Estera Kot, Ph.D. in Computer Science. Chief Technology Officer at Clouds on Mars, lecturer at Kozminski University, former Principal Product Manager at Microsoft for the Apache Spark runtime in Azure Synapse Analytics and Microsoft Fabric. Research in deep learning for medical imaging and large-scale data systems.",
    og="Computer scientist. CTO at Clouds on Mars, lecturer at Kozminski University, former Microsoft Principal PM for Apache Spark in Azure Synapse Analytics and Microsoft Fabric.",
    alt="Portrait of Dr. Estera Kot",
    nav=["Research", "Publications", "Teaching", "Industry", "Honors", "Contact"],
    titles=["Chief Technology Officer, Clouds on Mars", "Lecturer, Kozminski University, Warsaw", "Formerly Principal Product Manager, Microsoft (Azure Synapse Analytics, Microsoft Fabric)"],
    office="Office hours",
    h_about="About",
    about=[
        "Dr. Estera Kot is a computer scientist working at the intersection of machine learning, large-scale data systems, and the organizations that depend on them. Her doctoral research applied deep learning to brain biomedical image segmentation for glioma volume estimation. Her industry work took that interest in scale to its logical end: the Apache Spark runtime that powers analytics, machine learning, and Copilot workloads across Azure Synapse Analytics and Microsoft Fabric.",
        "She earned her Ph.D. in Computer Science with distinction from the Warsaw University of Technology. She holds a U.S. patent in big data processing and has published fifteen peer-reviewed papers, twelve as first author, presented at venues including Glasgow and Redmond.",
        "Her position on AI is uncompromising. The engineer who builds a system cannot outsource moral responsibility to regulators or ethicists. Ethics are not a compliance layer added after the architecture is fixed. They live in every optimization target, every default, every choice about what the machine rewards and what it ignores.",
    ],
    h_research="Research", h_interests="Interests", h_selected="Selected work",
    interests=["Deep learning for biomedical image analysis, in particular brain tumor segmentation and volume estimation", "Vectorized execution engines for Apache Spark and lakehouse architectures", "Large-scale data platform migration and engine lifecycle management", "AI governance as an engineering discipline rather than a compliance layer"],
    selected=["Ph.D. dissertation: brain biomedical image segmentation for glioma volume estimation, Warsaw University of Technology, with distinction", "U.S. patent in big data processing", "Native Execution Engine for Microsoft Fabric: a vectorized Spark runtime built with Intel, Meta, and IBM, four times faster than open-source Spark", "Fifteen peer-reviewed publications. Full list on {scholar} and {orcid}"],
    h_pubs="Publications", pubs_intro="From {scholar}. Author names as published. Works published in Polish are listed with an English title and the original in brackets.",
    pub_groups={"journal": "Journal articles", "conference": "Conference papers", "thesis": "Doctoral dissertation", "other": "Other manuscripts"},
    h_teaching="Teaching",
    teaching=[
        "Dr. Kot teaches Python programming at Kozminski University in Warsaw and has lectured as a guest at UCLA and Łazarski University. At the Warsaw University of Technology she designed original graduate and postgraduate curricula in AI-in-Cloud technologies, including the postgraduate program <em>Applications of Cloud Technologies Based on Data and Artificial Intelligence</em> (2022). Her former students now work at CERN, Google, Meta, and other research institutions.",
        "She creates and hosts <em>Fabric Espresso</em>, a technical video series on Microsoft Fabric with 89 episodes, and speaks regularly at FabCon Europe.",
    ],
    h_service="Service",
    service=["Chair, later member, Faculty Doctoral Council, Faculty of Electrical Engineering, Warsaw University of Technology", "Recognized by the Rector of the Warsaw University of Technology for leadership in the Doctoral Council"],
    h_industry="Industry",
    industry=[
        "As Chief Technology Officer at Clouds on Mars, a Microsoft and Databricks partner delivering data and AI across Europe and the Middle East, Dr. Kot owns technical strategy, engineering delivery, and the architecture behind the firm's most strategic accounts in healthcare, insurance, and enterprise data platforms.",
        "At Microsoft she was Principal Product Manager for the Apache Spark runtime across Azure Synapse Analytics and Microsoft Fabric. She migrated 25,000 Synapse customers to Fabric, automated the program that moves 30,000 customers between engine versions every six months, and led cross-functional teams of nearly 300 engineers, designers, and stakeholders. Her earlier roles include Intel, Sony, Citi, and Procter and Gamble, where she introduced Apache Spark and Delta Lake in 2018.",
    ],
    h_honors="Honors",
    honors=["Microsoft Most Valuable Professional (MVP), {mvp}", "Laureate, Polka XXI wieku, innovation and new technology, 2026", "Top 100 Women in AI in Poland; Top 3 for AI Leadership; Top 100 Women in Cloud Computing", "Winner, Microsoft Global Hackathon, healthcare, 2021", "Distinction award for top-performing doctoral candidates, every year of doctoral studies, Warsaw University of Technology"],
    mvp_label="profile",
    h_contact="Contact",
    contact="The quickest way to reach Dr. Kot is to book a slot: {book}. For research correspondence, use the e-mail listed on her {orcid_record}.",
    orcid_record="ORCID record",
    footer="Dr. Estera Kot, Warsaw and Gdynia, Poland.", privacy="Privacy", terms="Terms",
    ld_desc="Computer scientist. Chief Technology Officer at Clouds on Mars, lecturer at Kozminski University, former Principal Product Manager at Microsoft for the Apache Spark runtime in Azure Synapse Analytics and Microsoft Fabric. Ph.D. in Computer Science with distinction, Warsaw University of Technology.",
    ld_jobs=["Chief Technology Officer", "Lecturer"],
    ld_knows=["Machine learning", "Deep learning", "Biomedical image segmentation", "Glioma volume estimation", "Apache Spark", "Microsoft Fabric", "Azure Synapse Analytics", "Lakehouse architecture", "Big data processing", "AI governance", "Cloud computing"],
    ld_awards=["Microsoft Most Valuable Professional (MVP)", "Laureate, Polka XXI wieku, innovation and new technology (2026)", "Top 100 Women in AI in Poland", "Top 3 for AI Leadership, Poland", "Top 100 Women in Cloud Computing", "Winner, Microsoft Global Hackathon, healthcare (2021)"],
    ld_phd="Ph.D. in Computer Science, with distinction",
    orgs=dict(com="Clouds on Mars", koz="Kozminski University", pw="Warsaw University of Technology"),
    alt_names=["Dr. Estera Kot", "dr Estera Kot", "Estera Kot, Ph.D.", "Estera Kot PhD"],
    pubs_name="Publications of Dr. Estera Kot",
)

# British English: spelling only.
_gb = json.loads(json.dumps(T["en"]))
def _british(s):
    for a, b in [("organizations", "organisations"), ("optimization", "optimisation"), ("Recognized", "Recognised"), ("program ", "programme "), ("program<", "programme<"), ("postgraduate program", "postgraduate programme"), ("Honors", "Honours"), ("tumor", "tumour"), ("healthcare", "healthcare"), ("center", "centre"), ("vectorized", "vectorised"), ("Vectorized", "Vectorised"), ("visualization", "visualisation")]:
        s = s.replace(a, b)
    return s
def _walk(o):
    if isinstance(o, str): return _british(o)
    if isinstance(o, list): return [_walk(x) for x in o]
    if isinstance(o, dict): return {k: _walk(v) for k, v in o.items()}
    return o
T["en-gb"] = _walk(_gb)
T["en-gb"]["ld_phd"] = "PhD in Computer Science, with distinction"
T["en-gb"]["titles"][2] = "Formerly Principal Product Manager, Microsoft (Azure Synapse Analytics, Microsoft Fabric)"
T["en-gb"]["alt_names"] = ["Dr Estera Kot", "dr Estera Kot", "Estera Kot PhD", "Estera Kot, Ph.D."]
T["en-gb"]["name"] = "Dr Estera Kot"; T["en-gb"]["page_title"] = "Dr Estera Kot"
T["en-gb"]["footer"] = "Dr Estera Kot, Warsaw and Gdynia, Poland."
T["en-gb"]["alt"] = "Portrait of Dr Estera Kot"
T["en-gb"]["pubs_name"] = "Publications of Dr Estera Kot"

T["pl"] = dict(
    name="dr Estera Kot", page_title="dr Estera Kot",
    meta="Dr Estera Kot, doktor nauk technicznych w dyscyplinie informatyka. Chief Technology Officer w Clouds on Mars, wykładowczyni Akademii Leona Koźmińskiego, wcześniej Principal Product Manager w Microsoft odpowiedzialna za środowisko Apache Spark w Azure Synapse Analytics i Microsoft Fabric. Badania: głębokie uczenie w obrazowaniu medycznym i systemy danych wielkiej skali.",
    og="Informatyczka. CTO w Clouds on Mars, wykładowczyni Akademii Leona Koźmińskiego, była Principal PM w Microsoft odpowiedzialna za Apache Spark w Azure Synapse Analytics i Microsoft Fabric.",
    alt="Portret dr Estery Kot",
    nav=["Badania", "Publikacje", "Dydaktyka", "Przemysł", "Wyróżnienia", "Kontakt"],
    titles=["Chief Technology Officer, Clouds on Mars", "Wykładowczyni, Akademia Leona Koźmińskiego, Warszawa", "Wcześniej Principal Product Manager, Microsoft (Azure Synapse Analytics, Microsoft Fabric)"],
    office="Konsultacje",
    h_about="O mnie",
    about=[
        "Dr Estera Kot jest informatyczką pracującą na styku uczenia maszynowego, systemów danych wielkiej skali i organizacji, które od nich zależą. W rozprawie doktorskiej zastosowała głębokie uczenie do segmentacji biomedycznych obrazów mózgu w celu wyznaczania objętości glejaka. W przemyśle doprowadziła to zainteresowanie skalą do logicznego końca: do środowiska uruchomieniowego Apache Spark, które napędza analitykę, uczenie maszynowe i obciążenia Copilot w Azure Synapse Analytics i Microsoft Fabric.",
        "Stopień doktora nauk technicznych w dyscyplinie informatyka uzyskała z wyróżnieniem na Politechnice Warszawskiej. Jest współautorką patentu w USA z zakresu przetwarzania big data i autorką piętnastu recenzowanych publikacji, w tym dwunastu jako pierwsza autorka, prezentowanych między innymi w Glasgow i Redmond.",
        "Jej stanowisko wobec AI jest bezkompromisowe. Inżynier, który buduje system, nie może przerzucić odpowiedzialności moralnej na regulatorów ani etyków. Etyka nie jest warstwą zgodności dokładaną po ustaleniu architektury. Mieszka w każdej funkcji celu, w każdym ustawieniu domyślnym, w każdej decyzji o tym, co maszyna nagradza, a co ignoruje.",
    ],
    h_research="Badania", h_interests="Zainteresowania", h_selected="Wybrane prace",
    interests=["Głębokie uczenie w analizie obrazów biomedycznych, w szczególności segmentacja guzów mózgu i wyznaczanie ich objętości", "Wektoryzowane silniki wykonawcze dla Apache Spark i architektury lakehouse", "Migracje platform danych wielkiej skali i zarządzanie cyklem życia silników", "Nadzór nad AI jako dyscyplina inżynierska, a nie warstwa zgodności"],
    selected=["Rozprawa doktorska: segmentacja biomedycznych obrazów mózgu do wyznaczania objętości glejaka, Politechnika Warszawska, z wyróżnieniem", "Patent w USA z zakresu przetwarzania big data", "Native Execution Engine dla Microsoft Fabric: wektoryzowane środowisko Spark zbudowane z Intel, Meta i IBM, czterokrotnie szybsze od otwartego Sparka", "Piętnaście recenzowanych publikacji. Pełna lista w {scholar} i {orcid}"],
    h_pubs="Publikacje", pubs_intro="Za {scholar}. Nazwiska autorów jak w publikacjach, tytuły w oryginale.",
    pub_groups={"journal": "Artykuły w czasopismach", "conference": "Referaty konferencyjne", "thesis": "Rozprawa doktorska", "other": "Inne manuskrypty"},
    h_teaching="Dydaktyka",
    teaching=[
        "Dr Kot prowadzi zajęcia z programowania w Pythonie w Akademii Leona Koźmińskiego w Warszawie, wykładała gościnnie na UCLA i Uczelni Łazarskiego. Na Politechnice Warszawskiej zaprojektowała autorskie programy studiów magisterskich i podyplomowych z technologii AI w chmurze, w tym studia podyplomowe <em>Zastosowania technologii chmurowych opartych na danych i sztucznej inteligencji</em> (2022). Jej byli studenci pracują dziś w CERN, Google, Meta i innych instytucjach badawczych.",
        "Tworzy i prowadzi <em>Fabric Espresso</em>, techniczną serię wideo o Microsoft Fabric liczącą 89 odcinków, i regularnie występuje na FabCon Europe.",
    ],
    h_service="Działalność organizacyjna",
    service=["Przewodnicząca, później członkini Wydziałowej Rady Doktorantów, Wydział Elektryczny Politechniki Warszawskiej", "Wyróżniona przez Rektora Politechniki Warszawskiej za przewodzenie Radzie Doktorantów"],
    h_industry="Przemysł",
    industry=[
        "Jako Chief Technology Officer w Clouds on Mars, partnerze Microsoft i Databricks dostarczającym rozwiązania danych i AI w Europie i na Bliskim Wschodzie, dr Kot odpowiada za strategię technologiczną, realizację inżynierską i architekturę najważniejszych projektów firmy w ochronie zdrowia, ubezpieczeniach i platformach danych klasy enterprise.",
        "W Microsoft była Principal Product Manager odpowiedzialną za środowisko Apache Spark w Azure Synapse Analytics i Microsoft Fabric. Przeprowadziła migrację 25 000 klientów Synapse do Fabric, zautomatyzowała program przenoszący 30 000 klientów między wersjami silnika co sześć miesięcy i kierowała interdyscyplinarnymi zespołami liczącymi blisko 300 inżynierów, projektantów i interesariuszy. Wcześniej pracowała w Intel, Sony, Citi i Procter and Gamble, gdzie w 2018 roku wprowadziła Apache Spark i Delta Lake.",
    ],
    h_honors="Wyróżnienia",
    honors=["Microsoft Most Valuable Professional (MVP), {mvp}", "Laureatka konkursu Polka XXI wieku w kategorii innowacje i nowe technologie, 2026", "Top 100 Kobiet w AI w Polsce; Top 3 w kategorii AI Leadership; Top 100 Kobiet w Chmurze", "Zwyciężczyni Microsoft Global Hackathon w kategorii ochrona zdrowia, 2021", "Stypendium dla najlepszych doktorantów w każdym roku studiów doktoranckich, Politechnika Warszawska"],
    mvp_label="profil",
    h_contact="Kontakt",
    contact="Najszybsza droga do dr Kot to rezerwacja terminu: {book}. W sprawach naukowych proszę pisać na adres podany w jej {orcid_record}.",
    orcid_record="rekordzie ORCID",
    footer="dr Estera Kot, Warszawa i Gdynia.", privacy="Prywatność", terms="Regulamin",
    ld_desc="Informatyczka. Chief Technology Officer w Clouds on Mars, wykładowczyni Akademii Leona Koźmińskiego, była Principal Product Manager w Microsoft odpowiedzialna za środowisko Apache Spark w Azure Synapse Analytics i Microsoft Fabric. Doktor nauk technicznych w dyscyplinie informatyka z wyróżnieniem, Politechnika Warszawska.",
    ld_jobs=["Chief Technology Officer", "Wykładowczyni"],
    ld_knows=["Uczenie maszynowe", "Głębokie uczenie", "Segmentacja obrazów biomedycznych", "Wyznaczanie objętości glejaka", "Apache Spark", "Microsoft Fabric", "Azure Synapse Analytics", "Architektura lakehouse", "Przetwarzanie big data", "Nadzór nad AI", "Chmura obliczeniowa"],
    ld_awards=["Microsoft Most Valuable Professional (MVP)", "Laureatka Polka XXI wieku, innowacje i nowe technologie (2026)", "Top 100 Kobiet w AI w Polsce", "Top 3 AI Leadership, Polska", "Top 100 Kobiet w Chmurze", "Zwyciężczyni Microsoft Global Hackathon, ochrona zdrowia (2021)"],
    ld_phd="Doktor nauk technicznych w dyscyplinie informatyka, z wyróżnieniem",
    orgs=dict(com="Clouds on Mars", koz="Akademia Leona Koźmińskiego", pw="Politechnika Warszawska"),
    alt_names=["dr Estera Kot", "Dr Estera Kot", "dr inż. Estera Kot", "Estera Kot"],
    pubs_name="Publikacje dr Estery Kot",
)

T["de"] = dict(
    name="Dr. Estera Kot", page_title="Dr. Estera Kot",
    meta="Dr. Estera Kot, promovierte Informatikerin. Chief Technology Officer bei Clouds on Mars, Dozentin an der Kozminski-Universität Warschau, zuvor Principal Product Manager bei Microsoft für die Apache-Spark-Laufzeit in Azure Synapse Analytics und Microsoft Fabric. Forschung zu Deep Learning in der medizinischen Bildgebung und zu Datensystemen im großen Maßstab.",
    og="Informatikerin. CTO bei Clouds on Mars, Dozentin an der Kozminski-Universität, ehemalige Principal PM bei Microsoft für Apache Spark in Azure Synapse Analytics und Microsoft Fabric.",
    alt="Porträt von Dr. Estera Kot",
    nav=["Forschung", "Publikationen", "Lehre", "Industrie", "Auszeichnungen", "Kontakt"],
    titles=["Chief Technology Officer, Clouds on Mars", "Dozentin, Kozminski-Universität, Warschau", "Zuvor Principal Product Manager, Microsoft (Azure Synapse Analytics, Microsoft Fabric)"],
    office="Sprechstunde",
    h_about="Über",
    about=[
        "Dr. Estera Kot ist Informatikerin und arbeitet an der Schnittstelle von maschinellem Lernen, Datensystemen im großen Maßstab und den Organisationen, die davon abhängen. In ihrer Dissertation wandte sie Deep Learning auf die Segmentierung biomedizinischer Hirnaufnahmen zur Bestimmung des Gliomvolumens an. In der Industrie führte sie dieses Interesse an Skalierung zu seinem logischen Ende: der Apache-Spark-Laufzeit, die Analytik, maschinelles Lernen und Copilot-Workloads in Azure Synapse Analytics und Microsoft Fabric antreibt.",
        "Sie promovierte mit Auszeichnung in Informatik an der Technischen Universität Warschau. Sie hält ein US-Patent im Bereich Big-Data-Verarbeitung und hat fünfzehn begutachtete Arbeiten veröffentlicht, zwölf davon als Erstautorin, vorgestellt unter anderem in Glasgow und Redmond.",
        "Ihre Haltung zur KI ist kompromisslos. Wer ein System baut, kann die moralische Verantwortung nicht an Regulierer oder Ethiker auslagern. Ethik ist keine Compliance-Schicht, die nach Festlegung der Architektur hinzugefügt wird. Sie lebt in jedem Optimierungsziel, in jeder Voreinstellung, in jeder Entscheidung darüber, was die Maschine belohnt und was sie ignoriert.",
    ],
    h_research="Forschung", h_interests="Schwerpunkte", h_selected="Ausgewählte Arbeiten",
    interests=["Deep Learning für die biomedizinische Bildanalyse, insbesondere Segmentierung von Hirntumoren und Volumenbestimmung", "Vektorisierte Ausführungs-Engines für Apache Spark und Lakehouse-Architekturen", "Migration großer Datenplattformen und Lebenszyklusmanagement von Engines", "KI-Governance als Ingenieursdisziplin statt als Compliance-Schicht"],
    selected=["Dissertation: Segmentierung biomedizinischer Hirnaufnahmen zur Bestimmung des Gliomvolumens, Technische Universität Warschau, mit Auszeichnung", "US-Patent im Bereich Big-Data-Verarbeitung", "Native Execution Engine für Microsoft Fabric: eine vektorisierte Spark-Laufzeit, entwickelt mit Intel, Meta und IBM, viermal schneller als Open-Source-Spark", "Fünfzehn begutachtete Publikationen. Vollständige Liste bei {scholar} und {orcid}"],
    h_pubs="Publikationen", pubs_intro="Nach {scholar}. Autorennamen wie veröffentlicht, Titel im Original.",
    pub_groups={"journal": "Zeitschriftenartikel", "conference": "Konferenzbeiträge", "thesis": "Dissertation", "other": "Weitere Manuskripte"},
    h_teaching="Lehre",
    teaching=[
        "Dr. Kot unterrichtet Python-Programmierung an der Kozminski-Universität in Warschau und war Gastdozentin an der UCLA und der Łazarski-Universität. An der Technischen Universität Warschau entwarf sie eigene Master- und Weiterbildungscurricula zu KI-in-der-Cloud-Technologien, darunter den Weiterbildungsstudiengang <em>Applications of Cloud Technologies Based on Data and Artificial Intelligence</em> (2022). Ihre ehemaligen Studierenden arbeiten heute bei CERN, Google, Meta und anderen Forschungseinrichtungen.",
        "Sie produziert und moderiert <em>Fabric Espresso</em>, eine technische Videoreihe zu Microsoft Fabric mit 89 Folgen, und spricht regelmäßig auf der FabCon Europe.",
    ],
    h_service="Gremienarbeit",
    service=["Vorsitzende, später Mitglied des Doktorandenrats der Fakultät für Elektrotechnik, Technische Universität Warschau", "Vom Rektor der Technischen Universität Warschau für die Leitung des Doktorandenrats ausgezeichnet"],
    h_industry="Industrie",
    industry=[
        "Als Chief Technology Officer bei Clouds on Mars, einem Microsoft- und Databricks-Partner für Daten und KI in Europa und dem Nahen Osten, verantwortet Dr. Kot die Technologiestrategie, die technische Umsetzung und die Architektur der strategisch wichtigsten Kundenprojekte des Unternehmens im Gesundheitswesen, in der Versicherungsbranche und bei Unternehmensdatenplattformen.",
        "Bei Microsoft war sie Principal Product Manager für die Apache-Spark-Laufzeit in Azure Synapse Analytics und Microsoft Fabric. Sie migrierte 25.000 Synapse-Kunden zu Fabric, automatisierte das Programm, das alle sechs Monate 30.000 Kunden zwischen Engine-Versionen bewegt, und leitete bereichsübergreifende Teams mit nahezu 300 Ingenieuren, Designern und Stakeholdern. Frühere Stationen waren Intel, Sony, Citi und Procter and Gamble, wo sie 2018 Apache Spark und Delta Lake einführte.",
    ],
    h_honors="Auszeichnungen",
    honors=["Microsoft Most Valuable Professional (MVP), {mvp}", "Preisträgerin Polka XXI wieku, Innovation und neue Technologien, 2026", "Top 100 Frauen in der KI in Polen; Top 3 für KI-Führung; Top 100 Frauen im Cloud Computing", "Gewinnerin des Microsoft Global Hackathon, Gesundheitswesen, 2021", "Auszeichnung für die besten Doktoranden in jedem Jahr der Promotion, Technische Universität Warschau"],
    mvp_label="Profil",
    h_contact="Kontakt",
    contact="Am schnellsten erreicht man Dr. Kot über eine Terminbuchung: {book}. Für wissenschaftliche Korrespondenz gilt die E-Mail-Adresse in ihrem {orcid_record}.",
    orcid_record="ORCID-Eintrag",
    footer="Dr. Estera Kot, Warschau und Gdynia, Polen.", privacy="Datenschutz", terms="Nutzungsbedingungen",
    ld_desc="Informatikerin. Chief Technology Officer bei Clouds on Mars, Dozentin an der Kozminski-Universität, ehemalige Principal Product Manager bei Microsoft für die Apache-Spark-Laufzeit in Azure Synapse Analytics und Microsoft Fabric. Promotion in Informatik mit Auszeichnung, Technische Universität Warschau.",
    ld_jobs=["Chief Technology Officer", "Dozentin"],
    ld_knows=["Maschinelles Lernen", "Deep Learning", "Biomedizinische Bildsegmentierung", "Gliomvolumenbestimmung", "Apache Spark", "Microsoft Fabric", "Azure Synapse Analytics", "Lakehouse-Architektur", "Big-Data-Verarbeitung", "KI-Governance", "Cloud Computing"],
    ld_awards=["Microsoft Most Valuable Professional (MVP)", "Preisträgerin Polka XXI wieku, Innovation und neue Technologien (2026)", "Top 100 Frauen in der KI in Polen", "Top 3 KI-Führung, Polen", "Top 100 Frauen im Cloud Computing", "Gewinnerin Microsoft Global Hackathon, Gesundheitswesen (2021)"],
    ld_phd="Promotion in Informatik, mit Auszeichnung",
    orgs=dict(com="Clouds on Mars", koz="Kozminski-Universität", pw="Technische Universität Warschau"),
    alt_names=["Dr. Estera Kot", "Estera Kot", "Dr Estera Kot"],
    pubs_name="Publikationen von Dr. Estera Kot",
)

T["fr"] = dict(
    name="Dr Estera Kot", page_title="Dr Estera Kot",
    meta="Dr Estera Kot, docteure en informatique. Directrice de la technologie (CTO) chez Clouds on Mars, enseignante à l'université Kozminski de Varsovie, ancienne Principal Product Manager chez Microsoft, responsable du moteur Apache Spark d'Azure Synapse Analytics et de Microsoft Fabric. Recherche en apprentissage profond pour l'imagerie médicale et en systèmes de données à grande échelle.",
    og="Informaticienne. CTO chez Clouds on Mars, enseignante à l'université Kozminski, ancienne Principal PM chez Microsoft pour Apache Spark dans Azure Synapse Analytics et Microsoft Fabric.",
    alt="Portrait de la Dr Estera Kot",
    nav=["Recherche", "Publications", "Enseignement", "Industrie", "Distinctions", "Contact"],
    titles=["Directrice de la technologie (CTO), Clouds on Mars", "Enseignante, université Kozminski, Varsovie", "Anciennement Principal Product Manager, Microsoft (Azure Synapse Analytics, Microsoft Fabric)"],
    office="Prendre rendez-vous",
    h_about="À propos",
    about=[
        "La Dr Estera Kot est une informaticienne qui travaille à la croisée de l'apprentissage automatique, des systèmes de données à grande échelle et des organisations qui en dépendent. Sa recherche doctorale a appliqué l'apprentissage profond à la segmentation d'images biomédicales du cerveau pour estimer le volume des gliomes. Son parcours industriel a poussé cet intérêt pour l'échelle jusqu'à sa conclusion logique : le moteur Apache Spark qui alimente l'analytique, l'apprentissage automatique et les charges Copilot dans Azure Synapse Analytics et Microsoft Fabric.",
        "Elle a obtenu son doctorat en informatique avec distinction à l'École polytechnique de Varsovie. Elle est titulaire d'un brevet américain en traitement de données massives et a publié quinze articles évalués par les pairs, dont douze en tant que première auteure, présentés notamment à Glasgow et à Redmond.",
        "Sa position sur l'IA est sans compromis. L'ingénieure qui construit un système ne peut pas déléguer sa responsabilité morale aux régulateurs ou aux éthiciens. L'éthique n'est pas une couche de conformité ajoutée une fois l'architecture figée. Elle vit dans chaque objectif d'optimisation, chaque valeur par défaut, chaque choix sur ce que la machine récompense et ce qu'elle ignore.",
    ],
    h_research="Recherche", h_interests="Thèmes", h_selected="Travaux choisis",
    interests=["Apprentissage profond pour l'analyse d'images biomédicales, en particulier la segmentation des tumeurs cérébrales et l'estimation de leur volume", "Moteurs d'exécution vectorisés pour Apache Spark et architectures lakehouse", "Migration de plateformes de données à grande échelle et gestion du cycle de vie des moteurs", "Gouvernance de l'IA comme discipline d'ingénierie plutôt que comme couche de conformité"],
    selected=["Thèse de doctorat : segmentation d'images biomédicales du cerveau pour l'estimation du volume des gliomes, École polytechnique de Varsovie, avec distinction", "Brevet américain en traitement de données massives", "Native Execution Engine pour Microsoft Fabric : un moteur Spark vectorisé développé avec Intel, Meta et IBM, quatre fois plus rapide que Spark open source", "Quinze publications évaluées par les pairs. Liste complète sur {scholar} et {orcid}"],
    h_pubs="Publications", pubs_intro="D'après {scholar}. Noms d'auteurs tels que publiés, titres dans la langue d'origine.",
    pub_groups={"journal": "Articles de revues", "conference": "Communications en conférence", "thesis": "Thèse de doctorat", "other": "Autres manuscrits"},
    h_teaching="Enseignement",
    teaching=[
        "La Dr Kot enseigne la programmation Python à l'université Kozminski de Varsovie et a donné des cours en tant qu'invitée à l'UCLA et à l'université Łazarski. À l'École polytechnique de Varsovie, elle a conçu des programmes originaux de master et de formation continue en technologies d'IA dans le cloud, dont le programme de formation continue <em>Applications of Cloud Technologies Based on Data and Artificial Intelligence</em> (2022). Ses anciens étudiants travaillent aujourd'hui au CERN, chez Google, chez Meta et dans d'autres institutions de recherche.",
        "Elle crée et anime <em>Fabric Espresso</em>, une série vidéo technique sur Microsoft Fabric comptant 89 épisodes, et intervient régulièrement à la FabCon Europe.",
    ],
    h_service="Responsabilités",
    service=["Présidente, puis membre, du conseil des doctorants de la faculté de génie électrique, École polytechnique de Varsovie", "Distinguée par le recteur de l'École polytechnique de Varsovie pour sa direction du conseil des doctorants"],
    h_industry="Industrie",
    industry=[
        "En tant que directrice de la technologie chez Clouds on Mars, partenaire Microsoft et Databricks en données et IA en Europe et au Moyen-Orient, la Dr Kot est responsable de la stratégie technique, de la réalisation et de l'architecture des comptes les plus stratégiques de l'entreprise dans la santé, l'assurance et les plateformes de données d'entreprise.",
        "Chez Microsoft, elle était Principal Product Manager du moteur Apache Spark dans Azure Synapse Analytics et Microsoft Fabric. Elle a migré 25 000 clients Synapse vers Fabric, automatisé le programme qui déplace 30 000 clients entre versions de moteur tous les six mois, et dirigé des équipes transversales de près de 300 ingénieurs, designers et parties prenantes. Elle a auparavant travaillé chez Intel, Sony, Citi et Procter and Gamble, où elle a introduit Apache Spark et Delta Lake en 2018.",
    ],
    h_honors="Distinctions",
    honors=["Microsoft Most Valuable Professional (MVP), {mvp}", "Lauréate du prix Polka XXI wieku, innovation et nouvelles technologies, 2026", "Top 100 des femmes de l'IA en Pologne ; Top 3 pour le leadership en IA ; Top 100 des femmes du cloud computing", "Gagnante du Microsoft Global Hackathon, santé, 2021", "Bourse d'excellence pour les meilleurs doctorants, chaque année du doctorat, École polytechnique de Varsovie"],
    mvp_label="profil",
    h_contact="Contact",
    contact="Le moyen le plus rapide de joindre la Dr Kot est de réserver un créneau : {book}. Pour la correspondance scientifique, utilisez l'adresse indiquée dans sa {orcid_record}.",
    orcid_record="fiche ORCID",
    footer="Dr Estera Kot, Varsovie et Gdynia, Pologne.", privacy="Confidentialité", terms="Conditions",
    ld_desc="Informaticienne. Directrice de la technologie chez Clouds on Mars, enseignante à l'université Kozminski, ancienne Principal Product Manager chez Microsoft pour le moteur Apache Spark d'Azure Synapse Analytics et de Microsoft Fabric. Doctorat en informatique avec distinction, École polytechnique de Varsovie.",
    ld_jobs=["Directrice de la technologie", "Enseignante"],
    ld_knows=["Apprentissage automatique", "Apprentissage profond", "Segmentation d'images biomédicales", "Estimation du volume des gliomes", "Apache Spark", "Microsoft Fabric", "Azure Synapse Analytics", "Architecture lakehouse", "Traitement de données massives", "Gouvernance de l'IA", "Informatique en nuage"],
    ld_awards=["Microsoft Most Valuable Professional (MVP)", "Lauréate Polka XXI wieku, innovation et nouvelles technologies (2026)", "Top 100 des femmes de l'IA en Pologne", "Top 3 leadership en IA, Pologne", "Top 100 des femmes du cloud computing", "Gagnante Microsoft Global Hackathon, santé (2021)"],
    ld_phd="Doctorat en informatique, avec distinction",
    orgs=dict(com="Clouds on Mars", koz="Université Kozminski", pw="École polytechnique de Varsovie"),
    alt_names=["Dr Estera Kot", "Estera Kot", "Dre Estera Kot"],
    pubs_name="Publications de la Dr Estera Kot",
)

T["es"] = dict(
    name="Dra. Estera Kot", page_title="Dra. Estera Kot",
    meta="Dra. Estera Kot, doctora en Informática. Directora de Tecnología (CTO) en Clouds on Mars, profesora en la Universidad Kozminski de Varsovia, antes Principal Product Manager en Microsoft a cargo del motor Apache Spark de Azure Synapse Analytics y Microsoft Fabric. Investigación en aprendizaje profundo para imagen médica y sistemas de datos a gran escala.",
    og="Informática. CTO en Clouds on Mars, profesora en la Universidad Kozminski, ex Principal PM en Microsoft para Apache Spark en Azure Synapse Analytics y Microsoft Fabric.",
    alt="Retrato de la Dra. Estera Kot",
    nav=["Investigación", "Publicaciones", "Docencia", "Industria", "Reconocimientos", "Contacto"],
    titles=["Directora de Tecnología (CTO), Clouds on Mars", "Profesora, Universidad Kozminski, Varsovia", "Anteriormente Principal Product Manager, Microsoft (Azure Synapse Analytics, Microsoft Fabric)"],
    office="Reservar cita",
    h_about="Acerca de",
    about=[
        "La Dra. Estera Kot es una informática que trabaja en la intersección del aprendizaje automático, los sistemas de datos a gran escala y las organizaciones que dependen de ellos. Su investigación doctoral aplicó el aprendizaje profundo a la segmentación de imágenes biomédicas del cerebro para estimar el volumen de gliomas. Su trabajo en la industria llevó ese interés por la escala hasta su conclusión lógica: el motor Apache Spark que impulsa la analítica, el aprendizaje automático y las cargas de Copilot en Azure Synapse Analytics y Microsoft Fabric.",
        "Obtuvo su doctorado en Informática con distinción en la Universidad Politécnica de Varsovia. Es titular de una patente estadounidense en procesamiento de big data y ha publicado quince artículos revisados por pares, doce de ellos como primera autora, presentados en foros como Glasgow y Redmond.",
        "Su postura sobre la IA es inflexible. La ingeniera que construye un sistema no puede delegar la responsabilidad moral en reguladores ni en especialistas en ética. La ética no es una capa de cumplimiento que se añade una vez fijada la arquitectura. Vive en cada objetivo de optimización, en cada valor por defecto, en cada decisión sobre lo que la máquina premia y lo que ignora.",
    ],
    h_research="Investigación", h_interests="Líneas", h_selected="Trabajos destacados",
    interests=["Aprendizaje profundo para el análisis de imágenes biomédicas, en particular la segmentación de tumores cerebrales y la estimación de su volumen", "Motores de ejecución vectorizados para Apache Spark y arquitecturas lakehouse", "Migración de plataformas de datos a gran escala y gestión del ciclo de vida de los motores", "Gobernanza de la IA como disciplina de ingeniería y no como capa de cumplimiento"],
    selected=["Tesis doctoral: segmentación de imágenes biomédicas del cerebro para la estimación del volumen de gliomas, Universidad Politécnica de Varsovia, con distinción", "Patente estadounidense en procesamiento de big data", "Native Execution Engine para Microsoft Fabric: un motor Spark vectorizado desarrollado con Intel, Meta e IBM, cuatro veces más rápido que Spark de código abierto", "Quince publicaciones revisadas por pares. Lista completa en {scholar} y {orcid}"],
    h_pubs="Publicaciones", pubs_intro="Según {scholar}. Nombres de autores tal como se publicaron, títulos en el idioma original.",
    pub_groups={"journal": "Artículos en revistas", "conference": "Ponencias en congresos", "thesis": "Tesis doctoral", "other": "Otros manuscritos"},
    h_teaching="Docencia",
    teaching=[
        "La Dra. Kot imparte programación en Python en la Universidad Kozminski de Varsovia y ha sido profesora invitada en UCLA y en la Universidad Łazarski. En la Universidad Politécnica de Varsovia diseñó planes de estudio originales de máster y posgrado en tecnologías de IA en la nube, entre ellos el programa de posgrado <em>Applications of Cloud Technologies Based on Data and Artificial Intelligence</em> (2022). Sus antiguos estudiantes trabajan hoy en el CERN, Google, Meta y otras instituciones de investigación.",
        "Crea y presenta <em>Fabric Espresso</em>, una serie técnica en vídeo sobre Microsoft Fabric con 89 episodios, y participa regularmente como ponente en FabCon Europe.",
    ],
    h_service="Gestión académica",
    service=["Presidenta, y después miembro, del Consejo de Doctorandos de la Facultad de Ingeniería Eléctrica, Universidad Politécnica de Varsovia", "Reconocida por el Rector de la Universidad Politécnica de Varsovia por su liderazgo en el Consejo de Doctorandos"],
    h_industry="Industria",
    industry=[
        "Como Directora de Tecnología en Clouds on Mars, socio de Microsoft y Databricks en datos e IA para Europa y Oriente Medio, la Dra. Kot es responsable de la estrategia técnica, la ejecución de ingeniería y la arquitectura de las cuentas más estratégicas de la firma en sanidad, seguros y plataformas de datos empresariales.",
        "En Microsoft fue Principal Product Manager del motor Apache Spark en Azure Synapse Analytics y Microsoft Fabric. Migró a 25 000 clientes de Synapse a Fabric, automatizó el programa que traslada a 30 000 clientes entre versiones del motor cada seis meses y dirigió equipos multidisciplinares de cerca de 300 ingenieros, diseñadores y partes interesadas. Antes trabajó en Intel, Sony, Citi y Procter and Gamble, donde introdujo Apache Spark y Delta Lake en 2018.",
    ],
    h_honors="Reconocimientos",
    honors=["Microsoft Most Valuable Professional (MVP), {mvp}", "Galardonada Polka XXI wieku, innovación y nuevas tecnologías, 2026", "Top 100 Mujeres en IA de Polonia; Top 3 en liderazgo en IA; Top 100 Mujeres en Cloud Computing", "Ganadora del Microsoft Global Hackathon, sanidad, 2021", "Beca de excelencia para los mejores doctorandos en cada año del doctorado, Universidad Politécnica de Varsovia"],
    mvp_label="perfil",
    h_contact="Contacto",
    contact="La forma más rápida de contactar con la Dra. Kot es reservar una cita: {book}. Para correspondencia científica, utilice el correo indicado en su {orcid_record}.",
    orcid_record="registro ORCID",
    footer="Dra. Estera Kot, Varsovia y Gdynia, Polonia.", privacy="Privacidad", terms="Condiciones",
    ld_desc="Informática. Directora de Tecnología en Clouds on Mars, profesora en la Universidad Kozminski, ex Principal Product Manager en Microsoft a cargo del motor Apache Spark de Azure Synapse Analytics y Microsoft Fabric. Doctorado en Informática con distinción, Universidad Politécnica de Varsovia.",
    ld_jobs=["Directora de Tecnología", "Profesora"],
    ld_knows=["Aprendizaje automático", "Aprendizaje profundo", "Segmentación de imágenes biomédicas", "Estimación del volumen de gliomas", "Apache Spark", "Microsoft Fabric", "Azure Synapse Analytics", "Arquitectura lakehouse", "Procesamiento de big data", "Gobernanza de la IA", "Computación en la nube"],
    ld_awards=["Microsoft Most Valuable Professional (MVP)", "Galardonada Polka XXI wieku, innovación y nuevas tecnologías (2026)", "Top 100 Mujeres en IA de Polonia", "Top 3 liderazgo en IA, Polonia", "Top 100 Mujeres en Cloud Computing", "Ganadora Microsoft Global Hackathon, sanidad (2021)"],
    ld_phd="Doctorado en Informática, con distinción",
    orgs=dict(com="Clouds on Mars", koz="Universidad Kozminski", pw="Universidad Politécnica de Varsovia"),
    alt_names=["Dra. Estera Kot", "Estera Kot", "Dr. Estera Kot"],
    pubs_name="Publicaciones de la Dra. Estera Kot",
)

T["it"] = dict(
    name="Dott.ssa Estera Kot", page_title="Dott.ssa Estera Kot",
    meta="Dott.ssa Estera Kot, dottore di ricerca in Informatica. Chief Technology Officer di Clouds on Mars, docente all'Università Kozminski di Varsavia, in precedenza Principal Product Manager in Microsoft responsabile del runtime Apache Spark di Azure Synapse Analytics e Microsoft Fabric. Ricerca su deep learning per l'imaging medico e sistemi di dati su larga scala.",
    og="Informatica. CTO di Clouds on Mars, docente all'Università Kozminski, ex Principal PM in Microsoft per Apache Spark in Azure Synapse Analytics e Microsoft Fabric.",
    alt="Ritratto della Dott.ssa Estera Kot",
    nav=["Ricerca", "Pubblicazioni", "Didattica", "Industria", "Riconoscimenti", "Contatti"],
    titles=["Chief Technology Officer, Clouds on Mars", "Docente, Università Kozminski, Varsavia", "In precedenza Principal Product Manager, Microsoft (Azure Synapse Analytics, Microsoft Fabric)"],
    office="Prenota un incontro",
    h_about="Profilo",
    about=[
        "La Dott.ssa Estera Kot è un'informatica che lavora all'intersezione tra apprendimento automatico, sistemi di dati su larga scala e organizzazioni che da essi dipendono. La sua ricerca di dottorato ha applicato il deep learning alla segmentazione di immagini biomediche del cervello per la stima del volume dei gliomi. Il suo percorso industriale ha portato quell'interesse per la scala alla sua conclusione logica: il runtime Apache Spark che alimenta analisi, apprendimento automatico e carichi Copilot in Azure Synapse Analytics e Microsoft Fabric.",
        "Ha conseguito il dottorato in Informatica con lode presso il Politecnico di Varsavia. È titolare di un brevetto statunitense nell'elaborazione di big data e ha pubblicato quindici articoli sottoposti a revisione paritaria, dodici dei quali come prima autrice, presentati tra l'altro a Glasgow e Redmond.",
        "La sua posizione sull'IA è senza compromessi. L'ingegnere che costruisce un sistema non può delegare la responsabilità morale a regolatori o eticisti. L'etica non è uno strato di conformità aggiunto dopo che l'architettura è stata fissata. Vive in ogni obiettivo di ottimizzazione, in ogni impostazione predefinita, in ogni scelta su ciò che la macchina premia e ciò che ignora.",
    ],
    h_research="Ricerca", h_interests="Interessi", h_selected="Lavori selezionati",
    interests=["Deep learning per l'analisi di immagini biomediche, in particolare segmentazione dei tumori cerebrali e stima del volume", "Motori di esecuzione vettorizzati per Apache Spark e architetture lakehouse", "Migrazione di piattaforme dati su larga scala e gestione del ciclo di vita dei motori", "Governance dell'IA come disciplina ingegneristica e non come strato di conformità"],
    selected=["Tesi di dottorato: segmentazione di immagini biomediche del cervello per la stima del volume dei gliomi, Politecnico di Varsavia, con lode", "Brevetto statunitense nell'elaborazione di big data", "Native Execution Engine per Microsoft Fabric: un runtime Spark vettorizzato sviluppato con Intel, Meta e IBM, quattro volte più veloce di Spark open source", "Quindici pubblicazioni sottoposte a revisione paritaria. Elenco completo su {scholar} e {orcid}"],
    h_pubs="Pubblicazioni", pubs_intro="Da {scholar}. Nomi degli autori come pubblicati, titoli in lingua originale.",
    pub_groups={"journal": "Articoli su rivista", "conference": "Contributi a conferenze", "thesis": "Tesi di dottorato", "other": "Altri manoscritti"},
    h_teaching="Didattica",
    teaching=[
        "La Dott.ssa Kot insegna programmazione Python all'Università Kozminski di Varsavia ed è stata docente ospite alla UCLA e all'Università Łazarski. Al Politecnico di Varsavia ha progettato percorsi originali di laurea magistrale e post-laurea sulle tecnologie di IA nel cloud, tra cui il programma post-laurea <em>Applications of Cloud Technologies Based on Data and Artificial Intelligence</em> (2022). I suoi ex studenti lavorano oggi al CERN, in Google, in Meta e in altri istituti di ricerca.",
        "Crea e conduce <em>Fabric Espresso</em>, una serie video tecnica su Microsoft Fabric con 89 episodi, e interviene regolarmente a FabCon Europe.",
    ],
    h_service="Incarichi",
    service=["Presidente, poi membro, del Consiglio dei dottorandi della Facoltà di Ingegneria Elettrica, Politecnico di Varsavia", "Riconosciuta dal Rettore del Politecnico di Varsavia per la guida del Consiglio dei dottorandi"],
    h_industry="Industria",
    industry=[
        "Come Chief Technology Officer di Clouds on Mars, partner Microsoft e Databricks per dati e IA in Europa e Medio Oriente, la Dott.ssa Kot è responsabile della strategia tecnologica, della realizzazione ingegneristica e dell'architettura dei progetti più strategici dell'azienda in sanità, assicurazioni e piattaforme dati enterprise.",
        "In Microsoft è stata Principal Product Manager del runtime Apache Spark in Azure Synapse Analytics e Microsoft Fabric. Ha migrato 25.000 clienti Synapse a Fabric, automatizzato il programma che sposta 30.000 clienti tra versioni del motore ogni sei mesi e guidato team interfunzionali di quasi 300 ingegneri, designer e stakeholder. In precedenza ha lavorato in Intel, Sony, Citi e Procter and Gamble, dove nel 2018 ha introdotto Apache Spark e Delta Lake.",
    ],
    h_honors="Riconoscimenti",
    honors=["Microsoft Most Valuable Professional (MVP), {mvp}", "Vincitrice del premio Polka XXI wieku, innovazione e nuove tecnologie, 2026", "Top 100 Donne nell'IA in Polonia; Top 3 per la leadership nell'IA; Top 100 Donne nel Cloud Computing", "Vincitrice del Microsoft Global Hackathon, sanità, 2021", "Borsa di merito per i migliori dottorandi in ogni anno del dottorato, Politecnico di Varsavia"],
    mvp_label="profilo",
    h_contact="Contatti",
    contact="Il modo più rapido per raggiungere la Dott.ssa Kot è prenotare un incontro: {book}. Per la corrispondenza scientifica, utilizzare l'indirizzo indicato nel suo {orcid_record}.",
    orcid_record="profilo ORCID",
    footer="Dott.ssa Estera Kot, Varsavia e Gdynia, Polonia.", privacy="Privacy", terms="Condizioni",
    ld_desc="Informatica. Chief Technology Officer di Clouds on Mars, docente all'Università Kozminski, ex Principal Product Manager in Microsoft responsabile del runtime Apache Spark di Azure Synapse Analytics e Microsoft Fabric. Dottorato in Informatica con lode, Politecnico di Varsavia.",
    ld_jobs=["Chief Technology Officer", "Docente"],
    ld_knows=["Apprendimento automatico", "Deep learning", "Segmentazione di immagini biomediche", "Stima del volume dei gliomi", "Apache Spark", "Microsoft Fabric", "Azure Synapse Analytics", "Architettura lakehouse", "Elaborazione di big data", "Governance dell'IA", "Cloud computing"],
    ld_awards=["Microsoft Most Valuable Professional (MVP)", "Vincitrice Polka XXI wieku, innovazione e nuove tecnologie (2026)", "Top 100 Donne nell'IA in Polonia", "Top 3 leadership nell'IA, Polonia", "Top 100 Donne nel Cloud Computing", "Vincitrice Microsoft Global Hackathon, sanità (2021)"],
    ld_phd="Dottorato in Informatica, con lode",
    orgs=dict(com="Clouds on Mars", koz="Università Kozminski", pw="Politecnico di Varsavia"),
    alt_names=["Dott.ssa Estera Kot", "Estera Kot", "Dr. Estera Kot"],
    pubs_name="Pubblicazioni della Dott.ssa Estera Kot",
)

T["ar"] = dict(
    name="الدكتورة إستيرا كوت", page_title="الدكتورة إستيرا كوت | Dr. Estera Kot",
    meta="الدكتورة إستيرا كوت، حاصلة على الدكتوراه في علوم الحاسوب. المديرة التنفيذية للتكنولوجيا في شركة Clouds on Mars، ومحاضِرة في جامعة كوزمينسكي في وارسو، وسابقًا مديرة منتجات رئيسية في مايكروسوفت مسؤولة عن بيئة تشغيل Apache Spark في Azure Synapse Analytics وMicrosoft Fabric. أبحاث في التعلم العميق للتصوير الطبي ونظم البيانات واسعة النطاق.",
    og="عالمة حاسوب. المديرة التنفيذية للتكنولوجيا في Clouds on Mars، محاضِرة في جامعة كوزمينسكي، وسابقًا مديرة منتجات رئيسية في مايكروسوفت لـ Apache Spark في Azure Synapse Analytics وMicrosoft Fabric.",
    alt="صورة الدكتورة إستيرا كوت",
    nav=["البحث", "المنشورات", "التدريس", "الصناعة", "الجوائز", "التواصل"],
    titles=["المديرة التنفيذية للتكنولوجيا، Clouds on Mars", "محاضِرة، جامعة كوزمينسكي، وارسو", "سابقًا مديرة منتجات رئيسية، مايكروسوفت (Azure Synapse Analytics وMicrosoft Fabric)"],
    office="حجز موعد",
    h_about="نبذة",
    about=[
        "الدكتورة إستيرا كوت عالمة حاسوب تعمل عند تقاطع التعلم الآلي ونظم البيانات واسعة النطاق والمؤسسات التي تعتمد عليها. طبّقت في بحثها للدكتوراه التعلم العميق على تجزئة الصور الطبية الحيوية للدماغ لتقدير حجم الورم الدبقي. وقد أخذ عملها في الصناعة هذا الاهتمام بالنطاق الواسع إلى نهايته المنطقية: بيئة تشغيل Apache Spark التي تشغّل التحليلات والتعلم الآلي وأحمال Copilot في Azure Synapse Analytics وMicrosoft Fabric.",
        "حصلت على الدكتوراه في علوم الحاسوب بامتياز من جامعة وارسو للتكنولوجيا. وهي صاحبة براءة اختراع أمريكية في معالجة البيانات الضخمة، ونشرت خمس عشرة ورقة علمية محكّمة، اثنتا عشرة منها كمؤلفة أولى، قُدّمت في محافل منها غلاسكو وريدموند.",
        "موقفها من الذكاء الاصطناعي لا يقبل المساومة. فالمهندس الذي يبني النظام لا يستطيع أن يُحيل المسؤولية الأخلاقية إلى الجهات التنظيمية أو خبراء الأخلاقيات. الأخلاقيات ليست طبقة امتثال تُضاف بعد تثبيت البنية. إنها تسكن في كل هدف تحسين، وكل إعداد افتراضي، وكل قرار بشأن ما تكافئه الآلة وما تتجاهله.",
    ],
    h_research="البحث", h_interests="الاهتمامات", h_selected="أعمال مختارة",
    interests=["التعلم العميق لتحليل الصور الطبية الحيوية، وخاصة تجزئة أورام الدماغ وتقدير حجمها", "محركات التنفيذ المتجهية لـ Apache Spark وبنى lakehouse", "ترحيل منصات البيانات واسعة النطاق وإدارة دورة حياة المحركات", "حوكمة الذكاء الاصطناعي بوصفها تخصصًا هندسيًا لا طبقة امتثال"],
    selected=["أطروحة الدكتوراه: تجزئة الصور الطبية الحيوية للدماغ لتقدير حجم الورم الدبقي، جامعة وارسو للتكنولوجيا، بامتياز", "براءة اختراع أمريكية في معالجة البيانات الضخمة", "Native Execution Engine لـ Microsoft Fabric: بيئة تشغيل Spark متجهية طُوّرت مع Intel وMeta وIBM، أسرع أربع مرات من Spark مفتوح المصدر", "خمس عشرة ورقة علمية محكّمة. القائمة الكاملة على {scholar} و{orcid}"],
    h_pubs="المنشورات", pubs_intro="وفق {scholar}. أسماء المؤلفين كما نُشرت، والعناوين بلغتها الأصلية.",
    pub_groups={"journal": "مقالات في دوريات", "conference": "أوراق مؤتمرات", "thesis": "أطروحة الدكتوراه", "other": "مخطوطات أخرى"},
    h_teaching="التدريس",
    teaching=[
        "تدرّس الدكتورة كوت البرمجة بلغة Python في جامعة كوزمينسكي في وارسو، وحاضرت بصفة ضيفة في جامعة كاليفورنيا في لوس أنجلوس (UCLA) وجامعة وازارسكي. وفي جامعة وارسو للتكنولوجيا صمّمت مناهج أصلية للدراسات العليا والدراسات التكميلية في تقنيات الذكاء الاصطناعي في السحابة، من بينها برنامج الدراسات التكميلية <em>Applications of Cloud Technologies Based on Data and Artificial Intelligence</em> (2022). يعمل طلابها السابقون اليوم في CERN وGoogle وMeta ومؤسسات بحثية أخرى.",
        "تُعدّ وتقدّم <em>Fabric Espresso</em>، سلسلة فيديو تقنية عن Microsoft Fabric تضم 89 حلقة، وتتحدث بانتظام في مؤتمر FabCon Europe.",
    ],
    h_service="الخدمة الأكاديمية",
    service=["رئيسة، ثم عضو، مجلس طلاب الدكتوراه بكلية الهندسة الكهربائية، جامعة وارسو للتكنولوجيا", "كُرّمت من رئيس جامعة وارسو للتكنولوجيا لقيادتها مجلس طلاب الدكتوراه"],
    h_industry="الصناعة",
    industry=[
        "بصفتها المديرة التنفيذية للتكنولوجيا في Clouds on Mars، شريك مايكروسوفت وDatabricks في البيانات والذكاء الاصطناعي في أوروبا والشرق الأوسط، تتولى الدكتورة كوت الاستراتيجية التقنية والتنفيذ الهندسي والبنية المعمارية لأهم حسابات الشركة الاستراتيجية في الرعاية الصحية والتأمين ومنصات البيانات المؤسسية.",
        "في مايكروسوفت كانت مديرة منتجات رئيسية لبيئة تشغيل Apache Spark في Azure Synapse Analytics وMicrosoft Fabric. رحّلت 25,000 عميل من Synapse إلى Fabric، وأتمتت البرنامج الذي ينقل 30,000 عميل بين إصدارات المحرك كل ستة أشهر، وقادت فرقًا متعددة التخصصات تضم نحو 300 مهندس ومصمم وصاحب مصلحة. وشملت أدوارها السابقة Intel وSony وCiti وProcter and Gamble، حيث أدخلت Apache Spark وDelta Lake عام 2018.",
    ],
    h_honors="الجوائز",
    honors=["Microsoft Most Valuable Professional (MVP)، {mvp}", "الفائزة بجائزة Polka XXI wieku في فئة الابتكار والتقنيات الجديدة، 2026", "ضمن أفضل 100 امرأة في الذكاء الاصطناعي في بولندا؛ وأفضل 3 في قيادة الذكاء الاصطناعي؛ وأفضل 100 امرأة في الحوسبة السحابية", "الفائزة في Microsoft Global Hackathon، فئة الرعاية الصحية، 2021", "جائزة التميز لأفضل طلاب الدكتوراه في كل سنة من سنوات الدكتوراه، جامعة وارسو للتكنولوجيا"],
    mvp_label="الملف الشخصي",
    h_contact="التواصل",
    contact="أسرع طريقة للتواصل مع الدكتورة كوت هي حجز موعد: {book}. وللمراسلات البحثية، يُرجى استخدام البريد الإلكتروني المذكور في {orcid_record}.",
    orcid_record="سجلها على ORCID",
    footer="الدكتورة إستيرا كوت، وارسو وغدينيا، بولندا.", privacy="الخصوصية", terms="الشروط",
    ld_desc="عالمة حاسوب. المديرة التنفيذية للتكنولوجيا في Clouds on Mars، محاضِرة في جامعة كوزمينسكي، وسابقًا مديرة منتجات رئيسية في مايكروسوفت لبيئة تشغيل Apache Spark في Azure Synapse Analytics وMicrosoft Fabric. دكتوراه في علوم الحاسوب بامتياز من جامعة وارسو للتكنولوجيا.",
    ld_jobs=["المديرة التنفيذية للتكنولوجيا", "محاضِرة"],
    ld_knows=["التعلم الآلي", "التعلم العميق", "تجزئة الصور الطبية الحيوية", "تقدير حجم الورم الدبقي", "Apache Spark", "Microsoft Fabric", "Azure Synapse Analytics", "بنية lakehouse", "معالجة البيانات الضخمة", "حوكمة الذكاء الاصطناعي", "الحوسبة السحابية"],
    ld_awards=["Microsoft Most Valuable Professional (MVP)", "الفائزة بجائزة Polka XXI wieku، الابتكار والتقنيات الجديدة (2026)", "أفضل 100 امرأة في الذكاء الاصطناعي في بولندا", "أفضل 3 في قيادة الذكاء الاصطناعي، بولندا", "أفضل 100 امرأة في الحوسبة السحابية", "الفائزة في Microsoft Global Hackathon، الرعاية الصحية (2021)"],
    ld_phd="دكتوراه في علوم الحاسوب، بامتياز",
    orgs=dict(com="Clouds on Mars", koz="جامعة كوزمينسكي", pw="جامعة وارسو للتكنولوجيا"),
    alt_names=["الدكتورة إستيرا كوت", "إستيرا كوت", "Dr. Estera Kot", "Estera Kot"],
    pubs_name="منشورات الدكتورة إستيرا كوت",
)

ESPRESSO = "https://www.youtube.com/playlist?list=PLnfmGXUkCC7SypXJ6AcSk155pcUS0DPIX"
FABRIC = {
    "en": ("Microsoft Fabric", [
        "Microsoft Fabric is the thread that runs through Dr. Kot's industry work. At Microsoft she owned the Apache Spark runtime that Fabric and Azure Synapse Analytics share: the engine beneath notebooks, Spark jobs, lakehouse pipelines, machine learning, and Copilot workloads. She created the Native Execution Engine, a vectorized Spark runtime built with Intel, Meta, and IBM that runs four times faster than open-source Spark and ships to every Fabric customer at no added cost. She migrated 25,000 Azure Synapse customers to Fabric and automated the program that moves 30,000 customers between Spark engine versions every six months.",
        "She explains this work in public. <em>Fabric Espresso</em> is her technical video series on Microsoft Fabric: 89 short episodes on Spark in Fabric, the Native Execution Engine, lakehouse and Delta Lake design, data engineering, performance tuning, and migration from Synapse. The full series is on YouTube: {espresso}. She speaks regularly at FabCon Europe and is a Microsoft Most Valuable Professional (MVP).",
        "At Clouds on Mars she applies the same engine knowledge from the customer side, designing Fabric and Databricks lakehouse architectures for enterprises in healthcare, insurance, and enterprise data platforms across Europe and the Middle East, and teaching Fabric to data teams in workshops and conference sessions.",
        'Read her <a href="fabric/">Microsoft Fabric implementation guide</a> and the <a href="fabric/maturity-model/">Fabric Maturity Model</a>.',
    ], "Fabric Espresso playlist"),
    "en-gb": ("Microsoft Fabric", [
        "Microsoft Fabric is the thread that runs through Dr Kot's industry work. At Microsoft she owned the Apache Spark runtime that Fabric and Azure Synapse Analytics share: the engine beneath notebooks, Spark jobs, lakehouse pipelines, machine learning, and Copilot workloads. She created the Native Execution Engine, a vectorised Spark runtime built with Intel, Meta, and IBM that runs four times faster than open-source Spark and ships to every Fabric customer at no added cost. She migrated 25,000 Azure Synapse customers to Fabric and automated the programme that moves 30,000 customers between Spark engine versions every six months.",
        "She explains this work in public. <em>Fabric Espresso</em> is her technical video series on Microsoft Fabric: 89 short episodes on Spark in Fabric, the Native Execution Engine, lakehouse and Delta Lake design, data engineering, performance tuning, and migration from Synapse. The full series is on YouTube: {espresso}. She speaks regularly at FabCon Europe and is a Microsoft Most Valuable Professional (MVP).",
        "At Clouds on Mars she applies the same engine knowledge from the customer side, designing Fabric and Databricks lakehouse architectures for enterprises in healthcare, insurance, and enterprise data platforms across Europe and the Middle East, and teaching Fabric to data teams in workshops and conference sessions.",
        'Read her <a href="../fabric/">Microsoft Fabric implementation guide</a> and the <a href="../fabric/maturity-model/">Fabric Maturity Model</a>.',
    ], "Fabric Espresso playlist"),
    "pl": ("Microsoft Fabric", [
        "Microsoft Fabric to nić, która łączy całą zawodową drogę dr Kot. W Microsoft odpowiadała za środowisko uruchomieniowe Apache Spark wspólne dla Fabric i Azure Synapse Analytics: silnik pod notatnikami, zadaniami Spark, potokami lakehouse, uczeniem maszynowym i obciążeniami Copilot. Stworzyła Native Execution Engine, wektoryzowane środowisko Spark zbudowane z Intel, Meta i IBM, czterokrotnie szybsze od otwartego Sparka i dostępne dla każdego klienta Fabric bez dopłaty. Przeprowadziła migrację 25 000 klientów Azure Synapse do Fabric i zautomatyzowała program przenoszący 30 000 klientów między wersjami silnika Spark co sześć miesięcy.",
        "O tej pracy opowiada publicznie. <em>Fabric Espresso</em> to jej techniczna seria wideo o Microsoft Fabric: 89 krótkich odcinków o Sparku w Fabric, Native Execution Engine, projektowaniu lakehouse i Delta Lake, inżynierii danych, strojeniu wydajności i migracji z Synapse. Cała seria jest na YouTube: {espresso}. Regularnie występuje na FabCon Europe i jest Microsoft Most Valuable Professional (MVP).",
        "W Clouds on Mars wykorzystuje tę samą wiedzę o silniku po stronie klienta: projektuje architektury lakehouse na Fabric i Databricks dla przedsiębiorstw z ochrony zdrowia, ubezpieczeń i platform danych klasy enterprise w Europie i na Bliskim Wschodzie oraz uczy Fabric zespoły danych na warsztatach i sesjach konferencyjnych.",
        'Przeczytaj jej <a href="../fabric/">przewodnik po wdrażaniu Microsoft Fabric</a> i opis <a href="../fabric/maturity-model/">Fabric Maturity Model</a>.',
    ], "playlista Fabric Espresso"),
    "de": ("Microsoft Fabric", [
        "Microsoft Fabric ist der rote Faden in der Industriearbeit von Dr. Kot. Bei Microsoft verantwortete sie die Apache-Spark-Laufzeit, die Fabric und Azure Synapse Analytics gemeinsam nutzen: die Engine unter Notebooks, Spark-Jobs, Lakehouse-Pipelines, maschinellem Lernen und Copilot-Workloads. Sie schuf die Native Execution Engine, eine vektorisierte Spark-Laufzeit, entwickelt mit Intel, Meta und IBM, viermal schneller als Open-Source-Spark und für jeden Fabric-Kunden ohne Aufpreis verfügbar. Sie migrierte 25.000 Azure-Synapse-Kunden zu Fabric und automatisierte das Programm, das alle sechs Monate 30.000 Kunden zwischen Spark-Engine-Versionen bewegt.",
        "Diese Arbeit erklärt sie öffentlich. <em>Fabric Espresso</em> ist ihre technische Videoreihe zu Microsoft Fabric: 89 kurze Folgen zu Spark in Fabric, zur Native Execution Engine, zum Lakehouse- und Delta-Lake-Design, zu Data Engineering, Performance-Tuning und Migration von Synapse. Die vollständige Reihe auf YouTube: {espresso}. Sie spricht regelmäßig auf der FabCon Europe und ist Microsoft Most Valuable Professional (MVP).",
        "Bei Clouds on Mars wendet sie dasselbe Engine-Wissen von der Kundenseite an: Sie entwirft Fabric- und Databricks-Lakehouse-Architekturen für Unternehmen aus Gesundheitswesen, Versicherung und Unternehmensdatenplattformen in Europa und dem Nahen Osten und vermittelt Fabric in Workshops und Konferenzsessions an Datenteams.",
        'Lesen Sie ihren <a href="../fabric/">Leitfaden zur Implementierung von Microsoft Fabric</a> und das <a href="../fabric/maturity-model/">Fabric Maturity Model</a>.',
    ], "Fabric-Espresso-Playlist"),
    "fr": ("Microsoft Fabric", [
        "Microsoft Fabric est le fil conducteur du parcours industriel de la Dr Kot. Chez Microsoft, elle était responsable du moteur Apache Spark partagé par Fabric et Azure Synapse Analytics : le moteur sous les notebooks, les jobs Spark, les pipelines lakehouse, l'apprentissage automatique et les charges Copilot. Elle a créé le Native Execution Engine, un moteur Spark vectorisé développé avec Intel, Meta et IBM, quatre fois plus rapide que Spark open source et fourni à tous les clients Fabric sans surcoût. Elle a migré 25 000 clients Azure Synapse vers Fabric et automatisé le programme qui déplace 30 000 clients entre versions du moteur Spark tous les six mois.",
        "Elle explique ce travail publiquement. <em>Fabric Espresso</em> est sa série vidéo technique sur Microsoft Fabric : 89 épisodes courts sur Spark dans Fabric, le Native Execution Engine, la conception lakehouse et Delta Lake, l'ingénierie des données, l'optimisation des performances et la migration depuis Synapse. La série complète est sur YouTube : {espresso}. Elle intervient régulièrement à la FabCon Europe et est Microsoft Most Valuable Professional (MVP).",
        "Chez Clouds on Mars, elle applique cette connaissance du moteur du côté client : elle conçoit des architectures lakehouse Fabric et Databricks pour des entreprises de la santé, de l'assurance et des plateformes de données d'entreprise en Europe et au Moyen-Orient, et forme les équipes data à Fabric lors d'ateliers et de conférences.",
        'Lisez son <a href="../fabric/">guide de mise en œuvre de Microsoft Fabric</a> et le <a href="../fabric/maturity-model/">Fabric Maturity Model</a>.',
    ], "playlist Fabric Espresso"),
    "es": ("Microsoft Fabric", [
        "Microsoft Fabric es el hilo conductor de la trayectoria industrial de la Dra. Kot. En Microsoft fue responsable del motor Apache Spark que comparten Fabric y Azure Synapse Analytics: el motor bajo los notebooks, los trabajos Spark, las canalizaciones lakehouse, el aprendizaje automático y las cargas de Copilot. Creó el Native Execution Engine, un motor Spark vectorizado desarrollado con Intel, Meta e IBM, cuatro veces más rápido que Spark de código abierto y disponible para todos los clientes de Fabric sin coste adicional. Migró a 25 000 clientes de Azure Synapse a Fabric y automatizó el programa que traslada a 30 000 clientes entre versiones del motor Spark cada seis meses.",
        "Explica este trabajo en público. <em>Fabric Espresso</em> es su serie técnica en vídeo sobre Microsoft Fabric: 89 episodios breves sobre Spark en Fabric, el Native Execution Engine, el diseño lakehouse y Delta Lake, la ingeniería de datos, el ajuste de rendimiento y la migración desde Synapse. La serie completa está en YouTube: {espresso}. Participa regularmente como ponente en FabCon Europe y es Microsoft Most Valuable Professional (MVP).",
        "En Clouds on Mars aplica ese mismo conocimiento del motor desde el lado del cliente: diseña arquitecturas lakehouse en Fabric y Databricks para empresas de sanidad, seguros y plataformas de datos empresariales en Europa y Oriente Medio, y forma a equipos de datos en Fabric en talleres y sesiones de conferencias.",
        'Lea su <a href="../fabric/">guía de implementación de Microsoft Fabric</a> y el <a href="../fabric/maturity-model/">Fabric Maturity Model</a>.',
    ], "lista de reproducción de Fabric Espresso"),
    "it": ("Microsoft Fabric", [
        "Microsoft Fabric è il filo conduttore del percorso industriale della Dott.ssa Kot. In Microsoft è stata responsabile del runtime Apache Spark condiviso da Fabric e Azure Synapse Analytics: il motore sotto notebook, job Spark, pipeline lakehouse, apprendimento automatico e carichi Copilot. Ha creato il Native Execution Engine, un runtime Spark vettorizzato sviluppato con Intel, Meta e IBM, quattro volte più veloce di Spark open source e disponibile per ogni cliente Fabric senza costi aggiuntivi. Ha migrato 25.000 clienti Azure Synapse a Fabric e automatizzato il programma che sposta 30.000 clienti tra versioni del motore Spark ogni sei mesi.",
        "Racconta questo lavoro pubblicamente. <em>Fabric Espresso</em> è la sua serie video tecnica su Microsoft Fabric: 89 brevi episodi su Spark in Fabric, il Native Execution Engine, la progettazione lakehouse e Delta Lake, il data engineering, l'ottimizzazione delle prestazioni e la migrazione da Synapse. La serie completa è su YouTube: {espresso}. Interviene regolarmente a FabCon Europe ed è Microsoft Most Valuable Professional (MVP).",
        "In Clouds on Mars applica la stessa conoscenza del motore dal lato del cliente: progetta architetture lakehouse su Fabric e Databricks per imprese di sanità, assicurazioni e piattaforme dati enterprise in Europa e Medio Oriente, e forma i team dati su Fabric in workshop e sessioni di conferenza.",
        'Leggi la sua <a href="../fabric/">guida all\'implementazione di Microsoft Fabric</a> e il <a href="../fabric/maturity-model/">Fabric Maturity Model</a>.',
    ], "playlist Fabric Espresso"),
    "ar": ("Microsoft Fabric", [
        "Microsoft Fabric هو الخيط الذي يجمع مسيرة الدكتورة كوت في الصناعة. في مايكروسوفت تولّت مسؤولية بيئة تشغيل Apache Spark المشتركة بين Fabric وAzure Synapse Analytics: المحرك الذي يعمل تحت الدفاتر البرمجية ومهام Spark وخطوط lakehouse والتعلم الآلي وأحمال Copilot. أنشأت Native Execution Engine، وهي بيئة تشغيل Spark متجهية طُوّرت مع Intel وMeta وIBM، أسرع أربع مرات من Spark مفتوح المصدر ومتاحة لكل عملاء Fabric دون تكلفة إضافية. رحّلت 25,000 عميل من Azure Synapse إلى Fabric، وأتمتت البرنامج الذي ينقل 30,000 عميل بين إصدارات محرك Spark كل ستة أشهر.",
        "وتشرح هذا العمل علنًا. <em>Fabric Espresso</em> هي سلسلتها التقنية بالفيديو عن Microsoft Fabric: 89 حلقة قصيرة عن Spark في Fabric، وNative Execution Engine، وتصميم lakehouse وDelta Lake، وهندسة البيانات، وضبط الأداء، والترحيل من Synapse. السلسلة الكاملة على YouTube: {espresso}. تتحدث بانتظام في FabCon Europe وهي حاصلة على لقب Microsoft Most Valuable Professional (MVP).",
        "في Clouds on Mars تطبّق المعرفة نفسها بالمحرك من جانب العميل: تصمّم بنى lakehouse على Fabric وDatabricks لمؤسسات في الرعاية الصحية والتأمين ومنصات البيانات المؤسسية في أوروبا والشرق الأوسط، وتدرّب فرق البيانات على Fabric في ورش العمل وجلسات المؤتمرات.",
        'اقرأ <a href="../fabric/">دليلها لتطبيق Microsoft Fabric</a> و<a href="../fabric/maturity-model/">نموذج Fabric Maturity Model</a>.',
    ], "قائمة تشغيل Fabric Espresso"),
}
NAME_VARIANTS = ["Ester Kot", "Esther Kot", "Dr. Ester Kot", "Dr. Esther Kot", "Dr Esther Kot", "Estera Kot PhD"]
NAME_NOTE = {
    "en": "Name also written as Ester Kot or Esther Kot.",
    "en-gb": "Name also written as Ester Kot or Esther Kot.",
    "pl": "Imię bywa zapisywane także jako Ester Kot lub, po angielsku, Esther Kot.",
    "de": "Der Name wird auch als Ester Kot oder Esther Kot geschrieben.",
    "fr": "Nom également écrit Ester Kot ou Esther Kot.",
    "es": "Nombre escrito también como Ester Kot o Esther Kot.",
    "it": "Nome scritto anche come Ester Kot o Esther Kot.",
    "ar": "يُكتب الاسم أيضًا Ester Kot أو Esther Kot.",
}
for _c in T:
    T[_c]["alt_names"] = T[_c]["alt_names"] + [v for v in NAME_VARIANTS if v not in T[_c]["alt_names"]]
    T[_c]["name_note"] = NAME_NOTE[_c]
for _c, (_h, _ps, _lbl) in FABRIC.items():
    T[_c]["h_fabric"], T[_c]["fabric"], T[_c]["espresso_label"] = _h, _ps, _lbl

# ---------------------------------------------------------------- rendering
E = html.escape

def a(url, label): return f'<a href="{url}">{E(label)}</a>'

def fill(s, **k): return s.format(**k)

def hreflang_links():
    out = [f'  <link rel="alternate" hreflang="{hl}" href="{SITE}/{p}">' for c, (p, hl, _, _) in LANGS.items()]
    out.append(f'  <link rel="alternate" hreflang="x-default" href="{SITE}/">')
    return "\n".join(out)

def switcher(cur, prefix):
    parts = []
    for code, label in SWITCH:
        p = LANGS[code][0]
        href = f"{prefix}{p}" if p else f"{prefix}"
        cls = ' class="cur"' if code == cur else ""
        parts.append(f'<a href="{href or "./"}" lang="{LANGS[code][1]}" hreflang="{LANGS[code][1]}"{cls}>{label}</a>')
    return '<div class="langs" aria-label="Languages">' + " ".join(parts) + "</div>"

def person_ld(t, code, url):
    p, hl, _, _ = LANGS[code]
    return {
        "@context": "https://schema.org", "@type": "ProfilePage", "@id": url + "#page", "url": url,
        "name": t["name"], "dateCreated": "2026-10-19", "dateModified": TODAY, "inLanguage": hl,
        "mainEntity": {
            "@type": "Person", "@id": SITE + "/#person", "name": "Estera Kot", "givenName": "Estera", "familyName": "Kot",
            "honorificPrefix": "Dr.", "alternateName": t["alt_names"], "url": SITE + "/", "image": SITE + "/headshot.jpg",
            "description": t["ld_desc"], "jobTitle": t["ld_jobs"],
            "worksFor": {"@type": "Organization", "name": "Clouds on Mars", "url": "https://cloudsonmars.com/", "sameAs": ["https://www.youtube.com/@cloudsonmarshq"]},
            "affiliation": [
                {"@type": "Organization", "name": t["orgs"]["com"], "url": "https://cloudsonmars.com/"},
                {"@type": "CollegeOrUniversity", "name": t["orgs"]["koz"], "url": "https://www.kozminski.edu.pl/"},
            ],
            "alumniOf": {"@type": "CollegeOrUniversity", "name": t["orgs"]["pw"], "url": "https://www.pw.edu.pl/"},
            "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "Ph.D.", "name": t["ld_phd"], "recognizedBy": {"@type": "CollegeOrUniversity", "name": t["orgs"]["pw"]}},
            "knowsAbout": t["ld_knows"], "knowsLanguage": ["pl", "en"],
            "nationality": {"@type": "Country", "name": "Poland"},
            "address": {"@type": "PostalAddress", "addressLocality": "Warsaw", "addressCountry": "PL"},
            "identifier": {"@type": "PropertyValue", "propertyID": "ORCID", "value": "0000-0001-8308-7129"},
            "sameAs": SAME_AS, "award": t["ld_awards"],
        },
    }

def pubs_ld(t):
    items = []
    for y, k, title, auth, venue, doi in PUBS:
        o = {"@type": "Thesis" if k == "thesis" else "ScholarlyArticle", "name": PUB_TITLE_EN.get(title, title), "datePublished": str(y),
             "author": [{"@type": "Person", "name": n.strip()} for n in auth.split(",")]}
        if title in PUB_TITLE_EN: o["alternateName"] = title; o["inLanguage"] = "pl"
        if venue: o["isPartOf"] = {"@type": "Periodical" if k == "journal" else "CreativeWorkSeries", "name": venue}
        if doi:
            o["identifier"] = {"@type": "PropertyValue", "propertyID": "DOI", "value": doi}
            o["sameAs"] = o["url"] = f"https://doi.org/{doi}"
        items.append(o)
    return {"@context": "https://schema.org", "@type": "ItemList", "name": t["pubs_name"],
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": it} for i, it in enumerate(items)]}

def ld_script(obj):
    return '  <script type="application/ld+json">\n  ' + json.dumps(obj, ensure_ascii=False, indent=2).replace("\n", "\n  ") + "\n  </script>"

def pub_li(p, code="en"):
    y, k, title, auth, venue, doi = p
    tail = f", <em>{E(venue)}</em>" if venue else ""
    d = f'. <a href="https://doi.org/{doi}">doi:{doi}</a>' if doi else "."
    shown = E(title)
    if code != "pl" and title in PUB_TITLE_EN:
        shown = f'{E(PUB_TITLE_EN[title])} <span lang="pl">[{E(title)}]</span> ({E(PUB_IN_POLISH[code])})'
    auth_html = E(auth).replace("E. Kot", "<strong>E. Kot</strong>")
    return f"        <li class=\"pub\">{auth_html}. {shown}{tail}, {y}{d}</li>"

def render(code):
    t = T[code]; p, hl, loc, direction = LANGS[code]
    url = f"{SITE}/{p}"; prefix = "../" if p else ""
    scholar = a("https://scholar.google.com/citations?user=wF7USzwAAAAJ", "Google Scholar")
    orcid = a("https://orcid.org/0000-0001-8308-7129", "ORCID")
    mvp = a("https://mvp.microsoft.com/en-US/MVP/profile/dee98064-3431-4a89-80f8-148643d8f705", t["mvp_label"])
    book = a("https://bit.ly/bookdrkot", "bit.ly/bookdrkot")
    orcid_record = a("https://orcid.org/0000-0001-8308-7129", t["orcid_record"])
    nav_ids = ["research", "publications", "teaching", "industry", "fabric", "honors", "contact"]
    nav_labels = t["nav"][:4] + ["Fabric"] + t["nav"][4:]
    nav = "\n".join(f'        <a href="#{i}">{E(n)}</a>' for i, n in zip(nav_ids, nav_labels))
    links = "\n".join(f'          {a(u, l)}' for u, l in LINKS) + f'\n          {a(prefix + "Estera_Kot_Bio.pdf", CV_LABEL[code])}' + f'\n          {a("https://bit.ly/bookdrkot", t["office"])}'
    pubs = []
    for k in ["journal", "conference", "thesis", "other"]:
        pubs.append(f"      <h3>{E(t['pub_groups'][k])}</h3>\n      <ul>\n" + "\n".join(pub_li(x, code) for x in sorted([x for x in PUBS if x[1] == k], key=lambda x: -x[0])) + "\n      </ul>")
    arabic_font = '\n  <link href="https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;600&display=swap" rel="stylesheet">' if code == "ar" else ""
    return f'''<!doctype html>
<html lang="{hl}" dir="{direction}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#8C1515">
  <title>{E(t["page_title"])}</title>
  <meta name="description" content="{E(t["meta"])}">
  {VERIFY}
  <link rel="canonical" href="{url}">
{hreflang_links()}
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="author" content="Dr. Estera Kot">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="{E(t["name"])}">
  <meta property="og:description" content="{E(t["og"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/headshot.jpg">
  <meta property="og:image:alt" content="{E(t["alt"])}">
  <meta property="og:locale" content="{loc}">
{chr(10).join(f'  <meta property="og:locale:alternate" content="{l}">' for c, (_, _, l, _) in LANGS.items() if c != code)}
  <meta property="profile:first_name" content="Estera">
  <meta property="profile:last_name" content="Kot">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:site" content="@estera_kot">
  <meta name="twitter:creator" content="@estera_kot">
  <meta name="twitter:title" content="{E(t["name"])}">
  <meta name="twitter:description" content="{E(t["og"])}">
  <meta name="twitter:image" content="{SITE}/headshot.jpg">
{ld_script(person_ld(t, code, url))}
{ld_script(pubs_ld(t))}
{ld_script({"@context": "https://schema.org", "@type": "CreativeWorkSeries", "@id": ESPRESSO, "name": "Fabric Espresso", "url": ESPRESSO, "inLanguage": "en", "genre": "Technical video series", "about": ["Microsoft Fabric", "Apache Spark", "Native Execution Engine", "Lakehouse", "Delta Lake", "Azure Synapse Analytics"], "numberOfEpisodes": 89, "creator": {"@id": SITE + "/#person"}, "author": {"@id": SITE + "/#person"}, "publisher": {"@type": "Organization", "name": "Clouds on Mars", "url": "https://cloudsonmars.com/", "sameAs": ["https://www.youtube.com/@cloudsonmarshq"]}})}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">{arabic_font}
  <link rel="stylesheet" href="{prefix}style.css?v=4">
</head>
<body>
  <header class="topbar">
    <div class="inner">
      <a class="brand" href="./">{E(t["name"])}</a>
      <nav>
{nav}
      </nav>
      {switcher(code, prefix)}
    </div>
  </header>

  <main class="wrap">
    <div class="hero">
      <img src="{prefix}headshot.jpg" alt="{E(t["alt"])}" width="220" height="220">
      <div>
        <h1>{E(t["name"])}</h1>
        <p class="title">
{chr(10).join(f"          <span>{E(x)}</span>" for x in t["titles"])}
        </p>
        <p class="links">
{links}
        </p>
        <p class="namenote">{E(t["name_note"])}</p>
      </div>
    </div>

    <section id="about">
      <h2>{E(t["h_about"])}</h2>
{chr(10).join(f"      <p>{E(x)}</p>" for x in t["about"])}
    </section>

    <section id="research">
      <h2>{E(t["h_research"])}</h2>
      <div class="cols">
        <div>
          <h3>{E(t["h_interests"])}</h3>
          <ul>
{chr(10).join(f"            <li>{E(x)}</li>" for x in t["interests"])}
          </ul>
        </div>
        <div>
          <h3>{E(t["h_selected"])}</h3>
          <ul>
{chr(10).join("            <li>" + fill(E(x), scholar=scholar, orcid=orcid) + "</li>" for x in t["selected"])}
          </ul>
        </div>
      </div>
    </section>

    <section id="publications">
      <h2>{E(t["h_pubs"])}</h2>
      <p>{fill(E(t["pubs_intro"]), scholar=scholar)}</p>
{chr(10).join(pubs)}
    </section>

    <section id="teaching">
      <h2>{E(t["h_teaching"])}</h2>
{chr(10).join(f"      <p>{x}</p>" for x in t["teaching"])}
      <h3>{E(t["h_service"])}</h3>
      <ul>
{chr(10).join(f"        <li>{E(x)}</li>" for x in t["service"])}
      </ul>
    </section>

    <section id="industry">
      <h2>{E(t["h_industry"])}</h2>
{chr(10).join(f"      <p>{E(x)}</p>" for x in t["industry"])}
    </section>

    <section id="fabric">
      <h2>{E(t["h_fabric"])}</h2>
{chr(10).join("      <p>" + fill(x, espresso=a(ESPRESSO, t["espresso_label"])) + "</p>" for x in t["fabric"])}
    </section>

    <section id="honors">
      <h2>{E(t["h_honors"])}</h2>
      <ul>
{chr(10).join("        <li>" + fill(E(x), mvp=mvp) + "</li>" for x in t["honors"])}
      </ul>
    </section>

    <section id="contact">
      <h2>{E(t["h_contact"])}</h2>
      <p>{fill(E(t["contact"]), book=book, orcid_record=orcid_record)}</p>
    </section>

    <footer>
      <a href="{prefix}privacy.html">{E(t["privacy"])}</a>
      <a href="{prefix}terms.html">{E(t["terms"])}</a>
      <span>{E(t["footer"])}</span>
      <p class="footlinks">{" ".join(a(u, l) for u, l in FOOTER_LINKS)}</p>
      <p class="updated">{E(UPDATED[code])}: {TODAY}.</p>
    </footer>
  </main>
</body>
</html>
'''

def sitemap():
    alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{hl}" href="{SITE}/{p}"/>' for c, (p, hl, _, _) in LANGS.items()) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>'
    urls = "".join(f'\n  <url><loc>{SITE}/{p}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{"1.0" if not p else "0.9"}</priority>{alts}\n  </url>' for c, (p, hl, _, _) in LANGS.items())
    urls += f'\n  <url><loc>{SITE}/privacy.html</loc><lastmod>2026-10-19</lastmod><changefreq>yearly</changefreq><priority>0.2</priority></url>'
    urls += f'\n  <url><loc>{SITE}/terms.html</loc><lastmod>2026-10-19</lastmod><changefreq>yearly</changefreq><priority>0.2</priority></url>'
    urls += f'\n  <url><loc>{SITE}/fabric/</loc><lastmod>2026-10-19</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>'
    urls += f'\n  <url><loc>{SITE}/fabric/maturity-model/</loc><lastmod>2026-10-19</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>'
    urls += f'\n  <url><loc>{SITE}/fabric/espresso/</loc><lastmod>2026-10-19</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>'
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}\n</urlset>\n'

if __name__ == "__main__":
    for code, (p, *_r) in LANGS.items():
        out = ROOT / p / "index.html" if p else ROOT / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(code), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print("wrote sitemap.xml")
