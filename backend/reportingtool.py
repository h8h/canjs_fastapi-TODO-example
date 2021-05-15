import uvicorn
from uuid import uuid4
from typing import Iterable, Optional, Union
from pydantic import BaseModel, Field
from fastapi import FastAPI
from starlette.responses import FileResponse 
from fastapi.staticfiles import StaticFiles

app  = FastAPI()
app.mount("/dist", StaticFiles(directory="../frontend/dist/dist", html=False), name="static")
#app.mount("/dist", StaticFiles(directory="../frontend/dist/", html=False), name="static")

api  = FastAPI()
app.mount("/api/v1", api)

fake_todos_db = [{"id":str(uuid4()), "name": "Task 1", "complete": False}, {"id":str(uuid4()), "name": "Task 2","complete": True}, {"id":str(uuid4()), "name": "Task 3", "complete": False}]

class Todo(BaseModel):
    id: Optional[str] = None
    name: str
    complete: bool

@app.get("/")
async def staticindex():
    return FileResponse('../frontend/dist/index.html')

@api.get("/")
async def index():
    return {"ping": "pong"}

@api.get("/todos")
async def read_todos():
    return fake_todos_db

@api.get("/todos/{id}")
async def read_todo(id: str):
    return next((todo for todo in fake_todos_db if todo['id'] == id), Todo())


@api.post("/todos")
async def create_todo(todo: Todo):
    dtodo = dict(todo)
    if "id" not in dtodo or dtodo["id"] == None:
        dtodo['id'] = str(uuid4())
    fake_todos_db.append(dtodo)
    return dtodo

@api.put("/todos/{id}")
async def change_todo(id: str, todo: Todo):
    update_todo = next((t for t in fake_todos_db if t['id'] == id), None)
    dtodo = dict(todo)
    dtodo["id"] = id
    update_todo.update(dtodo)
    return dtodo

@api.delete("/todos/{id}")
async def delete_todo(id: str):
    fake_todos_db[:] = [t for t in fake_todos_db if t.get('id') != id]
    return {"id": id}

if __name__ == "__main__":
    uvicorn.run("reportingtool:app", host="0.0.0.0", port=7000, log_level="info")
