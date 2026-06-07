-- =============================================================
-- IFRI_MentorLink — Données de test (seed)
-- À exécuter APRÈS schema.sql
-- Les mots de passe hashés correspondent à "password123"
-- =============================================================

-- Skills disponibles
INSERT INTO skills (nom) VALUES
('Python'), ('SQL'), ('Algorithmique'), ('Réseaux'), ('Mathématiques'),
('JavaScript'), ('HTML/CSS'), ('Linux'), ('Bases de données'), ('Machine Learning');

-- Utilisateurs de test
INSERT INTO users (nom, prenom, email, telephone, mot_de_passe) VALUES
('Akpovi',  'Koffi',   'koffi@ifri.bj',   '+22961000001', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMeSSmd61.aeFAX6MQqhm/8i22'),
('Dossou',  'Aline',   'aline@ifri.bj',   '+22961000002', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMeSSmd61.aeFAX6MQqhm/8i22'),
('Bello',   'Moussa',  'moussa@ifri.bj',  '+22961000003', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMeSSmd61.aeFAX6MQqhm/8i22'),
('Hounsou', 'Clarisse','clarisse@ifri.bj','+22961000004', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMeSSmd61.aeFAX6MQqhm/8i22'),
('Adjovi',  'Steve',   'steve@ifri.bj',   '+22961000005', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMeSSmd61.aeFAX6MQqhm/8i22');

-- Profils
INSERT INTO profiles (user_id, filiere, niveau, bio) VALUES
(1, 'IA',     1, 'Passionné de machine learning et Python.'),
(2, 'GL',     1, 'Forte en algo et mathématiques.'),
(3, 'SI',     1, 'Intéressé par les réseaux et la sécurité.'),
(4, 'IM',     1, 'Aime le web et les bases de données.'),
(5, 'SE_IoT', 1, 'Curieux de tout, fort en Linux.');

-- Compétences fortes
INSERT INTO user_skills (user_id, skill_id, type) VALUES
(1, 1, 'fort'),   -- Koffi fort en Python
(1, 10,'fort'),   -- Koffi fort en ML
(2, 3, 'fort'),   -- Aline forte en Algo
(2, 5, 'fort'),   -- Aline forte en Maths
(3, 4, 'fort'),   -- Moussa fort en Réseaux
(3, 8, 'fort'),   -- Moussa fort en Linux
(4, 2, 'fort'),   -- Clarisse forte en SQL
(4, 9, 'fort'),   -- Clarisse forte en BDD
(5, 6, 'fort'),   -- Steve fort en JS
(5, 7, 'fort');   -- Steve fort en HTML/CSS

-- Lacunes
INSERT INTO user_skills (user_id, skill_id, type) VALUES
(1, 4, 'faible'),  -- Koffi faible en Réseaux
(2, 1, 'faible'),  -- Aline faible en Python
(3, 2, 'faible'),  -- Moussa faible en SQL
(4, 3, 'faible'),  -- Clarisse faible en Algo
(5, 5, 'faible');  -- Steve faible en Maths

-- Disponibilités
INSERT INTO availabilities (user_id, jour, heure_debut, heure_fin) VALUES
(1, 'Lundi',    '14:00', '17:00'),
(1, 'Mercredi', '09:00', '12:00'),
(2, 'Lundi',    '15:00', '18:00'),
(2, 'Jeudi',    '08:00', '11:00'),
(3, 'Mardi',    '13:00', '16:00'),
(4, 'Mercredi', '10:00', '13:00'),
(5, 'Vendredi', '14:00', '17:00');

-- Posts de mentorat
INSERT INTO mentoring_posts (user_id, type_post, skill_id, format, description) VALUES
(1, 'offre',  1,  'en ligne',   'Je propose du soutien en Python pour débutants.'),
(2, 'offre',  3,  'présentiel', 'Cours d''algo niveau L1, exercices inclus.'),
(3, 'demande',2,  'en ligne',   'Besoin d''aide pour comprendre les requêtes SQL.'),
(4, 'offre',  9,  'les deux',   'Je peux aider sur la conception BDD et le SQL.'),
(5, 'demande',5,  'présentiel', 'J''ai du mal avec les suites et séries en Maths.');

-- Un match accepté entre Koffi (mentor Python) et Aline (veut apprendre Python)
INSERT INTO matches (mentor_id, mentee_id, score, statut) VALUES
(1, 2, 87.5, 'accepté');

-- Conversation liée à ce match
INSERT INTO conversations (match_id) VALUES (1);

-- Quelques messages
INSERT INTO messages (conversation_id, sender_id, contenu) VALUES
(1, 1, 'Salut Aline ! On commence quand pour les sessions Python ?'),
(1, 2, 'Bonjour Koffi ! Je suis dispo lundi après-midi si ça te va.'),
(1, 1, 'Parfait, on se retrouve à 14h alors. Je prépare des exercices.');
