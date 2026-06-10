-- Fcihier présentant la structure de la base de données finale
-- Extensions utiles
CREATE EXTENSION IF NOT EXISTS pgcrypto;  -- pour gen_random_uuid() si besoin

-- =============================================================
-- TABLE : users
-- =============================================================
CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    nom           VARCHAR(100) NOT NULL,
    prenom        VARCHAR(100) NOT NULL,
    email         VARCHAR(150) NOT NULL UNIQUE,
    telephone     VARCHAR(20)  NOT NULL UNIQUE,
    mot_de_passe  VARCHAR(255) NOT NULL,  -- stocké hashé (bcrypt côté Python)
    created_at    TIMESTAMP DEFAULT NOW()
);

-- =============================================================
-- TABLE : profiles
-- =============================================================
CREATE TYPE filiere_enum AS ENUM ('IA', 'IM', 'GL', 'SE_IoT', 'SI');

CREATE TABLE profiles (
    id         SERIAL PRIMARY KEY,
    user_id    INT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    filiere    filiere_enum NOT NULL,
    niveau     INT NOT NULL CHECK (niveau BETWEEN 1 AND 5),
    photo_url  VARCHAR(255),
    bio        TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =============================================================
-- TABLE : skills
-- Liste fixe des matières/compétences disponibles
-- =============================================================
CREATE TABLE skills (
    id   SERIAL PRIMARY KEY,
    nom  VARCHAR(100) NOT NULL UNIQUE
);

-- =============================================================
-- TABLE : user_skills
-- Compétences maîtrisées ou lacunes d'un utilisateur
-- =============================================================
CREATE TYPE skill_type_enum AS ENUM ('fort', 'faible');

CREATE TABLE user_skills (
    id        SERIAL PRIMARY KEY,
    user_id   INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    skill_id  INT NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    type      skill_type_enum NOT NULL,
    UNIQUE (user_id, skill_id, type)
);

-- =============================================================
-- TABLE : availabilities
-- Créneaux horaires habituels d'un utilisateur
-- =============================================================
CREATE TYPE jour_enum AS ENUM (
    'Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'
);

CREATE TABLE availabilities (
    id           SERIAL PRIMARY KEY,
    user_id      INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    jour         jour_enum NOT NULL,
    heure_debut  TIME NOT NULL,
    heure_fin    TIME NOT NULL,
    CHECK (heure_fin > heure_debut)
);

-- =============================================================
-- TABLE : mentoring_posts
-- Offres ou demandes de mentorat publiées
-- =============================================================
CREATE TYPE post_type_enum   AS ENUM ('offre', 'demande');
CREATE TYPE format_enum      AS ENUM ('présentiel', 'en ligne', 'les deux');
CREATE TYPE post_statut_enum AS ENUM ('actif', 'fermé');

CREATE TABLE mentoring_posts (
    id          SERIAL PRIMARY KEY,
    user_id     INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type_post   post_type_enum NOT NULL,
    skill_id    INT NOT NULL REFERENCES skills(id),
    format      format_enum NOT NULL,
    statut      post_statut_enum DEFAULT 'actif',
    description TEXT,
    created_at  TIMESTAMP DEFAULT NOW()
);

-- =============================================================
-- TABLE : post_availabilities
-- Créneaux spécifiques liés à un post (peuvent différer des dispo habituelles)
-- =============================================================
CREATE TABLE post_availabilities (
    id           SERIAL PRIMARY KEY,
    post_id      INT NOT NULL REFERENCES mentoring_posts(id) ON DELETE CASCADE,
    jour         jour_enum NOT NULL,
    heure_debut  TIME NOT NULL,
    heure_fin    TIME NOT NULL,
    CHECK (heure_fin > heure_debut)
);

-- =============================================================
-- TABLE : matches
-- Paires mentor-mentoré générées par l'algorithme
-- =============================================================
CREATE TYPE match_statut_enum AS ENUM ('proposé', 'accepté', 'refusé');

CREATE TABLE matches (
    id          SERIAL PRIMARY KEY,
    mentor_id   INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    mentee_id   INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    score       FLOAT NOT NULL CHECK (score >= 0 AND score <= 100),
    statut      match_statut_enum DEFAULT 'proposé',
    created_at  TIMESTAMP DEFAULT NOW(),
    UNIQUE (mentor_id, mentee_id),
    CHECK (mentor_id <> mentee_id)  -- RG01 : pas d'auto-match
);

-- =============================================================
-- TABLE : conversations
-- Une conversation = un match accepté
-- =============================================================
CREATE TABLE conversations (
    id         SERIAL PRIMARY KEY,
    match_id   INT NOT NULL UNIQUE REFERENCES matches(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =============================================================
-- TABLE : messages
-- Messages échangés dans une conversation
-- =============================================================
CREATE TABLE messages (
    id               SERIAL PRIMARY KEY,
    conversation_id  INT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id        INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    contenu          TEXT NOT NULL,
    lu               BOOLEAN DEFAULT FALSE,
    sent_at          TIMESTAMP DEFAULT NOW()
);

-- =============================================================
-- INDEX utiles pour les performances
-- =============================================================
CREATE INDEX idx_user_skills_user     ON user_skills(user_id);
CREATE INDEX idx_user_skills_skill    ON user_skills(skill_id);
CREATE INDEX idx_availabilities_user  ON availabilities(user_id);
CREATE INDEX idx_posts_user           ON mentoring_posts(user_id);
CREATE INDEX idx_posts_skill          ON mentoring_posts(skill_id);
CREATE INDEX idx_matches_mentor       ON matches(mentor_id);
CREATE INDEX idx_matches_mentee       ON matches(mentee_id);
CREATE INDEX idx_messages_conv        ON messages(conversation_id);
CREATE INDEX idx_messages_sender      ON messages(sender_id);

-- les conversions de type
-- -------------------------------------------------------------
ALTER TABLE availabilities      DROP CONSTRAINT IF EXISTS availabilities_check;
ALTER TABLE post_availabilities DROP CONSTRAINT IF EXISTS post_availabilities_check;

-- -------------------------------------------------------------

-- erreurs de cast lors des INSERT via Python
-- -------------------------------------------------------------
ALTER TABLE availabilities       ALTER COLUMN jour      TYPE VARCHAR(20) USING jour::text;
ALTER TABLE mentoring_posts      ALTER COLUMN type_post TYPE VARCHAR(10) USING type_post::text;
ALTER TABLE mentoring_posts      ALTER COLUMN format    TYPE VARCHAR(20) USING format::text;
ALTER TABLE post_availabilities  ALTER COLUMN jour      TYPE VARCHAR(20) USING jour::text;

-- -------------------------------------------------------------

-- -------------------------------------------------------------
ALTER TABLE mentoring_posts ALTER COLUMN statut DROP DEFAULT;
ALTER TABLE mentoring_posts ALTER COLUMN statut TYPE VARCHAR(20) USING statut::text;
ALTER TABLE mentoring_posts ALTER COLUMN statut SET DEFAULT 'actif';

ALTER TABLE matches ALTER COLUMN statut DROP DEFAULT;
ALTER TABLE matches ALTER COLUMN statut TYPE VARCHAR(20) USING statut::text;
ALTER TABLE matches ALTER COLUMN statut SET DEFAULT 'propose';

-- -------------------------------------------------------------
ALTER TABLE user_skills ALTER COLUMN type    TYPE VARCHAR(10) USING type::text;
ALTER TABLE profiles    ALTER COLUMN filiere TYPE VARCHAR(20) USING filiere::text;

-- -------------------------------------------------------------
-- -------------------------------------------------------------
DROP TYPE IF EXISTS jour_enum          CASCADE;
DROP TYPE IF EXISTS post_type_enum     CASCADE;
DROP TYPE IF EXISTS format_enum        CASCADE;
DROP TYPE IF EXISTS post_statut_enum   CASCADE;
DROP TYPE IF EXISTS match_statut_enum  CASCADE;
DROP TYPE IF EXISTS skill_type_enum    CASCADE;
DROP TYPE IF EXISTS filiere_enum       CASCADE;

-- Les heures sont gérées comme strings "HH:MM" côté Python
-- -------------------------------------------------------------
ALTER TABLE availabilities      ALTER COLUMN heure_debut TYPE VARCHAR(8) USING heure_debut::text;
ALTER TABLE availabilities      ALTER COLUMN heure_fin   TYPE VARCHAR(8) USING heure_fin::text;
ALTER TABLE post_availabilities ALTER COLUMN heure_debut TYPE VARCHAR(8) USING heure_debut::text;
ALTER TABLE post_availabilities ALTER COLUMN heure_fin   TYPE VARCHAR(8) USING heure_fin::text;

-- -------------------------------------------------------------
-- Affiche les types actuels de toutes les colonnes modifiées
-- -------------------------------------------------------------
SELECT table_name, column_name, data_type, character_maximum_length
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('availabilities','mentoring_posts','matches','user_skills','profiles','post_availabilities')
  AND column_name IN ('jour','type_post','format','statut','type','filiere','heure_debut','heure_fin')
ORDER BY table_name, column_name;
