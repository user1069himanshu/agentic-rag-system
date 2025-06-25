from fastapi import FastAPI,Depends,status
from typing import Optional
from pydantic import BaseModel
from .database import engine,sessionlocal #if we want any specific class from local module
from . import models #if we want to import whole local module
from sqlalchemy.orm import Session #Session is not a pydantic thing
from . import schemas



app = FastAPI()


models.Base.metadata.create_all(engine) #Table migrating into the main module

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()

#To add blog in db
@app.post('/blog')
def firstblog(request:schemas.Blog,db: Session=Depends(get_db)): #Session used to update the db
    new_blog=models.Blog(title=request.title, body=request.content)#import blog from models module
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


#To get all the entries of db
@app.get('/blog')
def allblog(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()#all returns all the entries in db
    return blogs

#Retrieve particular blog using id no.
@app.get('/blog/{id}',response_model=schemas.Showblog)
def getblog(id,db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blogs:
        return{f'No blog found with id {id}'}
    return blogs
'''filter gives number of option to filter out the options 
whereas the first option gives us the only first entry of thr filtered options, 
it will return null if no entry matched with the filter applied'''

#To delete a particular blog from databse
@app.delete('/blog/{id}')
def delblog(id,db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return {f'Blog with id {id} is deleted'}

# put method, used for updating db
@app.put('/blog/{id}')
def update(id,request:schemas.Blog,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if blog.first():
        blog.update({'title':"Title Updated",'body':"Content also updated"})
    else:
        return {f"No blog with id {id}"}
    db.commit()
    return {f"Title & Content updated of blog {id}"}


#Response Model
'''In sqlalchemy pydantic models are not considered as models,
they are treated as schemas'''
