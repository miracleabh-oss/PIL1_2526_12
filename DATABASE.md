# DATABASE.md — IFRI_MentorLink

> **Responsable BDD :** [Ton nom]  
> Toute question sur la structure → me contacter avant de modifier quoi que ce soit.

---

## 1. Setup local (à faire une seule fois)

### Prérequis
- PostgreSQL installé (v14+)
- Accès au terminal / psql

### Étapes

```bash
# 1. Se connecter à PostgreSQL
psql -U postgres

# 2. Créer la base
CREATE DATABASE mentorlink;

# 3. Quitter psql
\q

# 4. Importer le schéma
psql -U postgres -d mentorlink -f schema.sql

# 5. Importer les données de test
psql -U postgres -d mentorlink -f seed.sql

# 6. Vérifier
psql -U postgres -d mentorlink
\dt   -- liste toutes les tables
```

---

## 2. Connexion depuis le backend Python (Flask)

```python
# Dans votre fichier config.py ou .env
DATABASE_URL = "postgresql://postgres:VOTRE_MOT_DE_PASSE@localhost:5432/mentorlink"

# Avec SQLAlchemy (si vous l'utilisez)
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)

# Avec psycopg2 directement
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="mentorlink",
    user="postgres",
    password="VOTRE_MOT_DE_PASSE"
)
```

---

## 3. Tables disponibles

| Table | Description |
|---|---|
| `users` | Comptes utilisateurs (email, téléphone, mot de passe hashé) |
| `profiles` | Infos de profil (filière, niveau, bio, photo) |
| `skills` | Liste des matières/compétences disponibles |
| `user_skills` | Liens user↔skill avec type `fort` ou `faible` |
| `availabilities` | Créneaux horaires habituels d'un user |
| `mentoring_posts` | Offres et demandes de mentorat publiées |
| `post_availabilities` | Créneaux spécifiques d'un post |
| `matches` | Paires mentor-mentoré avec score de compatibilité |
| `conversations` | Une conversation par match accepté |
| `messages` | Messages échangés dans une conversation |

---

## 4. Requêtes fréquentes — copiez-collez directement

### Récupérer un user avec son profil
```sql
SELECT u.id, u.nom, u.prenom, u.email, p.filiere, p.niveau, p.bio
FROM users u
JOIN profiles p ON p.user_id = u.id
WHERE u.id = $1;
```

### Compétences fortes d'un user
```sql
SELECT s.nom
FROM user_skills us
JOIN skills s ON s.id = us.skill_id
WHERE us.user_id = $1 AND us.type = 'fort';
```

### Lacunes d'un user
```sql
SELECT s.nom
FROM user_skills us
JOIN skills s ON s.id = us.skill_id
WHERE us.user_id = $1 AND us.type = 'faible';
```

### Posts actifs disponibles (pour la recherche)
```sql
SELECT mp.*, s.nom as skill_nom, u.nom, u.prenom
FROM mentoring_posts mp
JOIN skills s ON s.id = mp.skill_id
JOIN users u ON u.id = mp.user_id
WHERE mp.statut = 'actif'
ORDER BY mp.created_at DESC;
```

### Matchs d'un utilisateur (acceptés)
```sql
SELECT m.id, m.score,
       mentor.nom AS mentor_nom, mentor.prenom AS mentor_prenom,
       mentee.nom AS mentee_nom, mentee.prenom AS mentee_prenom
FROM matches m
JOIN users mentor ON mentor.id = m.mentor_id
JOIN users mentee ON mentee.id = m.mentee_id
WHERE (m.mentor_id = $1 OR m.mentee_id = $1)
  AND m.statut = 'accepté';
```

### Messages d'une conversation
```sql
SELECT m.contenu, m.sent_at, m.lu,
       u.nom AS expediteur_nom, u.prenom AS expediteur_prenom
FROM messages m
JOIN users u ON u.id = m.sender_id
WHERE m.conversation_id = $1
ORDER BY m.sent_at ASC;
```

### Marquer les messages comme lus
```sql
UPDATE messages
SET lu = TRUE
WHERE conversation_id = $1 AND sender_id <> $2;
```

---

## 5. Règles importantes (NE PAS contourner)

| Règle | Qui l'applique |
|---|---|
| Les mots de passe sont toujours hashés avec bcrypt avant insertion | Backend |
| On ne crée une conversation que si le match est `'accepté'` | Backend |
| Un user ne peut pas se matcher avec lui-même | BDD (contrainte CHECK) |
| Seuls les participants d'une conversation peuvent voir ses messages | Backend |
| L'email et le téléphone sont uniques — vérifier avant INSERT | Backend |

---

## 6. Données de test disponibles

| ID | Nom | Filière | Fort en | Faible en | Mot de passe |
|---|---|---|---|---|---|
| 1 | Koffi Akpovi | IA | Python, ML | Réseaux | `password123` |
| 2 | Aline Dossou | GL | Algo, Maths | Python | `password123` |
| 3 | Moussa Bello | SI | Réseaux, Linux | SQL | `password123` |
| 4 | Clarisse Hounsou | IM | SQL, BDD | Algo | `password123` |
| 5 | Steve Adjovi | SE_IoT | JS, HTML/CSS | Maths | `password123` |
