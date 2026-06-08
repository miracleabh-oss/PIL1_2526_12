from flask import Blueprint, render_template, request, redirect, url_for
auth = Blueprint('auth', __name__)
@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    return render_template('inscription.html')
@auth.route('/connexion', methods=['GET', 'POST'])
def connexion():
    return  render_template('connexion.html')
@auth.route('/deconnexion')
def deconnexion():
    return redirect(url_for('auth.connexion'))
@auth.route('/')
def accueil():
    return render_template('accueil.html')