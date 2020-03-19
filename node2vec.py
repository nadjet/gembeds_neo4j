import os
import argparse

import networkx as nx

# fast node2vec implementation: https://github.com/VHRanger/nodevectors
from nodevectors import Node2Vec

if __name__ == "__main__":
    description_msg = 'Generating graph embeddings with node2vec'
    parser = argparse.ArgumentParser(description=description_msg)
    parser.add_argument('-i', '--input', help='The input file containing the list of edges', required=True)
    parser.add_argument('-o', '--output', help='The output folder', required=True)

    args = vars(parser.parse_args())

    G = nx.read_edgelist(args["input"], delimiter='\t')
    embedding_size = 64

    # Fit embedding model to graph
    g2v = Node2Vec(walklen=5,
                   epochs=10,
                   threads=4,
                   n_components=embedding_size,
                   keep_walks=False,
                   w2vparams={"window": 3, "negative": 3, "iter": 3,
                              "batch_words": 64, "workers": 2})
    # way faster than other node2vec implementations
    # Graph edge weights are handled automatically
    g2v.fit(G)

    # query embeddings for node 42
    print(g2v.predict(42))

    g2v.save(os.path.join(args["output"], 'node2vec.pckl'))
    # Save model to gensim.KeyedVector format
    g2v.save_vectors(os.path.join(args["output"], "wheel_model.bin"))
