# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['AzureBlobStorage']

# Cell
import pandas as pd
import fastcore
from fastcore.foundation import *
import azure
from azure.storage.blob import BlockBlobService

class AzureBlobStorage:
    def __init__(self, credential_file):

        account, key = self.load_credentials(credential_file)

        if account:
            self.account = account
        else:
            self.account = account
        if key:
            self.key = key
        else:
            self.key = key
        self.is_connected = False
        self.blob_service = None

# Cell
@patch
def load_credentials(self:AzureBlobStorage, credential_file):
    """Load Azure Blob Storage credentials from file"""
    credentials = pd.read_json(credential_file)
    return list(credentials['account'].values)[0], list(credentials['key'].values)[0]

# Cell
@patch
def connect(self:AzureBlobStorage):
    """Connect to Azure Blob Storage"""
    self.blob_service = BlockBlobService(
        account_name=self.account, account_key=self.key
    )
    self.is_connected = True

# Cell
@patch
def list_all_containers(self:AzureBlobStorage):
    """Return all container names from blob storage"""
    container_names = []
    containers = self.blob_service.list_containers()
    for container in containers:
        container_names.append(container.name)
    return container_names


# Cell
@patch
def delete_container(self:AzureBlobStorage, container_name):
    """Delete specified container"""
    self.blob_service.delete_container(
        container_name=container_name, fail_not_exist=False
    )

# Cell
@patch
def make_container(self:AzureBlobStorage, container_name):
    """Make specified container (if it does not exist)"""
    try:
        self.blob_service.list_blobs(container_name)
    except:
        # assumption container does not exist and must be created
        self.blob_service.create_container(container_name)

# Cell
@patch
def list_all_blobs(self:AzureBlobStorage, container_name):
    """List all blobs in a container"""
    blob_names = []
    blobs = self.blob_service.list_blobs(container_name)
    for blob in blobs:
        blob_names.append(blob.name)
    return blob_names

# Cell
@patch
def delete_blobs(self:AzureBlobStorage, container_name):
    """Delete all blobs in specified container"""
    try:
        blobs = self.blob_service.list_blobs(container_name)
    except azure.common.AzureMissingResourceHttpError:
        pass
    else:
        for blob in blobs:
            self.blob_service.delete_blob(container_name, blob.name)

# Cell
@patch
def delete_blob(self:AzureBlobStorage, container_name, blob_name):
    """Delete all blobs in specified container"""
    self.blob_service.delete_blob(container_name, blob_name)

# Cell
@patch
def file_to_blob(self:AzureBlobStorage, container_name, blob_name, file_name):
    self.blob_service.create_blob_from_path(container_name, blob_name, file_name)

# Cell
@patch
def folder_to_container(self:AzureBlobStorage, folder_path, container_name=None):
    """Upload all files in a folder to a specified container"""
    files_in_folder = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    [self.file_to_blob(container_name=container_name, blob_name=f, file_name=join(folder_path, f)) for f in files_in_folder]

# Cell
@patch
def df_to_blob(self:AzureBlobStorage, container_name, blob_name, df):
    """Write Pandas dataframe to blob"""
    extension = blob_name.split(".")[-1]
    output = io.StringIO()
    if extension == "json":
        output = df.to_json()
    elif extension == "csv":
        output = df.to_csv(index=False, index_label=False)
    elif extension == "parquet":
        output = io.BytesIO()
        output = df.to_parquet()
    self.blob_service.create_blob_from_text(container_name, blob_name, output)

# Cell
@patch
def blob_to_df(self:AzureBlobStorage, container_name, blob_name):
    """Load blob and return Pandas dataframe"""
    extension = blob_name.split(".")[-1]

    with io.BytesIO() as input_stream:
        self.blob_service.get_blob_to_stream(
            container_name=container_name, blob_name=blob_name, stream=input_stream
        )

        input_stream.seek(0)
        if extension == "csv":
            df = pd.read_csv(input_stream, lineterminator="\n")
        elif extension == "json":
            df = pd.read_json(input_stream)
        elif extension == "parquet":
            df = pd.read_parquet(input_stream)
        elif extension == "xlsx":
            df = pd.read_excel(input_stream)
    return df


# Cell
@patch
def blobs_to_df(self:AzureBlobStorage, container_name):
    """Load blobs and write to Pandas dataframe"""
    dfs = []
    generator = self.blob_service.list_blobs(container_name)
    for blob in generator:
        df = self.blob_to_df(container_name, blob.name)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

# Cell
@patch
def copy_blobs_to_other_container(self:AzureBlobStorage, source_container_name, destination_container_name, delete_after_copy=False):
    """Copy all blobs in one container to another container"""
    generator = self.blob_service.list_blobs(source_container_name)
    for blob in generator:
        blob_url = self.blob_service.make_blob_url(source_container_name, blob.name)
        self.blob_service.copy_blob(destination_container_name, blob.name, blob_url)
    if delete_after_copy:
        for blob in generator:
            self.blob_service.delete_blob(source_container_name, blob.name)


# Cell
@patch
def download_blobs_from_container(self:AzureBlobStorage, container_name, destination_path):
    """Download all blobs from container"""
    generator = self.blob_service.list_blobs(container_name)

    path = Path(download_path)

    zf = zipfile.ZipFile(
        path / f"{container_name}.zip", mode="w", compression=zipfile.ZIP_DEFLATED
    )

    for blob in generator:
        b = self.blob_service.get_blob_to_bytes(container_name, blob.name)
        zf.writestr(blob.name, b.content)

    zf.close()