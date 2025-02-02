import logging

from core.config import get_settings

settings = get_settings()


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "otelTraceID"):
            record.otelTraceID = "00000000000000000000000000000000"
        if not hasattr(record, "otelSpanID"):
            record.otelSpanID = "0000000000000000"
        return super().format(record)


formatter = CustomFormatter(
    fmt="%(asctime)s.%(msecs)03d %(levelname)-8s [%(otelTraceID)s-%(otelSpanID)s] %(filename)s:%(lineno)d (%(funcName)s) - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler = logging.StreamHandler()
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
