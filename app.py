import os
import sys
import logging
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# DB URI: default to sqlite for local testing; production set DB_URI env to RDS connection string
DB_URI = os.environ.get('DB_URI', 'sqlite:///employee.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Prometheus counters
REQUEST_COUNT = Counter('employee_app_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(80))
    salary = db.Column(db.Float)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'role': self.role, 'salary': self.salary}

@app.route('/')
def home():
    employees = Employee.query.all()
    REQUEST_COUNT.labels(method='GET', endpoint='/', http_status='200').inc()
    return render_template('employees.html', employees=employees)

@app.route('/api/employees', methods=['GET'])
def get_employees():
    employees = [e.to_dict() for e in Employee.query.all()]
    REQUEST_COUNT.labels(method='GET', endpoint='/api/employees', http_status='200').inc()
    return jsonify(employees), 200

@app.route('/api/employees', methods=['POST'])
def add_employee():
    data = request.get_json() or request.form
    e = Employee(name=data.get('name'), role=data.get('role'), salary=float(data.get('salary', 0)))
    db.session.add(e)
    db.session.commit()
    REQUEST_COUNT.labels(method='POST', endpoint='/api/employees', http_status='201').inc()
    logger.info("Added employee %s", e.name)
    return jsonify(e.to_dict()), 201

@app.route('/api/employees/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    data = request.get_json()
    e = Employee.query.get_or_404(emp_id)
    e.name = data.get('name', e.name)
    e.role = data.get('role', e.role)
    e.salary = float(data.get('salary', e.salary))
    db.session.commit()
    REQUEST_COUNT.labels(method='PUT', endpoint='/api/employees/<id>', http_status='200').inc()
    return jsonify(e.to_dict()), 200

@app.route('/api/employees/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    e = Employee.query.get_or_404(emp_id)
    db.session.delete(e)
    db.session.commit()
    REQUEST_COUNT.labels(method='DELETE', endpoint='/api/employees/<id>', http_status='204').inc()
    return '', 204

@app.route('/health')
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health', http_status='200').inc()
    return 'OK', 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
