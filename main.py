
empty = 0
player_x = 1
player_o = 2

class Board():
    def __init__(self):
        self.grid = [0] * 9
        self.player = player_x # Variable de test pour savoir a quel joueur c'est

        print("===== Bienvenue dans le jeu du morpion =====")
        print("\n————— LES REGLES ————— : \n- Chacun son tour un joueur choisira une case sur laquelle poser sa croix ou son rond.\n- Pour sélectionner la case il devra taper un chiffre entre 1 et 9 en suivant la grille suivante :\n  1 | 2 | 3\n  —————————\n  4 | 5 | 6\n  —————————\n  7 | 8 | 9")
        print("- Le joueur 1 est celui qui a les X et le joueur 2 celui qui a les O.\n- En sélectionnant un numéro le joueur fera apparaitre son symbole sur la grille de jeu.")
        print("\n————— Le jeu commence —————")
        gagnant_trouve = False
        grille_pleine = False
        nb_joueur = 1
        while(not(gagnant_trouve) and not(grille_pleine)):
            print(f"\nC'est au joueur {nb_joueur} de joueur, grille actuelle : ")
            self.display()
            action = self.get_human_move()
            self.make_move(action, nb_joueur)
            gagnant_trouve = self.check_winner()
            grille_pleine = self.is_grid_full()
            nb_joueur = self.exchange_player(nb_joueur)
        if gagnant_trouve == True:
            nb_joueur = self.exchange_player(nb_joueur)
            print(f"Bravo au joueur {nb_joueur} pour avoir remporté la partie ! La grille est : ")
            self.display()
        else: 
            print("\n Match Nul : La grille est rempli et personne n'a gagné : ")
            self.display()
            
         


    def display(self): # Afficher la grille
        compteur_indice = 0               
        for i in range(3): # On boucle trois fois pour les 3 lignes 
            print(f"{self.afficher_croix_ou_rond(compteur_indice)} | {self.afficher_croix_ou_rond(compteur_indice+1)} | {self.afficher_croix_ou_rond(compteur_indice+2)}")
            print("—————————")
            compteur_indice += 3
        

    def afficher_croix_ou_rond(self, indice): # Savoir quoi afficher dans une case
        retour = ""
        if self.grid[indice] == empty: # donc égal à zéro :
            retour = " "
        elif self.grid[indice] == player_x: # donc égal à 1:
            retour = "X"
        elif self.grid[indice] == player_o: # donc égal à 2:
            retour = "O"
        
        return retour 


    def is_move_valid(self, case): # Vérifier si la case est bien vide
        retour = False
        if self.grid[case] == empty:
            retour = True
        return retour
    

    def get_human_move(self): # Demander une action et vérifier si le move est légal
        case_choisie = False
        retour = int
        while(not(case_choisie)):
            action_user = input("Sur quelle case souhaitez vous poser votre symbole ? Case : ")
            if action_user.isdigit():
                action = int(action_user) - 1
                if 0 <= action <= 8:
                    if self.is_move_valid(action):
                        retour = action
                        case_choisie = True
                    else: print("ERREUR : La case que vous avez choisie n'est pas vide !")
                else : print("ERREUR : Le nombre que vous avez entré n'est pas compris entre 1 et 9 !")
            
            else : print("ERREUR : Vous n'avez pas entré un nombre !")

        return retour
    

    def make_move(self, case_a_modif, player): # Modifier la liste de la grille
        if player == player_x:
            self.grid[case_a_modif] = player_x
        else : self.grid[case_a_modif] = player_o


    def is_grid_full(self): # Vérifer si la liste est rempli
        retour = True
        trouve = False
        i = 0
        while (not(trouve) and i < len(self.grid)):
            if self.grid[i] == 0:
                trouve = True
                retour = False
            i += 1
        return retour
                

    def check_winner(self): # Vérifier si un joueur gagne et renvoyer lequel c'est
        winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Les lignes
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Les colonnes
        [0, 4, 8], [2, 4, 6]]             # Les diagonales
        gagnant = None
        for combo in winning_combinations:
            element1_grille = self.grid[combo[0]]
            element2_grille = self.grid[combo[1]]
            element3_grille = self.grid[combo[2]]
            if element1_grille == element2_grille == element3_grille and element1_grille != 0:
                gagnant = element1_grille
        return gagnant

    def exchange_player(self, nb_joueur):
        if nb_joueur == 1: 
                nb_joueur = 2
        elif nb_joueur == 2: 
            nb_joueur = 1
        return nb_joueur
    
