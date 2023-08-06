# Declare smartsheet functions
import requests
import json
#####################

#Initialize smartsheet class
class SmartSheet():

    def __init__(self, sheet_id, api_token):
        self.api_url =  "https://api.smartsheet.com/2.0/"
        self.api_token = api_token
        self.std_header =  {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}  
        self.sheet_id = sheet_id
    

    def get_sheet(self):
        api_url = f"{self.api_url}sheets/{self.sheet_id}"
        r = requests.get(api_url, headers=self.std_header)
        if r.status_code != 200:
            print(r.status_code, r.text)
        return r.json()


    def add_smartsheet_row(self, payload):
        api_url = f"{self.api_url}sheets/{self.sheet_id}/rows"
        payload = json.dumps(payload)
        r = requests.post(api_url, headers=self.std_header, data=payload)
        if r.status_code != 200:
            print(r.status_code, r.text)
        return r.json()


    def delete_smartsheet_row(self, row_id):
        api_url = f"{self.api_url}sheets/{self.sheet_id}/rows?ids={row_id}"
        r = requests.delete(api_url, headers=self.std_header)
        if r.status_code != 200:
            print(r.status_code, r.text)
        return r.json()


    def sheet_column_ids(self):
        sheet = self.get_sheet()
        col_ids = []
        for columns in sheet["columns"]:
            col_id = columns["id"]
            col_ids.append(col_id)
        return col_ids


    def sheet_row_ids(self):
        sheet = self.get_sheet()
        row_ids = []
        for row in sheet["rows"]:
            row_id = row["id"]
            row_ids.append(row_id)
        return row_ids


    def get_column_info(self, columnid):
        api_url = f"{self.api_url}sheets/{self.sheet_id}/columns/{columnid}"
        r = requests.get(api_url, headers=self.std_header)
        if r.status_code != 200:
            print(r.status_code, r.text)
        return r.json()
    
    
    def get_column_values(self, column_name_list):
        self.get_sheet() 
        row_ids = self.sheet_row_ids()
        col_names = self.column_names() 
        col_ids = self.sheet_column_ids()
        num_cols = len(col_ids)
        col_range = list(range(num_cols))
        col_index_dict = create_dictionary_fr_list(col_names, col_range)
        master_data_dict = dict.fromkeys(column_name_list)#create dictionary of with keys of column names
        for key in master_data_dict.keys():
            master_data_dict[key] = []

        for key in list(col_index_dict.keys()):#remove columns that are not needed from dictionary
            if key not in column_name_list:
                col_index_dict.pop(key)

        for row_id in row_ids:
            data = self.get_sheet_row(row_id)
            for col_name, col_index in col_index_dict.items():
                try:
                    master_data_dict[col_name].append(data["cells"][col_index]["value"])
                except KeyError:
                    master_data_dict[col_name].append("")
        
        return master_data_dict


    def update_cell_text(self, row_id, column_id, value):
        api_url = f"{self.api_url}sheets/{self.sheet_id}/rows"
        payload = json.dumps([{"id": row_id, "cells": [{"columnId": column_id, "value": value}]}])
        r = requests.put(api_url, headers=self.std_header, data=payload)
        if r.status_code != 200:
            print(r.status_code, r.text)
        return r.json()


    def column_names(self):
        sheet = self.get_sheet()
        column_names = []
        for columns in sheet["columns"]:
            column_names.append(columns["title"])
        return column_names


    def get_sheet_row(self, row_id):
        api_url = f"{self.api_url}sheets/{self.sheet_id}/rows/{row_id}"
        r = requests.get(api_url, headers=self.std_header)
        if r.status_code != 200:
            print(r.status_code, r.text)
        return r.json()


    def update_row(self, payload):
        api_url = f"{self.api_url}sheets/{self.sheet_id}/rows"
        payload = json.dumps(payload)
        r = requests.put(api_url, headers=self.std_header, data=payload)
        if r.status_code != 200:
            print(r.status_code, r.text)
        return r.json()


    def upload_attachment(self, row_id, attachment, filename):
        file_header = {"Authorization": f"Bearer {self.api_token}", "Content-Disposition": f"attachment; filename={filename}", "Content-Type": "application/pdf", "Content-Lenght": ""}
        api_url = f"{self.api_url}sheets/{self.sheet_id}/rows/{row_id}/attachments"
        with open(attachment, 'rb') as f:
            data = f.read()
            r = requests.post(api_url, headers=file_header, data=data)
        if r.status_code != 200:
            print(r.status_code, r.text)
        return r.json()


    def get_sheet_attachments(self):
        api_url = f"{self.api_url}sheets/{self.sheet_id}/attachments"
        r = requests.get(api_url, headers=self.std_header)
        if r.status_code != 200:
            print(r.status_code, r.text)
        return r.json()


    def update_attachment(self, attachment, filename, attachmentId):
        file_header = {"Authorization": f"Bearer {self.api_token}", "Content-Disposition": f"attachment; filename={filename}", "Content-Type": "application/pdf", "Content-Lenght": ""}
        api_url = f"{self.api_url}sheets/{self.sheet_id}/attachments/{attachmentId}/versions"
        with open(attachment, 'rb') as f:
            data = f.read()
            r = requests.post(api_url, headers=file_header, data=data)
        if r.status_code != 200:
            print(r.status_code, r.text)
        return r.json()


    def get_attachment_url(self, attachment_id):
        api_url = f"{self.api_url}sheets/{self.sheet_id}/attachments/{attachment_id}"
        r = requests.get(api_url, headers=self.std_header)
        if r.status_code != 200:
            print(r.status_code, r.text)
        download_info = r.json()
        download_url = download_info["url"]
        return download_url 


    def list_attachment_versions(self, attachment_id):
        api_url = f"{self.api_url}sheets/{self.sheet_id}/attachments/{attachment_id}/versions"
        r = requests.get(api_url, headers=self.std_header)
        if r.status_code != 200:
            print(r.status_code, r.text)
        return r.json()


    def delete_attachment(self, attachment_id):
        api_url = f"{self.api_url}sheets/{self.sheet_id}/attachments/{attachment_id}"
        r = requests.delete(api_url, headers=self.std_header)
        if r.status_code != 200:
            print(r.status_code, r.text)

    
    def column_dictionary(self, column_names, column_ids):
        #creates a dictionary that allows referencing columns by name to get id
        dictionary = dict(zip(column_names, column_ids))
        return dictionary

    
    def add_columns(self, payload):
        api_url = f"{self.api_url}sheets/{self.sheet_id}/columns"
        payload = json.dumps(payload)
        r = requests.post(api_url, headers=self.std_header, data=payload)
        if r.status_code != 200:
            print(r.status_code, r.text)
        return r.json()


class SmartFolder():

    def __init__(self, folderid, api_token):
        self.api_url =  "https://api.smartsheet.com/2.0/folders"
        self.api_token = api_token
        self.std_header =  {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}  
        self.folderid = folderid
    
    
    def get_folder(self):
        api_url = f"{self.api_url}/{self.folderid}"
        r = requests.get(api_url, headers=self.std_header)
        if r.status_code != 200:
            print(r.status_code, r.text)
        return r.json()
    

    def create_folder(self, name):
        api_url = f"{self.api_url}/{self.folderid}/folders" 
        r = requests.post(api_url, headers=self.std_header, data = {"name": name})
        if r.status_code != 200:
            print(r.status_code, r.text)


def create_smartsheet(folderid, api_token, name):
    api_url = f"https://api.smartsheet.com/2.0/folders/{folderid}/sheets"
    header =  {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
    payload = {"name": name, "columns": [{"title": "Primary Column", "primary": True, "type": "TEXT_NUMBER"}]}
    payload = json.dumps(payload)
    r = requests.post(api_url, headers=header, data = payload)
    if r.status_code != 200:
        print(r.status_code, r.text)


def create_dictionary_fr_list(first_list, second_list):
    #creates a dictionary that allows referencing columns by name to get id
    dictionary = dict(zip(first_list, second_list))
    return dictionary
#################