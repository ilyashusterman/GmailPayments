#!/usr/bin/env python

import logging
import pandas as pd
from datetime import datetime
from plugins.core.DbSqlAlchemy import DbSqlAlchemy


class TableBase(object):
    """
    Base class for MySQL table implementations.
    """

    @staticmethod
    def make_date_parser(date_format):
        def date_parser(date_string):
            return datetime.strptime(date_string, date_format)

        return date_parser

    @staticmethod
    def timestamp_parser(date_string):
        if '.' in date_string:
            return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
        else:
            return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

    def __init__(self, table_name, columns, columns_not_null, date_columns,
                 round_columns=None, date_parser=None):
        self.table_name = table_name
        self.columns = columns
        self.columns_not_null = columns_not_null
        self.date_columns_index = date_columns
        self.round_columns = round_columns
        self.date_parser = date_parser

    def count_rows(self):
        db = DbSqlAlchemy()
        db.connect()
        assert db.cursor
        sql = 'SELECT COUNT(*) AS row_count FROM %s;' % self.table_name
        row_count = 0
        for row in db.cursor.execute(sql):
            row_count = int(row[0])
            break
        db.disconnect()
        return int(row_count)

    def read_csv(self, csv_filename, date_parser=None, **kwargs):
        """Loads CSV date for this table into DataFrame"""
        got_date_columns = bool(self.date_columns_index)
        if got_date_columns:
            self.date_parser = date_parser or self.date_parser
            assert self.date_parser,\
                'Provide an explicit date parser function for date/time ' \
                'columns: {}'.format(self.date_columns_index)
        data_frame = pd.read_csv(csv_filename,
                                 parse_dates=self.date_columns_index,
                                 infer_datetime_format=got_date_columns,
                                 encoding='utf-8')
        self.validate_columns(data_frame)
        # Drop any columns not in the table schema
        drop_columns = frozenset(data_frame.columns) - frozenset(self.columns)
        data_frame.drop(drop_columns, axis=1, inplace=True)
        if self.round_columns:
            data_frame = data_frame.round(self.round_columns)
        return data_frame

    def insert_csv(self, csv_filename, dry_run):
        data_frame = self.read_csv(csv_filename)
        if not dry_run:
            if data_frame.empty:
                logging.info('Empty data frame, nothing to insert')
            else:
                logging.info('Inserting {} new rows, columns: {}'.format(data_frame.shape[0], data_frame.columns))
                rows_before = self.count_rows()
                self.insert_data_frame(data_frame)
                rows_added = len(data_frame.index)
                expected = rows_before + rows_added
                actual = self.count_rows()
                if expected != actual:
                    raise AssertionError('Failed row count sanity check, expected: %u actual:%u '
                                         '(was:%u added:%u now:%u)' % \
                                         (expected, actual, rows_before, rows_added, actual))
        return data_frame

    def insert_data_frame(self, data_frame):
        assert isinstance(data_frame, pd.DataFrame)
        db = DbSqlAlchemy()
        db.connect()
        data_frame = data_frame.fillna('')
        data_frame.to_sql(con=db.connection,
                          name=self.table_name,
                          if_exists='append',
                          chunksize=10000,
                          index=False)
        db.disconnect()
        return data_frame

    def validate_columns(self, data_frame):
        existing_columns = list(data_frame.columns.values)
        missing_columns = ''
        for column in self.columns_not_null:
            if column not in existing_columns:
                missing_columns += ' %s' % column
        if missing_columns:
            raise Exception('All NOT NULL columns must be present in the input '
                            'CSV. Missing columns: %s' % missing_columns)
