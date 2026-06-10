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
