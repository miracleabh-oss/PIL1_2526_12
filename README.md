  IFRI_MentorLink 

 Description

IFRI_MentorLink est une application web développée dans le cadre du Projet Intégrateur 2025-2026 de l'Institut de Formation et de Recherche en Informatique (IFRI).
L'objectif de cette plateforme est de faciliter la mise en relation entre les étudiants souhaitant bénéficier d'un accompagnement académique ou professionnel et ceux disposés à partager leurs connaissances et leurs compétences.
L'application permet la création de profils utilisateurs, la publication d'offres et de demandes de mentorat, la mise en correspondance automatique des utilisateurs grâce à un algorithme de matching ainsi qu'une messagerie intégrée.

 Fonctionnalités

- Inscription et connexion des utilisateurs
- Gestion des profils utilisateurs
- Publication d'offres de mentorat
- Publication de demandes de mentorat
- Algorithme de matching
- Consultation des résultats de matching
- Messagerie instantanée
- Gestion des conversations

 Technologies utilisées

 Frontend
- HTML5
- CSS3
- JavaScript

 
Backend
- Python
- Flask

 Base de données
- PostgreSQL

Outils de collaboration
- Git
- GitHub

 Structure du projet

PIL1_2526_12/

├── app/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── matching.py
│   │   ├── profil.py
│   │   └── messagerie.py
│   │
│   ├── templates/
│   ├── static/
│   └── matching.py
│
├── schema.sql
├── seed.sql
└── run.py

Installation
•	Cloner le dépôt en tapant dans le terminal : git clone https://github.com/miracleabh-oss/PIL1_2526_12.git
•	Installer les dépendances en exécutant dans le terminal : pip install flask psycopg2

•	Créer la base de données en exécutant dans le terminal : psql -U postgres -c "CREATE DATABASE mentorlink
•	Créer la base de données en exécutant dans le terminal : psql -U postgres -c "CREATE DATABASE mentorlink
•	Importer la structure de la base de données en exécutant dans le terminal : psql -U postgres -d mentorlink -f schema.sql
•	Charger les données de test en exécutant dans le terminal : psql -U postgres -d mentorlink -f seed.sql
•	  Lancer l'application en exécutant : python run.py
•	  Ouvrir l'application dans un navigateur : http://127.0.0.1:5000


Utilisation
1.	Aller sur la page d'accueil
2.	Cliquer sur S'inscrire et remplir le formulaire
3.	Se connecter avec son email et mot de passe
4.	Consulter son profil et modifier ses compétences et disponibilités
5.	Consulter les résultats de matching pour trouver un mentor ou mentoré. Le système vous propose une liste de mentors ou mentorés selon les compétences et les horaires. Cliquez sur Contacter, pour ouvrir une discussion.
6.	Envoyer un message via la messagerie intégrée


 Membres du groupe
- Gedeon — Algorithme de matching
- Ghislaine — Base de données
- Alex — Authentification
- Miraculé — Messagerie
- Merveille — Interfaces profils et matching
- Amos — Interfaces connexion et messagerie
- Juste — Documentation, README, rapport HTML et déploiement

 Projet académique

Projet Intégrateur 2025-2026

Institut de Formation et de Recherche en Informatique (IFRI)

Université d'Abomey-Calavi
