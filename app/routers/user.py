from fastapi import HTTPException , Depends , APIRouter
from .. import models , schemas , utils
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

# Show All users
@router.get('/' , response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()
    return users

# Create User
@router.post('/', status_code=201 , response_model= schemas.UserResponse)
def create_user(user: schemas.UserCreate , db: Session = Depends(get_db)):

    #Hashed the password - user.password
    hashed = utils.hash(user.password)
    user.password = hashed

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#Show user by ID
@router.get('/{user_id}' , response_model=schemas.UserResponse)
def get_user_by_ID(user_id : int , db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

