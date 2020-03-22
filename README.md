# Node similarity with graph embeddings using Node2Vec

I created a graph to model athletes and their participation to event at olympic games in Neo4J. The data and cypher queries to do so is included in this [repository](https://github.com/nadjet/neo4j_example).

To find out the similarity between athletes, I run node2vec that learns a feature representation for each node in the graph using random walks. Having an embedding for every node, I can now find the most similar nodes to a given node using, say Gensim, just like word2vec.



## Content

1. `node4j_edges.py` queries Neo4J to output a csv with all the edges in the graph.
 
2. `node2vec.py` runs [an implementation of node2vec](https://github.com/VHRanger/nodevectors) on the list of edges and produces the embeddings model.

3. `embeddings.py`, which, for each athlete node, looks for its most similar athlete nodes in the top 20 with a similarity threshold >=0.9.
 
## Examples

Each graph in the following examples was part obtained with the following query, so as to display the Athlete's sport and show if they have any in common:

```
MATCH (s1:Sport)-[]-(e1:Event)-[]-(p1:Participation)-[]-(m:Athlete),
      (s2:Sport)-[]-(e2:Event)-[]-(p2:Participation)-[]-(n:Athlete),
      (s3:Sport)-[]-(e3:Event)-[]-(p3:Participation)-[]-(o:Athlete) 
WHERE 
      id(n)=3 AND id(m)=130302 AND id(o)=42807 
RETURN m,n,o,s1,e1,p1,s2,e2,p2,s3,e3,p3
```

### Example 1
For node with id 3, we get only 2 nodes with similarity above 0.9. The subgraph subsuming those 3 athlete nodes is shown in the screenshot below.
The similarity of node 3 with the two other nodes is quite remote in this case: they share the same game (1900 Summer) and the fact that they all got at least a gold medal in that game. Furthermore, although they share to have only participated in this particular game, it is unclear whether this is a distinctive feature that sets them apart from the other athletes participating in the game. The two similar nodes share neither team nor sport with node 3 (although they share sport amongst themselves). All in all, it is probably the conjunction of those features that make them similar.


![alt text](https://github.com/nadjet/gembeds_neo4j/blob/master/images/example1.png)

### Example 2

Node with id 8807 is also most similar to only 2 nodes given the threshold, as shown in the figure below. These share the game and team, and the fact that none earnt any medal. Also none of those athletes participated in any other games. On the other hand, neither athletes share any event or sport.

![alt text](https://github.com/nadjet/gembeds_neo4j/blob/master/images/example2.png)

### Example 3

Node with id 4 has all 20 most similar nodes with similarity threshold above 0.9. The figure below display the 4 most similar nodes, which all share team and sport.

![alt text](https://github.com/nadjet/gembeds_neo4j/blob/master/images/example3.png)

## What next?

An idea would be to implement a template-based Natural Language Generation system that verbalizes the nodes similarities (and possibly differences) in a short text.