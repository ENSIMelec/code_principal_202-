import tkinter as tk


class Application:
    def __init__(self, master):
        self.master = master
        master.title("Comptage de points")

        self.score_label = tk.Label(master, text="Score actuel : 0")
        self.score_label.pack()

        self.calculs_intermediaires_label = tk.Label(master, text="")
        self.calculs_intermediaires_label.pack()

    def mettre_a_jour_score(self, nouveau_score, calcul_intermediaire):
        self.score_label.config(text="Score actuel : " + str(nouveau_score))
        self.calculs_intermediaires_label.config(text=calcul_intermediaire)


class Affichage:
    @staticmethod
    def mettre_a_jour(score, calcul_intermediaire):
        app.mettre_a_jour_score(score, calcul_intermediaire)


class comptage_pts:
    def __init__(self):
        self.score = 0
        self.calculs_intermediaires = ""

    def pts_plante_jardiniere(self, nombre_plantes):
        points_plante_jardiniere = nombre_plantes * 4
        self.score += points_plante_jardiniere
        self.calculs_intermediaires += f"Ajout de {points_plante_jardiniere} points pour {nombre_plantes} plantes dans la jardinière\n"
        Affichage.mettre_a_jour(self.score, self.calculs_intermediaires)

    def pts_panneau_solaire(self, nombre_panneaux):
        points_panneau_solaire = nombre_panneaux * 5
        self.score += points_panneau_solaire
        self.calculs_intermediaires += f"Ajout de {points_panneau_solaire} points pour {nombre_panneaux} panneaux solaires\n"
        Affichage.mettre_a_jour(self.score, self.calculs_intermediaires)

    def pts_plante_violet_zone(self, nombre_plantes_violet):
        points_plante_violet_zone = nombre_plantes_violet * 3 
        self.score += points_plante_violet_zone
        self.calculs_intermediaires += f"Ajout de {points_plante_violet_zone} points pour {nombre_plantes_violet} panneaux solaires\n"
        Affichage.mettre_a_jour(self.score, self.calculs_intermediaires)

    def pts_zone_finale(self):
        points_zone_finale =  10  
        self.score += points_zone_finale
        self.calculs_intermediaires += f"Ajout de {points_zone_finale} points pour zone finale\n"
        Affichage.mettre_a_jour(self.score, self.calculs_intermediaires)


# Initialisation de Tkinter
root = tk.Tk()

# Création de l'application
app = Application(root)

# Exemple d'utilisation
comptage = ComptagePoints()
comptage.pts_panneau_solaire(4)
comptage.pts_plante_jardiniere(3)
comptage.pts_plante_violet_zone(2)
comptage.pts_zone_finale()

# Lancement de la boucle principale de Tkinter
root.mainloop()