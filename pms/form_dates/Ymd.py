from datetime import datetime

class Ymd():
    def __init__(self,ymd_str) -> datetime:
        self.date = None
        if(ymd_str):
            date_format = "%Y-%m-%d"
            self.date = datetime.strptime(ymd_str, date_format)
        return 
    def __str__(self) -> datetime:
        return self.date
    def __sub__(self,other):
        return (self.date-other.date).days