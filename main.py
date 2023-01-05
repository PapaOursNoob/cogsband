from flask import Flask, render_template
import unidecode
import sqlite3

app = Flask(__name__)
#forme des données :
# {faction :{nom:fôô,nom_normalise:foo,regle:[{nom:exemple,description:patati patata},..],combattants:[{profil1},{profil2},{profil3}]}}
with  sqlite3.connect("Database/COGS.sqlite") as connection:
  curseur = connection.cursor()
#initialisation de la donnée de debug
test=[]

#def soldats(faction_id):

def regles_sp(faction_id : str):
  #ajout des règles spéciales à chaque faction
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

# Ajout des règles spéciales pour chaque profil 
def regles_soldat(soldat_id):
  soldat_regle_cursor = curseur.execute(
    "SELECT Regles_sp.Nom,Regles_sp.Description,Combattant_Regle_sp.Precision FROM Regles_sp, Combattant_Regle_sp WHERE Combattant_Regle_sp.Combattant_ID=(?) AND Combattant_Regle_sp.Regles_sp_ID=Regles_sp.ID",
    str(soldat_id))
  soldat_regle_col_names = [colr[0] for colr in soldat_regle_cursor.description]
  liste_soldat_regle = []
  for soldat_regle in soldat_regle_cursor.fetchall():
    soldat_regle_data = list(soldat_regle)
    liste_soldat_regle.append(dict(zip(soldat_regle_col_names,regles_sp_data)))

#récupération liste des factions
armies_cursor = curseur.execute(
  "SELECT * FROM Faction")
#initialisation des noms de colonnes pour les factions
col_names = [col[0] for col in armies_cursor.description]
#Suppression de l'ID dans les noms de colonnes pour la boucle
del col_names[0]
#Ajout de la colonne de nom de faction normalisé, de règle de faction et des profils
col_names.append('Nom_normalise')
col_names.append('Regle_Faction')
col_names.append('Profils')
#Initialisation de la liste des factions
armies = []


#Boucle de récupération des infos
for faction in armies_cursor.fetchall():
  #initialisation de la liste des infos de la faction analysée
  faction_donnees = []
  faction_donnees .append(faction[1])

  ###############################################
  #ajout de la liste des profils à chaque faction"""
  liste_nom_profils = connection.execute(
    "SELECT ID FROM Combattant WHERE Faction_ID =(?)",
    str(faction[0])).fetchall()
  profildata = list(liste_nom_profils)
  liste_profils = {}
  # Parcours de la liste des profils pour la faction analysée
  for profil in liste_nom_profils:
      profil_cursor = connection.execute(
        "SELECT ID,Nom,Type,Rang,M,E,V,C FROM Combattant WHERE ID =(?)", 
        profil)
      profil_col_names = [col[0] for col in profil_cursor.description]
      #suppression de la colonne ID
      del profil_col_names[0]
      profil_row_data = [str(x) for x in profil_cursor.fetchone()]
    
      # Ajout des règles spéciales pour chaque profil     
      regle_sp_cursor = connection.execute(
        "SELECT Regles_sp.Nom,Regles_sp.Description,Combattant_Regle_sp.Precision FROM Regles_sp, Combattant_Regle_sp WHERE Combattant_Regle_sp.Combattant_ID=(?) AND    Combattant_Regle_sp.Regles_sp_ID=Regles_sp.ID",
        profil)
      regles_sp_col_names = [colr[0] for colr in regle_sp_cursor.description]
      liste_regles_sp = []
      for regles_sp in regle_sp_cursor.fetchall():
        regles_sp_data = list(regles_sp)
        liste_regles_sp.append(dict(zip(regles_sp_col_names,regles_sp_data)))
        
      # Ajout des armes pour chaque profil     
      combattants_armes_cursor = connection.execute(
        "SELECT Armes.Nom, Armes.L, Armes.R, Armes.P, Combattant_Armes.Couleur FROM Armes, Combattant_Armes WHERE Combattant_Armes.Combattant_ID=(?) AND Combattant_Armes.ARMES_ID=Armes.ID ORDER BY Combattant_Armes.Couleur",
        profil)
      #Nom des colonnes des armes
      combattants_armes_col_names = [col[0] for col in combattants_armes_cursor.description]
      #initialisation de la liste des armes pour chaque combattant
      liste_armes_combattants = []
      for combattant_armes in combattants_armes_cursor.fetchall():
        combattant_armes_data = list(combattant_armes)
        liste_armes_combattants.append(dict(zip(combattants_armes_col_names,combattant_armes_data)))
      #suppression de l'ID avant d'intégrer les données au profil
      del profil_row_data[0] 
      # création du dictionnaire de caractéristique
      profil_description = [dict(zip(profil_col_names, profil_row_data))]
      profil_description.append(liste_regles_sp)
      profil_description.append(liste_armes_combattants)
      liste_profils[profil[0]] = profil_description
    
  #Construction de la structure des données de toutes les factions
  ###  Nom normalisé  ###
  faction_donnees.append(unidecode.unidecode(faction_donnees[0]))
  ### Règles de faction  ###
  regles_sp_test=[{"Nom":"Règle 1", "Description":"C'est la règle 1"},{"Nom":"Règle 2","Description":"C'estla lrègle 2"}]
  faction_donnees.append(regles_sp_test)
#  faction_donnees.append(regles_sp(faction[0]))
  ### Liste des profils  ###
  faction_donnees.append(liste_profils)
  armies.append(dict(zip(col_names, faction_donnees)))
equipements = connection.execute("SELECT * FROM Equipement").fetchall()
capacites = connection.execute("SELECT * FROM Capacite").fetchall()

test= regles_sp(1)

@app.route('/')
def index():
    return render_template('Presentation.html',
                           armies=armies,
                           profildata=regles_sp_test)


@app.route('/Equipements')
def equipement():
    Liste = []
    for val in equipements:
        Liste.append(val)
    return render_template('Liste-sp.html',
                           armies=armies,
                           Liste=Liste,
                           Titre="Equipement")

@app.route('/Capacite')
def capacite():
    Liste = []
    for val in capacites:
        Liste.append(val)
    return render_template('Liste-sp.html',
                           armies=armies,
                           Liste=Liste,
                           Titre="Capacités")

app.run(host='0.0.0.0', port=81)
