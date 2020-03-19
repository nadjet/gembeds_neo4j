import pandas as pd
import csv
from utils.log import logger
from gensim.models import KeyedVectors
import os
import argparse

class ConceptWithEmbeddings:
    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name
        self.embeddings = None

    def __eq__(self, other):
        if not isinstance(other,ConceptWithEmbeddings) or other.identifier != self.identifier:
            return False
        return True

    def __key(self):
        return self.identifier

    def __hash__(self):
        return hash(self.__key())

    def set_embeddings(self, embeddings):
        self.embeddings = embeddings

    def get_embeddings(self):
        return self.embeddings

    def get_name(self):
        return self.name

    def get_identifier(self):
        return self.identifier


class ConceptsWithEmbeddings:

    def __init__(self,folder):
        self.folder = folder
        self.model = KeyedVectors.load_word2vec_format(os.path.join(folder, "wheel_model.bin"))
        self.concepts = set()

    def add_concept(self,identifier,name):
        concept = ConceptWithEmbeddings(identifier,name)
        if concept not in self.concepts:
            concept.set_embeddings(self.model[str(concept.identifier)])
            self.concepts.add(concept)

    def set_concepts(self,file_name="relations.csv"):
        df = pd.read_csv(os.path.join(self.folder,file_name),sep="\t")
        for i,row in df.iterrows():
            if i%100==0:
                logger.info("{} {}".format(i,len(self.concepts)))
            if row["source_type"]=="Athlete":
                self.add_concept(row["source"],row["source_name"])
            if row["target_type"]=="Athlete":
                self.add_concept(row["target"],row["target_name"])

    def get_embeddings_and_names(self):
        assert (self.concepts is not None and len(self.concepts) > 0)
        concept = self.concepts.pop()
        embeddings = [concept.get_embeddings()]
        names = [concept.get_name()]
        for concept in self.concepts:
            embeddings.append(concept.get_embeddings())
            names.append(concept.get_name())
        logger.info(len(embeddings))
        logger.info(len(names))
        return embeddings,names

    def get_embeddings_and_ids(self):
        assert (self.concepts is not None and len(self.concepts) > 0)
        concept = self.concepts.pop()
        embeddings = [concept.get_embeddings()]
        identifiers = [concept.get_identifier()]
        for concept in self.concepts:
            embeddings.append(concept.get_embeddings())
            identifiers.append(concept.get_identifier())
        logger.info(len(embeddings))
        logger.info(len(identifiers))
        return embeddings,identifiers


if __name__ == "__main__":
    description_msg = 'For each athlete, get its most similar athletes with similarity above threshold'
    parser = argparse.ArgumentParser(description=description_msg)
    parser.add_argument('-i', '--input', help='The input folder containing the bin model and relations csv', required=True)
    parser.add_argument('-o', '--output', help='The output folder', required=True)
    parser.add_argument('-t', '--threshold', help='The similarity threshold', default=0.9)

    args = vars(parser.parse_args())

    concepts = ConceptsWithEmbeddings(args["input"])
    concepts.set_concepts()
    _,ids = concepts.get_embeddings_and_ids()
    ids = set(ids)

    counter = 0

    with open(os.path.join(args["output"],"similar.csv"),"w") as fw:
        wr = csv.writer(fw,delimiter="\t")
        wr.writerow(["id","similarity","similar"])
        for identifier in ids:
            if counter % 100 == 0:
                logger.info(counter)
            tuples = concepts.model.most_similar(str(identifier),topn=20)
            for tuple in tuples:
                if tuple[1]>=args["threshold"] and int(tuple[0]) in ids: # the most similar item must be a node
                    wr.writerow([identifier,tuple[1],tuple[0]])
                elif tuple[1]<args["threshold"]:
                    break
            counter=counter+1