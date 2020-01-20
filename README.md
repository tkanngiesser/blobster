# Blobster
> A convenient way to manage your Azure Data Storage with Python.


## Install

`pip install blobster`

## How to use

### Loading credentials
Edit the `blob_storage_credentials.json` and enter your blob storage `account` and `key` information.

```python
azure_blob_storage = AzureBlobStorage(credential_file='blob_storage_credentials.json')
```

### Connnect to Azure Blob Storage
Once the credentials have been loaded with `load_credentials` 
a connection can be established by calling the `connect`method.

```python
azure_blob_storage.connect()
```
