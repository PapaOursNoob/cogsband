from flask import Flask,render_template,jsonify
import unidecode
import sqlite3

app = Flask(__name__)
app.jinja_env.variable_start_string = '(( '
app.jinja_env.variable_end_string = ' ))'
#forme des données :
# {faction :{nom:fôô,nom_normalise:foo,regle:[{nom:exemple,description:patati patata},..],combattants:[{profil1},{profil2},{profil3}]}}
with  sqlite3.connect("database/COGS.sqlite") as connection:
  curseur = connection.cursor()
#initialisation de la donnée de debug
test=[]

#def soldats(faction_id):

# Regles spéciales de facion
# format des données retournées :
# {"Nom": "regle", "Description":"Contenu de la regle"}
def regles_faction(faction_id : str):
  faction_regle_cursor = curseur.execute(
    "SELECT Nom, Description FROM Regles_Faction WHERE Faction_ID = (?)",
    faction_id)
    #initialisation des noms de colonnes pour les règles spéciales
  faction_regle_col = [col[0] for col in faction_regle_cursor.description]
  faction_regle_liste = faction_regle_cursor.fetchall()
  #faction_regle = []
  # Ajout des règles de faction
  for regle in faction_regle_liste:
      faction_regle_description = dict(zip(faction_regle_col, regle))
      #faction_regle.append(faction_regle_description)
  return faction_regle_description


# Caractéristique de profil
# format des données retournées :
# [{'Nom': 'Occultivur', 'Type': 'Infanterie', 'Rang': '2', 'M': '20', 'E': '8', 'V': '8', 'C': '4'}]
def profil_soldat(soldat_id : str):
  #carac du profil
  profil_curseur = curseur.execute(
    "SELECT Nom,Type,Rang,M,E,V,C FROM Combattant WHERE ID =(?)", 
    soldat_id)
  profil_col_names = [col[0] for col in profil_curseur.description]
  profil_caracteristiques = [str(x) for x in profil_curseur.fetchone()]  
  # création du dictionnaire de caractéristique
  profil_description = [dict(zip(profil_col_names,   profil_caracteristiques))]
  return profil_description

# Règles spéciales de profil 
# format des données retournées :
# [{'Nom': 'Furtif', 'Description': 'Furtif', 'Precision': None}]
def regles_soldat(soldat_id : str):
  soldat_regle_cursor = curseur.execute(
    "SELECT Regles_sp.Nom,Regles_sp.Description,Combattant_Regle_sp.Precision FROM Regles_sp, Combattant_Regle_sp WHERE Combattant_Regle_sp.Combattant_ID=(?) AND Combattant_Regle_sp.Regles_sp_ID=Regles_sp.ID",
    soldat_id)
  soldat_regle_col_names = [colr[0] for colr in soldat_regle_cursor.description]
  liste_soldat_regle = []
  for soldat_regle in soldat_regle_cursor.fetchall():
    soldat_regle_data = list(soldat_regle)
    liste_soldat_regle.append(dict(zip(soldat_regle_col_names,soldat_regle_data)))
  return liste_soldat_regle

# Armes de profil
# format des données retournées :
# [{'Nom': 'Carabine Tesla', 'L': '70', 'R': 2, 'P': 5, 'Couleur': None}]
def armes_soldat(soldat_id : str):
  # Ajout des armes pour chaque profil     
  Armes_curseur = curseur.execute(
    "SELECT Armes.Nom, Armes.L, Armes.R, Armes.P, Combattant_Armes.Couleur FROM Armes, Combattant_Armes WHERE Combattant_Armes.Combattant_ID=(?) AND Combattant_Armes.ARMES_ID=Armes.ID ORDER BY Combattant_Armes.Couleur",
    soldat_id)
  #Nom des colonnes des armes
  armes_col_names = [col[0] for col in Armes_curseur.description]
  #initialisation de la liste des armes pour chaque combattant
  liste_armes = []
  for soldat_armes in Armes_curseur.fetchall():
    armes_donnees = list(soldat_armes)
    liste_armes.append(dict(zip(armes_col_names,armes_donnees)))
  return liste_armes

#récupération liste des factions
armies_cursor = curseur.execute(
  "SELECT * FROM Faction")
#initialisation des noms de colonnes pour les factions
col_names = [col[0] for col in armies_cursor.description]
#Suppression de l'ID dans les noms de colonnes pour la boucle
del col_names[0]
#Ajout de la colonne de nom de faction normalisé, de règle de faction et des profils
col_names.append('nom_normalise')
col_names.append('regle_faction')
col_names.append('profils')
#Initialisation de la liste des factions
armies = []


#Boucle de récupération des infos
for faction in armies_cursor.fetchall():
  #initialisation de la liste des infos de la faction analysée
  faction_donnees = []
  faction_donnees .append(faction[1])

  ###############################################
  #ajout de la liste des profils à chaque faction
  liste_nom_profils = curseur.execute(
    "SELECT ID FROM Combattant WHERE Faction_ID =(?)",
    str(faction[0])).fetchall()
  profildata = list(liste_nom_profils)
  liste_profils = {}
  # Parcours de la liste des profils pour la faction analysée
  for profil in liste_nom_profils:

      # création du dictionnaire de caractéristique
      profil_description={}
      soldat = profil_soldat(profil)
      
      # ajout des listes de règle de spéciales de chaaque profil
      regles_soldat_liste = regles_soldat(profil)

      # ajout des listes d'armes
      armes_soldat_liste = armes_soldat(profil)

      profil_description = [soldat,regles_soldat_liste,armes_soldat_liste]
#      profil_description = {"carac":soldat,"regles":regles_soldat_liste,"armes":armes_soldat_liste}

      # compilation des profils de la faction à chaque passage de boucle
      liste_profils[profil[0]] = profil_description
    
  #Construction de la structure des données de toutes les factions
  ###  Nom normalisé  ###
  faction_donnees.append(unidecode.unidecode(faction_donnees[0]))
  ### Règles de faction  ###
  regles_faction_liste=regles_faction(str(faction[0]))
  faction_donnees.append(regles_faction_liste)
  ### Liste des profils  ###
  faction_donnees.append(liste_profils)
  armies.append(dict(zip(col_names, faction_donnees)))
equipements = connection.execute("SELECT * FROM Equipement").fetchall()
capacites = connection.execute("SELECT * FROM Capacite").fetchall()
#donnees = {"factions":armies,"equipements":equipements,"capacites":capacites}
donnees = {"equipements":equipements,"capacites":capacites}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donnees')
def donnees():
  return jsonify(donnees)

app.run(host='0.0.0.0', port=81)
