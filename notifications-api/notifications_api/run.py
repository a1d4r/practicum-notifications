import uvicorn

import config
from application import app

settings = config.get_settings()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)
