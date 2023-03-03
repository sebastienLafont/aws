from os import name
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector


app = Flask(__name__)
CORS(app)



# Créer une connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="employees_db"
)

# Créer un curseur pour exécuter des requêtes
cursor = conn.cursor()
@ app.route('/', methods=['GET'])
def get_raouf():
     return 'hello Sebastien'

@app.route('/api/v1/employees', methods=['GET'])
def get_employees():
    # Exécuter une requête SELECT pour récupérer tous les employés
    cursor.execute("SELECT * FROM employees")
    result = cursor.fetchall()
    # Convertir le résultat en une liste de dictionnaires
    employees = []
    for row in result:
        employee = {"id": row[0], "firstName": row[1], "lastName": row[2], "emailId": row[3]}
        employees.append(employee)
        
     

@app.route('/api/v1/employees', methods=['POST'])
def add_employee():
    employee = request.get_json()
    firstName = employee['firstName']
    lastName = employee['lastName']
    emailId = employee['emailId']

    # Exécuter une requête INSERT pour ajouter l'employé dans la base de données
    sql = "INSERT INTO employees (firstName, lastName, emailId) VALUES (%s, %s, %s)"
    values = (firstName, lastName, emailId)
    cursor.execute(sql, values)
    conn.commit()

    return jsonify({"message": "Employee added successfully."}), 201


@app.route('/api/v1/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    # Récupérer les données de l'employé depuis la requête HTTP
    employee = request.get_json()
    firstName = employee['firstName']
    lastName = employee['lastName']
    emailId = employee['emailId']

    # Exécuter une requête UPDATE pour modifier l'employé dans la base de données
    sql = "UPDATE employees SET firstName = %s, lastName = %s, emailId = %s WHERE id = %s"
    values = (firstName, lastName, emailId, employee_id)
    cursor.execute(sql, values)
    conn.commit()

    return jsonify({"message": "Employee updated successfully."}), 200

@app.route('/api/v1/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    # Exécuter une requête DELETE pour supprimer l'employé de la base de données
    sql = "DELETE FROM employees WHERE id = %s"
    values = (employee_id,)
    cursor.execute(sql, values)
    conn.commit()

    return jsonify({"message": "Employee deleted successfully."}), 200

if name == 'main':
    app.run(host='0.0.0.0', port=8082, debug=True)
