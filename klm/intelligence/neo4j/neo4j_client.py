from typing import Any

import pandas as pd
from neo4j import GraphDatabase
from neo4j.exceptions import SessionExpired
from django.conf import settings


class Neo4jDriver:
    def __init__(self, uri: str, user: str, password: str):
        # Initialize Neo4j driver or any other necessary setup
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def execute_query(self, query: str, params: dict[str, Any] = None):
        try:
            # Implement Neo4j-specific query execution
            with self.driver.session() as session:
                response = session.run(query=query, parameters=params)
                nodes_list = response.data()
                return nodes_list
        except SessionExpired:
            # Handle session expiration by retrying the query in a new session
            self.execute_query(query=query, params=params)

    def execute_query_with_labels(self, query: str, params: dict[str, Any] = None):
        tree_df = pd.DataFrame(columns=[
            "Region",
            "VioScoreTotal",
            "Dimension",
            "Category",
            "Attribute"
        ]
        )
        # Drop any rows in case FastAPI is caching any data from previous response
        tree_df.drop(tree_df.index, inplace=True)

        try:
            with self.driver.session() as session:
                result = session.run(query=query, parameters=params)
                for i, record in enumerate(result):
                    for column in list(tree_df.columns):
                        tree_df.loc[i, column] = record[column] or 'None'
            return tree_df
        except SessionExpired:
            # Handle session expiration by retrying the query in a new session
            self.execute_query_with_labels(query=query, params=params)


def get_db_driver():
    return Neo4jDriver(uri=settings.NEO4J_URI, user=settings.NEO4J_USER, password=settings.NEO4J_PASSWORD)
