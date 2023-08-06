import uuid
from datetime import datetime, timedelta


class Request:
    """
    A Request to fetch dataframes from Wizata App.

    To execute the request please use a DS API client.

    :ivar equipments: List of Equipments containing Digital Twin item and datapoints to fetch.
    :ivar start: Datetime defining beginning of period.
    :ivar end: Datetime defining end of period.
    :ivar aggregation: Aggregation method to fetch, accept "mean" and "stddev".
    :ivar interval: Interval in seconds between each aggregation.
    :ivar filters: Filter to apply on the query (not yet fully implemented).
    :ivar connections: Connections rules between equipment to align data in time (not yet fully implemented).
    """

    def __init__(self):
        self.function = None
        self.equipments = []
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
        """
        prepare a dict JSON compatible only for the QUERY part of the request.

        :return: a dict JSON compatible
        """
        query = {}
        if self.equipments is not None:
            query["equipments_list"] = self.equipments
        else:
            raise KeyError("Missing data points inside the query - add_datapoints")
        if self.start is not None and self.end is not None:
            query["timeframe"] = {
                "start": self.__format_date(self.start),
                "end": self.__format_date(self.end)
            }
        else:
            raise KeyError("Missing start and end date, please use datatime format")
        if self.aggregation is not None and self.interval:
            query["aggregations"] = {
                "agg_method": self.aggregation,
                "interval": self.interval * 1000
            }
        else:
            raise KeyError("Missing aggregations information inside the request")
        return query

    def __format_date(self, dt_to_format):
        if isinstance(dt_to_format, datetime):
            millisec = dt_to_format.timestamp() * 1000
            return int(millisec)
        else:
            raise TypeError("date is not a valid datetime")

    # add datapoints without any reference to an equipment
    def add_datapoints(self, datapoints, shift: int = 0):
        """
        Add datapoints to fetch without defining its equipments.
        :param datapoints: List(str) of datapoints to fetch identified by Hardware ID.
        :param shift: Shift to apply in seconds on timestamp, by default 0.
        """
        self.equipments.append({
            "id": None,
            "datapoints": list(datapoints),
            "shift": str(shift) + "s"
        })

    def add_equipment(self, equipment_id: uuid.UUID, datapoints, shift=0):
        """
        Add datapoints to fetch with a Digital Twin ID identification.
        :param equipment_id: UUID of the Digital Twin ID to which the datapoints are linked.
        :param datapoints: List(str) of datapoints to fetch identified by Hardware ID.
        :param shift: Shift to apply in seconds on timestamp, by default 0.
        """
        if not isinstance(equipment_id, uuid.UUID):
            raise TypeError("equipment_id must be of type uuid.UUID")
        for equipment in self.equipments:
            if "id" in equipment.keys() and equipment["id"] == str(equipment_id):
                raise ValueError("equipment_id is already in the request please remove it before adding datapoints.")
        self.equipments.append({
            "id": str(equipment_id),
            "datapoints": list(datapoints),
            "shift": str(shift) + "s"
        })

    # attempt to remove equipment from the query if exists
    def remove_equipment(self, equipment_id: uuid.UUID):
        """
        Remove an equipment from the list including all its listed datapoints.
        :param equipment_id: UUID of the Digital Twin item.
        """
        if equipment_id is not None and not isinstance(equipment_id, uuid.UUID):
            raise TypeError("equipment_id must be None or of type uuid.UUID")
        found = None
        for equipment in self.equipments:
            if "id" in equipment.keys() and equipment["id"] == str(equipment_id):
                found = equipment
        if found is not None:
            self.equipments.remove(equipment)

    def set_aggregation(self, method, interval):
        """
        Specifies aggregation properties
        :param method: 'mean' or 'stddev'
        :param interval: interval in ms (will be stored in seconds)
        """
        self.aggregation = method
        self.interval = int(interval) / 1000

    def to_json(self):
        """
        convert to a dict JSON compatible for all properties. For query only, use prepare().

        :return: a dict JSON compatible
        """
        obj = self.prepare()
        if self.target_feat is not None:
            obj["target_feat"] = {
                "sensor": self.target_feat["sensor"],
                "operator": self.target_feat["operator"],
                "threshold": self.target_feat["threshold"]
            }
        if self.on_off_sensor is not None and self.restart_time is not None:
            obj["restart_filter"] = {
                "on_off_sensor": self.on_off_sensor,
                "stop_restart_time": self.restart_time
            }

        if self.sensitivity is not None:
            obj["sensitivity"] = self.sensitivity

        if self.extra_data is not None:
            obj["extra_data"] = self.extra_data

        return obj

    def from_json(self, json_data):
        """
        load a request based on dict from a JSON file.

        :param json_data: JSON formatted dictionnary object representing a query.
        """
        if "name" in json_data.keys():
            self.name = json_data["name"]

        if "equipments_list" not in json_data.keys():
            raise KeyError("No 'twin unit' nor 'data points' selected please select some and re-try.")
        self.equipments = json_data["equipments_list"]

        if "timeframe" not in json_data.keys():
            raise KeyError("No 'time range' have been selected, please set it up and re-try.")

        if "start" not in json_data["timeframe"].keys():
            raise KeyError("No 'start time' have been selected, please set it up and re-try.")
        self.start = datetime.fromtimestamp(json_data["timeframe"]["start"] / 1000)

        if "end" not in json_data["timeframe"].keys():
            raise KeyError("No 'end time' have been selected, please set it up and re-try.")
        self.end = datetime.fromtimestamp(json_data["timeframe"]["end"] / 1000)

        if "aggregations" not in json_data.keys():
            raise KeyError("No 'aggregations' have been selected, please set it up and re-try.")

        if "agg_method" not in json_data["aggregations"].keys():
            raise KeyError("No 'Aggregation Method' have been selected, please set it up and re-try.")
        self.aggregation = json_data["aggregations"]["agg_method"]

        if "interval" not in json_data["aggregations"].keys():
            raise KeyError("No 'Aggregation Interval' have been selected, please set it up and re-try.")
        self.interval = int(json_data["aggregations"]["interval"] / 1000)

        if "filters" in json_data.keys():
            self.filters = json_data["filters"]

        if "connections" in json_data.keys():
            self.connections = json_data["connections"]

        if "target_feat" in json_data.keys():
            self.target_feat = json_data["target_feat"]
            if "sensor" not in self.target_feat.keys():
                raise KeyError("No 'sensor' have been declared inside the target feature, this is a technical error.")
            if "operator" not in self.target_feat.keys():
                raise KeyError("No 'operator' have been declared inside the target feature, this is a technical error.")
            if "threshold" not in self.target_feat.keys():
                raise KeyError("No 'threshold' have been declared inside the target feature, this is a technical error.")

        if "restart_filter" in json_data.keys():
            self.on_off_sensor = json_data["restart_filter"]["on_off_sensor"]
            self.restart_time = json_data["restart_filter"]["stop_restart_time"]

        if "sensitivity" in json_data.keys():
            self.sensitivity = json_data["sensitivity"]

        if "extra_data" in json_data.keys():
            self.extra_data = json_data["extra_data"]

