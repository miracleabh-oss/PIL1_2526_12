import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Profile, Skill, UserSkill, Availability

profil = Blueprint('profil', __name__)

SKILLS_DISPONIBLES = [
    'Python', 'SQL', 'Algorithmique', 'Réseaux', 'Mathématiques',
    'JavaScript', 'HTML/CSS', 'Linux', 'Bases de données', 'Machine Learning',
    'Programmation web', "Systèmes d'exploitation", 'C/C++', 'Java',
    'Probabilités & Statistiques', 'Électronique', 'Sécurité informatique'
]

JOURS = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
HEURES = ['07:00','08:00','09:00','10:00','11:00','12:00','13:00',
          '14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00']

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@profil.route('/profil')
@login_required
def voir_profil():
    skills_forts   = [us.skill.nom for us in current_user.skills if us.type == 'fort']
    skills_faibles = [us.skill.nom for us in current_user.skills if us.type == 'faible']
    dispos         = current_user.availabilities

    return render_template('profil_utilisateur.html',
        user=current_user,
        profile=current_user.profile,
        skills_forts=skills_forts,
        skills_faibles=skills_faibles,
        dispos=dispos,
        skills_disponibles=SKILLS_DISPONIBLES,
        jours=JOURS,
        heures=HEURES
    )


@profil.route('/profil/modifier', methods=['POST'])
@login_required
def modifier_profil():
    data = request.get_json()

    # Infos de base
    if 'nom' in data:
        current_user.nom = data['nom'].strip()
    if 'prenom' in data:
        current_user.prenom = data['prenom'].strip()
    if 'bio' in data and current_user.profile:
        current_user.profile.bio = data['bio']
    if 'filiere' in data and current_user.profile:
        current_user.profile.filiere = data['filiere']
    if 'niveau' in data and current_user.profile:
        current_user.profile.niveau = int(data['niveau'])

    # ANOMALIE 1 : vérifier qu'aucune matière n'est fort ET faible
    skills_forts   = data.get('skills_forts', [])
    skills_faibles = data.get('skills_faibles', [])
    doublons = set(skills_forts) & set(skills_faibles)
    if doublons:
        return jsonify({
            'success': False,
            'message': f'Conflit détecté : "{", ".join(doublons)}" ne peut pas être point fort et lacune simultanément.'
        })

    # ANOMALIE 2 : disponibilités obligatoires
    disponibilites = data.get('disponibilites', [])
    if len(disponibilites) == 0:
        return jsonify({
            'success': False,
            'message': 'Veuillez sélectionner au moins un créneau de disponibilité.'
        })

    # Mise à jour skills forts
    UserSkill.query.filter_by(user_id=current_user.id, type='fort').delete()
    for nom_skill in skills_forts:
        skill = Skill.query.filter_by(nom=nom_skill).first()
        if not skill:
            skill = Skill(nom=nom_skill)
            db.session.add(skill)
            db.session.flush()
        db.session.add(UserSkill(user_id=current_user.id, skill_id=skill.id, type='fort'))

    # Mise à jour lacunes
    UserSkill.query.filter_by(user_id=current_user.id, type='faible').delete()
    for nom_skill in skills_faibles:
        skill = Skill.query.filter_by(nom=nom_skill).first()
        if not skill:
            skill = Skill(nom=nom_skill)
            db.session.add(skill)
            db.session.flush()
        db.session.add(UserSkill(user_id=current_user.id, skill_id=skill.id, type='faible'))

    # Mise à jour disponibilités
    Availability.query.filter_by(user_id=current_user.id).delete()
    for dispo in disponibilites:
        db.session.add(Availability(
            user_id=current_user.id,
            jour=dispo['jour'],
            heure_debut=dispo['heure_debut'],
            heure_fin=dispo['heure_fin']
        ))

    db.session.commit()
    return jsonify({'success': True, 'message': '✅ Profil mis à jour avec succès.'})


@profil.route('/profil/photo', methods=['POST'])
@login_required
def upload_photo():
    """ANOMALIE 3 : upload de photo de profil fonctionnel."""
    if 'photo' not in request.files:
        return jsonify({'success': False, 'message': 'Aucun fichier reçu.'})

    file = request.files['photo']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Fichier vide.'})

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Format non supporté. Utilisez jpg, png ou webp.'})

    # Créer le dossier uploads s'il n'existe pas
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Nom de fichier unique basé sur l'ID user
    ext      = file.filename.rsplit('.', 1)[1].lower()
    filename = secure_filename(f'user_{current_user.id}.{ext}')
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Mettre à jour la BDD
    photo_url = f'/static/uploads/{filename}'
    if current_user.profile:
        current_user.profile.photo_url = photo_url
        db.session.commit()
    else:
        return jsonify({'success': False, 'message': 'Profil introuvable.'})

    return jsonify({'success': True, 'photo_url': photo_url})


@profil.route('/parametres', methods=['GET', 'POST'])
@login_required
def parametres():
    if request.method == 'POST':
        data = request.get_json()
        from app.models import User
        from app import bcrypt

        if 'email' in data:
            existing = User.query.filter_by(email=data['email'].lower()).first()
            if existing and existing.id != current_user.id:
                return jsonify({'success': False, 'message': 'Email déjà utilisé.'})
            current_user.email = data['email'].lower().strip()

        if 'telephone' in data:
            existing = User.query.filter_by(telephone=data['telephone']).first()
            if existing and existing.id != current_user.id:
                return jsonify({'success': False, 'message': 'Téléphone déjà utilisé.'})
            current_user.telephone = data['telephone'].strip()

        if 'nouveau_mdp' in data and data['nouveau_mdp']:
            if not bcrypt.check_password_hash(current_user.mot_de_passe, data.get('ancien_mdp', '')):
                return jsonify({'success': False, 'message': 'Ancien mot de passe incorrect.'})
            current_user.mot_de_passe = bcrypt.generate_password_hash(data['nouveau_mdp']).decode('utf-8')

        db.session.commit()
        return jsonify({'success': True, 'message': 'Paramètres mis à jour.'})

    return render_template('parametres.html', user=current_user)
