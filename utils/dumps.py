import datetime
import json

class DateEnconding(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            o = o+ datetime.timedelta(hours=8)
            return o.strftime('%Y-%m-%d %H:%M:%S')

def response(data, code, message):
    return json.dumps({
        'data': data,
        'code': code,
        'message': message
    }, indent=2, ensure_ascii=False,cls=DateEnconding)