def test_create_user(client):
    response = client.post(
        '/user/createuser',
        json= {
            'name' : 'Ali',
            'email': 'ali@example.com',
            'password': '12345'
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Ali'
    assert data['email'] == 'ali@example.com'
    assert 'id' in data
    assert 'create_at' in data
    
def test_get_all_users(client):
    client.post(
            '/user/createuser',
        json= {
            'name' : 'Ali',
            'email': 'ali@example.com',
            'password': '12345'
        }
    )
    client.post(
            '/user/createuser',
            json= {
                'name' : 'Hassan',
                'email': 'hassan@example.com',
                'password': '12345'
            }
        )
    response = client.get('/user/users')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['name'] == 'Ali'
    assert data[1]['name'] == 'Hassan'

def test_get_user_by_id(client):
    response = client.post(
        '/user/createuser',
        json= {
            'name' : 'Ali',
            'email': 'ali@example.com',
            'password': '12345'
        }
    )
    user_id = response.json()["id"]
    response = client.get(f'/user/users/{user_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == user_id
    assert data['name'] == 'Ali'
    assert data['email']=='ali@example.com'
    
def test_get_user_not_found(client):
    response = client.get('/user/users/999')
    assert response.status_code == 404
    assert response.json() == {
        'detail' : 'User Not Found'
    }
    
def test_update_user(client):
    response = client.post(
        'user/createuser',
        json= {
            'name' : 'Ali',
            'email': 'ali@example.com',
            'password': '12345'
        }
    )
    assert response.status_code == 201
    user_id = response.json()['id']
    response = client.put(
        f'user/users/{user_id}',
        json={
            'name' : 'Ali Updated',
            'email' : 'ali.updated@gmail.com',
            'password': '12345'
        }
    )
    assert response.status_code == 200
    assert response.json() == f'User {user_id} Updated Successfully'
    response = client.get(f'user/users/{user_id}')
    assert response.json()['name'] == 'Ali Updated'
    assert response.json()['email'] == 'ali.updated@gmail.com'
    
def test_update_user_not_found(client):
    response = client.put(
        'user/users/999',
        json= {
            'name' : 'Ali',
            'email': 'ali@example.com',
            'password': '12345'
        }
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "User Not Found"
    }
        
def test_delete_user(client):
    response = client.post(
        '/user/createuser',
        json= {
            'name' : 'Ali',
            'email': 'ali@example.com',
            'password': '12345'
        }
    )
    assert response.status_code == 201
    user_id = response.json()['id']
    response = client.delete(f'/user/users/{user_id}')
    assert response.status_code == 200
    assert response.json() == f'User {user_id} Deleted Successfully'
    response = client.get(f'user/users/{user_id}')
    assert response.status_code == 404
    assert response.json() == {
        'detail' : 'User Not Found'
    }

def test_delete_user_not_found(client):
    response = client.delete('user/users/999')
    assert response.status_code == 404
    assert response.json() == {
        "detail": "User Not Found"
    }
    
def test_create_user_invalid_email(client):
    response = client.post(
        '/user/createuser',
        json= {
            'name' : 'Ali',
            'email': 'ali.example.com',
            'password': '12345'
        }
    )
    assert response.status_code == 422
    
def test_create_user_empty_name(client):
    response = client.post(
        '/user/createuser',
        json= {
            'name' : '',
            'email': 'ali@example.com',
            'password': '12345'
        }
    )
    assert response.status_code == 422
    
def test_create_user_duplicate_email(client):
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
        '/user/createuser',
        json={
            'name' : 'Hassan',
            'email' : 'ali@example.com',
            'password': '12345'
        }
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Email is Exist, Use A Diffrent Email"
    }
    
def test_update_user_duplicate_email(client):
    response = client.post(
        '/user/createuser',
        json= {
            'name' : 'Ali',
            'email': 'ali@example.com',
            'password': '12345'
        }
    )
    assert response.status_code == 201
    user1_id = response.json()['id']
    response = client.post(
        '/user/createuser',
        json= {
            'name' : 'Ali1',
            'email': 'ali1@example.com',
            'password': '12345'
        }
    )
    assert response.status_code == 201
    user2_id = response.json()['id']
    response = client.put(
        f'user/users/{user2_id}',
        json={
            'name' : 'Hassan',
            'email' : 'ali@example.com',
            'password': '12345'
        }
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Email is Exist"
    }
    