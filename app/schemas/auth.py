from pydantic import BaseModel, EmailStr

#1. User registeration
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

#2. User response 
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


#3. User Login
class UserLogin(BaseModel):
    username: str
    password: str

#4. Login Respone
class LoginResponse(BaseModel):
    message: str