// app.js — comportements globaux

// Disparition auto des flash messages
document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => el.style.opacity = '0', 3000);
});
