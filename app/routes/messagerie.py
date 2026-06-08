from flask import Blueprint, render_template
messagerie = Blueprint('messagerie', __name__)
@messagerie.route('/messagerie')
def voir_messagerie():
    return render_template('messagerie.html')