



# Les contraintes du problème sont ajoutées. Chaque destination doit être visitée une seule fois et la capacité de chaque camion ne doit pas être dépassée.


#systeme liniere
# Chaque destination est visitée une seule fois
# Capacité du camion





import pymysql.cursors
from pulp import *

# Connexion à la base de données MySQL
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='saw',
                             cursorclass=pymysql.cursors.DictCursor)

# Récupération des données depuis la base de données
with connection.cursor() as cursor:
    # Récupération des destinations
    sql = "SELECT * FROM Destination"
    cursor.execute(sql)
    destinations = cursor.fetchall()

    # Récupération des camions
    sql = "SELECT * FROM DeliveryTruck"
    cursor.execute(sql)
    trucks = cursor.fetchall()

# Fermeture de la connexion à la base de données
connection.close()

# Création du problème de minimisation
prob = LpProblem("Vehicle_Routing_Problem", LpMinimize)

# Variables de décision
x = LpVariable.dicts("Route", [(dest['DestinationID'], truck['TruckID']) for dest in destinations for truck in trucks], 0, 1, LpBinary)

# Fonction objectif
prob += lpSum([dist * x[(dest['DestinationID'], truck['TruckID'])] for dest, dist in zip(destinations, [100, 150]) for truck in trucks])

# Contraintes
for dest in destinations:
    prob += lpSum([x[(dest['DestinationID'], truck['TruckID'])] for truck in trucks]) == 1  # Chaque destination est visitée une seule fois

for truck in trucks:
    prob += lpSum([x[(dest['DestinationID'], truck['TruckID'])] for dest in destinations]) <= 1  # Capacité du camion

# Résolution du problème
prob.solve()

# Affichage des résultats
print("Status:", LpStatus[prob.status])
print("Total Distance:", value(prob.objective))
for v in prob.variables():
    if v.varValue == 1:
        print(v.name, "=", v.varValue)