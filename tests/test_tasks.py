from datetime import date, timedelta


def test_create_task(client):
    response = client.post(
        '/user/createuser',
        json= {
            'name' : 'Ali',
            'email': 'ali@example.com',
            'password': '12345'
        }
    )
    assert response.status_code == 201
    response = client.post(
        '/task/create_task/1',
        json={
            'title' : 'Hello',
            'description': 'World',
            'status' : 'todo',
            'priority' : 'low',
            'due_date' : (date.today() + timedelta(days=1)).isoformat(),
            'user_id' : 1
        }
    )
    assert response.status_code == 201
    data = response.json()

    assert data['title'] == 'Hello'
    assert data['description'] == 'World'
    assert data['status'] == 'todo'
    assert data['priority'] == 'low'
    assert data['due_date'] == (date.today() + timedelta(days=1)).isoformat()
    assert data['user_id'] == 1
    assert 'id' in data
    assert 'create_at' in data
    assert 'update_at' in data
    
def test_create_task_user_not_found(client):
    response = client.post(
        '/user/createuser',
        json= {
            'name' : 'Ali',
            'email': 'ali@example.com',
            'password': '12345'
        }
    )
    assert response.status_code == 201
    response = client.post(
        '/task/create_task/999',
        json={
            'title' : 'Hello',
            'description': 'World',
            'status' : 'todo',
            'priority' : 'low',
            'due_date' : (date.today() + timedelta(days=1)).isoformat(),
            'user_id' : 1
        }
    )
    assert response.status_code == 404 

def test_create_task_owner_not_found(client):
    response = client.post(
        '/user/createuser',
        json= {
            'name' : 'Ali',
            'email': 'ali@example.com',
            'password': '12345'
        }
    )
    assert response.status_code == 201
    response = client.post(
        '/task/create_task/1',
        json={
            'title' : 'Hello',
            'description': 'World',
            'status' : 'todo',
            'priority' : 'low',
            'due_date' : (date.today() + timedelta(days=1)).isoformat(),
            'user_id' : 999
        }
    )
    assert response.status_code == 404 
    