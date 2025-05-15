from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'personas_db')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Ruta para crear una nueva persona
@app.route('/personas', methods=['POST'])
def add_persona():
    try:
        data = request.get_json()
        nombre = data['nombre']
        apellido = data['apellido']
        cedula = data['cedula']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO personas (nombre, apellido, cedula) VALUES (%s, %s, %s)", 
                    (nombre, apellido, cedula))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({'message': 'Persona agregada correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta para obtener todas las personas
@app.route('/personas', methods=['GET'])
def get_personas():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM personas")
        personas = cur.fetchall()
        cur.close()
        
        return jsonify(personas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener una persona por cédula
@app.route('/personas/<cedula>', methods=['GET'])
def get_persona(cedula):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM personas WHERE cedula = %s", (cedula,))
        persona = cur.fetchone()
        cur.close()
        
        if persona:
            return jsonify(persona), 200
        else:
            return jsonify({'message': 'Persona no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar una persona
@app.route('/personas/<cedula>', methods=['PUT'])
def update_persona(cedula):
    try:
        data = request.get_json()
        nombre = data['nombre']
        apellido = data['apellido']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE personas SET nombre = %s, apellido = %s WHERE cedula = %s", 
                    (nombre, apellido, cedula))
        mysql.connection.commit()
        affected_rows = cur.rowcount
        cur.close()
        
        if affected_rows == 0:
            return jsonify({'message': 'Persona no encontrada'}), 404
        return jsonify({'message': 'Persona actualizada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar una persona
@app.route('/personas/<cedula>', methods=['DELETE'])
def delete_persona(cedula):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM personas WHERE cedula = %s", (cedula,))
        mysql.connection.commit()
        affected_rows = cur.rowcount
        cur.close()
        
        if affected_rows == 0:
            return jsonify({'message': 'Persona no encontrada'}), 404
        return jsonify({'message': 'Persona eliminada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)