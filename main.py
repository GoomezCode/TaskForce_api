import os
from fastapi import FastAPI
import uvicorn
from api import apiTask


app = FastAPI()
app.include_router(apiTask.router)

@app.get("/")
def raiz():
    return {"msg": "Api inicializada com sucesso...."}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info", reload=True)