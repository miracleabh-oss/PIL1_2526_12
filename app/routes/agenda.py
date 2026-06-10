from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Match, User, Availability

agenda = Blueprint('agenda', __name__)


@agenda.route('/agenda')
@login_required
def voir_agenda():
    # Matchs acceptés = sessions de mentorat planifiées
    matchs = Match.query.filter(
        ((Match.mentor_id == current_user.id) | (Match.mentee_id == current_user.id)),
        Match.statut == 'accepté'
    ).all()

    sessions = []
    for m in matchs:
        autre_id = m.mentee_id if m.mentor_id == current_user.id else m.mentor_id
        autre    = User.query.get(autre_id)
        role     = 'Mentor' if m.mentor_id == current_user.id else 'Mentoré'

        # Créneaux communs entre les deux
        dispos_moi   = current_user.availabilities
        dispos_autre = autre.availabilities
        creneaux_communs = []
        for d1 in dispos_moi:
            for d2 in dispos_autre:
                if d1.jour == d2.jour:
                    debut = max(d1.heure_debut, d2.heure_debut)
                    fin   = min(d1.heure_fin,   d2.heure_fin)
                    if debut < fin:
                        creneaux_communs.append({
                            'jour':        d1.jour,
                            'heure_debut': debut,
                            'heure_fin':   fin
                        })

        sessions.append({
            'match':            m,
            'autre':            autre,
            'role':             role,
            'creneaux_communs': creneaux_communs
        })

    return render_template('agenda.html', user=current_user, sessions=sessions)
