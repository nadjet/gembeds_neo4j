from neo4j import GraphDatabase
from utils.log import logger

VERBOSE = True


class Neo4jUtils(object):
    NEO4J_URL = "bolt://localhost"
    NEO4J_USERNAME = "neo4j"
    NEO4J_PWD = "admin"

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def get_driver(self):
        return self._driver

    def close(self):
        self._driver.close()

    def execute_query(self, query, variable_value, file_name):
        with self.get_driver().session() as session:
            # haven't figured out how to do that with session.run
            this_query = query.replace("\{{}\}".format(file_name),variable_value)
            logger.info("Executing neo4j main: " + this_query)
            results = session.run(this_query)
            logger.info("...Executing main done!")
            return results
        return None