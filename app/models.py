from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id           = db.Column(db.Integer, primary_key=True)
    nom          = db.Column(db.String(100), nullable=False)
    prenom       = db.Column(db.String(100), nullable=False)
    email        = db.Column(db.String(150), unique=True, nullable=False)
    telephone    = db.Column(db.String(20),  unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    profile        = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')
    skills         = db.relationship('UserSkill', backref='user', cascade='all, delete-orphan')
    availabilities = db.relationship('Availability', backref='user', cascade='all, delete-orphan')
    posts          = db.relationship('MentoringPost', backref='user', cascade='all, delete-orphan')


class Profile(db.Model):
    __tablename__ = 'profiles'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    filiere    = db.Column(db.String(20), nullable=False)
    niveau     = db.Column(db.Integer, nullable=False)
    photo_url  = db.Column(db.String(255))
    bio        = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Skill(db.Model):
    __tablename__ = 'skills'
    id  = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)


class UserSkill(db.Model):
    __tablename__ = 'user_skills'
    id       = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    type     = db.Column(db.String(10), nullable=False)  # 'fort' ou 'faible'
    skill    = db.relationship('Skill')


class Availability(db.Model):
    __tablename__ = 'availabilities'
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    jour        = db.Column(db.String(20), nullable=False)
    heure_debut = db.Column(db.String(8),  nullable=False)
    heure_fin   = db.Column(db.String(8),  nullable=False)


class MentoringPost(db.Model):
    __tablename__ = 'mentoring_posts'
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type_post   = db.Column(db.String(10), nullable=False)  # 'offre' ou 'demande'
    skill_id    = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    format      = db.Column(db.String(20), nullable=False)
    statut      = db.Column(db.String(10), default='actif')
    description = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    skill       = db.relationship('Skill')


class Match(db.Model):
    __tablename__ = 'matches'
    id         = db.Column(db.Integer, primary_key=True)
    mentor_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mentee_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score      = db.Column(db.Float,   nullable=False)
    statut     = db.Column(db.String(10), default='proposé')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    mentor     = db.relationship('User', foreign_keys=[mentor_id])
    mentee     = db.relationship('User', foreign_keys=[mentee_id])


class Conversation(db.Model):
    __tablename__ = 'conversations'
    id         = db.Column(db.Integer, primary_key=True)
    match_id   = db.Column(db.Integer, db.ForeignKey('matches.id'), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    match      = db.relationship('Match')
    messages   = db.relationship('Message', backref='conversation', cascade='all, delete-orphan', order_by='Message.sent_at')


class Message(db.Model):
    __tablename__ = 'messages'
    id              = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    sender_id       = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contenu         = db.Column(db.Text, nullable=False)
    lu              = db.Column(db.Boolean, default=False)
    sent_at         = db.Column(db.DateTime, default=datetime.utcnow)
    sender          = db.relationship('User')
