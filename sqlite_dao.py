import sqlite3

from models import Produit, Client


class SQLiteDAO:

    def __init__(self):
        try:
            self.conn = sqlite3.connect("boutique.db")
            self.conn.row_factory = sqlite3.Row
            self.creer_tables()

            print("Connexion SQLite réussie.")

        except sqlite3.Error as e:
            print("Erreur SQLite :", e)
            raise

    # Création des tables
    def creer_tables(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prix REAL NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)

        self.conn.commit()

    # Ajouter un produit
    def ajouter_produit(self, produit):

        try:
            cursor = self.conn.cursor()

            cursor.execute("""
                INSERT INTO produits (nom, prix)
                VALUES (?, ?)
            """, (produit.nom, produit.prix))

            self.conn.commit()

            print("Produit ajouté avec succès.")

        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erreur lors de l'ajout du produit :", e)

    # Ajouter un client
    def ajouter_client(self, client):

        try:
            cursor = self.conn.cursor()

            cursor.execute("""
                INSERT INTO clients (nom, email)
                VALUES (?, ?)
            """, (client.nom, client.email))

            self.conn.commit()

            print("Client ajouté avec succès.")

        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erreur lors de l'ajout du client :", e)

    # Lister tous les produits
    def lister_produits(self):

        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM produits")

        lignes = cursor.fetchall()

        produits = []

        for ligne in lignes:
            produit = Produit(
                ligne["id"],
                ligne["nom"],
                ligne["prix"]
            )

            produits.append(produit)

        return produits

    # Lister tous les clients
    def lister_clients(self):

        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM clients")

        lignes = cursor.fetchall()

        clients = []

        for ligne in lignes:
            client = Client(
                ligne["id"],
                ligne["nom"],
                ligne["email"]
            )

            clients.append(client)

        return clients

    # Rechercher un client par email
    def rechercher_client(self, email):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM clients
            WHERE email = ?
        """, (email,))

        ligne = cursor.fetchone()

        if ligne is not None:
            return Client(
                ligne["id"],
                ligne["nom"],
                ligne["email"]
            )

        return None

    # Modifier le prix d'un produit
    def modifier_prix(self, id_produit, nouveau_prix):

        try:
            cursor = self.conn.cursor()

            cursor.execute("""
                UPDATE produits
                SET prix = ?
                WHERE id = ?
            """, (nouveau_prix, id_produit))

            self.conn.commit()

            if cursor.rowcount > 0:
                print("Prix modifié avec succès.")
            else:
                print("Produit introuvable.")

        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erreur lors de la modification :", e)

    # Fermer la connexion
    def fermer(self):
        if self.conn:
            self.conn.close()
            print("Connexion SQLite fermée.")