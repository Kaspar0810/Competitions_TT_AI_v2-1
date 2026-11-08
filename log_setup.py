# log_setup.py
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from PyQt5.QtCore import QStandardPaths


def get_log_dir() -> str:
    """Папка для логов: %APPDATA%\<Org>\<App>\logs (устойчива к --onefile)."""
    base = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    if not base:  # страховка, если org/app не заданы
        base = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) \
               else os.path.abspath(".")
    log_dir = os.path.join(base, "logs")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def get_log_file() -> str:
    return os.path.join(get_log_dir(), "app.log")


def setup_logging() -> logging.Logger:
    """Настраивает файловый лог с ротацией и перехват необработанных исключений."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Приглушаем очень болтливые сторонние логгеры
    logging.getLogger("peewee").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # На случай повторного вызова — очищаем старые обработчики
    for h in logger.handlers[:]:
        logger.removeHandler(h)

    log_file = get_log_file()

    # Ротация: 5 МБ × 3 файла = максимум ~15 МБ
    fh = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # В режиме разработки (не в exe) дополнительно пишем в консоль
    if not getattr(sys, "frozen", False):
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logger.addHandler(ch)

    # Перехват необработанных исключений (то, что иначе «убивает» программу без следа)
    def _excepthook(exc_type, exc_value, exc_tb):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_tb)
            return
        logger.critical(
            "Необработанное исключение",
            exc_info=(exc_type, exc_value, exc_tb),
        )

    sys.excepthook = _excepthook

    # Также ловим падения в потоках (threading.excepthook появился в Py 3.8+)
    try:
        import threading
        def _thread_hook(args):
            logger.critical(
                "Необработанное исключение в потоке %s",
                args.thread.name if args.thread else "?",
                exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
            )
        threading.excepthook = _thread_hook
    except Exception:
        pass

    return logger