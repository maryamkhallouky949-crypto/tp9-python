import mysql.connector
from mysql.connector import Error

from models import Produit, Client


class MySQLDAO:

    def __init__(self):

        self.conn = None

        try:
            # Connexion au serveur MySQL
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""
            )

            cursor = self.conn.cursor()

            # Création de la base
            cursor.execute(
                "CREATE DATABASE IF NOT EXISTS boutique"
            )

            cursor.close()

            # Sélection de la base boutique
            self.conn.database = "boutique"

            self.creer_tables()

            print("Connexion MySQL réussie.")

        except Error as e:
            print("Erreur de connexion MySQL :", e)

            if self.conn is not None and self.conn.is_connected():
                self.conn.close()

            raise

    # Création des tables
    def creer_tables(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(100) NOT NULL,
                prix DECIMAL(10,2) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE
            )
        """)

        self.conn.commit()
        cursor.close()

    # Ajouter un produit
    def ajouter_produit(self, produit):

        try:
            cursor = self.conn.cursor()

            cursor.execute("""
                INSERT INTO produits (nom, prix)
                VALUES (%s, %s)
            """, (produit.nom, produit.prix))

            self.conn.commit()

            print("Produit ajouté avec succès.")

            cursor.close()

        except Error as e:
            self.conn.rollback()
            print("Erreur lors de l'ajout du produit :", e)

    # Ajouter un client
    def ajouter_client(self, client):

        try:
            cursor = self.conn.cursor()

            cursor.execute("""
                INSERT INTO clients (nom, email)
                VALUES (%s, %s)
            """, (client.nom, client.email))

            self.conn.commit()

            print("Client ajouté avec succès.")

            cursor.close()

        except Error as e:
            self.conn.rollback()
            print("Erreur lors de l'ajout du client :", e)

    # Lister les produits
    def lister_produits(self):

        cursor = self.conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM produits")

        lignes = cursor.fetchall()

        produits = []

        for ligne in lignes:
            produit = Produit(
                ligne["id"],
                ligne["nom"],
                float(ligne["prix"])
            )

            produits.append(produit)

        cursor.close()

        return produits

    # Lister les clients
    def lister_clients(self):

        cursor = self.conn.cursor(dictionary=True)

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

        cursor.close()

        return clients

    # Rechercher un client par email
    def rechercher_client(self, email):

        cursor = self.conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM clients
            WHERE email = %s
        """, (email,))

        ligne = cursor.fetchone()

        cursor.close()

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
                SET prix = %s
                WHERE id = %s
            """, (nouveau_prix, id_produit))

            self.conn.commit()

            if cursor.rowcount > 0:
                print("Prix modifié avec succès.")
            else:
                print("Produit introuvable.")

            cursor.close()

        except Error as e:
            self.conn.rollback()
            print("Erreur lors de la modification :", e)

    # Fermer la connexion
    def fermer(self):

        if self.conn is not None and self.conn.is_connected():
            self.conn.close()
            print("Connexion MySQL fermée.")