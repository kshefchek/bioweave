from typing import List

from koza.model.config.source_config import ColumnFilter


class RowFilter:
    """
    A Filter class that is initialized with a List of column filters, each specifying a column, an operator and a value
    """

    def __init__(
        self,
        filters: List[ColumnFilter] = None
    ):
        """
        :param filters: A collection of Filters to be applied
        """
        self.filters = filters
        self.operators = {
            'gt': self.gt,
            'gte': self.gte,
            'lt': self.lt,
            'lte': self.lte,
            'eq': self.eq,
            'ne': self.ne,
            'in': self.inlist
        }

    def include_row(self, row) -> bool:
        """
        :param row: A dictionary representing a single row
        :return: bool for whether the row should be included
        """
        column_filter: ColumnFilter
        for column_filter in self.filters:
            # None can't be greater, less than or equal to any specified value, right?
            if row.get(column_filter.column) is None:
                return False

            comparison_method = self.operators.get(column_filter.filter_code)
            return comparison_method(row.get(column_filter.column), column_filter.value)

    def gt(self, column_value, filter_value):
        return column_value > filter_value

    def gte(self, column_value, filter_value):
        return column_value >= filter_value

    def lt(self, column_value, filter_value):
        return column_value < filter_value

    def lte(self, column_value, filter_value):
        return column_value <= filter_value

    def eq(self, column_value, filter_value):
        return column_value == filter_value

    def ne(self, column_value, filter_value):
        return column_value != filter_value

    def inlist(self, column_value, filter_value):
        return column_value in filter_value
