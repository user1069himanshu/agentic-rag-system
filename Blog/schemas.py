from pydantic import BaseModel,ConfigDict

class Blog(BaseModel):
    Title:str
    Content:str

class Showblog(Blog):
    class Config():
        from_attributes=True
