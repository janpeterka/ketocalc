import logging
# from logging.handlers import SMTPHandler
from flask import request

from app.models import Log


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


class SQLAlchemyHandler(logging.Handler):
    def emit(self, record):
        try:
            remote_addr = record.__dict__['remote_addr']
        except Exception:
            remote_addr = None

        try:
            url = record.__dict__['url']
        except Exception:
            url = None

        log = Log(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            msg=record.__dict__['msg'],
            remote_addr=remote_addr,
            url=url,
            module=record.__dict__['module']
        )
        try:
            log.save()
        except Exception:
            pass


# DB handler
db_handler = SQLAlchemyHandler()
db_handler.setLevel(logging.INFO)
db_handler.setFormatter(RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s: %(levelname)s in %(module)s: %(message)s'
))

# Mail handler
# mail_handler = logging.handlers.SMTPHandler(
#     mailhost='127.0.0.1',
#     fromaddr='server-error@example.com',
#     toaddrs=['admin@example.com'],
#     subject='Application Error'
# )


# File error.log handler
# file_handler = logging.FileHandler('log/error.log')
# file_handler.setLevel(logging.WARNING)
# file_handler.setFormatter(RequestFormatter(
#     '[%(asctime)s] %(remote_addr)s requested %(url)s: %(levelname)s in %(module)s: %(message)s'
# ))

# gunicorn_logger = logging.getLogger('gunicorn.error')
# gunicorn_logger.setLevel(logging.DEBUG)
