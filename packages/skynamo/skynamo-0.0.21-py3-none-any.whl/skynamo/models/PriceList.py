class PriceList:
    def __init__(self,json:dict):
        self.id=json['id']
        self.name=json['name']
        self.last_modified_time=json['last_modified_time']
        self.active=json['active']
        self.prices_include_vat=json['prices_include_vat']