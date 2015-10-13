def test_app(app):
    assert app.name == 'example'


def test_indexview(client):
    assert 'Index' == client.get('/').text
    from example import IndexView
    assert IndexView.index.__doc__ == "A docstring for testing that docstrings are set"


def test_basicview(client):
    assert 'Index' == client.get('/basic').text
    assert 'Post: content' == client.post('/basic', 'content').text
    assert 'Get 1' == client.get('/basic/1').text
    assert 'Put 1: content' == client.put('/basic/1', 'content').text
    assert 'Custom Method' == client.get('/basic/custom_method').text
    assert 'Custom Method 1 2' == client.get('/basic/custom_method_with_params/1/2').text
    assert 'Routed Method' == client.get('/basic/routed').text
    assert 'Multi Routed Method' == client.get('/basic/route1').text
    assert 'Multi Routed Method' == client.get('/basic/route2').text
    assert 'No Slash Method' == client.get('/basic/noslash').text
    assert 'Custom HTTP Method' == client.post('/basic/route3').text


def test_foobar_endpoint(app):
    url = app.router['foobar'].url(parts={'param': 'param_value'})
    assert url == '/basic/endpoint/param_value'


def test_postindex(client):
    client.get('/post/check', status=405)
    assert 'Check' == client.post('/post/check').text
