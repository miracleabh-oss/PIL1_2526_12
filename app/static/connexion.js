document.getElementById("btn-connexion").addEventListener("click", 
    function() {
    let identifiant = document.getElementById("identifiant").value;
    let password = document.getElementById("password").value;
  
    if (identifiant === "" || password === "") {
    alert("Veuillez remplir tous les champs !");
  }
})