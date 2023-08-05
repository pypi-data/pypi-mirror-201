from starlette_exporter import PrometheusMiddleware, handle_metrics

from matter_observability.config import Config


def add_middleware(app, skip_paths=None):
    metrics_path = "/internal/metrics"

    if Config.ENABLE_METRICS:
        app.add_middleware(
            PrometheusMiddleware,
            app_name=Config.INSTANCE_NAME,
            group_paths=True,
            skip_paths=[metrics_path] + skip_paths if skip_paths else [metrics_path],
        )
        app.add_route(metrics_path, handle_metrics)
