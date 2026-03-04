import uvicorn
from fastapi import FastAPI
from routers import schedules

app = FastAPI()     #change to router next step


def configure_app():
    app.include_router(
        schedules.router, prefix="/api/schedules", tags=["schedules"]
    )



if __name__ == "__main__":
    configure_app()
    uvicorn.run(app=app, host="127.0.0.1", port=8000)