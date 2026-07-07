from pydantic import BaseModel

class task(BaseModel):
    id:int
    tarefa:str
    feito:bool
    date:str
    hour:str
