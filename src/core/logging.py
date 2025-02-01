import logging

from core.config import get_settings

settings = get_settings()

handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d [%(levelname)-8s] %(filename)s:%(lineno)d (%(funcName)s) - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)


def getLogger(name: str):
    logger = logging.getLogger(name)

    # 既にハンドラが設定されている場合は追加しない
    if not logger.hasHandlers():
        logger.addHandler(handler)

    # ログレベルの設定
    level = logging.getLevelNamesMapping().get(settings.log_level, logging.NOTSET)
    logger.setLevel(level)
    handler.setLevel(level)

    return logger
