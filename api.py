from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Créer une connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="employees_db"
)

# Créer un curseur pour exécuter des requêtes
cursor = conn.cursor()

@app.route('/api/v1/employees', methods=['GET'])
def get_employees():
    # Exécuter une requête SELECT pour récupérer tous les employés
    cursor.execute("SELECT * FROM employees")
    result = cursor.fetchall()
    # Convertir le résultat en une liste de dictionnaires
    employees = []
    for row in result:
        employee = {"id": row[0], "first_name": row[1], "last_name": row[2], "email": row[3]}
        employees.append(employee)
    return jsonify(employees)

@app.route('/api/v1/employees', methods=['POST'])
def add_employee():
    employee = request.get_json()
    # Insérer les informations de l'employé dans la base de données
    sql = "INSERT INTO employees (first_name, last_name, email) VALUES (%s, %s, %s)"
    val = (employee['first_name'], employee['last_name'], employee['email'])
    cursor.execute(sql, val)
    conn.commit()
    return jsonify({"message": "Employee added successfully."}), 201

@app.route('/api/v1/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    # Récupérer les informations de l'employé à mettre à jour
    sql = "SELECT * FROM employees WHERE id = %s"
    val = (employee_id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        # Mettre à jour les informations de l'employé dans la base de données
        employee = request.get_json()
        sql = "UPDATE employees SET first_name = %s, last_name = %s, email = %s WHERE id = %s"
        val = (employee['first_name'], employee['last_name'], employee['email'], employee_id)
        cursor.execute(sql, val)
        conn.commit()
        return jsonify({"message": "Employee updated successfully."}), 200
    else:
        return jsonify({"message": "Employee not found."}), 404

@app.route('/api/v1/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    # Vérifier si l'employé existe dans la base de données
    sql = "SELECT * FROM employees WHERE id = %s"
    val = (employee_id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        # Supprimer l'employé de la base de données
        sql = "DELETE FROM employees WHERE id = %s"
        val = (employee_id,)
        cursor.execute(sql, val)
        conn.commit()
        return jsonify({"message": "Employee deleted successfully."}), 200
    else:
        return jsonify({"message": "Employee not found."}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8088, debug=True)
