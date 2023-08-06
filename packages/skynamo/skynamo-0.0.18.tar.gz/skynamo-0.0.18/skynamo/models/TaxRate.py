from ..shared.helpers import getDateTimeObjectFromSkynamoDateTimeStr

class TaxRate:
    def __init__(self,json:dict):
        self.id=int(json['id'])
        self.name=str(json['name'])
        self.rate=float(json['rate'])
        self.active=bool(json['active'])
        self.last_modified_time=getDateTimeObjectFromSkynamoDateTimeStr(json['last_modified_time'])