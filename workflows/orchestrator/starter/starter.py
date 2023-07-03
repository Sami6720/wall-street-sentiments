from datetime import datetime
import pytz


def get_today() -> str:
    """Get today's date in the format of MM-DD-YYYY.

    return: Today's date.
    rtype: str
    """
    timezone = pytz.timezone('America/New_York')
    current_time = datetime.now(timezone)
    today = current_time.strftime('%m-%d-%Y')

    return today
