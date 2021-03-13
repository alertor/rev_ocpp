from user.auth import hash_password, authenticate_user
from db.session import session

a = hash_password('password')
print(a)

# with session() as db:
#     a = authenticate_user(db, email='tgpovey@gmail.com', password='password')
#     print(a)
#     print(a.email)
#     print(a.first_name)
#     print(a.last_name)