from url_shortener_app import create_app

def test_shorten(client):
    response = client.get('/')
    assert b'Shorten' in response.data