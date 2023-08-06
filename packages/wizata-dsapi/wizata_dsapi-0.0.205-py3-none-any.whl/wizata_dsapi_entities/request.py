import datetime


class Request:

    def __init__(self):
        self.function = None
        self.equipments = None
        self.start = None
        self.end = None
        self.aggregation = None
        self.interval = None
        self.filters = None
        self.on_off_sensor = None
        self.restart_time = None
        self.sensitivity = None
        self.dataframe = None
        self.extra_data = None
        self.target_feat = None
        self.connections = None
        self.name = None

    def prepare(self):
        query = {}
        if self.equipments is not None:
            query["equipments_list"] = self.equipments
        if self.start is not None and self.end is not None:
            query["timeframe"] = {
                "start": self.__format_date(self.start),
                "end": self.__format_date(self.end)
            }
        return query

    def __format_date(self, dt_to_format):
        if isinstance(dt_to_format, datetime.datetime):
            millisec = dt_to_format.timestamp() * 1000
            return int(millisec)

