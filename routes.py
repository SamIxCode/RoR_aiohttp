from aiohttp import web
from backend import hello, hello_world, querry_user, sms_sender

def setup_routes(app):
    app.add_routes([
        web.get('/', hello_world),
        #web.get('/{name}', hello),
        web.get('/sms', sms_sender),
        web.post('/q', querry_user)
    ])
