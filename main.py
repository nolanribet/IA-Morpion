import pickle
import os
import random
import time

empty = 0
player_x = 1
player_o = 2

class Board():
    def __init__(self):
        self.grid = [0] * 9       

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
    
    def moves_possible(self):
        liste_possible = []
        for i in range(len(self.grid)):
            if self.grid[i] == 0:
                liste_possible.append(i)
        return liste_possible
    

    def reset(self):
        self.grid = [0] * 9


class Agent():
    def __init__(self):
        self.alpha = 0.1 # Vitesse d'apprentissage : gère si l'IA préfère se conforter dans ces connaissances ou si elle veut en apprendre plus
        self.gamma = 0.9 # Facteur de réduction : gère la vision à long terme ou la récompense instantanée
        self.epsilon = 0.1 # Probabilité d'exploration
        self.q_table = {}
        self.symbol = ''

    def get_q_values(self, state): # Permettre à l'IA de lire le plateau
        state_tuple = tuple(state)
        if state_tuple not in self.q_table: # Si l'IA n'a jamais vu ce plateau, elle l'ajoute à sa liste de plateau
            self.q_table[state_tuple] = [0.0] * 9 # Par défaut on mets la note de 0 car on ne sait pas si le coup va être bien ou pas
        return self.q_table[state_tuple]

    def choose_action(self, board):
        vides = board.moves_possible()
        if not vides: # Sécurité dans le cas ou la liste serait pleine (pas censé arriver)
            return None
        # Gestion entre exploration et exploitation des connaissances 
        if random.random() < self.epsilon: # Cas d'exploration (on gère si on explore ou pas en générant un nombre aléatoire entre 0 et 1 et en regardant si il est inférieur a notre epsilon alors on explore)
            return random.choice(vides)
        else: # Cas d'exploitation des données 
            q_values = self.get_q_values(board.grid)
            meilleur_score = -float('inf') # On initialise avec - infini et pas zéro car le score de l'ia peut être de -1 en cas de défaite
            meilleur_coup = vides[0] # On initialise un meilleur coup
            for coup in vides: # Pour chaque case vide de la grille, on regarde son score dans la liste de mémoire  
                score = q_values[coup] # On récupère le score du coup
                if score > meilleur_score: # On compare si le score du nouveau coup est supérieur au meilleur score qu'on avait trouvé jusque la   
                    meilleur_score = score
                    meilleur_coup = coup
            return meilleur_coup # On renvoie l'index du coup avec le meilleur score
        

    def learn(self, state, action, reward, next_state):
        q_values = self.get_q_values(state) # On récupère les notes actuelles pour la situation
        next_q_values = self.get_q_values(next_state) # On regarde les possibilités
        meilleur_futur = max(next_q_values) # On garde la meilleure possibilité 
        target = reward + self.gamma * meilleur_futur # Deux parties : le reward qui est la récompense immédiate selon l'action faite, le gamma * meilleur_futur qui prend en compte le futur et calcule si ce coup peut être avantageux à l'avenir
        ancien_score = q_values[action] # On regarde le score que l'IA donnait au coup avant de le jouer  
        nouveau_score = ancien_score + self.alpha * (target - ancien_score) # target - ancien_score = l'écart entre la réalité et ce qu'avais prévu l'IA, le self.alpha sert à savoir si l'IA oublie tout ce qu'elle savait quand elle voit que cette action marche ou si elle garde en mémoire les anciennes.
        self.q_table[tuple(state)][action] = nouveau_score # On donne au tableau d'actions de l'IA le nouveau score pour affiner et la faire apprendre. On rempli donc la case de notre tableau correspondant à cette case de ce plateau


    def save_q_table(self, nom_fichier="ia_memoire.pkl"):
        with open(nom_fichier, "wb") as f:
            pickle.dump(self.q_table, f)
        print(f"Mémoire sauvegardé dans {nom_fichier} ({len(self.q_table)} états connues).")

    def load_q_table(self, nom_fichier="ia_memoire.pkl"):
        if os.path.exists(nom_fichier):
            with open(nom_fichier, "rb") as f:
                self.q_table = pickle.load(f)
            print(f"Mémoire chargée ! L'IA se souvient de {len(self.q_table)} situations.")
        else : print("Aucune mémoire trouvée. L'IA commence de zéro.")






def jouer_jcj(grille):
    grille.reset()
    print("===== Bienvenue dans le jeu du morpion =====")
    print("\n————— LES REGLES ————— : \n- Chacun son tour un joueur choisira une case sur laquelle poser sa croix ou son rond.\n- Pour sélectionner la case il devra taper un chiffre entre 1 et 9 en suivant la grille suivante :\n  1 | 2 | 3\n  —————————\n  4 | 5 | 6\n  —————————\n  7 | 8 | 9")
    print("- Le joueur 1 est celui qui a les X et le joueur 2 celui qui a les O.\n- En sélectionnant un numéro le joueur fera apparaitre son symbole sur la grille de jeu.")
    print("\n————— Le jeu commence —————")
    gagnant_trouve = False
    grille_pleine = False
    nb_joueur = 1
    while(not(gagnant_trouve) and not(grille_pleine)):
        print(f"\nC'est au joueur {nb_joueur} de joueur, grille actuelle : ")
        grille.display()
        action = grille.get_human_move()
        grille.make_move(action, nb_joueur)
        gagnant_trouve = grille.check_winner()
        grille_pleine = grille.is_grid_full()
        nb_joueur = grille.exchange_player(nb_joueur)
        if gagnant_trouve:
            nb_joueur = grille.exchange_player(nb_joueur)
            print(f"\n=== Bravo au joueur {nb_joueur} pour avoir remporté la partie ! La grille est : ")
            grille.display()
        else: 
            print("\n=== Match Nul : La grille est rempli et personne n'a gagné : ")
            grille.display()

def jouer_jcia(grille, agent_ia):
    grille.reset()
    # On désactive l'exploration pour que l'IA soit sérieuse
    old_epsilon = agent_ia.epsilon
    agent_ia.epsilon = 0 
    
    print("Vous êtes les O, l'IA est les X.")
    while True:
        # Tour Humain (X)
        grille.display()
        move = grille.get_human_move()
        grille.make_move(move, player_x)
        
        if grille.check_winner() == player_x:
            grille.display(); print("Vous avez battu l'IA !"); break
        if grille.is_grid_full():
            grille.display(); print("Match nul !"); break
            
        # Tour IA (O)
        print("L'IA réfléchit...")
        time.sleep(0.5)
        move_ia = agent_ia.choose_action(grille)
        grille.make_move(move_ia, player_o)
        
        if grille.check_winner() == player_o:
            grille.display(); print("L'IA a gagné !"); break
        if grille.is_grid_full():
            grille.display(); print("Match nul !"); break
    
    agent_ia.epsilon = old_epsilon # On remet l'epsilon d'origine

def jouer_ia_commence(grille, agent_ia):
    grille.reset()
    # On désactive l'exploration pour que l'IA soit au maximum de ses capacités
    old_epsilon = agent_ia.epsilon
    agent_ia.epsilon = 0 
    
    print("\nL'IA commence (elle est les X), vous êtes les O.")
    
    while True:
        # --- Tour IA (X) ---
        print("L'IA réfléchit...")
        time.sleep(0.5)
        # Ici l'IA utilise ses connaissances de "X" (ax)
        move_ia = agent_ia.choose_action(grille)
        grille.make_move(move_ia, player_x)
        
        if grille.check_winner() == player_x:
            grille.display()
            print("L'IA a gagné ! Elle est devenue trop forte...")
            break
        if grille.is_grid_full():
            grille.display()
            print("Match nul ! C'est déjà une victoire contre cette IA.")
            break
            
        # --- Tour Humain (O) ---
        grille.display()
        print("À vous de jouer (O) :")
        move = grille.get_human_move()
        grille.make_move(move, player_o)
        
        if grille.check_winner() == player_o:
            grille.display()
            print("Incroyable ! Vous avez battu l'IA alors qu'elle commençait !")
            break
        if grille.is_grid_full():
            grille.display()
            print("Match nul !")
            break
            
    agent_ia.epsilon = old_epsilon # On restaure l'epsilon

def entrainer_ia(grille, agent_x, agent_o, nb):
    attente_entre_tours = 1.5
    print(f"\nLancement de l'entraînement pour {nb} parties...")
    
    for i in range(nb):
        grille.reset()
        last_x, last_a_x = None, None
        last_o, last_a_o = None, None
        game_over = False
        
        visible = (i % 10 == 0 and i != 0)
        # visible = False
        
        if visible:
            print(f"\n{'='*20}")
            print(f"MATCH DE DÉMO : PARTIE n°{i}")
            print(f"{'='*20}")

        while not game_over:
            # TOUR X
            s_x = list(grille.grid)
            a_x = agent_x.choose_action(grille)
            grille.make_move(a_x, player_x)
            n_s_x = list(grille.grid)
            
            if visible:
                print("\nAgent X joue :")
                grille.display()
                time.sleep(attente_entre_tours)
            
            winner = grille.check_winner()
            if winner == player_x:
                agent_x.learn(s_x, a_x, 1, n_s_x)
                if last_o: agent_o.learn(last_o, last_a_o, -1, n_s_x)
                if visible: print("VICTOIRE DE L'AGENT X !"); print("-" * 20)
                game_over = True
            elif grille.is_grid_full():
                agent_x.learn(s_x, a_x, 0.5, n_s_x)
                if last_o: agent_o.learn(last_o, last_a_o, 0.5, n_s_x)
                if visible: print("MATCH NUL !"); print("-" * 20)
                game_over = True
            else:
                if last_o: agent_o.learn(last_o, last_a_o, 0, n_s_x)
                last_x, last_a_x = s_x, a_x
                
                # TOUR O
                if not game_over:
                    s_o = list(grille.grid)
                    a_o = agent_o.choose_action(grille)
                    grille.make_move(a_o, player_o)
                    n_s_o = list(grille.grid)
                    
                    if visible:
                        print("\nAgent O joue :")
                        grille.display()
                        time.sleep(attente_entre_tours)
                    
                    winner = grille.check_winner()
                    if winner == player_o:
                        agent_o.learn(s_o, a_o, 1, n_s_o)
                        agent_x.learn(last_x, last_a_x, -1, n_s_o)
                        if visible: print("VICTOIRE DE L'AGENT O !"); print("-" * 20)
                        game_over = True
                    elif grille.is_grid_full():
                        agent_o.learn(s_o, a_o, 0.5, n_s_o)
                        agent_x.learn(last_x, last_a_x, 0.5, n_s_o)
                        if visible: print("MATCH NUL !"); print("-" * 20)
                        game_over = True
                    else:
                        agent_x.learn(last_x, last_a_x, 0, n_s_o)
                        last_o, last_a_o = s_o, a_o

        if i % 500000 == 0 and i != 0:
            print(f"Progrès : {i}/{nb} parties (Mémoire X: {len(agent_x.q_table)} situations)")

    print(f"\nEntraînement terminé ! Les agents ont appris : Mémoire X = {len(agent_x.q_table)}, Mémoire O : {len(agent_o.q_table)}.")

def menu():
    board = Board()
    ax = Agent()
    ao = Agent()
    ax.load_q_table("agent_x.pkl")
    ao.load_q_table("agent_o.pkl")

    while True:
        print("\n--- MENU MORPION IA ---")
        print("1. Joueur vs Joueur")
        print("2. Joueur (X) vs IA (O)")
        print("3. Joueur (O) vs IA (X) mais IA commence")
        print("4. Entraîner l'IA (IA vs IA)")
        print("5. Sauvegarder et Quitter")
        
        c = input("Choix : ")
        if c == "1": jouer_jcj(board)
        elif c == "2": jouer_jcia(board, ao)
        elif c == "3": jouer_ia_commence(board, ao)
        elif c == "4":
            n = int(input("Combien de parties ? "))
            entrainer_ia(board, ax, ao, n)
        elif c == "5":
            ax.save_q_table("agent_x.pkl")
            ao.save_q_table("agent_o.pkl")
            break


menu()