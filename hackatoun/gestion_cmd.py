
 #Gestion des commandes et des informations clients  il prend les info de client ces donnees et les detail de la commande 



import pymysql

class OrderManagement:
    def _init_(self, db_config):
       
        self.conn = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='saw',
                             cursorclass=pymysql.cursors.DictCursor)
      

    def add_order(self, client_id, order_date, status):
        query = 'INSERT INTO Order (ClientID, OrderDate, Status) VALUES (%s, %s, %s)'
        self.cursor.execute(query, (client_id, order_date, status))
        self.conn.commit()

    def get_orders_by_client(self, client_id):
        query = 'SELECT OrderID, OrderDate, Status FROM Order WHERE ClientID = %s'
        self.cursor.execute(query, (client_id,))
        return self.cursor.fetchall()

    def update_client_address(self, client_id, new_address):
        query = 'UPDATE Client SET Address = %s WHERE ClientID = %s'
        self.cursor.execute(query, (new_address, client_id))
        self.conn.commit()

    def get_all_clients(self):
        query = 'SELECT ClientID, Name, Address, PreferredTimeSlot FROM Client'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

# Usage example
if __name__ == '_main_':
    db_config = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'your_database_name'
    }
    om = OrderManagement(db_config)
    
    # Example operations
    om.add_order(client_id=1, order_date='2024-04-24', status='Pending')
    print("Orders for Client ID 1:", om.get_orders_by_client(client_id=1))
    om.update_client_address(client_id=1, new_address='456 New Address St')
    print("All clients:", om.get_all_clients())

    # Don't forget to close the connection when done
    om.close()