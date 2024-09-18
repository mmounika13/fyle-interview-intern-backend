from flask import Blueprint, jsonify, request
from models import Assignment, Teacher, db

principal_blueprint = Blueprint('principal', __name__)

@principal_blueprint.route('/assignments', methods=['GET'])
def get_principal_assignments():
    assignments = Assignment.query.filter(
        (Assignment.state == 'SUBMITTED') | (Assignment.state == 'GRADED')
    ).all()
    return jsonify(data=[assignment.to_dict() for assignment in assignments]), 200

@principal_blueprint.route('/teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify(data=[teacher.to_dict() for teacher in teachers]), 200

@principal_blueprint.route('/assignments/grade', methods=['POST'])
def grade_assignment():
    data = request.get_json()
    assignment = Assignment.query.get(data['id'])
    
    if not assignment:
        return jsonify(error="Assignment not found"), 404

    assignment.grade = data['grade']
    assignment.state = 'GRADED'
    db.session.commit()
    
    return jsonify(data=assignment.to_dict()), 200
