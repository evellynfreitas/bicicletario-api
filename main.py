from fastapi import FastAPI
from controllers import hello_controller

app = FastAPI()
app.include_router(hello_controller.router)
