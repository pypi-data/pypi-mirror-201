import logging

from .labeled_metric import LabeledMetric
from .utils import publish_metrics


class LabeledGauge(LabeledMetric):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def label_parameter_name(self):
        return "parameter"

    def set(self, value):
        logging.info(f"Setting {self._labeled_metric._name} Metric as {value}")
        self._labeled_metric.set(value)

        if self.use_push_gateway:
            publish_metrics()
