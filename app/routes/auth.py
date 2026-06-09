from flask import Blueprint, render_template, request, redirect, url_for

auth = Blueprint('auth', __name__)

@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        filiere = request.form.get('filiere')
        niveau = request.form.get('niveau')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if password != password2:
            return "Les mots de passe ne correspondent pas"
        return redirect(url_for('auth.connexion'))
    return render_template('inscription.html')

@auth.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        identifiant = request.form.get('identifiant')
        password = request.form.get('password')
        
        if not identifiant or not password:
            return "Veuillez remplir tous les champs"
        
        return redirect(url_for('auth.accueil'))
    
    return render_template('connexion.html')

@auth.route('/deconnexion')
def deconnexion():
    return redirect(url_for('auth.connexion'))

@auth.route('/')
def accueil():
    return render_template('accueil.html')