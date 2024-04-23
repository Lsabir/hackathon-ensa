
#gps dans le camion il travail avec api de maps chaque 30s  il va faire un mise a jour a sa adresse de camion



import pymysql.cursors
import requests
import time

# Fonction pour récupérer les itinéraires en cours depuis la base de données
def get_current_itineraries(connection):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM Orders WHERE Status = 'In Progress'"
        cursor.execute(sql)
        itineraries = cursor.fetchall()
    return itineraries

# Fonction pour récupérer les destinations associées à un itinéraire
def get_destinations_for_itinerary(connection, itinerary_id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM Destination WHERE ItineraryID = %s"
        cursor.execute(sql, (itinerary_id,))
        destinations = cursor.fetchall()
    return destinations

# Fonction pour récupérer les coordonnées GPS d'une adresse via une API de géocodage
def get_coordinates(address):
    api_key = 'YOUR_MAPBOX_API_KEY'
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json?access_token={api_key}"
    response = requests.get(url)
    data = response.json()
    coordinates = data['features'][0]['geometry']['coordinates']
    return coordinates

# Fonction pour afficher les itinéraires et les positions des camions sur une carte
def display_truck_positions(itineraries):
    for itinerary in itineraries:
        print(f"Itinéraire {itinerary['ItineraryID']}, camion {itinerary['TruckID']}")
        destinations = get_destinations_for_itinerary(connection, itinerary['ItineraryID'])
        for destination in destinations:
            coordinates = get_coordinates(destination['Address'])
            print(f"Destination : {destination['Address']}, Coordonnées GPS : {coordinates}")
        print()

# Connexion à la base de données MySQL
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='saw',
                             cursorclass=pymysql.cursors.DictCursor)

# Boucle de suivi en temps réel
while True:
    # Récupération des itinéraires en cours depuis la base de données
    itineraries = get_current_itineraries(connection)

    # Affichage des itinéraires et des positions des camions
    display_truck_positions(itineraries)

    # Attente avant la prochaine mise à jour (par exemple, toutes les 30 secondes)
    time.sleep(30)

# Fermeture de la connexion à la base de données
connection.close()