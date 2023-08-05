import pandas as pd


class IMPSummaryDashboard:

    import pandas as pd

    def imp_summary_dashboard(self
                              , username: str
                              , warehouse: str
                              , database: str
                              , role: str
                              , date_min: str = '1900-01-01'
                              , date_max: str = '9999-12-31'
                              , column_filters=None):
        """
        Generate a SQL query for a dashboard summary report with optional column filters.

        Args:
            date_min (str): The minimum activity end date to include in the report. Default is '1900-01-01'.
            date_max (str): The maximum activity end date to include in the report. Default is '9999-12-31'.
            column_filters (list): A list of column names to include in the query SELECT and GROUP BY clauses. Default
            is None.

        Returns:
            DataFrame: .

        Raises:
            TypeError: If date_min, date_max, or column_filters is not a string or list, respectively.
            :param column_filters:
            :param date_max:
            :param date_min:
            :param role:
            :param database:
            :param warehouse:
            :param username:
        """

        from NikeCA import Snowflake

        if column_filters is None:
            column_filters = []
        import configparser

        config = configparser.ConfigParser()
        config.read('pip.ini')

        date_begin = config['imp_summary'].get('begin_date')
        date_end = config['imp_summary'].get('date_end')
        date = config['imp_summary'].get('date')
        table = config['imp_summary'].get('table')
        column = config['imp_summary'].get('column')
        column_filter = config['imp_summary'].get('column_filter')
        column_flag = config['imp_summary'].get('column_flag')
        column_flag_answer = config['imp_summary'].get('column_flag_answer')
        aggs = config['imp_summary'].get('aggs')

        # Ensure column_filters is a list
        if not isinstance(column_filters, list):
            raise TypeError("column_filters must be a list")

        # Join column filters into comma-separated string, if any
        if len(column_filters) > 0:
            column_filters_str = ', '.join(column_filters)
            group_column_filters_str = f'''GROUP BY 
                {column_filters_str}'''
            column_filters_str += ', '
        else:
            column_filters_str = column + ', '
            group_column_filters_str = f'GROUP BY {column}'

        query_dashboard = f"""
        SELECT
            {column_filters_str}
            MIN({date_begin}) AS MIN_{date_begin}
            , MAX({date_end}) AS MAX_{date_end}
            , {aggs}
        FROM 
            {table}
        WHERE
            {date} BETWEEN '{date_min}' AND '{date_max}'
            AND {column} = '{column_filter}'
            AND {column_flag} = '{column_flag_answer}'
        {group_column_filters_str} 
        UNION
    
        SELECT
            {column_filters_str}
            MIN({date_begin}) AS MIN_{date_begin}
            , MAX({date_end}) AS MAX_{date_end}
            , {aggs}
        FROM 
            {table}
        WHERE
            {date} BETWEEN '{date_min}' AND '{date_max}'
            AND {column} <> '{column_filter}'
            AND {column_flag} = '{column_flag_answer}'
        {group_column_filters_str}
        ;
        """
        print(query_dashboard)

        return Snowflake(username=username, warehouse=warehouse, database=database,
                         role=role).snowflake_pull(query=query_dashboard)

