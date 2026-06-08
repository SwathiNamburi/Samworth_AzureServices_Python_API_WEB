from datetime import datetime, timedelta


class DataGenerator:

    @staticmethod
    def generate_event_id():

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        return f"evt-ing-{timestamp}"

    @staticmethod
    def generate_current_timestamp():

        return datetime.utcnow().strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

    def generate_past_timestamp(minutes=5):
        past_time = (
                datetime.utcnow() - timedelta(minutes=minutes)
        )

        return past_time.strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )