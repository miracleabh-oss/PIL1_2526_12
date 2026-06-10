// profil.js — logique de la page profil

document.getElementById('btn-ouvrir-edition')?.addEventListener('click', () => {
    document.getElementById('vue-lecture').classList.add('cache');
    document.getElementById('vue-edition').classList.remove('cache');
});

document.getElementById('btn-annuler-edition')?.addEventListener('click', () => {
    document.getElementById('vue-edition').classList.add('cache');
    document.getElementById('vue-lecture').classList.remove('cache');
});

// ---- ANOMALIE 1 : empêcher qu'une même matière soit fort ET faible ----
document.querySelectorAll('.skill-chip').forEach(chip => {
    chip.addEventListener('click', () => {
        const skill = chip.dataset.skill;
        const type  = chip.dataset.type;
        const autreType = type === 'fort' ? 'faible' : 'fort';

        // Si la même matière est déjà sélectionnée dans l'autre liste → la désélectionner
        const doublon = document.querySelector(
            `.skill-chip.selected[data-skill="${skill}"][data-type="${autreType}"]`
        );
        if (doublon && !chip.classList.contains('selected')) {
            doublon.classList.remove('selected');
            afficherAvertissement(`"${skill}" retiré des ${autreType === 'fort' ? 'points forts' : 'lacunes'} car vous l'ajoutez à l'autre liste.`);
        }

        chip.classList.toggle('selected');
    });
});

function afficherAvertissement(msg) {
    let el = document.getElementById('avert-skill');
    if (!el) {
        el = document.createElement('p');
        el.id = 'avert-skill';
        el.style.cssText = 'color:#c47f00;font-size:0.85rem;font-weight:600;margin-top:6px;';
        document.getElementById('select-forts')?.parentElement?.after(el);
    }
    el.textContent = '⚠️ ' + msg;
    setTimeout(() => { el.textContent = ''; }, 3500);
}

// ---- Grille disponibilités ----
document.querySelectorAll('.creneau').forEach(cell => {
    cell.addEventListener('click', () => cell.classList.toggle('actif'));
});

// ---- Enregistrer le profil ----
document.getElementById('btn-enregistrer-profil')?.addEventListener('click', async () => {
    const msg = document.getElementById('msg-profil');

    const skills_forts   = [...document.querySelectorAll('.skill-chip.selected[data-type="fort"]')]
                             .map(c => c.dataset.skill);
    const skills_faibles = [...document.querySelectorAll('.skill-chip.selected[data-type="faible"]')]
                             .map(c => c.dataset.skill);

    // ---- ANOMALIE 1 : double vérification côté JS ----
    const doublon = skills_forts.find(s => skills_faibles.includes(s));
    if (doublon) {
        msg.textContent = `❌ "${doublon}" ne peut pas être à la fois point fort et lacune.`;
        msg.className = 'msg-retour msg-err';
        return;
    }

    const disponibilites = [...document.querySelectorAll('.creneau.actif')].map(c => ({
        jour:        c.dataset.jour,
        heure_debut: c.dataset.debut,
        heure_fin:   c.dataset.fin
    }));

    // ---- ANOMALIE 2 : disponibilités obligatoires ----
    if (disponibilites.length === 0) {
        msg.textContent = '❌ Veuillez sélectionner au moins un créneau de disponibilité.';
        msg.className = 'msg-retour msg-err';
        // Mettre en évidence la grille
        document.querySelector('.dispo-grid-wrapper')?.scrollIntoView({ behavior: 'smooth' });
        document.querySelector('.dispo-grid-wrapper').style.border = '2px solid #c62828';
        setTimeout(() => {
            document.querySelector('.dispo-grid-wrapper').style.border = '';
        }, 3000);
        return;
    }

    const data = {
        nom:          document.getElementById('edit-nom').value,
        prenom:       document.getElementById('edit-prenom').value,
        filiere:      document.getElementById('edit-filiere').value,
        niveau:       document.getElementById('edit-niveau').value,
        bio:          document.getElementById('edit-bio').value,
        skills_forts,
        skills_faibles,
        disponibilites
    };

    const r = await fetch('/profil/modifier', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const d = await r.json();
    msg.textContent = d.message;
    msg.className   = 'msg-retour ' + (d.success ? 'msg-ok' : 'msg-err');
    if (d.success) setTimeout(() => window.location.reload(), 1000);
});

// ---- ANOMALIE 3 : upload photo de profil ----
const inputPhoto = document.getElementById('input-photo');
if (inputPhoto) {
    inputPhoto.addEventListener('change', async () => {
        const file = inputPhoto.files[0];
        if (!file) return;

        // Vérifications client
        if (!file.type.startsWith('image/')) {
            alert('Veuillez sélectionner une image (jpg, png, etc.)');
            return;
        }
        if (file.size > 2 * 1024 * 1024) {
            alert('Image trop lourde (max 2 Mo).');
            return;
        }

        const formData = new FormData();
        formData.append('photo', file);

        const r = await fetch('/profil/photo', { method: 'POST', body: formData });
        const d = await r.json();
        if (d.success) {
            // Mettre à jour l'aperçu immédiatement
            document.querySelectorAll('.photo-profil').forEach(img => img.src = d.photo_url + '?t=' + Date.now());
        } else {
            alert(d.message || 'Erreur lors de l\'upload.');
        }
    });
}
