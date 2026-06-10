# Rapport d'Intégration : Messagerie Temps Réel & Notifications
**Projet :** IFRI_MentorLink (Projet Intégrateur 2025-2026)  
**Auteur :** Ghislaine ALAHOU ADJAHA  
**Spécialité :** Systèmes Embarqués et Internet des Objets (SEIoT)  
**Date :** Juin 2026  
**Institut :** Institut de Formation et de Recherche en Informatique (IFRI)  

---

## 1. Objectifs du Module
L'objectif de cette tâche était de finaliser la messagerie instantanée de l'application **IFRI_MentorLink** en intégrant trois fonctionnalités clés :
1. **L'historique des conversations :** Chargement automatique et ordonné des anciens messages depuis la base de données PostgreSQL.
2. **La communication en temps réel (WebSockets) :** Diffusion instantanée des messages au sein d'une discussion active sans rechargement de page.
3. **Les notifications globales en arrière-plan :** Alertes dynamiques et mise à jour des compteurs de messages non lus sur le menu latéral, même si l'utilisateur consulte une autre section de l'application.

---

## 2. Synthèse des Modifications Apportées

### A. Frontend HTML & JavaScript
* **`messagerie.html`** : Restructuration de la section des scripts pour exposer l'identifiant global de l'utilisateur connecté (`USER_ID`) et l'ID de la conversation active (`CONV_ID`) dès le chargement de la page.
* **`messagerie.js`** :
  * Connexion systématique à l'instance **Socket.IO** dès l'initialisation.
  * Implémentation de l'écouteur `nouveau_message` pour l'injection immédiate des bulles de texte dans le DOM avec défilement automatique (*scroll*) vers le bas.
  * Ajout d'un écouteur global `notification_message` chargé d'intercepter les notifications, de modifier en temps réel l'aperçu du dernier texte reçu dans la barre la liste gauche, et d'incrémenter dynamiquement le badge numérique des messages non lus (`.badge-non-lus`).

### B. Backend Python (Flask)
* **`messagerie.py`** :
  * Création de deux types de salons de discussion (*Rooms*) :
    * `conv_{id}` : Dédiée à la synchronisation des flux d'une discussion ouverte.
    * `user_{id}` : Salon personnel et unique à chaque utilisateur pour l'envoi des notifications privées en arrière-plan.
  * Mise à jour de la route API `/messagerie/envoyer` : Après la validation et l'écriture du message en base via l'ORM SQLAlchemy, le serveur émet simultanément deux événements distincts (`nouveau_message` et `notification_message`) pour garantir l'interactivité globale.

---

## 3. Résolution des Problèmes d'Environnement Local
Lors de la phase de lancement du serveur (`python run.py`), plusieurs anomalies liées à l'environnement virtuel (`venv`) ont été identifiées et corrigées avec succès :
1. **`ModuleNotFoundError: No module named 'flask_sqlalchemy'`** : Absence de la bibliothèque de gestion de la base de données. Résolu via l'installation du package correspondant.
2. **`ModuleNotFoundError: No module named 'flask_bcrypt'`** : Absence du module de hachage de sécurité des mots de passe requis par les règles métier définies dans `DATABASE.md`. Résolu via son installation explicite dans l'environnement virtuel.

---

## 4. Protocole de Recette & Validation (Avant Push)
Afin de valider l'implémentation avant la livraison sur la branche distante, le plan de test suivant a été exécuté :
1. **Ouverture de Sessions Multiples** : Simulation de deux utilisateurs distincts en exécutant une session sur un navigateur standard et une seconde sur une fenêtre de navigation privée.
2. **Vérification du Tri Chronologique** : Validation du bon ordonnancement de l'historique de haut en bas grâce à la clause `order_by='Message.sent_at'`.
3. **Test d'Instantanéité** : Envoi de messages croisés et observation de l'affichage immédiat dans les zones de chat respectives (latence < 100ms).
4. **Validation des Notifications** : Désactivation du focus sur la conversation principale pour un utilisateur. Envoi d'un message par le second utilisateur et validation visuelle de l'apparition instantanée du badge numérique sur la sidebar sans aucune action de rafraîchissement manuel.

---
**Statut du module :** Fonctionnel, validé localement et prêt à être fusionné (*push*) sur la branche de travail.