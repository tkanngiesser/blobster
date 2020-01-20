# Blobster 🦞
> A convenient way to manage your Azure Data Storage with Python.


## Install

`pip install blobster`

## How to use

### Import
`from blobster import *`

### Loading credentials

```python
azure_blob_storage = AzureBlobStorage(account='your_account_string', key='your_key_string')
```

### Connnect to Azure Blob Storage

```python
azure_blob_storage.connect()
```
