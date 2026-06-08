import json
import time

from azure.cosmos import CosmosClient, exceptions
from utilities.allure_report import AllureReport
from utilities.config_reader import ConfigReader


class CosmosDBHelper:

    def __init__(self):

        self.account_url = ConfigReader.get_api_config(
            "COSMOS_ACCOUNT_URL"
        )

        self.account_key = ConfigReader.get_api_config(
            "COSMOS_ACCOUNT_KEY"
        )

        self.database_id = ConfigReader.get_api_config(
            "COSMOS_DATABASE_ID"
        )

        self.database_id_wrong = ConfigReader.get_api_config(
            "COSMOS_DATABASE_ID_WRONG"
        )

        self.collection_id = ConfigReader.get_api_config(
            "COSMOS_COLLECTION_ID"
        )

        self.client = CosmosClient(
            url=self.account_url,
            credential=self.account_key
        )

        self.database = self.client.get_database_client(
            self.database_id
        )

        self.container = self.database.get_container_client(
            self.collection_id
        )

        self.database_wrong_database = self.client.get_database_client(
            self.database_id_wrong
        )

        self.invalid_container = self.database_wrong_database.get_container_client(
            self.collection_id
        )

    # ====================================================
    # GET MESSAGE FROM COSMOS DB USING EVENT ID
    # ====================================================

    def get_message_by_event_id(
            self,
            event_id,
            retry_count=10,
            retry_wait=5
    ):

        print(
            f"Fetching Cosmos DB message "
            f"for Event ID: {event_id}"
        )

        query = """
        SELECT * FROM c
        WHERE c.id = @eventId
        """

        parameters = [
            {
                "name": "@eventId",
                "value": event_id
            }
        ]

        try:

            for attempt in range(retry_count):

                results = self.container.query_items(
                    query=query,
                    parameters=parameters,
                    enable_cross_partition_query=True
                )

                records = list(results)

                if records:

                    matched_document = records[0]

                    print(
                        "Cosmos DB document found successfully"
                    )

                    print(
                        json.dumps(
                            matched_document,
                            indent=4
                        )
                    )

                    AllureReport.attach_text(
                        json.dumps(
                            matched_document,
                            indent=4
                        ),
                        "Cosmos DB Matched Document"
                    )

                    return matched_document

                print(
                    f"No document found. "
                    f"Retrying in {retry_wait} seconds..."
                )

                time.sleep(retry_wait)

            raise AssertionError(
                f"No Cosmos DB document found "
                f"for Event ID: {event_id}"
            )

        except exceptions.CosmosHttpResponseError as err:

            raise Exception(
                f"Cosmos DB Connection Failure: "
                f"{err.message}"
            )



    def verify_cosmodb_exception_failure(
            self,
            event_id,
            retry_count=10,
            retry_wait=5
    ):

        print(
            f"Fetching Cosmos DB message "
            f"for Event ID: {event_id}"
        )

        query = """
        SELECT * FROM c
        WHERE c.id = @eventId
        """

        parameters = [
            {
                "name": "@eventId",
                "value": event_id
            }
        ]

        try:

            for attempt in range(retry_count):
                results = self.container.query_items(
                    query=query,
                    parameters=parameters,
                    enable_cross_partition_query=True
                )
                raise Exception(
                    f"Cosmos DB Connection found is not expected: "
                )

        except exceptions.CosmosHttpResponseError as err:
            AllureReport.attach_text(f"Cosmos DB Connection Failure","Validate Cosmo DB Failure: " f"{err.message}")



    def verify_invalid_cosmodb_exception_failure(
            self,
            event_id,
            retry_count=10,
            retry_wait=5
    ):

        print(
            f"Fetching Cosmos DB message "
            f"for Event ID: {event_id}"
        )

        query = """
        SELECT * FROM c
        WHERE c.id = @eventId
        """

        parameters = [
            {
                "name": "@eventId",
                "value": event_id
            }
        ]

        try:

            for attempt in range(retry_count):
                results = self.invalid_container.query_items(
                    query=query,
                    parameters=parameters,
                    enable_cross_partition_query=True
                )
                raise Exception(
                    f"Cosmos DB Connection found is not expected: "
                )

        except exceptions.CosmosHttpResponseError as err:
            AllureReport.attach_text(f"Cosmos DB Connection Failure","Validate Cosmo DB Failure: " f"{err.message}")