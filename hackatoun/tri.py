

# la disponibilite de camion     un algorithme mathématique qui calcule 
# la somme des colis et comparer avec la capacité du camion si la capasite de camion est pas rempli est modifie par un requête sql sa statuts


import pandas as pd
import pymysql.cursors
from pulp import *

# Connexion à la base de données MySQL
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='saw',
                             cursorclass=pymysql.cursors.DictCursor)

# Récupération des données des camions
trucks_df = pd.read_sql_query("SELECT * FROM DeliveryTruck WHERE Status = 'Available'", connection)

# Récupération des données des colis
packages_df = pd.read_sql_query("SELECT * FROM Colis", connection)

# Capacité maximale du camion
truck_capacity = 1000  # Exemple, à remplacer par la capacité réelle

# Création du problème d'optimisation
prob = LpProblem("Optimization_Problem", LpMaximize)

# Variables
package_vars = LpVariable.dicts("Colis", packages_df['idColis'], 0, 1, LpBinary)
truck_var = LpVariable.dicts("Truck", trucks_df['TruckID'], 0, 1, LpBinary)

# Fonction objectif
prob += lpSum([package_vars[i] for i in packages_df['idColis']])

# Contraintes
for index, row in packages_df.iterrows():
    prob += lpSum(package_vars[row['idColis']]) <= truck_capacity * lpSum([truck_var[i] for i in trucks_df['TruckID']])

# Résolution du problème
prob.solve()

# Analyse de la solution
if LpStatus[prob.status] == "Optimal":
    print("Solution optimale trouvée.")
    # Modification du statut des camions
    for truck_id, var in truck_var.items():
        if var.value() == 1:
            # Mettre à jour le statut du camion dans la base de données
            cursor = connection.cursor()
            cursor.execute("UPDATE DeliveryTruck SET Status = 'Available' WHERE TruckID = %s", (truck_id,))
            connection.commit()
            cursor.close()
else:
    print("Aucune solution optimale trouvée.")

# Fermeture de la connexion à la base de données
connection.close()
