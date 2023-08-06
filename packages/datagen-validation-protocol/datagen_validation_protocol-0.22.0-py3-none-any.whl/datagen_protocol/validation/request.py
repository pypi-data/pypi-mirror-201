from typing import List

from datagen_protocol.schema import request as core_request_schema
from datagen_protocol.validation.humans.human import HumanDatapoint as ValidationHumanDatapoint


class DataRequest(core_request_schema.DataRequest):
    datapoints: List[ValidationHumanDatapoint]


core_request_schema.DataRequest = DataRequest
