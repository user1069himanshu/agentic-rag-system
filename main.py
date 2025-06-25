from fastapi import FastAPI

app = FastAPI()
#uvicorn main:app --reload
#/docs for swagger API
@app.get('/')
def about():
    return {'data': {'about page'}}

    
#Path parameter
#here 'id' is a path parameter
@app.get('/blog/{id}')
def about(id:int):
    return {'data': 2*id} 

@app.get('/blog/{id}/comments')
def about(id):
    return {'comments': '1'}

@app.get('/blog/{id}/blogs')
def about():
    return {'List of unpublished blogs'}


#Query parameter
'''here 'limit' and 'published' are query parameter
unless the parameter is not mentioned in the path, FastAPI consider it as query parameter'''
@app.get('/blog')
def about(limit:int,published:bool):
    if published:
        return {f'{limit} published blogs'}
    else:
        return 'No published blog available'
    
#Optional Query Parameter
from typing import Optional 
@app.get('/blog')
def about(limit:int,published:bool,sort:Optional [str]=None):
    if published:
        return{f'{limit} sorted published blog'}
    else:
        return {'Zero sorted published blogs from DB'}

#Post Method
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

#Request using class atrribute
@app.post('/postblog')
def about_post(request: Blog):
    return {f'blog is created with title as {request.title}'}

'''Change Port address
import uvicorn
if __name__=="__main__":
    uvicorn.run(app,host='127.0.0.1',port=9000)'''



