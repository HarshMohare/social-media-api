from fastapi import HTTPException , Depends , APIRouter
from .. import models , schemas , oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List , Optional
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# Show All the Post
@router.get('/' , response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user), Limit: int = 10 , skip: int = 0 , search: Optional[str] = ""):

    posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    return posts

# Add New Post
@router.post('/' , status_code=201 , response_model=schemas.Post)
def create_post(post:schemas.PostCreate , db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=current_user.id  ,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# Get Single Post
@router.get('/{id}' , response_model=schemas.PostOut)
def get_post(id: int , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post_obj, votes = post
    
    if post_obj.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    
    return post

# Delete Post
@router.delete('/{id}', status_code=204)
def delete_post(id: int , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    deleted = db.query(models.Post).filter(models.Post.id == id)

    post = deleted.first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    
    deleted.delete(synchronize_session=False)
    db.commit()


# Update post
@router.put('/{id}' , response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    existing_post = post_query.first()

    if not existing_post :
        raise HTTPException(status_code=404, detail="Post not found")
    

    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    

    
    post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()

    return post_query.first()