'''
Testing views.py
'''

def test_home_route(client):
    '''
    GIVEN some client
    WHEN '/' is requested
    THEN check the functionality
    '''
    response = client.get('/')

    assert response.status_code == 200
    assert b"Podcastify" in response.data
