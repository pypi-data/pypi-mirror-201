from typing import Literal
class VisitFrequency:
    def __init__(self,json:dict):
        self.id: int = json['id']
        self.customer_id: int = json['customer_id']
        self.customer_code: str = json['customer_code']
        self.customer_name: str = json['customer_name']
        self.user_id: int = json['user_id']
        self.user_name: str = json['user_name']
        self.numberOfCyclesPerPeriod:int = json['cycle']
        self.numberOfVisitsRequiredPerCycle:int = json['frequency']
        self.period:Literal['Week','Month','Year']= json['period']
        self.version:int = json['version']
        self.last_modified_time:str = json['last_modified_time']