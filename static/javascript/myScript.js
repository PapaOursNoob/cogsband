var ListeBande = (function() {
  // Méthode privée et propriétés
  cart = [];

  //Constructeur
  function Item(nom, compte) {
    this.nom = nom;
    this.compte = compte;
  }

  
})

function myFunction(DIVid) {
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

function mesReglesIn(DIVid, padding, index){
  var mesReglesDiv = document.getElementById(DIVid);
  mesReglesDiv.style.display = "block";
  padding = (padding * 5) + (20 + ((index - 1) * 40));
  mesReglesDiv.style.margin = ''.concat('20px ',padding.toString(),'px') ;
}
function mesReglesOut(DIVid){
  var mesReglesDiv = document.getElementById(DIVid);
  mesReglesDiv.style.display = "none";
}
