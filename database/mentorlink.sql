-- Base de données MentorLink
-- IFRI - 2025/2026

-- Table UTILISATEUR
CREATE TABLE UTILISATEUR (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telephone VARCHAR(20) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    photo_profil VARCHAR(255),
    filiere VARCHAR(50) NOT NULL,
    niveau VARCHAR(20) NOT NULL,
    bio TEXT,
    date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table COMPETENCE
CREATE TABLE COMPETENCE (
    id INT PRIMARY KEY AUTO_INCREMENT,
    utilisateur_id INT NOT NULL,
    matiere VARCHAR(100) NOT NULL,
    type ENUM('fort', 'faible') NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES UTILISATEUR(id)
);

-- Table DISPONIBILITE
CREATE TABLE DISPONIBILITE (
    id INT PRIMARY KEY AUTO_INCREMENT,
    utilisateur_id INT NOT NULL,
    jour ENUM('Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche') NOT NULL,
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES UTILISATEUR(id)
);

-- Table OFFRE_DEMANDE
CREATE TABLE OFFRE_DEMANDE (
    id INT PRIMARY KEY AUTO_INCREMENT,
    utilisateur_id INT NOT NULL,
    type ENUM('offre', 'demande') NOT NULL,
    matiere VARCHAR(100) NOT NULL,
    format ENUM('présentiel', 'en ligne', 'les deux') NOT NULL,
    description TEXT,
    date_publication DATETIME DEFAULT CURRENT_TIMESTAMP,
    statut ENUM('active', 'fermée') DEFAULT 'active',
    FOREIGN KEY (utilisateur_id) REFERENCES UTILISATEUR(id)
);

-- Table MATCHING
CREATE TABLE MATCHING (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mentor_id INT NOT NULL,
    mentore_id INT NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    statut ENUM('en attente', 'accepté', 'refusé') DEFAULT 'en attente',
    date_matching DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mentor_id) REFERENCES UTILISATEUR(id),
    FOREIGN KEY (mentore_id) REFERENCES UTILISATEUR(id)
);

-- Table CONVERSATION
CREATE TABLE CONVERSATION (
    id INT PRIMARY KEY AUTO_INCREMENT,
    matching_id INT NOT NULL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (matching_id) REFERENCES MATCHING(id)
);

-- Table MESSAGE
CREATE TABLE MESSAGE (
    id INT PRIMARY KEY AUTO_INCREMENT,
    conversation_id INT NOT NULL,
    expediteur_id INT NOT NULL,
    contenu TEXT NOT NULL,
    date_envoi DATETIME DEFAULT CURRENT_TIMESTAMP,
    lu BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (conversation_id) REFERENCES CONVERSATION(id),
    FOREIGN KEY (expediteur_id) REFERENCES UTILISATEUR(id)
);