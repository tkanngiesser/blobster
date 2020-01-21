# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['Datapipe', 'step_rename_column_headers', 'step_generate_data_profile']

# Cell
import json
import os
import glob
import io
import re
import zipfile
from datetime import date
from datetime import datetime
from functools import wraps
from pathlib import Path
import logging
import numpy as np
import pandas as pd
import pandas_profiling
import pandas_flavor as pf
import jdc

class Datapipe:
    def __init__(self, service=None, entity=None, meta=None, runtime=None):
        self.service: str = service
        self.runtime: str = runtime
        self.entity: str = entity
        self.meta = meta
        self.today = datetime.today().strftime("%Y-%m-%d")
        self.profile_report = None

datapipe = Datapipe()

# Cell
@pf.register_dataframe_method
def step_rename_column_headers(df):
    """Rename columns (name_raw -> name_clean)"""
    column_names_mapping = dict(
        zip(
            datapipe.meta["name_raw"].values,
            datapipe.meta["name_clean"].values,
        )
    )
    df = df.rename_columns(column_names_mapping)
    return df

# Cell
@pf.register_dataframe_method
def step_generate_data_profile(df, mode=None, title=None, file_path=None):
    """generates data profile report"""
    title = title
    profile_report = df.profile_report(title=title)
    if save_to:
        file_name = f"{title}.html"
        profile_report.to_file(output_file=os.path.join(file_path, file_name))
    return self.profile_report

# Cell
@pf.register_dataframe_method
def _get_non_unique_ids(self, df, id_col):
    """Return all non-unique ids"""
    return df[
        df[id_col].isin(df[id_col].value_counts()[df[id_col].value_counts() > 2].index)
    ]