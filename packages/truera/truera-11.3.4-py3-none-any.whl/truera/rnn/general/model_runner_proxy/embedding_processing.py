import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from truera.client.intelligence.explainer import NonTabularExplainer


class EmbeddingAnalyzer:
    """A class to help analyze embeddings. 
    """

    def __init__(self, explainer: NonTabularExplainer, cluster_centers):
        self.explainer = explainer
        # Used for analysis on embedding clustering centers
        self.clusters = cluster_centers

    def get_clusters(self):
        if self.clusters is None:
            self.clusters = self.find_clusters()

        return self.clusters

    def get_activations(self):
        """Returns the embedding activations.
        """
        artifacts_container = self.explainer._artifacts_container
        num_records = self.explainer._aiq.model.get_default_num_records(
            artifacts_container
        )
        neuron_activations = np.concatenate(
            self.explainer._aiq.model.get_activations(
                artifacts_container=artifacts_container,
                num_records=num_records
            ),
            axis=0
        )
        return neuron_activations

    def find_clusters(
        self, n_clusters: int = 3, mathematical_center=True
    ) -> np.ndarray:
        """Finds clusters via kmeans on the embedding activations

        Args:
            n_clusters (int, optional): number of clusters to find. Defaults to 3.
            mathematical_center (bool, optional): If True, uses the kmeans defaults. Otherwise, find the closest example. Defaults to True.
                Can be useful for centers that are far from its various records, but is experimental.

        Returns:
            np.ndarray: The cluster centers with shape (n_clusters x embedding_size)
        """
        neuron_activations = self.get_activations()
        kmeans = KMeans(n_clusters=n_clusters,
                        random_state=0).fit(neuron_activations)

        if mathematical_center:
            clusters = kmeans.cluster_centers_
        else:
            closest_embeddings = []
            for cluster_i in range(len(kmeans.cluster_centers_)):
                cluster_center = kmeans.cluster_centers_[cluster_i]
                repeated = np.expand_dims(cluster_center, axis=1).repeat(
                    len(neuron_activations), axis=1
                )

                reshaped = np.swapaxes(repeated, 0, 1)
                dist = np.sqrt(
                    np.square(neuron_activations - reshaped).sum(axis=-1)
                )
                closest_embeddings.append(neuron_activations[np.argmin(dist)])

            clusters = np.asarray(closest_embeddings)
        self.clusters = clusters
        return clusters

    def _scatter_data(
        self, embeddings: np.ndarray, pca: PCA, color='blue'
    ) -> go.Scatter3d:
        """Converts embeddings to 3d visualized scatter points

        Args:
            embeddings (np.ndarray): vectors of embeddings
            pca (PCA): The dimensionality reduction
            color (str, optional): the color of the scatter. Defaults to 'blue'.

        Returns:
            go.Scatter3d
        """
        dim_reduced = pca.fit_transform(embeddings)

        x = dim_reduced[:, 0]
        y = dim_reduced[:, 1]
        z = dim_reduced[:, 2]

        return go.Scatter3d(
            x=x, y=y, z=z, mode='markers', marker=dict(color=color)
        )

    def display(self):
        """Shows a 3D figure with the embeddings and their cluster centers in red
        """
        neuron_activations = self.get_activations()
        pca = PCA(n_components=3)
        pca.fit(neuron_activations)
        emb_3d = self._scatter_data(neuron_activations, pca)
        emb_3d.name = "embeddings"
        clusters = self.get_clusters()
        cluster_3d = self._scatter_data(clusters, pca, color='red')
        cluster_3d.name = "cluster centers"
        fig = go.Figure(data=[emb_3d, cluster_3d])
        fig.show()
