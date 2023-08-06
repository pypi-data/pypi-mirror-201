from sqlalchemy import Column, Identity, ForeignKey, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relationship
import pytz
from pandas import to_datetime

from sunpeek.components.helpers import ORMBase
from sunpeek.components.base import Component


class OperationalEvent(ORMBase):
    __tablename__ = 'operational_events'

    id = Column(Integer, Identity(0), primary_key=True)
    plant_id = Column(Integer, ForeignKey('plant.id', ondelete="CASCADE"))
    plant = relationship("Plant", back_populates="operational_events")
    _start = Column(DateTime(timezone=True))
    _end = Column(DateTime(timezone=True))
    ignored_range = Column(Boolean)
    description = Column(String)

    def __init__(self, plant, start, tz=None, description=None, end=None, ignored_range=False):
        self.plant = plant
        self.set_start(start, tz)
        self.set_end(end, tz)
        self.ignored_range = ignored_range
        self.description = description

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, val):
        assert val.tzinfo is not None, "start must be timezone aware. Pass a tz aware datetime object, or use set_start " \
                                       "with a tz argument, or a string like 2022-1-1 00:00+02"
        self._start = val

    def set_start(self, val, tz=None):
        dt = to_datetime(val).to_pydatetime()
        if tz is not None:
            dt = pytz.timezone(tz).localize(dt)
        self.start = dt

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, val):
        assert val.tzinfo is not None, "end must be timezone aware. Pass a tz aware datetime object, or use set_end " \
                                       "with a tz argument, or a string like 2022-1-1 00:00+02"
        self._end = val

    def set_end(self, val, tz=None):
        dt = to_datetime(val).to_pydatetime()
        if tz is not None:
            dt = pytz.timezone(tz).localize(dt)
        self.end = dt
