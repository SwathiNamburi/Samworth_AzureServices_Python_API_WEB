import configparser


class ConfigReader:

    config = configparser.ConfigParser()

    config.read("config/env_config.ini")

    @classmethod
    def get_api_config(
            cls,
            key
    ):

        return cls.config.get(
            "API",
            key
        )

    @classmethod
    def get_ui_config(
            cls,
            key
    ):

        return cls.config.get(
            "UI",
            key
        )