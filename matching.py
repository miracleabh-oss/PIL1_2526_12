from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Profile, UserSkill, Availability, MentoringPost, Skill, Match, Conversation
from app import matching as algo_matching

matching = Blueprint('matching', __name__)

SKILLS_DISPONIBLES = [
    'Python', 'SQL', 'Algorithmique', 'Réseaux', 'Mathématiques',
    'JavaScript', 'HTML/CSS', 'Linux', 'Bases de données', 'Machine Learning',
    'Programmation web', "Systèmes d'exploitation", 'C/C++', 'Java',
    'Probabilités & Statistiques', 'Électronique', 'Sécurité informatique'
]
JOURS   = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
FORMATS = ['présentiel', 'en ligne', 'les deux']


def _profil_dict(user):
    """Convertit un User SQLAlchemy en dict pour l'algo de matching."""
    p = user.profile
    competences = [us.skill.nom for us in user.skills if us.type == 'fort']
    lacunes     = [us.skill.nom for us in user.skills if us.type == 'faible']
    return {
        'id':             user.id,
        'nom':            user.nom,
        'prenom':         user.prenom,
        'filiere':        p.filiere   if p else '',
        'niveau':         p.niveau    if p else 1,
        'photo_url':      p.photo_url if p else None,
        'competences':    competences,
        'lacunes':        lacunes,
        # Aliases pour compatibilité avec différentes versions de l'algo
        'matieres_fortes':  competences,
        'matieres_faibles': lacunes,
        'points_forts':     competences,
        'points_faibles':   lacunes,
        'disponibilites': [
            {'jour': a.jour, 'heure_debut': a.heure_debut, 'heure_fin': a.heure_fin}
            for a in user.availabilities
        ]
    }


@matching.route('/demander-aide', methods=['GET', 'POST'])
@login_required
def demander_aide():
    if request.method == 'POST':
        data        = request.get_json()
        skill_nom   = data.get('skill')
        format_     = data.get('format')
        description = data.get('description', '')
        dispos      = data.get('disponibilites', [])

        skill = Skill.query.filter_by(nom=skill_nom).first()
        if not skill:
            skill = Skill(nom=skill_nom)
            db.session.add(skill)
            db.session.flush()

        post = MentoringPost(
            user_id=current_user.id,
            type_post='demande',
            skill_id=skill.id,
            format=format_,
            description=description
        )
        db.session.add(post)
        db.session.commit()
        return jsonify({'success': True, 'redirect': url_for('matching.voir_matching')})

    return render_template('demander_aide.html',
        skills=SKILLS_DISPONIBLES, jours=JOURS, formats=FORMATS, user=current_user)


@matching.route('/proposer-aide', methods=['GET', 'POST'])
@login_required
def proposer_aide():
    if request.method == 'POST':
        data        = request.get_json()
        skill_nom   = data.get('skill')
        format_     = data.get('format')
        description = data.get('description', '')

        skill = Skill.query.filter_by(nom=skill_nom).first()
        if not skill:
            skill = Skill(nom=skill_nom)
            db.session.add(skill)
            db.session.flush()

        post = MentoringPost(
            user_id=current_user.id,
            type_post='offre',
            skill_id=skill.id,
            format=format_,
            description=description
        )
        db.session.add(post)
        db.session.commit()
        return jsonify({'success': True, 'redirect': url_for('matching.voir_matching')})

    return render_template('proposer_aide.html',
        skills=SKILLS_DISPONIBLES, jours=JOURS, formats=FORMATS, user=current_user)


@matching.route('/matching')
@login_required
def voir_matching():
    # Profil de l'utilisateur courant
    moi = _profil_dict(current_user)

    # Tous les autres utilisateurs avec un profil
    tous = User.query.filter(User.id != current_user.id).all()
    tous_dicts = [_profil_dict(u) for u in tous if u.profile]

    # Matchs déjà existants (pour ne pas reproposer)
    deja_matches = {m.mentor_id for m in Match.query.filter_by(mentee_id=current_user.id).all()} | \
                   {m.mentee_id for m in Match.query.filter_by(mentor_id=current_user.id).all()}

    resultats_mentors  = algo_matching.trouver_meilleurs_matchs(moi, tous_dicts, role='mentee')
    resultats_mentores = algo_matching.trouver_meilleurs_matchs(moi, tous_dicts, role='mentor')

    # Filtrer ceux déjà matchés
    resultats_mentors  = [r for r in resultats_mentors  if r['id'] not in deja_matches][:5]
    resultats_mentores = [r for r in resultats_mentores if r['id'] not in deja_matches][:5]

    # Matchs acceptés
    mes_matchs = Match.query.filter(
        ((Match.mentor_id == current_user.id) | (Match.mentee_id == current_user.id)),
        Match.statut == 'accepté'
    ).all()

    return render_template('matching.html',
        user=current_user,
        resultats_mentors=resultats_mentors,
        resultats_mentores=resultats_mentores,
        mes_matchs=mes_matchs
    )


@matching.route('/matching/accepter/<int:autre_id>', methods=['POST'])
@login_required
def accepter_match(autre_id):
    data = request.get_json()
    role = data.get('role', 'mentee')  # 'mentee' = current_user est le mentoré

    if role == 'mentee':
        mentor_id = autre_id
        mentee_id = current_user.id
    else:
        mentor_id = current_user.id
        mentee_id = autre_id

    # Vérifier que le match n'existe pas déjà
    existing = Match.query.filter_by(mentor_id=mentor_id, mentee_id=mentee_id).first()
    if existing:
        if existing.statut != 'accepté':
            existing.statut = 'accepté'
            # Créer la conversation si elle n'existe pas
            if not Conversation.query.filter_by(match_id=existing.id).first():
                conv = Conversation(match_id=existing.id)
                db.session.add(conv)
            db.session.commit()
        return jsonify({'success': True})

    # Calculer le score
    autre = User.query.get(autre_id)
    from app import matching as algo_matching
    moi_dict   = _profil_dict(current_user)
    autre_dict = _profil_dict(autre)
    if role == 'mentee':
        res = algo_matching.calculer_score_total(mentor=autre_dict, mentee=moi_dict)
    else:
        res = algo_matching.calculer_score_total(mentor=moi_dict, mentee=autre_dict)

    match = Match(mentor_id=mentor_id, mentee_id=mentee_id,
                  score=res['score_total'], statut='accepté')
    db.session.add(match)
    db.session.flush()

    conv = Conversation(match_id=match.id)
    db.session.add(conv)
    db.session.commit()

    return jsonify({'success': True, 'conv_id': conv.id})
