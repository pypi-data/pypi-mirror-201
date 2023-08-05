import json
import requests


class BudibaseClient:
    def __init__(self, service_config):
        self.budibase_url = service_config['budibase_url']
        self.budibase_api_key = service_config['budibase_api_key']
        self.budibase_apps = []
        self.budibase_selected_app = ""
        self.budibase_app_tables = []

        self.budibase_request_headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-budibase-app-id": self.budibase_selected_app,
            "x-budibase-api-key": self.budibase_api_key
        }

        url = f"{self.budibase_url}/api/public/v1/applications/search"

        response = requests.post(url, headers=self.budibase_request_headers)

        self.budibase_apps = json.loads(response.text)["data"]

    def select_app(self, app_name):
        app = [app for app in self.budibase_apps if app["name"] == app_name and app["status"] == "published"]
        if len(app) != 1:
            exit() #TODO: error-handling

        app = app[0]

        self.budibase_selected_app = app["_id"]
        self.budibase_request_headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-budibase-app-id": self.budibase_selected_app,
            "x-budibase-api-key": self.budibase_api_key
        }

        url = f"{self.budibase_url}/api/public/v1/tables/search"

        response = requests.post(url, headers=self.budibase_request_headers)

        self.budibase_tables = json.loads(response.text)["data"]

    def get_tables(self):
        return self.budibase_tables
    
    def get_table(self, table_name):
        table = [table for table in self.budibase_tables if table["name"] == table_name]
        if len(table) != 1:
            exit()
        return table[0]

    def get_database_structure(self):
        database = {}
        database["tables"] = self.get_tables()
        database["name"] = self.
        tables = self.get_tables()
        table_structure = []
        for table in tables:
            table_structure.append({
                "name": table["name"],
                "columns": table["columns"]
            })
        return table_structure

    def upload_data_to_budibase(self, row, table_name):        
        if not self.budibase_selected_app:
            exit() #TODO: error-handling
        table = [table for table in self.budibase_tables if table["name"] == table_name]
        if len(table) != 1:
            exit() #TODO: error-handling
        
        table = table[0]
        table_id = table["_id"]

        # if no _id in data => insert data into database
        if not "_id" in row:

            url = f"{self.budibase_url}/api/public/v1/tables/{table_id}/rows/"
            response = requests.put(url, json=row, headers=self.budibase_request_headers)

        else: 

            row_id = row["_id"]
            url = f"{self.budibase_url}/api/public/v1/tables/{table_id}/rows/{row_id}"
            response = requests.put(url, json=row, headers=self.budibase_request_headers)

        print(json.loads(response.text)["data"])

    def get_rows_from_table(self, table_name):
        if not self.budibase_selected_app:
            exit() #TODO: error-handling
        table = [table for table in self.budibase_tables if table["name"] == table_name]
        if len(table) != 1:
            exit() #TODO: error-handling
        table = table[0]
        table_id = table["_id"]
        url = f"{self.budibase_url}/api/public/v1/tables/{table_id}/rows/search"
        
        response = requests.post(url, headers=self.budibase_request_headers)

        rows = json.loads(response.text)["data"]
        return rows

    def delete_row_from_budibase(self, row, table_name):        
        if not self.budibase_selected_app:
            exit() #TODO: error-handling
        table = [table for table in self.budibase_tables if table["name"] == table_name]
        if len(table) != 1:
            exit() #TODO: error-handling
        if not "_id" in row:
            exit() #TODO: error handling
        
        table = table[0]
        table_id = table["_id"]
                    
        row_id = row["_id"]
        url = f"{self.budibase_url}/api/public/v1/tables/{table_id}/rows/{row_id}"
        response = requests.delete(url, headers=self.budibase_request_headers)

        print(json.loads(response.text)["data"])