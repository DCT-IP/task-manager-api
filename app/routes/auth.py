from fastapi import APIRouter
#this a mock router for the auth system
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/")
def auth_check():
    return {"message": "Auth route working"}


#prefix makes it such that whatever is written in the file will automatically start with /auth
