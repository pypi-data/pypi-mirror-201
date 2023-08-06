from abc import ABC, abstractmethod


class LabeledMetric(ABC):
    def __init__(self, **kwargs):
        self.use_push_gateway = kwargs.get("use_push_gateway", False)
        self.metric = kwargs["metric"]
        self.label = kwargs["label"]
        self._labeled_metric = self.metric.labels(**{self.label_parameter_name: self.label})

    @property
    @abstractmethod
    def label_parameter_name(self):
        pass
