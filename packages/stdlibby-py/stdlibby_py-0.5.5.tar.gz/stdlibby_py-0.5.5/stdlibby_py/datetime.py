from datetime import datetime
from zoneinfo import ZoneInfo

def get_unix_time()->int:
    return int(datetime.now().replace(microsecond=0).timestamp())

def get_current_tz()->ZoneInfo:
    tz_str = str(datetime.utcnow().astimezone().tzname())
    if tz_str.lower() in ["pdt", "pst"]:
        tz = ZoneInfo("America/Los_Angeles")
    elif tz_str.lower() in ["utc"]:
        tz = ZoneInfo("Zulu")
    else:
        tz = ZoneInfo(tz_str)
    return tz

def localize_dt(dt: datetime|str|int,
                return_format: str="iso",
                tz: ZoneInfo=get_current_tz())->str|int|None:
    if isinstance(dt, datetime):
        res = dt.astimezone(tz)
    elif isinstance(dt, str):
        res =  datetime.fromisoformat(dt).astimezone(tz)
    elif isinstance(dt, int) and len(str(dt)) == 10:
        res = datetime.fromtimestamp(dt).astimezone(tz)
    else:
        raise Exception(f"{dt} is not a valid date format")

    if return_format == "iso":
        return res.isoformat()
    elif return_format == "ts":
        return int(res.timestamp())
    else:
        return res.isoformat()
