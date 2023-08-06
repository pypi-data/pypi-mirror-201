from prometheus_client import Gauge, Counter

from matter_observability.config import Config

from .utils import registry


GAUGE_PROCESSING_TIME = Gauge(
    f"{Config.INSTANCE_NAME.lower().replace('-','_')}_processing_time",
    f"Processing time in {Config.INSTANCE_NAME.capitalize()}",
    labelnames=["action"],
    registry=registry,
)

GAUGE_CUSTOM = Gauge(
    f"{Config.INSTANCE_NAME.lower().replace('-','_')}_gauge",
    f"Gauge a parameter in {Config.INSTANCE_NAME.capitalize()}",
    labelnames=["parameter"],
    registry=registry,
)

COUNTER_CUSTOM = Counter(
    f"{Config.INSTANCE_NAME.lower().replace('-','_')}_number_of_occurrences",
    f"Total {Config.INSTANCE_NAME.capitalize()} Count",
    labelnames=["counter"],
    registry=registry,
)
