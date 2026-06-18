from passlib.context import bcrypt
h = bcrypt.hash("password")
print(h)