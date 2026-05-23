from pydantic import BaseModel, Field
#pydanctic  does two jobs 1. data validation 2. data serialization
class TaskCreate(BaseModel):
    title: str = Field(..., example="Learn FastAPI")
#the task should have a title and it has to be a string, else a 422 error will occur 

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
#this defines what the responnse will look like when we get a task. 
    class Config:
        from_attributes = True
