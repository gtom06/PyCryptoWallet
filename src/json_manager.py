from datetime import datetime, timedelta, timezone
import json
import json

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
    def save_append_json(filename, data):
        try:
            with open(filename, "r") as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}
        existing_data.update(data)
        with open(filename, "w") as file:
            json.dump(existing_data, file, indent=4)


