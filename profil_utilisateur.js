const vueLecture = document.getElementById("vue-lecture");
const vueEdition = document.getElementById("vue-edition");
const formProfil = document.getElementById("form-profil");
const messageErreur = document.getElementById("message-erreur");

const photoAffichage = document.getElementById("photo-affichage");
const photoApercu = document.getElementById("photo-apercu");
const inputPhoto = document.getElementById("input-photo");

let photoUrl = photoAffichage.src;

function afficherEdition() {
    messageErreur.textContent = "";
    vueLecture.classList.add("cache");
    vueEdition.classList.remove("cache");
}

function afficherLecture() {
    vueEdition.classList.add("cache");
    vueLecture.classList.remove("cache");
}

function getNiveauTexte(valeur) {
    if (valeur === "L1") return "Licence 1";
    if (valeur === "L2") return "Licence 2";
    if (valeur === "L3") return "Licence 3";
    return valeur;
}

function creerTags(texte, classe) {
    const conteneur = document.createElement("div");
    conteneur.className = "tags";

    const matieres = texte.split(",").map(function(m) {
        return m.trim();
    }).filter(function(m) {
        return m.length > 0;
    });

    matieres.forEach(function(matiere) {
        const span = document.createElement("span");
        span.className = "tag " + classe;
        span.textContent = matiere;
        conteneur.appendChild(span);
    });

    return conteneur;
}

function creerDisponibilites(texte) {
    const liste = document.createElement("ul");
    liste.className = "disponibilites";

    const lignes = texte.split("\n").filter(function(ligne) {
        return ligne.trim().length > 0;
    });

    lignes.forEach(function(ligne) {
        const parties = ligne.split(":");
        const jour = parties[0] ? parties[0].trim() : "";
        const heure = parties[1] ? parties[1].trim() : "";

        const li = document.createElement("li");
        li.innerHTML = '<span class="jour">' + jour + '</span><span class="heure">' + heure + '</span>';
        liste.appendChild(li);
    });

    return liste;
}

function mettreAJourProfil() {
    const nom = document.getElementById("input-nom").value.trim();
    const prenom = document.getElementById("input-prenom").value.trim();
    const filiere = document.getElementById("input-filiere").value;
    const niveau = document.getElementById("input-niveau").value;
    const fortes = document.getElementById("input-fortes").value.trim();
    const lacunes = document.getElementById("input-lacunes").value.trim();
    const dispo = document.getElementById("input-dispo").value.trim();

    document.getElementById("nom-complet").textContent = nom + " " + prenom;
    document.getElementById("filiere-affichage").textContent = "Filière " + filiere;
    document.getElementById("niveau-affichage").textContent = "Niveau " + getNiveauTexte(niveau);

    photoUrl = photoApercu.src;
    photoAffichage.src = photoUrl;

    const fortesAffichage = document.getElementById("fortes-affichage");
    const nouvellesFortes = creerTags(fortes, "tag-fort");
    fortesAffichage.replaceWith(nouvellesFortes);
    nouvellesFortes.id = "fortes-affichage";

    const lacunesAffichage = document.getElementById("lacunes-affichage");
    const nouvellesLacunes = creerTags(lacunes, "tag-lacune");
    lacunesAffichage.replaceWith(nouvellesLacunes);
    nouvellesLacunes.id = "lacunes-affichage";

    const dispoAffichage = document.getElementById("dispo-affichage");
    const nouvellesDispo = creerDisponibilites(dispo);
    dispoAffichage.replaceWith(nouvellesDispo);
    nouvellesDispo.id = "dispo-affichage";

    afficherLecture();
}

document.getElementById("btn-modifier").addEventListener("click", afficherEdition);

document.getElementById("btn-annuler").addEventListener("click", function() {
    photoApercu.src = photoUrl;
    messageErreur.textContent = "";
    afficherLecture();
});

inputPhoto.addEventListener("change", function() {
    const fichier = inputPhoto.files[0];
    if (fichier) {
        const lecteur = new FileReader();
        lecteur.onload = function(e) {
            photoApercu.src = e.target.result;
        };
        lecteur.readAsDataURL(fichier);
    }
});

formProfil.addEventListener("submit", function(e) {
    const nom = document.getElementById("input-nom").value.trim();
    const prenom = document.getElementById("input-prenom").value.trim();
    const fortes = document.getElementById("input-fortes").value.trim();
    const lacunes = document.getElementById("input-lacunes").value.trim();
    const dispo = document.getElementById("input-dispo").value.trim();

    if (!nom || !prenom || !fortes || !lacunes || !dispo) {
        e.preventDefault();
        messageErreur.textContent = "Veuillez remplir tous les champs obligatoires.";
        alert("Veuillez remplir tous les champs obligatoires.");
        return;
    }

    e.preventDefault();
    messageErreur.textContent = "";
    mettreAJourProfil();
});
