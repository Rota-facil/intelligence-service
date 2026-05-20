import asyncio
import os

from contextlib import asynccontextmanager

import py_eureka_client.eureka_client as eureka

from fastapi import FastAPI

from http_routes.controllers.intelligence_controller import (
    router as router_intelligence
)

EUREKA_SERVER = os.environ.get(
    "EUREKA_SERVER",
    "http://localhost:8081/eureka/"
)

INTELLIGENCE_HOST = os.environ.get(
    "INTELLIGENCE_HOST",
    "localhost"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    while True:
        try:
            await eureka.init_async(
                eureka_server=EUREKA_SERVER,
                app_name="intelligence-service",
                instance_port=8000,
                instance_host=INTELLIGENCE_HOST
            )

            print("Connected to Eureka!")
            break

        except Exception as e:
            print(f"Eureka not ready yet: {e}")
            await asyncio.sleep(5)

    yield

    await eureka.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(router_intelligence)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}