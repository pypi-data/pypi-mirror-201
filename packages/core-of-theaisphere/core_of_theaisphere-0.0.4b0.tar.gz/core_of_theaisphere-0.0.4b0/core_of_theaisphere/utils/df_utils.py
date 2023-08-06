"""
A module containing DataFrame utilities.
"""
# Imports
import pandas as pd
from pathlib import Path


"""
Author: vickyparmar
File: df_utils.py
Created on: 31-03-2023, Fri, 17:39:13

Last modified by: vickyparmar
Last modified on: 31-3-2023, Fri, 17:39:16
"""


# Class with utility functions for DataFrame
class DataFrameUtils:
    """
            A class containing DataFrame utility functions
            to load/save different DataFrame formats.

            ...

            Method
            ------
            load_df(file: str or Path, **kwargs: dict)
                Load a pandas DataFrame from a file.
            save_df(df: pd.DataFrame, file: str or Path, **kwargs: dict)
                Save a pandas DataFrame to a file.

            Raise
            -----
            FileNotFoundError
                If the file does not exist.
            ValueError
                If the file extension is not supported
                or recognized.
            FileExistsError
                If the file already exists and the user
                chooses not to replace it.

            See Also
            --------
            othermodule : Other module to see.

            Notes
            -----
            Still to add more functionality.

            Example
            -------
            >>> csv = '/path/to/dataframe.csv'
            >>> df = DataFrameUtils.load_df(csv)
            >>> xlsx = '/path/to/dataframe.xlsx'
            >>> DataFrameUtils.save_df(df, xlsx)
            """
    @staticmethod
    def load_df(file: str or Path, **kwargs: dict) -> pd.DataFrame:
        """
        Load a pandas DataFrame from a file.

        Parameters
        ----------
        file : str or Path
            File path.
        **kwargs : dict
            Additional keyword arguments to pass
            to pandas read methods.

        Returns
        -------
        pd.DataFrame
            Loaded DataFrame.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        ValueError
            If the file extension is not supported or
            recognized.

        """
        file_path = Path(file)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path} 😞")

        extension = file_path.suffix

        if extension == '.csv':
            df = pd.read_csv(file_path, **kwargs)

        elif extension in ['.xlsx', '.xlx']:
            df = pd.read_excel(file_path, **kwargs)

        elif extension == '.json':
            df = pd.read_json(file_path, **kwargs)

        elif extension in ['.ftr', '.feather']:
            df = pd.read_feather(file_path, **kwargs)

        elif extension in ['.parquet', '.pq']:
            df = pd.read_parquet(file_path, **kwargs)

        elif extension == '.gz' and file_path.suffixes[-2] in ['.parquet', '.pq']:
            df = pd.read_parquet(file_path, **kwargs)

        elif extension in ['.h5', '.hdf', '.h5py']:
            df = pd.read_hdf(file_path, **kwargs)

        elif extension == '.xml':
            df = pd.read_xml(file_path, **kwargs)

        else:
            raise ValueError(f"Unsupported file extension: {extension} 😞")

        print(f"DataFrame loaded successfully from {file_path}! 🎉")

        return df

    @staticmethod
    def save_df(df: pd.DataFrame, file: str or Path, **kwargs: dict) -> None:
        """
        Save a pandas DataFrame to a file.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to save.
        file : str or Path
            File path.
        **kwargs : dict
            Additional keyword arguments to pass
            to pandas write methods.

        Raises
        ------
        FileExistsError
            If the file already exists and the user
            chooses not to replace it.
        ValueError
            If the file extension is not supported
            or recognized.

        """
        file_path = Path(file)
        if file_path.exists():
            replace_file = input(f"File already exists: {file_path}. Replace it? (y/n) ")
            if replace_file.lower() != 'y':
                return

        extension = file_path.suffix

        if extension == '.csv':
            df.to_csv(file_path, **kwargs)

        elif extension in ['.xlsx', '.xlx']:
            df.to_excel(file_path, **kwargs)

        elif extension == '.json':
            df.to_json(file_path, **kwargs)

        elif extension in ['.ftr', '.feather']:
            df.to_feather(file_path, **kwargs)

        elif extension in ['.parquet', '.pq']:
            df.to_parquet(file_path, engine='auto', **kwargs)

        elif extension == ':gz' and file_path.suffixes in ['.parquet', '.pq']:
            df.to_parqQuet(file_path, engine='auto', **kwargs)

        elif extension in ['.h5', '.hdf', '.h5py']:
            df.to_hdf(file_path, **kwargs)

        elif extension == '.xml':
            df.to_xml(file_path, **kwargs)

        else:
            raise ValueError(f"Unsupported file extension: {extension} 😞")

        print(f"DataFrame saved successfully to {file_path}! 🎉")
