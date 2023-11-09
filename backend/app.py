import os, logging

from flask import Flask
from logging.config import dictConfig
from flask_restful import Api
from flask_jwt_extended import JWTManager

from common.database import db
from common.config import LocalDev


# set the configurations for the log file
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s | %(module)s >>> %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "logs/flask.log",
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "file"]},
    }
)

# set app = None to initialize variable
app = None
api = None
jwt = None
celery = None


app = Flask(__name__, template_folder='templates')
app.config.from_object(LocalDev)

db.init_app(app)
app.app_context().push()
app.logger.info('Database plugin initialized')

api = Api(app)
app.app_context().push()
app.logger.info('API plugin initialized')

jwt = JWTManager(app)
app.app_context().push()
app.logger.info('JWT Manager initialized')

app.logger.info('App setup complete.')


@app.route('/')
def home():
    return "Hi"

if __name__ == '__main__':
    app.run()