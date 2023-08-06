import json
from datetime import datetime, date
from json import JSONEncoder
import re

def is_datetime_format(s):

    _datetime_regex = re.compile(
        r'^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?)?$'
    )

    _date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    _time_regex = re.compile(r'^\d{2}:\d{2}:\d{2}$')
    def is_valid_datetime_string(datetime_str):
        return bool(_datetime_regex.match(datetime_str))

    def is_valid_date_string(date_str):
        return bool(_date_regex.match(date_str))

    def is_valid_time_string(time_str):
        return bool(_time_regex.match(time_str))
    return is_valid_date_string(s) or is_valid_datetime_string(s) or is_valid_time_string(s)

class iJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)
 