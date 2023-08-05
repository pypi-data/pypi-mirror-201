import logging

from .utils import publish_metrics
from .labeled_metric import LabeledMetric


class LabeledCounter(LabeledMetric):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def label_parameter_name(self):
        return "counter"

    def inc(self):
        logging.info(f"Increasing value for {self._labeled_metric._name}.")
        self._labeled_metric.inc()

        if self.use_push_gateway:
            publish_metrics()
