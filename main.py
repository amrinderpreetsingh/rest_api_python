from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)


# Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200))
    position = db.Column(db.String(100))

    def __init__(self, name, email, position):
        self.name = name
        self.email = email
        self.position = position


# Employee Schema
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'position')


# Init schema
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


# Create an Employee
@app.route('/employee', methods=['POST'])
def add_employee():
    name = request.json['name']
    email = request.json['email']
    position = request.json['position']

    new_employee = Employee(name, email, position)

    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)


# Get All Employees
@app.route('/employee', methods=['GET'])
def get_employees():
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)
    return jsonify(result)


# Get Single Employee
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    return employee_schema.jsonify(employee)


# Update an Employee
@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)

    name = request.json['name']
    email = request.json['email']
    position = request.json['position']

    employee.name = name
    employee.email = email
    employee.position = position

    db.session.commit()

    return employee_schema.jsonify(employee)


# Delete Employee
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()

    return employee_schema.jsonify(employee)


# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
