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


def setup_otel_fastapi_logging():
    logger = logging.getLogger(settings.otel_service_name)

    # フォーマッター, ハンドラーの設定
    formatter = CustomFormatter(
        fmt="%(asctime)s.%(msecs)03d %(levelname)-8s [%(otelTraceID)s-%(otelSpanID)s] %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # 既存のハンドラがない場合のみロガーに追加
    if not logger.handlers:
        logger.addHandler(handler)

    # ログレベルの設定
    level = logging.getLevelNamesMapping().get(settings.log_level, logging.NOTSET)
    logger.setLevel(level)


def getLogger(name: str):
    if not name.startswith(f"{settings.otel_service_name}."):
        name = f"{settings.otel_service_name}.{name}"
    return logging.getLogger(name)
