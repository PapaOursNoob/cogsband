var ListeBande = (function () {
  // Méthode privée et propriétés
  cart = [];

  //Constructeur
  function Item(nom, compte) {
    this.nom = nom;
    this.compte = compte;
  }


})

function myFaction(DIVid) {
  var myCurrentDiv = document.getElementById(DIVid);
  var myTitreDiv = document.getElementById("titre");
  const allFactionNavDiv = document.getElementsByClassName("faction");
  if (myCurrentDiv.style.display !== "block") {
    for (let i = 0; i < allFactionNavDiv.length; i++) {
      allFactionNavDiv[i].style.display = "none";
    }
    myTitreDiv.style.display = "none";
    myCurrentDiv.style.display = "block";
  }
}

function mesReglesIn(DIVid, padding, index) {
  var mesReglesDiv = document.getElementById(DIVid);
  mesReglesDiv.style.display = "block";
  padding = (padding * 5) + (20 + ((index - 1) * 40));
  mesReglesDiv.style.margin = ''.concat('20px ', padding.toString(), 'px');
}
function mesReglesOut(DIVid) {
  var mesReglesDiv = document.getElementById(DIVid);
  mesReglesDiv.style.display = "none";
}

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function maFactionSelect() {
  document.getElementById("maFactionBouton").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
  if (!event.target.matches('.DDbouton')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}