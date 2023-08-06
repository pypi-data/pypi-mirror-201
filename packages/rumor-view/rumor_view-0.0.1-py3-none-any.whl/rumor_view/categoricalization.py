import logging
import abc


logger = logging.getLogger(__name__)


def make_index(df):
    for c in df.columns:
        logger.info()


class Column(abc.ABC):
    def __init__(self, series, min_freq_ratio):
        self.values = self._categoricalize(series, min_freq_ratio)

    @abc.abstractmethod
    def _categoricalize(self, series, min_freq_ratio):
        pass


class NumericColumn(object):
    def _categoricalize(self, series, min_freq_ratio):
        value_counts = series.value_counts()
