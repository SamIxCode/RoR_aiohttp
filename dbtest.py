from db import get_session
from db import User
session = get_session()

user = session.query(User).filter(User.email =='abc@abc.com').first()
print(user.created_at, user.updated_at)

