# SmartSheetFunctions API Python Library

This Python library provides several easy-to-use methods for interacting with the SmartSheet API. The SmartSheet class is used to interact with sheets in a SmartSheet account, while the SmartFolder class is used to interact with folders.

## Usage

1. Import the library:

   ```python
   from smartsheet_api import SmartSheet, SmartFolder, create_smartsheet

2. Create a SmartSheet object by providing a sheet ID and an API token:
    ```python
    sheet_id = "your-sheet-id"
    api_token = "your-api-token"
    ss = SmartSheet(sheet_id, api_token)

3. Call any of the available methods on the SmartSheet object:
    ```python
    # Get the sheet
    sheet = ss.get_sheet()

    # Get the IDs of all the columns in the sheet
    column_ids = ss.sheet_column_ids()

    # Get the values of specified columns for all rows in the sheet
    column_names = ["Column 1", "Column 2", "Column 3"]
    column_values = ss.get_column_values(column_names)

    # Add a row to the sheet
    payload = {"cells": [{"columnId": column_ids[0], "value": "Value 1"}, {"columnId": column_ids[1], "value": "Value 2"}]}
    ss.add_smartsheet_row(payload)

    # Update a cell in a row
    row_id = "your-row-id"
    column_id = "your-column-id"
    value = "new-value"
    ss.update_cell_text(row_id, column_id, value)

    # Upload an attachment to a row
    row_id = "your-row-id"
    attachment = "path/to/attachment.pdf"
    filename = "attachment.pdf"
    ss.upload_attachment(row_id, attachment, filename)

4. Create a SmartFolder object by providing a folder ID and an API token:
    ```python
    folder_id = "your-folder-id"
    api_token = "your-api-token"
    sf = SmartFolder(folder_id, api_token)

5. Call any of the available methods on the SmartFolder object:
    ```python
        # Get the folder
    folder = sf.get_folder()

    # Create a subfolder in the folder
    name = "subfolder-name"
    sf.create_folder(name)

6. Alternatively, create a new sheet in a folder using the create_smartsheet method:
    ```python
    folder_id = "your-folder-id"
    api_token = "your-api-token"
    name = "new-sheet-name"
    create_smartsheet(folder_id, api_token, name)


## Methods

### SmartSheet Class
#### __init__(self, sheet_id, api_token)
Constructor for the SmartSheet class. Takes in a sheet ID and an API token.

#### get_sheet(self)
Retrieves the sheet from the SmartSheet API.

#### add_smartsheet_row(self, payload)
Adds a new row to the sheet.

#### delete_smartsheet_row(self, row_id)
Deletes a row from the sheet.

#### sheet_column_ids(self)
Retrieves the IDs of all the columns in the sheet.

#### sheet_row_ids(self)
Retrieves the IDs of all the rows in the sheet.

#### get_column_info(self, column_id)
Retrieves information about a column.

#### get_column_values(self, column_name_list)
Retrieves all the values from a given column.

#### `update_cell_text(self, row_id, column_id, value)`

Updates the text in a cell.

#### `column_names(self)`

Retrieves the names of all the columns in the sheet.

#### `get_sheet_row(self, row_id)`

Retrieves a specific row from the sheet.

#### `update_row(self, payload)`

Updates a row in the sheet.

#### `upload_attachment(self, row_id, attachment, filename)`

Uploads an attachment to a specific row in the sheet.

#### `get_sheet_attachments(self)`

Retrieves all the attachments in the sheet.

#### `update_attachment(self, attachment, filename, attachment_id)`

Updates an attachment in the sheet.

#### `get_attachment_url(self, attachment_id)`

Retrieves the URL of an attachment.

#### `list_attachment_versions(self, attachment_id)`

Retrieves all the versions of an attachment.

#### `delete_attachment(self, attachment_id)`

Deletes an attachment from the sheet.

#### `column_dictionary(self, column_names, column_ids)`

Creates a dictionary that maps column names to their corresponding IDs.

#### `add_columns(self, payload)`

Adds one or more columns to the sheet.

### SmartFolder Class

#### `__init__(self, folder_id, api_token)`

Constructor for the `SmartFolder` class. Takes in a folder ID and an API token.

#### `get_folder(self)`

Retrieves the folder from the SmartSheet API.

#### `create_folder(self, name)`

Creates a subfolder in the folder.

### `create_smartsheet(folder_id, api_token, name)`

Creates a new sheet in a folder.


## Contributors

- __**Derek Bantel**__ - Main contributor

