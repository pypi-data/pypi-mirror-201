import importlib.util
import json
from pathlib import Path
from typing import Union

import pandas as pd
import yaml
from pandera.errors import SchemaErrors

from . import settings
from .app_logger import log
from .assets.constants import FILE_EXTENSIONS

module_name = "rules"
module_path = settings.DEFAULT_VALIDATION_RULES
validation_output_columns = settings.DEFAULT_VALIDATION_COLUMNS


class VirusEngine:
    """
    Object facilitate to get the mapping for dataset and schema, and validate the dataset with schema
    """

    def __init__(self, config_path: str = settings.DEFAULT_DATASET_RULES):
        # Current working directory is always at datasets project dir
        self.cwd = Path.cwd()
        self.schema_config_path = self.cwd / config_path

    def _get_schema_mapping(self):
        # There are only 2 file extensions supported: .yaml and .json
        if self.schema_config_path.suffix == ".yaml":
            with open(str(self.schema_config_path), "r") as f:
                schema_mapping = yaml.safe_load(f)
        elif self.schema_config_path.suffix == ".json":
            with open(str(self.schema_config_path), "r") as f:
                schema_mapping = json.load(f)
        else:
            raise ValueError("File format not supported")
        return schema_mapping

    def _get_schema(self, src: Union[str, Path]):
        schema_mapping = self._get_schema_mapping()
        try:
            schema_name = schema_mapping[src]
        except KeyError as ke:
            log.error(f"Schema not found for {src}")
            log.warn(ke)
            schema_name = False
        return schema_name

    def retrieve_dataset(self, src: Union[str, Path], **kwargs):
        real_paths = self.cwd.glob(src)
        ## Checks if the generator is empty
        try:
            _ = next(real_paths)
        except StopIteration:
            log.warning(f"Path does not exist: {src}")

        if src.endswith(FILE_EXTENSIONS):
            glob_path = src
        else:
            glob_path = src + "**/*.csv"
        for each_file in (self.cwd).glob(glob_path):
            log.info(f"Reading file: {each_file}")
            yield each_file, pd.read_csv(each_file, low_memory=False, **kwargs)

    def validate_with_schema(
        self, schema_name: str, df: pd.DataFrame
    ) -> pd.DataFrame:
        # create a module spec
        spec = importlib.util.spec_from_file_location(module_name, module_path)

        # create a module object
        module = importlib.util.module_from_spec(spec)

        # load the module
        spec.loader.exec_module(module)

        rule_class = getattr(module, schema_name)

        try:
            _ = rule_class.validate(df, lazy=True)
            return pd.DataFrame(columns=validation_output_columns)
        except SchemaErrors as err:
            return err.failure_cases.drop(columns=["index"]).drop_duplicates()
