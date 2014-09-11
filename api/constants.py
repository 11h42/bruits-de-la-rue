import datetime

TODAY = datetime.datetime.today()
TOMORROW = TODAY + datetime.timedelta(days=1)
YESTERDAY = TODAY - datetime.timedelta(days=1)
AFTER_TOMORROW = TOMORROW + + datetime.timedelta(days=1)

TODAY_ISO = TODAY.isoformat()
TOMORROW_ISO = TOMORROW.isoformat()
YESTERDAY_ISO = YESTERDAY.isoformat()
AFTER_TOMORROW_ISO = AFTER_TOMORROW.isoformat()