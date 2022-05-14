from fastapi import FastAPI
from uvicorn import Config, Server

from routers import admin, client, manager


app = FastAPI()

app.include_router(admin.router)
app.include_router(client.router)
app.include_router(manager.router)


if __name__ == "__main__":
    server = Server(Config(app, host="0.0.0.0", port=8000, loop="uvloop"))
    server.run()
