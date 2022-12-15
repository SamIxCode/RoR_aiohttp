from aiohttp import web
from db import session,User
from twilio.rest import Client
from settings import twilio as settings
from random import randint
from datetime import datetime, timedelta



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
        data = await request.json()
        # Set up the Twilio client
        account_sid = settings["TWILIO_ACCOUNT_SID"]
        auth_token = settings["TWILIO_AUTH_TOKEN"]
        
        # Get the user id from the request data
        uid = data['id']
        
        # Calculate the time at which the code will expire
        now=datetime.now()
        valid_time = str(now + timedelta(minutes=10))
        
        # Get the user from the database and set the sms_code field
        user = session.query(User).filter(User.id == uid).first()
        user.sms_code = {"sms_code": code, "valid_until": valid_time}
        session.add(user)
        session.commit()
        
        # Send the SMS message with the code
        client = Client(account_sid, auth_token)
        client.messages.create(body= code,from_=settings["sender_number"],to='+421949867743')
        response = {
                "message":"sms code has been send to your number"
            }
        return web.json_response(response,status=200)
        # Return a response indicating that the SMS was sent
    except Exception as e:
        # Log the error and return a response with the error message
        response = {
                "message":e,
                "status":400
            }
        return web.json_response(response,status=400)



async def sms_verify(request):
    try:
        data = await request.json()
        uid = data['id']
        code = data['sms_code']

        user = session.query(User).filter(User.id == uid).first()

        sms_code = user.sms_code['sms_code']
        valid_until = datetime.strptime(user.sms_code["valid_until"], "%Y-%m-%d %H:%M:%S.%f")

        if sms_code == int(code) and valid_until > datetime.now():
            print(valid_until)
            print(datetime.now())
            print(valid_until - datetime.now())
            user.verified = True
            session.add(user)
            session.commit
            response = {
                "message":"you have been veriefied",
            }
            return web.json_response(response,status=200)
        else:
            response = {
                "message":"you provided wrong verification code or it has expired",
            }
            return web.json_response(response,status=400)
    except Exception as e:
    # Log the error
        response = {
                "message":e,
            }
        return web.json_response(response,status=400)