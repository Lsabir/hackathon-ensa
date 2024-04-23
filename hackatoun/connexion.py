# Étape 1: Importer la bibliothèque
import pymysql

# Étape 2: Établir une connexion à la base de données
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='saw',
    charset='utf8mb4')

# Étape 3: Créer un curseur
cur = conn.cursor()

# Étape 4: Exécuter une requête SQL
cur.execute("SELECT * FROM Client")

# Étape 5: Récupérer les résultats
rows = cur.fetchall()
for row in rows:
    print(row)

# Étape 6: Fermer le curseur et la connexion
cur.close()
conn.close()