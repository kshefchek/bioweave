"""
Testing for row filtering

"""
import pytest

from koza.model.config.source_config import ColumnFilter, FilterInclusion, FilterCode

from koza.dsl.row_filter import RowFilter


@pytest.mark.parametrize("column, inclusion, code, value, result", [
  ('a', 'include', 'eq', .3, True),
  ('a', 'exclude', 'eq', .3, False),
  ('a', 'include', 'gte', .3, True),
  ('a', 'include', 'lte', .3, True),
  ('a', 'include', 'ne', .3, False),
  ('a', 'include', 'ne', .4, True),
  ('a', 'include', 'lt', .4, True),
  ('a', 'include', 'gt', .4, False),
  ('a', 'include', 'gt', .2, True),
  ('a', 'exclude', 'gt', .4, True),
  ('a', 'exclude', 'gt', .2, False),
  ('b', 'include', 'eq', 10, True),
  ('b', 'include', 'gte', 10, True),
  ('b', 'include', 'lte', 10, True),
  ('b', 'include', 'gt', 9, True),
  ('b', 'include', 'gt', 11, False),
  ('b', 'include', 'lt', 11, True),
  ('b', 'include', 'lt', 9, False),
  ('c', 'include', 'eq', 'llama', True),
  ('c', 'include', 'ne', 'alpaca', True),
  ('c', 'include', 'eq', 'alpaca', False),
  ('c', 'include', 'in', ['llama', 'alpaca'], True),
  ('c', 'include', 'in', ['condor', 'alpaca'], False)
  ])
def test_filter(column, inclusion, code, value, result):
    row = {'a': .3, 'b': 10, 'c': 'llama'}
    column_filter = ColumnFilter(column=column,
                                 inclusion=FilterInclusion(inclusion),
                                 filter_code=FilterCode(code),
                                 value=value)

    rf = RowFilter([column_filter])

    assert rf.include_row(row) is result


@pytest.mark.parametrize("column_filters, result", [
    ([ColumnFilter(column='a', inclusion=FilterInclusion('include'),
                   filter_code=FilterCode('lt'), value=.4),
      ColumnFilter(column='a', inclusion=FilterInclusion('include'),
                   filter_code=FilterCode('gt'), value=.1)], True),
    ([ColumnFilter(column='a', inclusion=FilterInclusion('include'),
                   filter_code=FilterCode('lt'), value=.4),
      ColumnFilter(column='a', inclusion=FilterInclusion('exclude'),
                   filter_code=FilterCode('gt'), value=.4)], True),
    ([ColumnFilter(column='a', inclusion=FilterInclusion('include'),
                   filter_code=FilterCode('in'), value=[.2, .3, .4]),
      ColumnFilter(column='b', inclusion=FilterInclusion('exclude'),
                   filter_code=FilterCode('lt'), value=9)], True),
    ([ColumnFilter(column='a', inclusion=FilterInclusion('include'),
                   filter_code=FilterCode('in'), value=[.2, .3, .4]),
      ColumnFilter(column='b', inclusion=FilterInclusion('exclude'),
                   filter_code=FilterCode('gt'), value=9)], False),
])
def test_multiple_filters(column_filters, result):
    row = {'a': .3, 'b': 10, 'c': 'llama'}

    rf = RowFilter(column_filters)

    assert rf.include_row(row) == result
