

class SnowflakeData:

    def __init__(self, username, warehouse, role, database=None, schema=None, table=None, column_name = None,
                 col_and_or = None, get_ex_val = None, like_flag = None):
        self.__username = username
        self.__warehouse = warehouse
        self.__role = role
        self.__database = database
        self.__schema = schema
        self.__table = table
        self.__column_name = column_name
        self.__col_and_or = col_and_or
        self.__get_ex_val = get_ex_val
        self.__like_flag = like_flag


    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def warehouse(self):
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value):
        self.__warehouse = value

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value):
        self.__role = value

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, value):
        self.__database = value

    @property
    def schema(self):
        return self.__schema

    @schema.setter
    def schema(self, value):
        self.__schema = value

    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self, value):
        self.__table = value

    @property
    def column_name(self):
        return self.__column_name

    @column_name.setter
    def column_name(self, value):
        self.__column_name = value

    @property
    def col_and_or(self):
        return self.__col_and_or

    @col_and_or.setter
    def col_and_or(self, value):
        self.__col_and_or = value

    @property
    def get_ex_val(self):
        return self.get_ex_val

    @get_ex_val.setter
    def get_ex_val(self, value):
        self.__get_ex_val = value

    @property
    def like_flag(self):
        return self.__like_flag

    @like_flag.setter
    def like_flag(self, value):
        self.__like_flag = value

    import pandas

    def build_search_query(self, inp_db=None, schema=None, table=None, column_name=None,like_flag=None,
                           col_and_or=None):

        if schema is None:
            schema = self.__schema
        if table is None:
            table = self.__table
        if column_name is None:
            column_name = self.__column_name
        if like_flag is None:
            like_flag = self.__like_flag
        if col_and_or is None:
            col_and_or = self.__col_and_or

        where_stmt = "WHERE 1=1 "  # ie. always TRUE --> allows us to search for tables/cols/etc. even without knowing the db
        where_stmt = where_stmt + f"AND table_catalog = '{inp_db}' " if inp_db else where_stmt
        where_stmt = where_stmt + f"AND table_schema = '{schema}' " if schema else where_stmt
        where_stmt = where_stmt + f"AND table_name = '{table}' " if table else where_stmt

        # add column(s) search criteria --> if column_name is a list add an AND statement for each search value in the list
        if column_name is not None:
            if type(column_name) == str:
                where_stmt = where_stmt + f"AND column_name like '{column_name}' " \
                    if like_flag else where_stmt + f"AND column_name = '{column_name}' "  # column name equals (if like_flag = false)
            elif (type(column_name) == list) & (like_flag == False):  # OR statement where value matches multiple
                where_stmt = where_stmt + f"""AND column_name in ({' ,'.join(f"'{str(x)}'" for x in column_name)})"""
            elif type(column_name) == list:  # --> user input list of search criteria
                for idx, x in enumerate(column_name):
                    if col_and_or.lower() == 'and':  # col contains all column_name search criteria
                        where_stmt = where_stmt + f"AND column_name like '{x}' " if like_flag == True else where_stmt + f"AND column_name = '{x}' "
                    elif col_and_or.lower() == 'or':  # col contains any of the column_name search criteria
                        where_stmt = where_stmt + f"AND (column_name like '{x}' " if idx == 0 else where_stmt + f"OR column_name like '{x}' "
                    else:  # non-matching input value
                        raise ValueError('col_and_or input must match: AND/And/and, OR/Or/or')
                where_stmt = where_stmt + ')' if (type(column_name) == list) & (col_and_or == 'or') else where_stmt
            else:  # --> invalid format
                raise ValueError(f'ERROR: column_name={column_name} does not match required input of list/string')

        print(where_stmt)

        # final search-schema query
        query = f'''        
        SELECT 
            DISTINCT
            TABLE_CATALOG
            ,TABLE_SCHEMA
            ,TABLE_NAME
            ,COLUMN_NAME
            ,IS_NULLABLE
            ,DATA_TYPE
        FROM 
            INFORMATION_SCHEMA.COLUMNS
        {where_stmt}
        ORDER BY 
            TABLE_CATALOG
            , TABLE_SCHEMA
            , TABLE_NAME
            , COLUMN_NAME
        '''

        return query

    def snowflake_pull(self, query: str, sample_table: bool = False,
                       sample_val: bool = False, table_sample: dict = None, dtypes_conv=None) -> pandas.DataFrame:

        un, wh, db = self.__username, self.__warehouse, self.__database

        """
        function: pulls snowflake data
    
        dependencies: [
            pandas,
            snowflake.connector,
            time,
            datetime.datetime
        ]
    
        :param query: str
            SQL query to run on Snowflake
            query = "SELECT * FROM  NGP_DA_PROD.POS.TO_DATE_AGG_CHANNEL_CY"
    
        :param un: str
            Nike Snowflake Username
                "USERNAME"
    
        :param db: str, default 'NA'
            Name of the Database
    
        :param wh: str
            Name of the Wharehouse
            e.g. "DA_DSM_SCANALYTICS_REPORTING_PROD"
    
        :param role: str
            Name of the role under which you are running Snowflake
                "DF_######"
    
        :param sample_table: bool, default: False
    
        :param sample_val: bool, default: False
    
        :param table_sample: dict, default: None
            later
                if table_sample = None
                    table_sample = {'db': None, 'schema': None, 'table': None, 'col': None}
    
        :param dtypes_conv: default: None
    
        :return: pandas.DataFrame
        """

        # snowflake connection packages:
        import pandas as pd
        import snowflake.connector

        if table_sample != None:
            table_sample = {'db': None, 'schema': None, 'table': None, 'col': None}

        # --> take a random sample from a table in snowflake
        query = f'''SELECT * FROM {table_sample['db']}.{table_sample['schema']}.{table_sample['table']} LIMIT 100''' if sample_table else query

        # --> take a random sample of a column from a table in snowflake
        query = f'''SELECT DISTINCT {table_sample['col']} FROM {table_sample['db']}.{table_sample['schema']}.{table_sample['table']} ORDER BY 1 LIMIT 10''' if sample_val == True else query

        conn = snowflake.connector.connect(
            user=un,
            account='nike',
            authenticator='externalbrowser',  # opens separate browser window to confirm authentication
            warehouse=wh,
            database=db,
            role=self.__role
        )  # connection settings

        cur = conn.cursor()  # connect to snowflake using conn variables
        cur.execute(query)  # execute sql, store into-->

        try:
            df = cur.fetch_pandas_all() if dtypes_conv == None else cur.fetch_pandas_all().astype(
                dtypes_conv)  # final data pull --> allows datatype-memory optimization

        except:  # --> allows metadata querying
            temp_df = cur.fetchall()  # return data
            cols = [x.name for x in cur.description]  # get column names
            df = pd.DataFrame(temp_df, columns=cols)  # create dataset

        conn.close()
        cur.close()  # close connections
        return df




