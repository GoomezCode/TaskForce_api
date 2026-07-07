from fastapi import APIRouter
from util.jsonFile import *


router = APIRouter(
    prefix=("/task"),
    tags=["task"]
)

@router.get("/get")
def get():
    return readJson()

@router.post("/create/{task}")
def create(task:str):
    createTarefa(task)

@router.delete("/delete/{idTask}")
def delete(idTask:int):
    deleteTarefa(idTask)

@router.put("/put/marcar/{idTask}")
def put_marcar(idTask:int):
    update_feitoTarefa(idTask)