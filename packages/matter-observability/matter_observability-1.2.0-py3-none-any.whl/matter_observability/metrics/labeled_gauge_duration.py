import time
import logging

from .labeled_gauge import LabeledGauge


class LabeledGaugeDuration(LabeledGauge):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def label_parameter_name(self):
        return "action"

    def start(self):
        self.start_time = time.time()
        logging.info(f"Start measuring for {self._labeled_metric._name} => {self._labeled_metric._documentation}")

    def stop(self):
        self.stop_time = time.time()
        self.duration_in_seconds = round(self.stop_time - self.start_time, 2)
        logging.info(f"{self._labeled_metric._name} => Took {self.duration_in_seconds} seconds.")
        self.set(self.duration_in_seconds)
