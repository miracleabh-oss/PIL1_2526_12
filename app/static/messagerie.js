// messagerie.js — chat temps réel via SocketIO

if (typeof CONV_ID !== 'undefined') {
    const socket = io();

    // Rejoindre la room de cette conversation
    socket.emit('rejoindre_conv', { conv_id: CONV_ID });

    // Scroll en bas au chargement
    const zone = document.getElementById('messages-zone');
    if (zone) zone.scrollTop = zone.scrollHeight;

    // Réception d'un message en temps réel
    socket.on('nouveau_message', (data) => {
        if (data.conv_id !== CONV_ID) return;
        const estMoi = data.sender_id === USER_ID;
        const div = document.createElement('div');
        div.className = `message ${estMoi ? 'message-moi' : 'message-autre'}`;
        div.innerHTML = `
            <div class="message-bulle">${data.contenu}</div>
            <div class="message-heure">${data.sent_at}</div>
        `;
        zone.appendChild(div);
        zone.scrollTop = zone.scrollHeight;
    });

    // Envoi d'un message
    async function envoyerMessage() {
        const input   = document.getElementById('input-message');
        const contenu = input.value.trim();
        if (!contenu) return;
        input.value = '';

        await fetch('/messagerie/envoyer', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ conv_id: CONV_ID, contenu })
        });
    }

    document.getElementById('btn-envoyer')?.addEventListener('click', envoyerMessage);
    document.getElementById('input-message')?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); envoyerMessage(); }
    });
}
