from models import Produit, Client
from sqlite_dao import SQLiteDAO


def afficher_menu():

    print("\n========== MENU BOUTIQUE ==========")
    print("1. Ajouter un produit")
    print("2. Ajouter un client")
    print("3. Lister les produits")
    print("4. Lister les clients")
    print("5. Rechercher un client par email")
    print("6. Modifier le prix d'un produit")
    print("0. Quitter")
    print("==================================")


def main():

    print("===== CHOIX DE LA BASE DE DONNEES =====")
    print("1. SQLite")
    print("2. MySQL")

    choix = input("Votre choix : ")

    if choix == "1":

        dao = SQLiteDAO()

    elif choix == "2":

        try:
            from mysql_dao import MySQLDAO
            dao = MySQLDAO()

        except Exception:
            print("Impossible de se connecter à MySQL.")
            return

    else:
        print("Choix invalide.")
        return

    try:

        while True:

            afficher_menu()

            choix = input("Choisissez une opération : ")

            # Ajouter un produit
            if choix == "1":

                nom = input("Nom du produit : ")

                try:
                    prix = float(input("Prix du produit : "))

                    if prix < 0:
                        print("Le prix ne peut pas être négatif.")
                        continue

                except ValueError:
                    print("Veuillez saisir un prix valide.")
                    continue

                produit = Produit(None, nom, prix)

                dao.ajouter_produit(produit)

            # Ajouter un client
            elif choix == "2":

                nom = input("Nom du client : ")
                email = input("Email du client : ")

                if "@" not in email or "." not in email:
                    print("Adresse email invalide.")
                    continue

                client = Client(None, nom, email)

                dao.ajouter_client(client)

            # Lister les produits
            elif choix == "3":

                print("\n===== LISTE DES PRODUITS =====")

                produits = dao.lister_produits()

                if len(produits) == 0:
                    print("Aucun produit.")

                for produit in produits:
                    print(produit)

            # Lister les clients
            elif choix == "4":

                print("\n===== LISTE DES CLIENTS =====")

                clients = dao.lister_clients()

                if len(clients) == 0:
                    print("Aucun client.")

                for client in clients:
                    print(client)

            # Rechercher un client
            elif choix == "5":

                email = input("Entrez l'email recherché : ")

                client = dao.rechercher_client(email)

                if client is not None:
                    print("Client trouvé :")
                    print(client)

                else:
                    print("Aucun client trouvé.")

            # Modifier le prix
            elif choix == "6":

                try:
                    id_produit = int(
                        input("ID du produit : ")
                    )

                    nouveau_prix = float(
                        input("Nouveau prix : ")
                    )

                    if nouveau_prix < 0:
                        print("Le prix ne peut pas être négatif.")
                        continue

                    dao.modifier_prix(
                        id_produit,
                        nouveau_prix
                    )

                except ValueError:
                    print("Veuillez saisir des valeurs numériques.")

            # Quitter
            elif choix == "0":

                print("Fermeture de l'application.")
                break

            else:
                print("Choix invalide.")

    finally:
        dao.fermer()


if __name__ == "__main__":
    main()