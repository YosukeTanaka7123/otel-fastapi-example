from typing import Any

from azure.monitor.opentelemetry import configure_azure_monitor
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from core.config import get_settings
from core.database import async_engine
from core.logging import getLogger

settings = get_settings()
logger = getLogger(__name__)


def configure_openobserve():
    provider = TracerProvider()
    processor = BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint=settings.openobserve_http_endpoint,
            headers={"Authorization": f"Basic {settings.openobserve_authorization}"},
        )
    )
    provider.add_span_processor(processor)

    # Sets the global default tracer provider
    trace.set_tracer_provider(provider)


def configure_console():
    provider = TracerProvider()
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)

    # Sets the global default tracer provider
    trace.set_tracer_provider(provider)


def client_request_hook(
    span: trace.Span, scope: dict[str, Any], message: dict[str, Any]
):
    if message["body"]:
        logger.info(
            "Request body received.",
            extra={"request_body": message["body"].decode("utf-8")},
        )


# OpenTelemetry configuration
def setup_opentelemetry(app: FastAPI):
    # Setup tracer and exporter
    if settings.applicationinsights_connection_string:
        configure_azure_monitor(logger_name=settings.otel_service_name)
    elif settings.openobserve_http_endpoint:
        configure_openobserve()
    else:
        configure_console()

    # Instrument Logging, FastAPI, HTTPX, and SQLAlchemy
    LoggingInstrumentor().instrument()
    FastAPIInstrumentor().instrument_app(
        app=app, client_request_hook=client_request_hook
    )
    HTTPXClientInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument(engine=async_engine.sync_engine)
