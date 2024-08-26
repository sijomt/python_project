from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
from mysql.connector import Error
import time
import os

app = Flask(__name__, static_folder='.', static_url_path='')

def create_connection():
    connection = None
    for _ in range(10):
        try:
            connection = mysql.connector.connect(
                host="db",
                user="root",
                passwd="yourpassword",
                database="user_data"
            )
            print("Connection to MySQL DB successful")
            break
        except Error as e:
            print(f"The error '{e}' occurred")
            time.sleep(5)
    return connection

def execute_query(connection, query, data):
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/submit', methods=['POST'])
def submit_contact():
    data = request.json
    email = data['email']
    phone = data['phone']

    connection = create_connection()
    if connection is None:
        return jsonify({"success": False, "message": "Failed to connect to the database"})

    insert_contact_query = """
    INSERT INTO contacts (email, phone) VALUES (%s, %s)
    """
    execute_query(connection, insert_contact_query, (email, phone))
    connection.close()

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
