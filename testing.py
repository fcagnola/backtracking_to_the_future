from backtracking_to_the_future import process_citations
from networkx import DiGraph

graph = process_citations('citations_sample.csv')

for i, n in graph.adj.items():
    print(i, n)