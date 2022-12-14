from aiohttp import web
from db import session,User
from twilio.rest import Client
from settings import twilio as settings
from random import randint
async def hello_world(request):
    return web.Response(text="Hello, world!")

async def hello(request):
    name = request.match_info.get('name', "Anonymous")
    return web.Response(text=f"Hello, {name}!")


async def querry_user(request):
    # Parse the request header as JSON
    data = await request.json()
    email = data['email']
    # Append '.com' to the email address
    user = session.query(User).filter(User.email == email).first()
    # Return the modified email address in the response
    return web.Response(text=f"your profile was created at{user.created_at}, and lastly updated at {user.updated_at}")

async def sms_sender(request):
    try:
        # Generate a random 6-digit code
        code = randint(100000, 999999)

        # Set up the Twilio client
        account_sid = settings["TWILIO_ACCOUNT_SID"]
        auth_token = settings["TWILIO_AUTH_TOKEN"]
        client = Client(account_sid, auth_token)

        # Send the SMS message with the code
        client.messages.create(body= code,from_=settings["sender_number"],to='+421949867743')
        return web.Response(text=f"sms code has been send to +421949867743")
    except Exception as e:
        # Log the error
        return web.Response(text=f"Error sending SMS: {e},code:{code}")

