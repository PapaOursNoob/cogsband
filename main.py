from flask import Flask,render_template
import json
import sqlite3

app = Flask(__name__)
app.jinja_env.variable_start_string = '(('
app.jinja_env.variable_end_string = '))'

#forme des données :
#
with  sqlite3.connect("database/COGS.sqlite") as connection:
  curseur = connection.cursor()

  """_summary_
  """
def factions():
  factions_data = []
  factions_curseur = curseur.execute("SELECT * FROM Faction")
  factions_col = [col[0] for col in factions_curseur.description]
  factions_liste = factions_curseur.fetchall()
  for faction in factions_liste:
    faction_dict = dict(zip(factions_col,faction))
    factions_data.append(faction_dict)
  return factions_data

def cette_faction(faction_ID):
  faction_data=[]
  faction_curseur = curseur.execute("SELECT * FROM Faction WHERE ID = (?)",faction_ID)
  faction_col = [col[0] for col in factions_curseur.description]
  faction_liste = faction_curseur.fetchone()
  faction_data.append(dict(zip(faction_col,faction_liste)))
  return faction_data

# Regles spéciales de facion
# format des données retournées :
# {"Nom": "regle", "Description":"Contenu de la regle"}
  """_summary_
  """
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
# {'Nom': 'Occultivur', 'Type': 'Infanterie', 'Rang': '2', 'M': '20', 'E': '8', 'V': '8', 'C': '4'}
def profil_soldat(soldat_id : str):
  #carac du profil
  profil_curseur = curseur.execute("SELECT * FROM Combattant WHERE ID =(?)",  [soldat_id] )
  profil_col_names = [col[0] for col in profil_curseur.description]
  profil_caracteristiques = [str(x) for x in profil_curseur.fetchone()]  
  # création du dictionnaire de caractéristique
  profil_description = dict(zip(profil_col_names,profil_caracteristiques))
  return profil_description

def liste_soldats_faction(faction_id : str):
  liste_soldat_id_curseur = curseur.execute(
    "SELECT ID FROM Combattant WHERE Faction_ID =(?)",
    faction_id
  )
  liste_soldat_id =  [ str(x[0]) for x in liste_soldat_id_curseur.fetchall()]
  return liste_soldat_id

# Règles spéciales de profil 
# format des données retournées :
# [{'Nom': 'Furtif', 'Description': 'Furtif', 'Precision': None}]
def regles_soldat(soldat_id : str):
  soldat_regle_cursor = curseur.execute(
    "SELECT Regles_sp.Nom,Regles_sp.Description,Combattant_Regle_sp.Precision FROM Regles_sp, Combattant_Regle_sp WHERE Combattant_Regle_sp.Combattant_ID=(?) AND Combattant_Regle_sp.Regles_sp_ID=Regles_sp.ID",
    [soldat_id])
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
    [soldat_id])
  #Nom des colonnes des armes
  armes_col_names = [col[0] for col in Armes_curseur.description]
  #initialisation de la liste des armes pour chaque combattant
  liste_armes = []
  for soldat_armes in Armes_curseur.fetchall():
    armes_donnees = list(soldat_armes)
    liste_armes.append(dict(zip(armes_col_names,armes_donnees)))
  return liste_armes

#
# format de données retournées :
#
def capacites():
  capacites_donnees = []
  capacites_curseur = curseur.execute("SELECT * FROM Capacite")
  capacites_col = [col[0] for col in capacites_curseur.description]
  for capacites_fetch in capacites_curseur.fetchall():
    capacites_ligne = list(capacites_fetch)
    capacites_dict = dict(zip(capacites_col,capacites_ligne))
    capacites_donnees.append(capacites_dict)
  return capacites_donnees
  

#
# format de données retournées :
#
def equipements():
  equipements_donnees = []
  equipements_curseur = curseur.execute("SELECT * FROM Equipement")
  equipements_col = [col[0] for col in equipements_curseur.description]
  for equipements_fetch in equipements_curseur.fetchall():
    equipements_ligne = list(equipements_fetch)
    equipements_dict = dict(zip(equipements_col,equipements_ligne))
    equipements_donnees.append(equipements_dict)
  return equipements_donnees

#récupération liste des factions
donnees_jeu={}
factions_donnees= []
liste_faction = factions()
for faction_ID in liste_faction:
  faction_regle = regles_faction( str(faction_ID['ID']) )
  faction_ID['regle'] = faction_regle
  liste_faction_soldats_ID = liste_soldats_faction( str(faction_ID['ID']))
  liste_profils = []
  faction_profils = {}
  for faction_soldat_ID in liste_faction_soldats_ID :
    carac_profil = profil_soldat(str(faction_soldat_ID))
    regles_profil = regles_soldat(str(faction_soldat_ID))
    armes_profil = armes_soldat(str(faction_soldat_ID))
    faction_profils =dict(zip(['carac','armes','regles'],[carac_profil,armes_profil,regles_profil]))
    liste_profils.append(faction_profils)
  faction_ID['profils'] = liste_profils
  factions_donnees.append(faction_ID)
capacites_donnees = curseur.execute("SELECT * FROM Capacite").fetchall()
equipements_donnees = curseur.execute("SELECT * FROM Equipement").fetchall()
donnees_jeu['factions'] = factions_donnees
donnees_jeu['capacites'] = capacites()
donnees_jeu['equipements'] = equipements()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donnees')
def donnees():
  return json.JSONEncoder().encode(donnees_jeu)

@app.route("/donnees/factions")
def faction():
  return json.JSONEncoder().encode(donnees_jeu['factions'])

@app.route("/donnees/factions/<str:unefaction>")
def lafaction(unefaction):
  return json.JSONEncoder().encode(cette_faction(unefaction))

@app.route("/donnees/equipements")
def equipement():
  return json.JSONEncoder().encode(donnees_jeu['equipements'])

@app.route("/donnees/capacites")
def capacite():
  return json.JSONEncoder().encode(donnees_jeu['capacites'])

app.run(host='0.0.0.0', port=81)