from datetime import datetime

# Convert to unix timestamp in seconds
def convert_datetime(date: str):
	return int(datetime.fromisoformat(date.replace("Z","+00:00")).timestamp())
