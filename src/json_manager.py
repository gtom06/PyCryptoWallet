import json
from datetime import datetime, timedelta, timezone

class JsonFileManager:
    @staticmethod
    def load_json(filename, default_value):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            JsonFileManager.save_json(filename, default_value)
            return default_value

    @staticmethod
    def save_json(filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def should_update_coins_list(coins_list_data, update_interval_days):
        last_requested_date = coins_list_data.get("last_requested_date")

        if not last_requested_date or not isinstance(last_requested_date, str):
            return True

        try:
            last_requested_date = datetime.fromisoformat(last_requested_date)
            update_threshold = datetime.now(timezone.utc) - timedelta(days=update_interval_days)
            return last_requested_date < update_threshold
        except ValueError:
            return True
