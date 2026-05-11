from fastapi import FastAPI
from http.intelligence_controller import router as router_intelligence

app = FastAPI()
app.include_router(router_intelligence)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
