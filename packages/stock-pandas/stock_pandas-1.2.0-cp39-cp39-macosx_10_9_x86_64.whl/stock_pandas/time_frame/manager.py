from stock_pandas._libs.indexer import IndexerBase


class TimeFrameManager(IndexerBase):
    ...


# Mixin
# -------------------------------------------------------

class TimeFrameMixin:
    """
    Usage::

        stock.timeFrame['15m']
    """

    @property
    def timeFrame(self):
        ...
