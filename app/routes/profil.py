from flask import Blueprint, render_template
profil = Blueprint('profil', __name__)
@profil.route('/profil')
def voir_profil():
    return render_template('profil.html')
@profil.route('/profil/modifier')
def modifier_profil():
    return render_template('modifier_profil.html')