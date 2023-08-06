

class GitHub:

    def github_dependencies_loop(self, tables, headers, df, org, g, save_path):
        """
        Retrieve code files from GitHub search and store them in a dictionary, for each table in the given list of tables.

        Args:
            tables (list): A list of strings representing the names of the tables to be searched.
            headers (dict): A dictionary containing the GitHub authorization token.
            df (dict): A dictionary to store the search results.
            org (str): A string representing the organization to be searched.
            g: An instance of the GitHub class.
            save_path (str): A string representing the path to save the search results.

        Returns:
            dict: A dictionary containing the search results.

        Raises:
            Exception: If an error occurs while searching for the tables.

        Examples:
            >>> headers = {'Authorization': 'token abc123'}
            >>> tables = ['table1', 'table2']
            >>> org = 'my_org'
            >>> g = GitHub()
            >>> save_path = 'results.json'
            >>> df = {}
            >>> res = g.github_dependencies_loop(tables, headers, df, org, g, save_path)
            >>> type(res)
            <class 'dict'>
        """

        import requests
        import random
        import time
        import re
        import json

        n = 3
        chunks = [tables[i:i + n] for i in range(0, len(tables), n)]

        lucky = 0
        counter = 1
        for chunk in chunks:

            used = requests.get('https://api.github.com/rate_limit', headers=headers).json()

            while used['resources']['search']['remaining'] < 3:
                lucky = 0
                dice = random.choice([2, 3, 4, 6, 7, 9, 10, 11, 12])

                print(f"\nWant to play?\nLet's roll the dice: \n\tYou rolled a {dice}\n\nIn the Jungle you must wait "
                      f"until the dice roll 5 or 8")

                print('\nYou must wait ' + str(int(used['resources']['search']['reset']) - int(time.time()) + 3) +
                      ' seconds before rolling again.\n')

                time_now = int(time.time())

                if int(used['resources']['search']['reset']) - int(time_now) > 0:
                    time.sleep(int(used['resources']['search']['reset']) - (time.time()) + 3)

                used = requests.get('https://api.github.com/rate_limit', headers=headers).json()

            if lucky == 0:
                lucky = 5
                dice = random.choice([5, 8])

                print(f"\nLet's roll the dice: \n\tYou rolled a {dice}\nPlease proceed:\n")

            for table in chunk:
                if table in df['TABLES_SEARCHED']:
                    if df['TABLES_NOT_SEARCHED'] is not None:
                        df['TABLES_NOT_SEARCHED'] = df['TABLES_NOT_SEARCHED'].remove(table)
                    continue

                print(table)
                if org is not None:
                    search = g.search_code('org:' + org + ' ' + table)
                else:
                    search = g.search_code(table)

                print(f'Searching {org} {str(table)}:\t\t\t\ttable number: {str(counter)}')

                df[table] = {}

                for file in search:
                    result = requests.get(file.download_url)

                    result = result.text

                    indexes = [index.start() for index in re.finditer(table.upper(), result.upper())]

                    instance = 1
                    for index in indexes:
                        if index < 250:
                            index = 250
                        instance += 1

                        df[table][str(file.repository.name) + '/' + str(file.path)] = {}
                        df[table][str(file.repository.name) + '/' + str(file.path)]['Start'] = result[:1000]
                        df[table][str(file.repository.name) + '/' + str(file.path)]['lines'] = {}
                        df[table][str(file.repository.name) + '/' + str(file.path)]['lines'][str(index)] = \
                            result[index - 250: index + 250]

                time.sleep(2.001)

                counter += 1

                df['TABLES_SEARCHED'].append(table)

                if df['TABLES_NOT_SEARCHED'] is not None:
                    df['TABLES_NOT_SEARCHED'] = df['TABLES_NOT_SEARCHED'].remove(table)

            if save_path is not None:
                with open(save_path, "w+") as f:
                    json.dump(df, f, indent=4)

        return df

    def github_dependencies(self, tables: list | str = None, token: str = None,
                            save_path: str | None = None, org: str | None = None):

        """
        Searches for dependencies of specified tables on GitHub and returns a dictionary with the dependencies.

        Args:
            tables (list or str, optional): A list of table names or a single table name. Defaults to None.
            token (str, optional): GitHub API token. Defaults to None.
            save_path (str, optional): Path to save the results. Defaults to None.
            org (str, optional): GitHub organization name. Defaults to None.

        Returns:
            dict: A dictionary with the dependencies of the specified tables on GitHub.

        Raises:
            StopIteration: Raised when there are no more tables left to search for.
            Exception: Raised when a general exception occurs.

        Examples:

        # Search for dependencies of a single table
        >>> dependencies = github_dependencies(tables='table1', token='your_github_token')
        Searching for 1 tables in github

        # Search for dependencies of multiple tables
        >>> dependencies = github_dependencies(tables=['table1', 'table2'], token='your_github_token')
        Searching for 2 tables in github

        # Search for dependencies of multiple tables with an organization name
        >>> dependencies = github_dependencies(tables=['table1', 'table2'], token='your_github_token', org='your_org_name')
        Searching for 2 tables in your_org_name

        # Save results to a file
        >>> dependencies = github_dependencies(tables='table1', token='your_github_token', save_path='dependencies.json')
        Searching for 1 tables in github
        """

        import pandas as pd
        import time
        import json
        import os
        from github import Github as g
        from warnings import simplefilter
        import random

        simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

        if tables is str:
            tables = [tables]

        gt = g(token)
        headers = {'Authorization': 'token ' + token}

        tables = [*set(tables)]
        print('Searching for ' + str(len(tables)) + ' tables in github')

        if save_path is not None and os.path.exists(save_path) and os.path.getsize(save_path) > 0:
            try:
                with open(save_path, 'r') as f:
                    df = json.load(f)
            except Exception as e:
                df = {}
                print(e)
        else:
            df = {}

        if 'TABLES_SEARCHED' not in df.keys():
            df['TABLES_SEARCHED'] = []
        if 'TABLES_NOT_SEARCHED' not in df.keys() or df['TABLES_NOT_SEARCHED'] is None:
            df['TABLES_NOT_SEARCHED'] = tables
        else:
            df['TABLES_NOT_SEARCHED'].append(tables)

        while len(df['TABLES_SEARCHED']) < len(tables):
            try:
                d_dict = GitHub.github_dependencies_loop(self, tables=tables, headers=headers, df=df, org=org, g=gt,
                                                         save_path=save_path)

                if save_path is None:
                    return d_dict

            except StopIteration:
                with open(save_path, 'r') as f:
                    d = json.load(f)
                return d
            except Exception as e:

                dice = random.choice([2, 3, 4, 6, 7, 9, 10, 11, 12])

                print(f"\n\nWant to play?\nLet's roll the dice: \n\tYou rolled a {dice}\n\nIn the Jungle you must wait "
                      f"until the dice roll 5 or 8\n\n")
                print(e)

                print('\n\n\nA General exception has occurred.\n\nWe will be put in the penalty box for 5 minutes\n\n')

                time.sleep(60*5)

                dice = random.choice([5, 8])

                print(f"\nLet's roll the dice: \n\tYou rolled a {dice}\nPlease proceed:\n")

                print("\n\nWe are free!!\n\nIt's go time!!\n")
                continue
        with open(save_path, 'r') as f:
            d = json.load(f)
        return d

