import os
from ai.embed import Embedder
import chromadb

class KnowledgeEmergence:
    def __init__(self):
        self.embedder = Embedder()
        self.knowledge_units = []
        self.vectors = []
        self.client = chromadb.Client()
        self.db = self.client.create_collection("coguniverse")

    def load_knowledge(self, file_list):
        for f in file_list:
            if os.path.exists(f):
                with open(f, 'r', encoding='utf-8') as fp:
                    content = fp.read().split("\n\n")
                    for line in content:
                        clean = line.strip()
                        if clean:
                            self.knowledge_units.append(clean)

    def build_vector_db(self):
        self.vectors = self.embedder.encode(self.knowledge_units)
        for i, vec in enumerate(self.vectors):
            self.db.add(
                embeddings=[vec.tolist()],
                ids=[str(i)]
            )

    def cluster_knowledge(self):
        from sklearn.cluster import KMeans
        n_clusters = min(8, len(self.vectors))
        model = KMeans(n_clusters=n_clusters)
        return model.fit_predict(self.vectors)

    def build_relations(self, threshold=0.7):
        relations = []
        vecs = self.vectors
        for i in range(len(vecs)):
            for j in range(i + 1, len(vecs)):
                sim = self.cosine_sim(vecs[i], vecs[j])
                if sim > threshold:
                    relations.append((i, j))
        return relations

    def cosine_sim(self, a, b):
        import numpy as np
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))