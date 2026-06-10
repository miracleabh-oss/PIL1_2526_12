from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User, Profile, Skill, UserSkill, Availability

auth = Blueprint('auth', __name__)

SKILLS_DISPONIBLES = [
    'Python', 'SQL', 'Algorithmique', 'Réseaux', 'Mathématiques',
    'JavaScript', 'HTML/CSS', 'Linux', 'Bases de données', 'Machine Learning',
    'Programmation web', 'Systèmes d\'exploitation', 'C/C++', 'Java',
    'Probabilités & Statistiques', 'Électronique', 'Sécurité informatique'
]

@auth.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('auth.accueil'))
    return redirect(url_for('auth.connexion'))

@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for('auth.accueil'))

    if request.method == 'POST':
        nom       = request.form.get('nom', '').strip()
        prenom    = request.form.get('prenom', '').strip()
        email     = request.form.get('email', '').strip().lower()
        telephone = request.form.get('telephone', '').strip()
        filiere   = request.form.get('filiere', '')
        niveau    = request.form.get('niveau', '')
        password  = request.form.get('password', '')
        password2 = request.form.get('password2', '')

        # Validations
        if not all([nom, prenom, email, telephone, filiere, niveau, password]):
            flash('Tous les champs sont obligatoires.', 'error')
            return render_template('inscription.html')

        if password != password2:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return render_template('inscription.html')

        if len(password) < 6:
            flash('Le mot de passe doit contenir au moins 6 caractères.', 'error')
            return render_template('inscription.html')

        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé.', 'error')
            return render_template('inscription.html')

        if User.query.filter_by(telephone=telephone).first():
            flash('Ce numéro de téléphone est déjà utilisé.', 'error')
            return render_template('inscription.html')

        # Créer l'utilisateur
        hash_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(nom=nom, prenom=prenom, email=email,
                    telephone=telephone, mot_de_passe=hash_pw)
        db.session.add(user)
        db.session.flush()  # pour obtenir user.id

        # Créer le profil
        profile = Profile(user_id=user.id, filiere=filiere, niveau=int(niveau))
        db.session.add(profile)

        db.session.commit()
        login_user(user)
        flash('Compte créé avec succès !', 'success')
        return redirect(url_for('profil.voir_profil'))  # première connexion → profil

    return render_template('inscription.html')


@auth.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for('auth.accueil'))

    if request.method == 'POST':
        identifiant = request.form.get('identifiant', '').strip()
        password    = request.form.get('password', '')

        if not identifiant or not password:
            flash('Veuillez remplir tous les champs.', 'error')
            return render_template('connexion.html')

        # Chercher par email ou téléphone
        user = User.query.filter_by(email=identifiant.lower()).first()
        if not user:
            user = User.query.filter_by(telephone=identifiant).first()

        if not user or not bcrypt.check_password_hash(user.mot_de_passe, password):
            flash('Identifiant ou mot de passe incorrect.', 'error')
            return render_template('connexion.html')

        login_user(user)

        # Première connexion (pas de skills ni de dispos) → page profil
        if not user.skills and not user.availabilities:
            return redirect(url_for('profil.voir_profil'))

        return redirect(url_for('auth.accueil'))

    return render_template('connexion.html')


@auth.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    return redirect(url_for('auth.connexion'))


@auth.route('/accueil')
@login_required
def accueil():
    return render_template('accueil.html', user=current_user)
