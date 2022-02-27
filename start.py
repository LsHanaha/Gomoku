import uvicorn
from app import settings
from app.custom_logging import initialize_logs

if __name__ == '__main__':
    uvicorn.run("app.main:web_app",
                host='0.0.0.0',
                port=8888,
                reload=settings.debug,
                debug=settings.debug,
                log_config=initialize_logs()
                )
