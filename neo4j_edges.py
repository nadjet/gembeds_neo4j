from utils.neo4j import Neo4jUtils
import argparse
import pandas as pd
from utils.log import logger
import os


class Neo4jEdges:

    QUERY = 'MATCH (a)-[r]->(b) RETURN id(a) as source, ' \
            'id(b) as target, ' \
            'labels(a)[0] as source_type, ' \
            'labels(b)[0] as target_type, ' \
            'COALESCE(a.name,"") as source_name,' \
            'COALESCE(b.name,"") as target_name,' \
            'type(r) as relation'

    def __init__(self):
        self.neo4j_utils = Neo4jUtils(Neo4jUtils.NEO4J_URL, Neo4jUtils.NEO4J_USERNAME, Neo4jUtils.NEO4J_PWD)
        self.edges = []

    def set_edges(self):
        with self.neo4j_utils.get_driver().session() as session:
            logger.info("Running query: {}".format(Neo4jEdges.QUERY))
            results = session.run(Neo4jEdges.QUERY)
            logger.info("...Running query done!")
            counter=0
            for edge in results:
                if counter%100==0:
                    logger.info(counter)
                counter+=1
                self.edges.append({"source":edge["source"],
                                   "source_name":edge["source_name"],
                                   "source_type":edge["source_type"],
                                   "target":edge["target"],
                                   "target_name":edge["target_name"],
                                   "target_type":edge["target_type"],
                                   "relation":edge["relation"]})


if __name__ == "__main__":
    description_msg = 'Query neo4j for list of edges'
    parser = argparse.ArgumentParser(description=description_msg)
    parser.add_argument('-o', '--output', help='The output folder', required=True)

    args = vars(parser.parse_args())
    neo4j_edges = Neo4jEdges()
    neo4j_edges.set_edges()

    df = pd.DataFrame(neo4j_edges.edges)
    df.to_csv(os.path.join(args["output"],"relations.csv"),index=False,sep="\t")
    df = df[["source","target"]]
    df.to_csv(os.path.join(args["output"],"edges.csv"),index=False,sep="\t",header=False)