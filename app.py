
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///itsm.db'
db = SQLAlchemy(app)

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/incidents', methods=['GET'])
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([{
        'id': i.id,
        'title': i.title,
        'description': i.description,
        'priority': i.priority,
        'status': i.status,
        'created_at': i.created_at.isoformat()
    } for i in incidents])

@app.route('/api/incidents', methods=['POST'])
def create_incident():
    data = request.json
    incident = Incident(
        title=data['title'],
        description=data['description'],
        priority=data['priority']
    )
    db.session.add(incident)
    db.session.commit()
    return jsonify({'message': 'Incident created', 'id': incident.id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
