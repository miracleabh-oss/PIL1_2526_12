document.getElementById("btn-envoyer").addEventListener("click", function() {
    let message = document.getElementById("input-message").value;

    if (message === "") {
        alert("Écrivez un message d'abord !");
        return;
    }

    let zone = document.getElementById("zone-messages");
    zone.innerHTML += "<p>" + message + "</p>";

    document.getElementById("input-message").value = "";
})