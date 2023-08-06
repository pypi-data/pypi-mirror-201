# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Common helper class for reading AzureML MLTable"""

import logging
import os
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

import mltable
import pandas as pd
from mltable import MLTable

from azure.ai.ml.exceptions import UserErrorException

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


@dataclass
class ImageDataFrameConstants:
    """
    A class to represent constants for image dataframe
    """

    DEFAULT_LABEL_COLUMN_NAME = "label"
    COLUMN_PROPERTY = "Column"
    IMAGE_COLUMN_PROPERTY = "_Image_Column:Image_"
    PORTABLE_PATH_COLUMN_NAME = "PortablePath"
    DEFAULT_IMAGE_COLUMN_NAME = "image_url"


def remove_leading_backslash(image_path: Union[str, Path]) -> str:
    """Utility method to remove the leading backslash from the image path
    :param image_path: Path of the image
    :type image_path: string

    :return: image path without leading backslash
    :rtype: str
    """
    if not image_path:
        return image_path
    if not isinstance(image_path, str):
        image_path = str(image_path)
    return image_path if image_path[0] != "/" else image_path[1:]


class DownloadManager:
    """A helper class that reads MLTable, download images and prepares the dataframe"""

    def __init__(
        self,
        mltable_path: str,
        ignore_data_errors: bool = False,
        image_column_name: str = ImageDataFrameConstants.DEFAULT_IMAGE_COLUMN_NAME,
        label_column_name: str = ImageDataFrameConstants.DEFAULT_LABEL_COLUMN_NAME,
        download_files: bool = True,
    ):

        """Constructor - This reads the MLTable and downloads the images that it contains.

        :param mltable_path: azureml MLTable path
        :type mltable_path: str
        :param ignore_data_errors: Setting this ignores and files in the dataset that fail to download.
        :type ignore_data_errors: bool
        :param image_column_name: The column name for the image file.
        :type image_column_name: str
        :param label_column_name: The column name for the labels.
        :type label_column_name: str
        :param download_files: Flag to download files or not.
        :type download_files: bool
        """
        self._loaded_mltable = DownloadManager._load_mltable(mltable_path)
        self._images_df = self._loaded_mltable.to_pandas_dataframe()
        self.image_column_name = image_column_name
        self._images_df[ImageDataFrameConstants.PORTABLE_PATH_COLUMN_NAME] = self._images_df[image_column_name]
        DownloadManager._validate_columns(self._images_df, [image_column_name, label_column_name])
        self._data_dir = DownloadManager._get_data_dir()

        if download_files:
            DownloadManager._download_image_files(self._loaded_mltable, image_column_name)

        # drop rows for which images are not downloaded
        if download_files and ignore_data_errors:
            missing_file_indices = []
            for index in self._images_df.index:
                full_path = self._get_image_full_path(index)
                if not os.path.exists(full_path):
                    missing_file_indices.append(index)
                    msg = "File not found. Since ignore_data_errors is True, this file will be ignored."
                    logger.warning(msg)
            self._images_df.drop(missing_file_indices, inplace=True)
            self._images_df.reset_index(inplace=True, drop=True)

        # Put absolute path in the image_url column
        self._images_df[image_column_name] = self._images_df[ImageDataFrameConstants.PORTABLE_PATH_COLUMN_NAME].apply(
            lambda row: os.path.join(self._data_dir, remove_leading_backslash(row))
        )

    @staticmethod
    def _load_mltable(mltable_path: str) -> MLTable:
        """Load the mltable into memory.

        :param mltable_path: MLTable containing dataset URI
        :type mltable_path: str
        :return: The loaded mltable object.
        :rtype: MLTable
        """

        dataset = None
        if mltable_path is None:
            raise UserErrorException(f"Mltable path is not provided, is {mltable_path}.")
        try:
            dataset = mltable.load(mltable_path)
        except (UserErrorException, ValueError) as e:
            msg = f"MLTable input is invalid. {e}"
            raise UserErrorException(msg)
        except Exception as e:
            msg = f"Error in loading MLTable. {e}"
            raise Exception(msg)  # pylint: disable=broad-exception-raised

        return dataset

    def _get_image_full_path(self, index: int) -> str:
        """Return the full local path for an image.

        :param index: index
        :type index: int
        :return: Full path for the local image file
        :rtype: str
        """
        rel_path = self._images_df[self.image_column_name].iloc[index]
        abs_path = os.path.join(self._data_dir, str(rel_path))
        return abs_path

    @staticmethod
    def _get_data_dir() -> str:
        """Get the data directory to download the image files to.

        :return: Data directory path
        :type: str
        """
        return tempfile.gettempdir()

    @staticmethod
    def _validate_columns(df: pd.DataFrame, columns_to_check: List) -> None:
        """Validate if specific columns exist in the loaded dataset

        :param ds: Loaded MLTable
        :type ds: MLTable
        :param columns_to_check: List of columns to check in the dataframe
        :type default_value: str
        :rtype: None
        """
        for col in columns_to_check:
            if col not in df.columns:
                raise UserErrorException(
                    f"The column '{col}' is not present in the dataset" f"Available columns are {df.columns}"
                )

    @staticmethod
    def _download_image_files(ds, image_column_name: str) -> None:
        """Helper method to download dataset files.

        :param ds: Aml Dataset object
        :type ds: TabularDataset
        :param image_column_name: The column name for the image file.
        :type image_column_name: str
        """
        logger.info("Start downloading image files")
        start_time = time.perf_counter()
        data_dir = DownloadManager._get_data_dir()
        logger.info(f"downloading images at path {data_dir}")  # pylint: disable=logging-fstring-interpolation
        try:
            ds._download(  # pylint: disable=protected-access
                stream_column=image_column_name, target_path=data_dir, ignore_not_found=True
            )
        except Exception as e:
            logger.error(  # pylint: disable=logging-fstring-interpolation
                "Could not download dataset files. " f"Please check the logs for more details. Error Code: {e}"
            )
            raise Exception(e)  # pylint: disable=broad-exception-raised

        logger.info(  # pylint: disable=logging-fstring-interpolation
            f"Downloading image files took {time.perf_counter() - start_time:.2f} seconds"
        )
