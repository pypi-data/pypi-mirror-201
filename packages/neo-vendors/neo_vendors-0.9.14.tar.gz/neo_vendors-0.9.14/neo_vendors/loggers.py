from __future__ import annotations

import logging.config
import socket
import sys
import types
import typing
from logging import LogRecord

import sentry_sdk


class NonLoggableExceptionsFilter(logging.Filter):
    exclude_exception_types: typing.Sequence[typing.Type[Exception]]

    def __init__(
            self,
            *,
            exclude_exception_types: typing.Sequence[typing.Type[Exception]] = (),
            name: str = '',
    ):
        self.exclude_exception_types = exclude_exception_types
        super().__init__(name=name)

    def filter(self, record: LogRecord) -> bool:
        if record.exc_info is None:
            return True
        try:
            exception_type = record.exc_info[0]
        except TypeError:
            return True
        return exception_type not in self.exclude_exception_types


def get_dict_config(
        *,
        sentry_dsn: typing.Optional[str] = None,
        tg_token: typing.Optional[str] = None,
        tg_chat: typing.Optional[int] = None,
        exclude_exception_types: typing.Sequence[typing.Type[Exception]] = (),
) -> typing.Dict[str, typing.Any]:
    hostname: str = socket.gethostname()
    null_handler: typing.Dict[str, str] = {
        "class": "logging.NullHandler",
    }
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(asctime)s [%(levelname)s] [{0} %(name)s:%(lineno)s] %(message)s".format(hostname)
            }
        },
        "filters": {
            "non_loggable_exceptions": {
                "()": NonLoggableExceptionsFilter,
                "exclude_exception_types": exclude_exception_types,
            },
        },
        "handlers": {
            "console_handler": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
                "filters": ["non_loggable_exceptions"],
            },
            "telegram_handler": {
                "class": "neo_vendors.telegram_log.handler.TelegramHandler",
                "token": tg_token,
                "chat_id": tg_chat,
                "level": "ERROR",
                "formatter": "verbose",
                "filters": ["non_loggable_exceptions"],
            } if tg_token and tg_token else null_handler,
            "sentry_handler": {
                "class": "sentry_sdk.integrations.logging.EventHandler",
                "level": "ERROR",
                "formatter": "verbose",
                "filters": ["non_loggable_exceptions"],
            } if sentry_dsn is not None else null_handler,
        },
        "loggers": {
            "root": {
                "level": "DEBUG",
                "handlers": ["console_handler", "telegram_handler", "sentry_handler"]
            },
            "uvicorn.error": {
                "level": "ERROR",
                "handlers": ["console_handler", "telegram_handler", "sentry_handler"],
                "propagate": False,
            },
            "telegram.bot": {
                "propagate": False,
            },
            "apscheduler": {
                "propagate": False,
            },
            "urllib3": {
                "level": "INFO",
                "propagate": False,
            },
        }
    }


def create_tg_info_logger(
        *,
        tg_token: str,
        tg_chat: str,
) -> logging.Logger:
    logger_name = 'tg_info'
    dict_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "telegram_handler": {
                "class": "neo_vendors.telegram_log.handler.TelegramHandler",
                "token": tg_token,
                "chat_id": tg_chat,
                "level": "INFO",
            }
        },
        "loggers": {
            logger_name: {
                "handlers": ["telegram_handler"],
                "propagate": False,
            },
        }
    }
    logging.config.dictConfig(dict_config)
    return logging.getLogger(logger_name)


def init_root_logger(
        sentry_dsn: typing.Optional[str] = None,
        tg_token: typing.Optional[str] = None,
        tg_chat: typing.Optional[int] = None,
        exclude_exception_types: typing.Sequence[typing.Type[Exception]] = (),
):
    if sentry_dsn is not None:
        sentry_sdk.init(
            dsn=sentry_dsn,
            traces_sample_rate=1.0,
            default_integrations=True,
        )
    dict_config = get_dict_config(
        sentry_dsn=sentry_dsn,
        tg_token=tg_token,
        tg_chat=tg_chat,
        exclude_exception_types=exclude_exception_types,
    )
    logging.config.dictConfig(dict_config)
    return logging.getLogger()


class LogContext:
    orig_handlers: typing.List[logging.Handler]
    orig_filters: typing.List[logging.Filter]
    exc_hook_previous: typing.Optional[typing.Callable]

    def __init__(
            self,
            *,
            sentry_dsn: typing.Optional[str] = None,
            tg_token: typing.Optional[str] = None,
            tg_chat: typing.Optional[int] = None,
            exclude_exception_types: typing.Sequence[typing.Type[Exception]] = (),
    ):
        self.orig_handlers = self.logger.handlers[:]
        self.orig_filters = self.logger.filters[:]
        self.exc_hook_previous = None
        _ = init_root_logger(
            sentry_dsn=sentry_dsn,
            tg_token=tg_token,
            tg_chat=tg_chat,
            exclude_exception_types=exclude_exception_types,
        )

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger()

    def restore_logger(self):
        self.logger.handlers = self.orig_handlers
        self.logger.filters = self.orig_filters

    def __enter__(self) -> logging.Logger:
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb) -> typing.Literal[False]:
        if exc_val is not None:
            logger = logging.getLogger()
            logger.exception(exc_val)
        self.restore_logger()
        return False

    def exc_hook_patched(
            self,
            exc_type: typing.Type[BaseException],
            exc_val: BaseException,
            exc_tb: types.TracebackType,
    ):
        self.logger.critical("Uncaught exception:", exc_info=(exc_type, exc_val, exc_tb))

    def set_exc_hook(self):
        self.exc_hook_previous = sys.excepthook
        sys.excepthook = self.exc_hook_patched

    def restore_exc_hook(self):
        sys.excepthook = self.exc_hook_previous
        self.exc_hook_previous = None
