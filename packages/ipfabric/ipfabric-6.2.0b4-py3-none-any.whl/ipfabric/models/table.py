import logging
from typing import Optional, Dict, List, Any, Union

import deepdiff
from pydantic import BaseModel

logger = logging.getLogger("ipfabric")

IGNORE_COLUMNS = {"id"}


class BaseTable(BaseModel):
    """model for table data"""

    endpoint: str
    client: Any

    @property
    def name(self):
        return self.endpoint.split("/")[-1]

    @property
    def abs_endpoint(self):
        return self.endpoint if self.endpoint[0] == "/" else "/" + self.endpoint

    def fetch(
        self,
        columns: list = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        sort: Optional[dict] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
    ) -> list:
        """Gets all data from corresponding endpoint

        Args:
            columns: Optional columns to return, default is all
            filters: Optional filters'
            attr_filters: dict: Optional dictionary of Attribute filters
            sort: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
            limit: Default to 1,000 rows
            start: Starts at 0

        Returns:
            list: List of Dictionaries
        """
        return self.client.fetch(
            self.endpoint,
            columns=columns,
            filters=filters,
            attr_filters=attr_filters,
            sort=sort,
            limit=limit,
            start=start,
            snapshot=False,
        )

    def all(
        self,
        columns: list = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        sort: Optional[dict] = None,
    ):
        """Gets all data from corresponding endpoint

        Args:
            columns: Optional columns to return, default is all
            filters: Optional filters
            attr_filters: dict: Optional dictionary of Attribute filters
            sort: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
        Returns:
            list: List of Dictionaries
        """
        return self.client.fetch_all(
            self.endpoint, columns=columns, filters=filters, attr_filters=attr_filters, sort=sort, snapshot=False
        )

    def count(
        self,
        filters: Optional[dict] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
    ):
        """
        Gets count of table
        :param filters: dict: Optional filters
        :param attr_filters: dict: Optional dictionary of Attribute filters
        :return: int: Count
        """
        return self.client.get_count(self.endpoint, filters=filters, attr_filters=attr_filters, snapshot=False)


class Table(BaseTable, BaseModel):
    """model for table data"""

    def fetch(
        self,
        columns: list = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
    ) -> list:
        """Gets all data from corresponding endpoint

        Args:
            columns: Optional columns to return, default is all
            filters: Optional filters'
            attr_filters: dict: Optional dictionary of Attribute filters
            snapshot_id: Optional snapshot ID to override class
            reports: True to return Intent Rules (also accepts string of frontend URL) or a list of report IDs
            sort: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
            limit: Default to 1,000 rows
            start: Starts at 0

        Returns:
            list: List of Dictionaries
        """
        return self.client.fetch(
            self.endpoint,
            columns=columns,
            filters=filters,
            attr_filters=attr_filters,
            snapshot_id=snapshot_id,
            reports=reports,
            sort=sort,
            limit=limit,
            start=start,
        )

    def all(
        self,
        columns: list = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
    ):
        """Gets all data from corresponding endpoint

        Args:
            columns: Optional columns to return, default is all
            filters: Optional filters
            attr_filters: dict: Optional dictionary of Attribute filters
            snapshot_id: Optional snapshot ID to override class
            reports: True to return Intent Rules (also accepts string of frontend URL) or a list of report IDs
            sort: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
        Returns:
            list: List of Dictionaries
        """
        return self.client.fetch_all(
            self.endpoint,
            columns=columns,
            filters=filters,
            attr_filters=attr_filters,
            snapshot_id=snapshot_id,
            reports=reports,
            sort=sort,
        )

    def count(
        self,
        filters: Optional[dict] = None,
        snapshot_id: Optional[str] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
    ):
        """
        Gets count of table
        Args:
            filters: dict: Optional filters
            snapshot_id: str: Optional snapshot ID to override class
            attr_filters: dict: Optional dictionary of Attribute filters

        Returns:
            int: Count of rows
        """
        return self.client.get_count(self.endpoint, filters=filters, attr_filters=attr_filters, snapshot_id=snapshot_id)

    @staticmethod
    def _ignore_columns(columns: set, columns_ignore: set):
        """
        Determines which columns to use in the query.
        Args:
            columns: set : Set of columns to use
            columns_ignore: set : Set of columns to ignore

        Returns:
            list[str]: List of columns to use
        """
        cols_for_return = set()
        for col in columns:
            if col in columns_ignore and col != "id":
                logger.debug(f"Column {col} in columns_ignore, ignoring")
                continue
            cols_for_return.add(col)
        return cols_for_return

    def _compare_determine_columns(self, columns: set, columns_ignore: set, unique_keys: set):
        """
        Determines which columns to use in the query.
        Args:
            columns: set : Set of columns to use
            columns_ignore: set : Set of columns to ignore
            unique_keys: set : Set of columns for unique keys

        Returns:
            list[str]: List of columns to use
        """
        # get all columns for the table
        table_columns = set(self.client.get_columns(self.endpoint))

        # Must always ignore some columns
        columns_ignore.update(IGNORE_COLUMNS)

        cols_for_return = set()
        # user passes unique_keys
        if unique_keys:
            if not table_columns.issuperset(unique_keys):
                raise ValueError(f"Unique Key(s) {unique_keys - table_columns} not in table {self.name}")
            [cols_for_return.add(u) for u in unique_keys]
        # user passes columns
        if columns:
            if not table_columns.issuperset(columns):
                raise ValueError(f"Column(s) {columns - table_columns} not in table {self.name}")
            cols_for_return.update(self._ignore_columns(columns, columns_ignore))
        # user does not pass columns
        else:
            cols_for_return.update(self._ignore_columns(table_columns, columns_ignore))
        return list(cols_for_return)

    @staticmethod
    def _hash_data(json_data, unique_keys=None):
        """
        Hashes data. Turns any data into a string and hashes it, then returns the hash as a key for the data
        Args:
            json_data: list[dict] : List of dictionaries to hash
            unique_keys: list[str] : List of keys to use for hashing

        Returns:
            dict[str]: dictionary with hash as key and values as the original data
        """
        # loop over each obj, turn the obj into a string, and hash it
        return_json = dict()
        if unique_keys:
            for dict_obj in json_data:
                hash_key = {key: dict_obj[key] for key in unique_keys}
                unique_hash = deepdiff.DeepHash(hash_key)[hash_key]
                if unique_hash in return_json:
                    raise KeyError(f"Unique Key(s) {unique_keys} are not unique, please adjust unique_keys input.")
                return_json[unique_hash] = dict_obj
        else:
            for dict_obj in json_data:
                return_json[deepdiff.DeepHash(dict_obj)[dict_obj]] = dict_obj
        return return_json

    @staticmethod
    def _make_set(data: Union[list, set, str] = None):
        if isinstance(data, str):
            return {data}
        elif data is None:
            return set()
        else:
            return set(data)

    def compare(
        self,
        snapshot_id: str = None,
        columns: Union[list, set] = None,
        columns_ignore: Union[list, set, str] = None,
        unique_keys: Union[list, set, str] = None,
        **kwargs,
    ):
        """
        Compares a table from the current snapshot to the snapshot_id passed.
        Args:
            snapshot_id: str : The snapshot_id to compare to.
            columns: list : List of columns to compare. If None, will compare all columns.
            columns_ignore: list : List of columns to ignore. If None, will always ignore 'id' column.
            unique_keys: list : List of columns to use as unique keys. If None, will use all columns as primary key.
            **kwargs: dict : Optional Table.all() arguments to apply to the table before comparing.

        Returns:
            dict : dictionary containing the differences between the two snapshots.
                   Possible keys are 'added', 'removed' and 'changed'.
        """
        return_dict = dict()

        # determine which columns to use in query
        columns = self._make_set(columns)
        columns_ignore = self._make_set(columns_ignore)
        unique_keys = self._make_set(unique_keys)
        cols_for_query = self._compare_determine_columns(columns, columns_ignore, unique_keys)

        data = self.all(columns=cols_for_query, **kwargs)
        data_compare = self.all(snapshot_id=snapshot_id, columns=cols_for_query, **kwargs)

        # since we turned the values into a hash, we can just compare the keys
        if unique_keys:
            hashed_data_unique = self._hash_data(data, unique_keys)
            hashed_data_compare_unique = self._hash_data(data_compare, unique_keys)
            changed = [
                hashed_data_unique[hashed_str]
                for hashed_str in hashed_data_unique.keys()
                if hashed_str not in hashed_data_compare_unique.keys()
            ]
            return_dict["changed"] = changed
            return return_dict
        # compare both ways
        hashed_data = self._hash_data(data)
        hashed_data_compare = self._hash_data(data_compare)
        added = [
            hashed_data[hashed_str] for hashed_str in hashed_data.keys() if hashed_str not in hashed_data_compare.keys()
        ]
        removed = [
            hashed_data_compare[hashed_str]
            for hashed_str in hashed_data_compare.keys()
            if hashed_str not in hashed_data.keys()
        ]
        return_dict["added"] = added
        return_dict["removed"] = removed
        return return_dict
