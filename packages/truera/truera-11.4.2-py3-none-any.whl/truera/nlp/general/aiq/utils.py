from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

import numpy as np
import pandas as pd

from truera.nlp.general.aiq.filtering_utils import get_accuracy_group_name_dict
from truera.nlp.general.container.model import NLPModelProxy
from truera.nlp.general.utils.configs import TokenType
from truera.protobuf.public.aiq import intelligence_service_pb2 as is_pb
from truera.rnn.general.aiq.clustering import SpectralHierarchicalClusterer
from truera.rnn.general.container.artifacts import ArtifactsContainer

WIDGET_STYLE = dict(description_width='initial')
# Max length of strings representing multiple words/tokens.
WORD_COLLECTION_MAX_LENGTH = 64


# Anywhere else this should live?
@dataclass
class NLPSplitData:
    ids: Sequence[int]
    tokens: Sequence[Sequence[int]]
    token_map: Mapping[int, str]
    preds: Sequence[int]
    labels: Sequence[int]
    influences: Sequence[Sequence[int]]
    seq_lengths: Optional[Sequence[int]] = None

    segments: Optional[Sequence[int]] = None
    segment_id_to_name: Optional[Sequence[int]] = None
    segment_name_to_point_id: Optional[Sequence[int]] = None
    grad_paths: Optional[Sequence[int]] = None

    # TODO: Could/should this be a dataframe instead?

    def __post_init__(self):
        # Cast to numpy array
        self.ids = np.array(self.ids)
        self.tokens = np.array(self.tokens)
        self.preds = np.array(self.preds)
        self.labels = np.array(self.labels)
        self.influences = np.array(self.influences)
        self.seq_lengths = np.array(self.seq_lengths)

        self.n_records = len(self.ids)
        self.classes = set(np.unique(self.preds)) | set(np.unique(self.labels))

        self.output_dim = np.array(self.influences).shape[1]
        self.n_classes = 1 if self.output_dim == 2 else self.output_dim

        self.influences_comparative = self._get_infl_comparative()

    def convert_token_type(self):
        #TODO: Tokens -> word conversion
        pass

    def get_correlation_matrices(
        self,
        class_idx: int,
        data_idx: int = None,
        filter_top_n=None
    ) -> Union[List[np.ndarray], np.ndarray]:
        """Computes correlation matrices from gradients

        Args:
            class_idx (int): Index of the class QoI to select 
            data_idx (int, optional): Index of the data to select. If None, computes for all records. Defaults to None.
            filter_top_n (_type_, optional): Filters only top n correlated gradient paths. If None, computes across all paths. Defaults to None.

        Raises:
            ValueError: If grad_paths is not ingested into NLPSplitData.

        Returns:
            Union[List[np.ndarray], np.ndarray]: Either correlation matrix for a single record or a list of correlation matrcies for all records
        """
        if data_idx is not None:
            gp = [self.grad_paths[class_idx][data_idx]]
        else:
            gp = self.grad_paths[class_idx]

        if not self.grad_paths:
            raise ValueError(
                "Missing grad_paths from NLPSplitData. Cannot get correlation matrices"
            )
        else:
            return SpectralHierarchicalClusterer._get_correlation_matrices(
                gp, filter_top_n=filter_top_n
            )

    @classmethod
    def from_artifacts_container(
        cls,
        artifacts_container: ArtifactsContainer,
        model_proxy: NLPModelProxy,
        num_records: int = None,
        offset: int = 0,
        token_type: TokenType = TokenType.TOKEN
    ) -> NLPSplitData:
        """Creates NLPSplitData from ArtifactsContainer

        Args:
            artifacts_container (ArtifactsContainer): the ArtifactsContainer object to read from
            model_proxy (NLPModelProxy): The NLPModelProxy object to read from.
            num_records (int, optional): The number of records to read. Defaults to None.
            offset (int, optional): Offset value to start reading from. Defaults to 0.
            token_type (TokenType, optional): The TokenType format to read. Defaults to TokenType.TOKEN.

        Returns:
            NLPSplitData: An NLPSplitData instance containing data from the ArtifactsContainer
        """
        if num_records is None:
            num_records = model_proxy.get_default_num_records(
                artifacts_container
            )

        # eventually deprecate distinction between word/token. User uploads whatever format they want to work in
        artifacts_df = model_proxy.get_artifacts_df(
            artifacts_container,
            token_type=token_type,
            num_records=num_records,
            offset=offset
        )

        # Get segments
        try:
            segment_id_to_name = model_proxy.get_segment_id_to_name(
                artifacts_container
            )
            segments = model_proxy.get_segments(
                artifacts_container, num_records=num_records, offset=offset
            )[0]

            segment_name_to_point_id = defaultdict(list)
            for point_id, segment_id in enumerate(segments):
                segment_name = segment_id_to_name[int(segment_id)]
                segment_name_to_point_id[segment_name].append(point_id)
            segment_name_to_point_id = segment_name_to_point_id
        except FileNotFoundError:
            segments = None
            segment_id_to_name = None
            segment_name_to_point_id = None

        try:
            grad_paths = []
            # NOTE: grad paths are loaded in memory. will this be an issue?
            for cls_idx in range(
                model_proxy.get_num_classes(artifacts_container)
            ):
                grad_paths.append(
                    model_proxy.get_grad_path_influences(
                        artifacts_container,
                        num_records=num_records,
                        token_type=token_type,
                        offset=offset,
                        class_idx=cls_idx
                    )
                )
        except FileNotFoundError:
            grad_paths = None
        return NLPSplitData(
            ids=artifacts_df.original_index.to_list(),
            tokens=artifacts_df.tokens.to_list(),
            token_map=model_proxy.get_vocab(artifacts_container),
            preds=artifacts_df.preds.to_list(),
            labels=artifacts_df.labels.to_list(),
            influences=artifacts_df.influences.to_list(),
            seq_lengths=artifacts_df.lengths.to_list(),
            segment_name_to_point_id=segment_name_to_point_id,
            grad_paths=grad_paths
        )

    @classmethod
    def from_pb(cls, pb_resp: is_pb.SplitDataResponse) -> NLPSplitData:
        """Create NLPSplitData from is_pb.SplitDataResponse

        Args:
            pb_resp (is_pb.SplitDataResponse): The protobuf response to read from

        Returns:
            NLPSplitData: The NLPSplitData object
        """
        # TODO: Adapt to NLP protobuf response
        values = pb_resp.split_data.column_value_map

        ids = list(values['ids'].ints.values)
        orig_text = list(values['text'].strings.values)
        tokens = list(values['tokens'].strings.values)
        labels = list(values['labels'].floats.values)
        preds = list(values['preds'].floats.values)
        infl = list(values['influences'].floats.values)
        seq_lengths = list(values['seq_length'].ints.values)
        return NLPSplitData(
            ids=ids,
            tokens=tokens,
            token_map=None,
            preds=preds,
            labels=labels,
            influences=infl,
            seq_lengths=seq_lengths
        )

    def _get_infl_comparative(self) -> np.ndarray:
        """Computes comparative influences from existing influences

        Returns:
            np.ndarray: comparative influences.
        """
        if self.output_dim == 1:
            influences_comparative = np.squeeze(self.influences, axis=1)
            comparative_direction = np.copy(self.labels)
            comparative_direction[comparative_direction == 0] = -1
            comparative_direction = np.expand_dims(
                comparative_direction, axis=-1
            )  # allow broadcastable shape since labels are dimsize=1, and influences are dimsize=num_tokens
            influences_comparative = influences_comparative * comparative_direction
        else:
            all_labels = np.arange(self.output_dim
                                  )[None, :].repeat(len(self.labels), 0)

            non_labels = all_labels[(all_labels - self.labels[:, None]) != 0
                                   ].reshape(len(self.labels), -1)

            # influences_comparative is the influence of the label class minues the nonlabel classes
            # It is used for sorting in some downstream cases.
            influences_comparative = self.influences[
                np.arange(len(self.influences)), self.labels] - self.influences[
                    np.arange(len(self.influences))[:, None].
                    repeat(self.output_dim - 1, -1), non_labels].mean(1)
        return influences_comparative

    def slice_data(self, num_records: int, offset: int = 0) -> NLPSplitData:
        if num_records is None and offset == 0:
            return self
        elif num_records is None:
            slicer = lambda x: x[offset:]
        else:
            slicer = lambda x: x[offset:offset + num_records]
        return NLPSplitData(
            ids=slicer(self.ids),
            tokens=slicer(self.tokens),
            token_map=self.token_map,
            preds=slicer(self.preds),
            labels=slicer(self.labels),
            influences=slicer(self.influences),
        )

    def as_df(self) -> pd.DataFrame:
        """Formats NLPSplitData into a DataFrame

        Returns:
            pd.DataFrame: Each column is an attribute and each row a record.
        """
        df = {}
        # Add unparsed text here?
        df['tokens'] = list(self.tokens)
        df['influences'] = list(self.influences)
        df['influences_comparative'] = list(self.influences_comparative)
        df['lengths'] = self.seq_lengths
        df['preds'] = self.preds
        df['labels'] = self.labels
        df['original_index'] = self.ids
        df['data_index'] = np.arange(len(self.ids))
        return pd.DataFrame(df)


# TODO: Migrate util functions out to original locations after applications use standardized NLPSplitData as input (MLNN-520)
def get_group_ind_dict(split_data: NLPSplitData):
    """
    get a dictionary of data indices divided into each accuracy-based group
    """

    # Typically we treat binary as a single class. But for confusion matrix, we need to break it out
    n_classes = max(split_data.n_classes, 2)

    accuracy_group_name_dict = get_accuracy_group_name_dict(n_classes)
    group_ind_dict = {}

    for label in range(n_classes):
        for pred in range(n_classes):
            group_ind_dict[accuracy_group_name_dict[(label, pred)]] = np.where(
                (split_data.preds == pred) & (split_data.labels == label)
            )[0]
    group_ind_dict['All'] = np.arange(split_data.n_records)
    return group_ind_dict


def filter_token_influences_df(
    token_influence_df: pd.DataFrame,
    group_inds: np.ndarray,
    max_words_to_track: int,
    two_tailed=False,
    filter_func=lambda x: np.ones(len(x), dtype=bool),
    ranking_col_name='occurrences',
    ascending=False
):
    """
    filter and rank token_influence df based on influence and
    append other metadata such as average influence and occurrences.
    two_tailed: how to select top max_words_to_track in the ranked df. if True,
    select evenly from both ends
    """

    token_influence_filtered_df = token_influence_df[
        token_influence_df.data_index.isin(group_inds)]
    token_influence_filtered_df = token_influence_filtered_df[
        filter_func(token_influence_filtered_df)]

    influence_cols = [
        cn for cn in token_influence_filtered_df.columns if 'influence' in cn
    ]
    token_influence_filtered_df = token_influence_filtered_df.groupby(
        ['tokens']
    ).agg(lambda x: list(x)).reset_index()

    for c in influence_cols:
        token_influence_filtered_df[
            c + '_mean'] = token_influence_filtered_df[c].apply(np.mean)
        token_influence_filtered_df[
            c + '_std'] = token_influence_filtered_df[c].apply(np.std)
    token_influence_filtered_df[
        'word_occurrences'] = token_influence_filtered_df.data_index.apply(len)
    token_influence_filtered_df[
        'word_frequencies'] = token_influence_filtered_df[
            'word_occurrences'] / len(token_influence_df)
    token_influence_filtered_df['occurrences'
                               ] = token_influence_filtered_df.data_index.apply(
                                   lambda x: len(set(x))
                               )
    if (len(token_influence_filtered_df) == 0):
        token_influence_filtered_df[
            'frequencies'] = token_influence_filtered_df['occurrences']
    else:
        token_influence_filtered_df[
            'frequencies'] = token_influence_filtered_df['occurrences'] / len(
                np.unique(
                    np.concatenate(token_influence_filtered_df.data_index)
                )
            )
    token_influence_filtered_df = token_influence_filtered_df.sort_values(
        by=ranking_col_name, ascending=ascending
    )
    num_vocab = len(token_influence_filtered_df)
    max_words_to_track = min(max_words_to_track, num_vocab)
    if two_tailed:
        return pd.concat(
            [
                token_influence_filtered_df.iloc[:int(max_words_to_track / 2)],
                token_influence_filtered_df.iloc[-int(max_words_to_track / 2):]
            ],
            axis=0
        )
    else:
        return token_influence_filtered_df.iloc[:int(max_words_to_track)]


def token_influence_info(
    split_data: NLPSplitData,
    max_words_to_track: int,
    token_type=TokenType.TOKEN,
    ranking='influence',
    filter_by_error_drivers=False,
    language: str = "english",
    aggregate_stop_words: bool = False,
    aggregate_stems: bool = False,
):
    """
    Get token df of each accuracy-based groups and 
    (1) filter error driver tokens, 
    (2) rank tokens according to their influence or occurrences, 
    (3) aggregate tokens based on stop words and/or stems.
    """
    group_ind_dict = get_group_ind_dict(split_data)

    token_maps = []

    seen_stems = defaultdict(set)
    seen_stop_words = set()

    if aggregate_stems or aggregate_stop_words:
        import nltk
        stop_words = nltk.corpus.stopwords.words(language)
        stemmer = nltk.stem.SnowballStemmer(language)

        def word_collection(words):
            """
            Render a string representing a collection of words but shorten it if
            it is too long.
            """
            if len(words) == 1:
                # Any word collection with a single example will produce that
                # example instead of the "{ ... }" format.
                return next(iter(words))

            temp = ",".join(words)
            if len(temp) > WORD_COLLECTION_MAX_LENGTH - 2:
                temp = temp[0:WORD_COLLECTION_MAX_LENGTH - 2] + ".."

            return "{" + temp + "}"

        def track_words(tok):
            if tok in stop_words:
                seen_stop_words.add(tok)

            stem = stemmer.stem(tok)
            seen_stems[stem].add(tok)

            return tok

        token_maps.append(track_words)

    if aggregate_stop_words:

        def map_stop_words(tok):
            if tok in stop_words:
                return word_collection(seen_stop_words)
            else:
                return tok

        token_maps.append(map_stop_words)

    if aggregate_stems:

        def map_stem(tok):
            if tok[0] == "{":
                # ignore the stop word aggregates
                return tok

            stem = stemmer.stem(tok)
            return word_collection(seen_stems[stem])

        token_maps.append(map_stem)

    def get_filter_func(filter_by_error_drivers=False):
        if filter_by_error_drivers:
            # Find the tokens moving it away from the correct class
            return lambda df: df.influences_comparative < 0
        else:
            return lambda df: np.ones(len(df), dtype=bool)

    tokens = split_data.tokens

    for m in token_maps:
        tokens = np.vectorize(m)(tokens)

    token_influence_df = NLPModelProxy._aggregate_by_token(
        tokens,
        split_data.influences,
        split_data.influences_comparative,
        split_data.seq_lengths,
        split_data.preds,
        split_data.labels,
        np.arange(split_data.n_records),
    )

    token_influences_group_dict = {}

    filter_func = get_filter_func(filter_by_error_drivers)

    if ranking == 'occurrence':
        ranking_col_name = 'occurrences'
        two_tailed = False
        ascending = False
    elif ranking == 'frequency':
        ranking_col_name = 'frequencies'
        two_tailed = False
        ascending = False
    elif ranking == 'influence':
        ranking_col_name = 'influences_comparative_mean'
        ascending = True

    for group_name, group_inds in group_ind_dict.items():
        if group_name == 'All' and ranking == 'influence':
            two_tailed = True
        elif group_name != 'All' and ranking == 'influence':
            two_tailed = False

        token_influences_group_dict[group_name] = filter_token_influences_df(
            token_influence_df,
            group_inds,
            filter_func=filter_func,
            two_tailed=two_tailed,
            max_words_to_track=max_words_to_track,
            ranking_col_name=ranking_col_name,
            ascending=ascending
        )
    return token_influences_group_dict
