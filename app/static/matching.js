// matching.js — accepter un match

document.querySelectorAll('.btn-accepter').forEach(btn => {
    btn.addEventListener('click', async () => {
        const id   = btn.dataset.id;
        const role = btn.dataset.role;
        btn.disabled = true;
        btn.textContent = '...';

        const r = await fetch(`/matching/accepter/${id}`, {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ role })
        });
        const d = await r.json();

        if (d.success) {
            const toast = document.getElementById('toast-match');
            toast.classList.remove('cache');
            setTimeout(() => window.location.reload(), 2000);
        }
    });
});
