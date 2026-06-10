// profil.js — logique de la page profil

document.getElementById('btn-ouvrir-edition')?.addEventListener('click', () => {
    document.getElementById('vue-lecture').classList.add('cache');
    document.getElementById('vue-edition').classList.remove('cache');
});

document.getElementById('btn-annuler-edition')?.addEventListener('click', () => {
    document.getElementById('vue-edition').classList.add('cache');
    document.getElementById('vue-lecture').classList.remove('cache');
});

// Sélection multiple de skills (chips)
document.querySelectorAll('.skill-chip').forEach(chip => {
    chip.addEventListener('click', () => chip.classList.toggle('selected'));
});

// Grille disponibilités
document.querySelectorAll('.creneau').forEach(cell => {
    cell.addEventListener('click', () => cell.classList.toggle('actif'));
});

// Enregistrer le profil
document.getElementById('btn-enregistrer-profil')?.addEventListener('click', async () => {
    const skills_forts   = [...document.querySelectorAll('.skill-chip.selected[data-type="fort"]')]
                             .map(c => c.dataset.skill);
    const skills_faibles = [...document.querySelectorAll('.skill-chip.selected[data-type="faible"]')]
                             .map(c => c.dataset.skill);

    const disponibilites = [...document.querySelectorAll('.creneau.actif')].map(c => ({
        jour:        c.dataset.jour,
        heure_debut: c.dataset.debut,
        heure_fin:   c.dataset.fin
    }));

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
    const msg = document.getElementById('msg-profil');
    msg.textContent = d.message;
    msg.className   = 'msg-retour ' + (d.success ? 'msg-ok' : 'msg-err');
    if (d.success) setTimeout(() => window.location.reload(), 1000);
});
