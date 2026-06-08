from flask import Blueprint, render_template
matching = Blueprint('matching', __name__)
@matching.route('/matching')
def voir_matching():
    return render_template('matching.html')