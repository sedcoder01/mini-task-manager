
def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Mini Task Management API"}
    
def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == { "status": "ok" }
    
def test_db_health(client):
    response = client.get('/health/db')
    assert response.status_code == 200
    assert response.json() == { "database": "ok" }