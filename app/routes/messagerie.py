from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from app import db, socketio
from app.models import Conversation, Message, Match, User

messagerie = Blueprint('messagerie', __name__)


def _get_mes_conversations():
    """Retourne toutes les conversations de l'utilisateur courant."""
    matchs = Match.query.filter(
        ((Match.mentor_id == current_user.id) | (Match.mentee_id == current_user.id)),
        Match.statut == 'accepté'
    ).all()
    convs = []
    for m in matchs:
        conv = Conversation.query.filter_by(match_id=m.id).first()
        if conv:
            autre_id = m.mentee_id if m.mentor_id == current_user.id else m.mentor_id
            autre    = User.query.get(autre_id)
            dernier  = conv.messages[-1] if conv.messages else None
            non_lus  = Message.query.filter_by(
                conversation_id=conv.id, lu=False
            ).filter(Message.sender_id != current_user.id).count()
            convs.append({
                'id':          conv.id,
                'autre':       autre,
                'dernier_msg': dernier,
                'non_lus':     non_lus
            })
    return convs


@messagerie.route('/messagerie')
@login_required
def voir_messagerie():
    convs = _get_mes_conversations()
    conv_id = request.args.get('conv', type=int)
    messages_actifs = []
    conv_active = None
    autre_actif = None

    if conv_id:
        conv_active = Conversation.query.get(conv_id)
        if conv_active:
            m = conv_active.match
            if m.mentor_id == current_user.id or m.mentee_id == current_user.id:
                messages_actifs = conv_active.messages
                autre_id = m.mentee_id if m.mentor_id == current_user.id else m.mentor_id
                autre_actif = User.query.get(autre_id)
                # Marquer comme lus
                Message.query.filter_by(
                    conversation_id=conv_id, lu=False
                ).filter(Message.sender_id != current_user.id).update({'lu': True})
                db.session.commit()

    return render_template('messagerie.html',
        user=current_user,
        conversations=convs,
        messages_actifs=messages_actifs,
        conv_active=conv_active,
        autre_actif=autre_actif
    )


@messagerie.route('/messagerie/envoyer', methods=['POST'])
@login_required
def envoyer_message():
    data    = request.get_json()
    conv_id = data.get('conv_id')
    contenu = data.get('contenu', '').strip()

    if not contenu:
        return jsonify({'success': False, 'message': 'Message vide.'})

    conv = Conversation.query.get(conv_id)
    if not conv:
        return jsonify({'success': False, 'message': 'Conversation introuvable.'})

    m = conv.match
    if m.mentor_id != current_user.id and m.mentee_id != current_user.id:
        return jsonify({'success': False, 'message': 'Accès refusé.'})

    msg = Message(conversation_id=conv_id, sender_id=current_user.id, contenu=contenu)
    db.session.add(msg)
    db.session.commit()

    # Émettre via SocketIO
    socketio.emit('nouveau_message', {
        'conv_id':    conv_id,
        'sender_id':  current_user.id,
        'sender_nom': f'{current_user.prenom} {current_user.nom}',
        'contenu':    contenu,
        'sent_at':    msg.sent_at.strftime('%H:%M')
    }, room=f'conv_{conv_id}')

    return jsonify({'success': True})


# SocketIO events
@socketio.on('rejoindre_conv')
def rejoindre_conv(data):
    conv_id = data.get('conv_id')
    join_room(f'conv_{conv_id}')
