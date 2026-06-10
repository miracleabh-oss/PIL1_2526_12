"""
app/matching.py
Algorithme de matching mentor-mentoré pour IFRI_MentorLink.
"""


def _score_competences(mentor: dict, mentee: dict) -> float:
    """
    Score basé sur le recouvrement entre les compétences fortes du mentor
    et les lacunes du mentoré.
    Retourne un score entre 0 et 40.
    """
    forts_mentor  = set(mentor.get('competences', []))
    lacunes_mentee = set(mentee.get('lacunes', []))

    if not lacunes_mentee:
        return 0.0

    recouvrement = forts_mentor & lacunes_mentee
    ratio = len(recouvrement) / len(lacunes_mentee)
    return round(ratio * 40, 2)


def _score_disponibilites(mentor: dict, mentee: dict) -> float:
    """
    Score basé sur les créneaux horaires communs.
    Retourne un score entre 0 et 35.
    """
    dispos_mentor  = mentor.get('disponibilites', [])
    dispos_mentee  = mentee.get('disponibilites', [])

    if not dispos_mentor or not dispos_mentee:
        return 0.0

    creneaux_communs = 0
    for d1 in dispos_mentor:
        for d2 in dispos_mentee:
            if d1['jour'] == d2['jour']:
                debut = max(d1['heure_debut'], d2['heure_debut'])
                fin   = min(d1['heure_fin'],   d2['heure_fin'])
                if debut < fin:
                    creneaux_communs += 1

    # Normaliser : 3 créneaux communs = score max
    ratio = min(creneaux_communs / 3, 1.0)
    return round(ratio * 35, 2)


def _score_filiere(mentor: dict, mentee: dict) -> float:
    """
    Score basé sur la proximité de filière et le niveau.
    Retourne un score entre 0 et 25.
    """
    score = 0.0

    # Même filière = 15 pts
    if mentor.get('filiere') and mentor['filiere'] == mentee.get('filiere'):
        score += 15

    # Niveau : mentor doit être >= mentoré (idéalement 1 ou 2 niveaux au-dessus)
    niv_mentor = mentor.get('niveau', 1)
    niv_mentee = mentee.get('niveau', 1)
    diff = niv_mentor - niv_mentee

    if diff == 1:
        score += 10   # Un niveau au-dessus : idéal
    elif diff == 2:
        score += 7
    elif diff == 0:
        score += 5    # Même niveau : pair learning
    elif diff > 2:
        score += 3    # Trop d'écart : moins pertinent
    # diff < 0 : mentor moins avancé = 0 pts

    return round(min(score, 25), 2)


def calculer_score_total(mentor: dict, mentee: dict) -> dict:
    """
    Calcule le score total de compatibilité entre un mentor et un mentoré.
    Retourne un dict avec le score total et le détail.
    """
    sc = _score_competences(mentor, mentee)
    sd = _score_disponibilites(mentor, mentee)
    sf = _score_filiere(mentor, mentee)
    total = round(sc + sd + sf, 2)

    return {
        'score_total':        total,
        'score_competences':  sc,
        'score_disponibilites': sd,
        'score_filiere':      sf,
    }


def trouver_meilleurs_matchs(utilisateur: dict, candidats: list, role: str = 'mentee', top_n: int = 5) -> list:
    """
    Trouve les meilleurs matchs pour un utilisateur.

    Args:
        utilisateur : profil de l'utilisateur courant (dict)
        candidats   : liste de profils candidats (list of dict)
        role        : 'mentee' → cherche un mentor pour l'utilisateur
                      'mentor' → cherche des mentorés pour l'utilisateur
        top_n       : nombre de résultats à retourner

    Returns:
        Liste triée par score décroissant, chaque élément contenant
        les infos du candidat + le score.
    """
    resultats = []

    for candidat in candidats:
        if candidat['id'] == utilisateur['id']:
            continue

        if role == 'mentee':
            # utilisateur est le mentoré, candidat est le mentor
            scores = calculer_score_total(mentor=candidat, mentee=utilisateur)
        else:
            # utilisateur est le mentor, candidat est le mentoré
            scores = calculer_score_total(mentor=utilisateur, mentee=candidat)

        if scores['score_total'] > 0:
            resultats.append({
                **candidat,
                'score':                  scores['score_total'],
                'score_competences':      scores['score_competences'],
                'score_disponibilites':   scores['score_disponibilites'],
                'score_filiere':          scores['score_filiere'],
            })

    # Trier par score décroissant
    resultats.sort(key=lambda x: x['score'], reverse=True)
    return resultats[:top_n]
