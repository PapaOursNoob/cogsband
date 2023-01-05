CREATE TABLE "Faction"("Nom" TEXT NOT NULL, PRIMARY KEY("Nom"));

CREATE TABLE "Combattant"(
  "Nom" TEXT NOT NULL,
  "Type" TEXT NOT NULL,
  "Rang" INTEGER NOT NULL,
  "M" INTEGER NOT NULL,
  "E" INTEGER NOT NULL,
  "V" INTEGER NOT NULL,
  "C" INTEGER NOT NULL,
  "Faction_Nom" TEXT NOT NULL,
  PRIMARY KEY("Nom"),
  CONSTRAINT "Faction_Combattant"
    FOREIGN KEY ("Faction_Nom") REFERENCES "Faction" ("Nom")
);

CREATE TABLE "Capacité"
  ("Nom" TEXT NOT NULL, "Description" BLOB NOT NULL, PRIMARY KEY("Nom"));

CREATE TABLE "Equipement"
  ("Nom" TEXT NOT NULL, "Description" BLOB NOT NULL, PRIMARY KEY("Nom"));

CREATE TABLE "Armes"(
  "Nom" TEXT NOT NULL,
  "L" INTEGER,
  "R" INTEGER,
  "P" INTEGER NOT NULL,
  PRIMARY KEY("Nom")
);

CREATE TABLE "Regles sp"
  ("Nom" TEXT NOT NULL, "Description" BLOB NOT NULL, PRIMARY KEY("Nom"));

CREATE TABLE "Combattant_Regle_sp"(
  id INTEGER NOT NULL,
  "Regles sp_Nom" TEXT NOT NULL,
  "Combattant_Nom" TEXT NOT NULL,
  PRIMARY KEY(id),
  CONSTRAINT "Regles sp_Combattant_Regle_sp"
    FOREIGN KEY ("Regles sp_Nom") REFERENCES "Regles sp" ("Nom"),
  CONSTRAINT "Combattant_Combattant_Regle_sp"
    FOREIGN KEY ("Combattant_Nom") REFERENCES "Combattant" ("Nom")
);

CREATE TABLE "Combattant_Armes"(
  id INTEGER NOT NULL,
  "Combattant_Nom" TEXT NOT NULL,
  "Armes_Nom" TEXT NOT NULL,
  PRIMARY KEY(id),
  CONSTRAINT "Combattant_Combattant_Armes"
    FOREIGN KEY ("Combattant_Nom") REFERENCES "Combattant" ("Nom"),
  CONSTRAINT "Armes_Combattant_Armes"
    FOREIGN KEY ("Armes_Nom") REFERENCES "Armes" ("Nom")
);
