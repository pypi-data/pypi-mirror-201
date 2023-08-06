"""Module for handling data input/output from and to files.
"""
from __future__ import annotations

__author__ = "Matteo Gabba"
__copyright__ = "Copyright 2022, all right reserved Gabba Scientific"
__status__ = "Development"

import csv
from pathlib import Path
from typing import Iterator, Iterable

import pandas as pd

# TODO: write fun to create columns mapping dictionary def create_columns_mapping_dict(usecols, new_colnames):
#  return dict(zip(usecols, new_colnames))


class CSVReader:
    """
    Class to read .csv files.

    Attributes
    ----------
        source : Path, required
            Path of a .csv file.

    Methods
    -------
        to_data_frame
            Read .csv file into a pd.DataFrame.

        row_iter
            Iterate over the rows of the .csv file mapped into a dictionary with header column names as key values.
    """
    def __init__(self, source: Path) -> None:
        """
            source : Path, required
                Path of a .csv file.
        """
        self.source = source

    @staticmethod
    def _rename_keys(
        old_dict: dict[str, str], key_map_dict: dict[str, str]
    ) -> dict[str, str]:
        """
        Rename keys of input dictionary according to mapping dictionary.

        Parameters
        ----------
        old_dict : dict(str, str), required

        key_map_dict : dict[str, str], required
            Dictionary mapping old to new keys -> {'old_key_1': 'new_key_1, 'old_key_2': 'new_key_2',}

        Returns
        -------
            The input dictionary with the new keys.
        """
        return {
            (key_map_dict[key] if key in key_map_dict else key): value
            for key, value in old_dict.items()
        }

    @staticmethod
    def _filter_by_key(old_dict: dict, keys: Iterable[str]) -> dict:
        """
        Filter dictionary by key value.

        Discard items of old_dict not in the given list of keys.

        Parameters
        ----------
        old_dict : dict, required

        keys : List or Tuple, required
            Discard dictionary items not in keys.

        Returns
        -------
            A subset of the input dictionary.
        """
        return {key: value for key, value in old_dict.items() if key in keys}

    @staticmethod
    def _check_missing_columns(
        csv_reader: csv.DictReader, usecols: Iterable[str]
    ) -> None:
        """
        Check if selected column names exists in the .csv file, raise ValueError otherwise.

        Parameters
        ----------
        csv_reader : csv.DictReader instance, required
            Instance of csv.DictReader.

        usecols : List or Tuple, required
            List of column names.

        Returns
        -------
            None if all column names exists in the .csv file header, raise ValueError otherwise.
        """
        header = csv_reader.fieldnames
        missing_cols = [col for col in usecols if col not in header]

        if missing_cols:
            raise ValueError(f"invalid column name(s): {missing_cols}")

    def row_iter(
        self,
        *,
        usecols: Iterable[str] = None,
        col_map_dict: dict[str, str] = None,
    ) -> Iterator[dict[str, str]]:
        """
        Iterator over the rows of the .csv file mapped to a dictionary of strings:

         {'col1_name': 'row_i1', 'col2_name': 'row_i2', 'col3_name': 'row_i3'}.
          Optionally, a subset of columns can be loaded and/or renamed to user defined column names.

        Parameters
        ----------
            usecols : List or Tuple, optional, key-word only, defaults to None
                Returns a subset of the columns. If empty, returns all columns. Raise ValueError for incorrect
                column names.

            col_map_dict : dict[str, str], optional, key-word only, default to None
                Dictionary mapping old (keys) to new (values) column names.

        Returns
        -------
            Iterator over the .csv rows.
        """
        # TODO: decide if ordering the dictionary according to usecols and colmap order
        # ordered_dict = {k : new_colnames_row[k] for k in new_cols}

        with open(self.source, "r") as data:

            # Instantiate csv_reader
            csv_reader = csv.DictReader(data)

            # For each row of the .csv file generate a dictionary: {col_name: value}
            for row in csv_reader:

                if not usecols and not col_map_dict:
                    yield row

                elif not usecols and col_map_dict:
                    yield self._rename_keys(row, col_map_dict)

                elif usecols and not col_map_dict:
                    self._check_missing_columns(csv_reader, usecols)
                    yield self._filter_by_key(row, usecols)

                elif usecols and col_map_dict:
                    self._check_missing_columns(csv_reader, usecols)
                    filtered_row = self._filter_by_key(row, usecols)
                    yield self._rename_keys(filtered_row, col_map_dict)

    def to_data_frame(self, **kwargs) -> pd.DataFrame:
        """
        Read .csv file into a pd.DataFrame.

        Parameters
        ----------
            **kwargs : dict, required
                keyword arguments of pandas.read_csv() method.
                See: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

        Returns
        -------
            pd.DataFrame
        """
        return pd.read_csv(self.source, **kwargs)
