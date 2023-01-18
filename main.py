from flask import Flask,render_template,jsonify
import sqlite3

app = Flask(__name__)
app.jinja_env.variable_start_string = '(('
app.jinja_env.variable_end_string = '))'

#forme des données :
#
with  sqlite3.connect("database/COGS.sqlite") as connection:
  curseur = connection.cursor()

def factions():
  factions_data = []
  factions_curseur = curseur.execute("SELECT * FROM Faction")
  factions_col = [col[0] for col in factions_curseur.description]
  factions_liste = factions_curseur.fetchall()
  for faction in factions_liste:
    faction_dict = dict(zip(factions_col,faction))
    factions_data.append(faction_dict)
  return factions_data

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
  faction_regle = []
  # Ajout des règles de faction
  for regle in faction_regle_liste:
      faction_regle_description = dict(zip(faction_regle_col, regle))
      faction_regle.append(faction_regle_description)
  return faction_regle


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
  profil_description = dict(zip(profil_col_names,   profil_caracteristiques))
  
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
factions_donnees= []
liste_faction = factions()
for faction_ID in liste_faction:
  faction_regle = regles_faction( faction_ID['ID'].str() )
  faction_ID['regle'] = faction_regle
  factions_donnees.append(faction_ID)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donnees')
def donnees():
  return jsonify(factions_donnees)

app.run(host='0.0.0.0', port=81)
