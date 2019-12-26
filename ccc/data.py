'''
Cost-of-Capital-Calculator asset data class.
'''
# CODING-STYLE CHECKS:
# pycodestyle records.py
# pylint --disable=locally-disabled records.py

import os
import pandas as pd
from ccc.utils import read_egg_csv, read_egg_json, json_to_dict
from ccc.utils import ASSET_DATA_CSV_YEAR


class Assets():
    '''
    Constructor for the asset-entity type Records class.

    Args:
        data (string or Pandas DataFrame): string describes CSV file in
            which records data reside; DataFrame already contains records
            data; default value is the string 'asset_data.csv'
        start_year (integer): specifies calendar year of the input data;
            default value is ASSET_DATA_CSV_YEAR.

    Returns:
    Assets (class instance)

    Raises:
        ValueError:
            * if data is not the appropriate type.

            * if start_year is not an integer.

            * if files cannot be found.

    Notes:
        Typical usage when using ccc_asset_data.csv input data is as follows::

            >>> assets = Assets()

        which uses all the default parameters of the constructor.

    '''
    # suppress pylint warnings about unrecognized Records variables:
    # pylint: disable=no-member
    # suppress pylint warnings about uppercase variable names:
    # pylint: disable=invalid-name
    # suppress pylint warnings about too many class instance attributes:
    # pylint: disable=too-many-instance-attributes

    ASSET_YEAR = ASSET_DATA_CSV_YEAR

    CUR_PATH = os.path.abspath(os.path.dirname(__file__))
    VAR_INFO_FILENAME = 'records_variables.json'

    def __init__(self,
                 data='ccc_asset_data.csv',
                 start_year=ASSET_DATA_CSV_YEAR):
        # pylint: disable=too-many-arguments,too-many-locals
        self.__data_year = start_year
        # read specified data
        self._read_data(data)
        # If have any checks on data, do there here...
        # specify that variable values do not include behavioral responses
        self.behavioral_responses_are_included = False

    @property
    def data_year(self):
        '''
        Records class original data year property.
        '''
        return self.__data_year

    @property
    def current_year(self):
        '''
        Records class current calendar year property.
        '''
        return self.__current_year

    @property
    def array_length(self):
        '''
        Length of arrays in Records class's DataFrame.
        '''
        return self.__dim

    def _read_data(self, data):
        '''
        Read Records data from file or use specified DataFrame as data.

        Args:
            data (string or Pandas DataFrame): data or path to data

        Returns:
            None

        '''
        # pylint: disable=too-many-statements,too-many-branches
        if Assets.INTEGER_VARS == set():
            Assets.read_var_info()
        # read specified data
        if isinstance(data, pd.DataFrame):
            assetdf = data
        elif isinstance(data, str):
            if os.path.isfile(data):
                assetdf = pd.read_csv(data)
            else:
                # cannot call read_egg_ function in unit tests
                assetdf = read_egg_csv(data)  # pragma: no cover
        else:
            msg = 'data is neither a string nor a Pandas DataFrame'
            raise ValueError(msg)
        self.__dim = len(assetdf.index)
        self.__index = assetdf.index

        self.df = assetdf
