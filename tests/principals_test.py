import pytest
from core.models.assignments import AssignmentStateEnum, GradeEnum

# Assuming h_principal is a fixture that provides the necessary headers for a principal
def test_get_principal_assignments(client, h_principal):
    response = client.get('/principal/assignments', headers=h_principal)
    assert response.status_code == 200
    assert 'data' in response.json

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED.value, AssignmentStateEnum.GRADED.value]

def test_get_teachers(client, h_principal):
    response = client.get('/principal/teachers', headers=h_principal)
    assert response.status_code == 200
    assert 'data' in response.json

def test_grade_assignment(client, h_principal):
    response = client.post('/principal/assignments/grade', json={'id': 1, 'grade': 'A'}, headers=h_principal)
    assert response.status_code == 200
    assert response.json['data']['grade'] == 'A'

def test_grade_assignment_draft_assignment(client, h_principal):
    """Failure case: If an assignment is in Draft state, it cannot be graded by principal"""
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 5, 'grade': GradeEnum.A.value},
        headers=h_principal
    )
    assert response.status_code == 400

def test_grade_existing_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 4, 'grade': GradeEnum.C.value},
        headers=h_principal
    )
    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C

def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 4, 'grade': GradeEnum.B.value},
        headers=h_principal
    )
    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B
