from aiohttp import web
from db import session,User
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
