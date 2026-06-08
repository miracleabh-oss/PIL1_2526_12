# =============================================================
# app/matching.py
# IFRI_MentorLink — Algorithme de matching mentor/mentoré
# Auteur : Rudy — Responsable Backend & Matching
# =============================================================


def creneaux_se_chevauchent(debut1, fin1, debut2, fin2):
    """
    Vérifie si deux créneaux horaires se chevauchent.
    Les heures sont des strings au format "HH:MM".
    Exemple : "14:00" et "17:00"
    """
    # Convertir "HH:MM" en minutes pour comparer facilement
    def en_minutes(h):
        heures, minutes = map(int, h.split(":"))
        return heures * 60 + minutes

    d1, f1 = en_minutes(debut1), en_minutes(fin1)
    d2, f2 = en_minutes(debut2), en_minutes(fin2)

    # Chevauchement si les deux intervalles se croisent
    return d1 < f2 and d2 < f1


def calculer_score_competences(competences_mentor, lacunes_mentee):
    """
    Score sur 50 points.
    On cherche combien de points forts du mentor
    correspondent aux lacunes du mentoré.

    competences_mentor : liste de noms de skills (ex: ['Python', 'ML'])
    lacunes_mentee     : liste de noms de skills (ex: ['Python', 'SQL'])
    """
    if not competences_mentor or not lacunes_mentee:
        return 0

    comp = set(c.lower() for c in competences_mentor)
    lac  = set(l.lower() for l in lacunes_mentee)

    correspondances = comp & lac  # intersection

    score = (len(correspondances) / len(lac)) * 50
    return round(score, 2)


def calculer_score_disponibilites(dispos_mentor, dispos_mentee):
    """
    Score sur 30 points.
    On cherche les créneaux horaires qui se chevauchent.

    dispos_mentor / dispos_mentee : liste de dicts
    [
        {"jour": "Lundi", "heure_debut": "14:00", "heure_fin": "17:00"},
        ...
    ]
    """
    if not dispos_mentor or not dispos_mentee:
        return 0

    creneaux_communs = 0

    for d_mentor in dispos_mentor:
        for d_mentee in dispos_mentee:
            # Même jour ET créneaux qui se chevauchent
            if d_mentor["jour"] == d_mentee["jour"]:
                if creneaux_se_chevauchent(
                    d_mentor["heure_debut"], d_mentor["heure_fin"],
                    d_mentee["heure_debut"], d_mentee["heure_fin"]
                ):
                    creneaux_communs += 1

    # Normaliser par rapport au minimum des deux
    base = min(len(dispos_mentor), len(dispos_mentee))
    if base == 0:
        return 0

    score = (creneaux_communs / base) * 30
    return round(min(score, 30), 2)  # max 30 points


def calculer_score_filiere(filiere_mentor, niveau_mentor,
                            filiere_mentee, niveau_mentee):
    """
    Score sur 20 points.
    - Même filière            = 15 points
    - Mentor de niveau supérieur = 5 points bonus

    filiere : string (ex: 'GL', 'IA', 'SI', 'IM', 'SE_IoT')
    niveau  : int (1 à 5)
    """
    score = 0

    if filiere_mentor and filiere_mentee:
        if filiere_mentor.lower() == filiere_mentee.lower():
            score += 15

    if niveau_mentor and niveau_mentee:
        if int(niveau_mentor) > int(niveau_mentee):
            score += 5

    return score


def calculer_score_total(mentor, mentee):
    """
    Calcule le score de compatibilité entre un mentor et un mentoré.

    Paramètres (chaque profil est un dict) :
    {
        "id"            : 1,
        "nom"           : "Akpovi",
        "prenom"        : "Koffi",
        "filiere"       : "IA",
        "niveau"        : 1,
        "competences"   : ["Python", "Machine Learning"],
        "lacunes"       : ["Réseaux"],
        "disponibilites": [
            {"jour": "Lundi", "heure_debut": "14:00", "heure_fin": "17:00"}
        ]
    }

    Retourne un dict avec le score total et le détail.
    """
    score_comp = calculer_score_competences(
        mentor.get("competences", []),
        mentee.get("lacunes", [])
    )

    score_dispo = calculer_score_disponibilites(
        mentor.get("disponibilites", []),
        mentee.get("disponibilites", [])
    )

    score_fil = calculer_score_filiere(
        mentor.get("filiere"), mentor.get("niveau"),
        mentee.get("filiere"), mentee.get("niveau")
    )

    score_total = score_comp + score_dispo + score_fil

    return {
        "score_total": round(score_total, 2),
        "detail": {
            "competences":    score_comp,
            "disponibilites": score_dispo,
            "filiere_niveau": score_fil
        }
    }


def trouver_meilleurs_matchs(utilisateur, tous_les_utilisateurs, role="mentee"):
    """
    Trouve les meilleurs matchs pour un utilisateur donné.

    - role="mentee" : l'utilisateur cherche un mentor
                      → on cherche quelqu'un dont les compétences
                        couvrent les lacunes de l'utilisateur
    - role="mentor" : l'utilisateur est mentor
                      → on cherche quelqu'un dont les lacunes
                        correspondent aux compétences de l'utilisateur

    Retourne une liste triée par score décroissant.
    """
    resultats = []

    for autre in tous_les_utilisateurs:
        # Ne pas se matcher avec soi-même (RG01)
        if autre.get("id") == utilisateur.get("id"):
            continue

        if role == "mentee":
            resultat = calculer_score_total(mentor=autre, mentee=utilisateur)
        else:
            resultat = calculer_score_total(mentor=utilisateur, mentee=autre)

        resultats.append({
            "id":             autre.get("id"),
            "nom":            autre.get("nom"),
            "prenom":         autre.get("prenom"),
            "filiere":        autre.get("filiere"),
            "niveau":         autre.get("niveau"),
            "competences":    autre.get("competences", []),
            "disponibilites": autre.get("disponibilites", []),
            "score":          resultat["score_total"],
            "detail":         resultat["detail"]
        })

    # Trier par score décroissant
    resultats.sort(key=lambda x: x["score"], reverse=True)

    return resultats


