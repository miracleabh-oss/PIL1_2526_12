document.getElementById("btn-inscription").addEventListener("click", function() {
    let password = document.getElementById("password").value;
    let password2 = document.getElementById("password2").value;

    if (password !== password2) {
        alert("Les mots de passe ne correspondent pas !");
    }
})