from aiohttp import web
from backend import querry_user, sms_sender, sms_verify

def setup_routes(app):
    app.add_routes([
        web.post('/sms', sms_sender),
        web.post('/q', querry_user),
        web.post('/verify', sms_verify)
    ])
