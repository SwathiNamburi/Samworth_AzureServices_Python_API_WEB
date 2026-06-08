import json
import csv
import pandas as pd
import xml.etree.ElementTree as ET
import os


class FileReader:

    def __init__(self):

        self.base_path = os.path.join(
            os.getcwd(),
            "testdata"
        )

    def read_json(self, file_name):

        path = os.path.join(
            self.base_path,
            "json_files",
            file_name
        )

        with open(path, 'r') as file:

            return json.load(file)

    def read_csv(self, file_name):

        path = os.path.join(
            self.base_path,
            "csv_files",
            file_name
        )

        data_list = []

        with open(path, mode='r') as file:

            reader = csv.DictReader(file)

            for row in reader:
                data_list.append(row)

        return data_list

    def read_excel(
            self,
            file_name,
            sheet_name=0
    ):

        path = os.path.join(
            self.base_path,
            "excel_files",
            file_name
        )

        df = pd.read_excel(
            path,
            sheet_name=sheet_name
        )

        return df.to_dict(orient='records')

    def read_xml(self, file_name):

        path = os.path.join(
            self.base_path,
            "xml_files",
            file_name
        )

        tree = ET.parse(path)

        root = tree.getroot()

        return root