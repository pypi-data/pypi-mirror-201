import logging
import random
import re
import string
from typing import Any, Mapping, Optional, Sequence

import pandas as pd
import pkg_resources

pkg_resources.require("shap>=0.41.0")
import shap
# pylint: disable=E0102
from shap import *

from truera.client.truera_authentication import TokenAuthentication
from truera.client.truera_workspace import TrueraWorkspace


def _id_generator(
    size: int = 5,
    chars: Optional[str] = None,
) -> str:
    if chars is None:
        chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(size))


def _filter_kwargs(kwargs: Mapping[str, str],
                   extracted_kws: Sequence[str]) -> Mapping[str, str]:
    return {x: kwargs[x] for x in extracted_kws if x in kwargs}


def _infer_classification_or_regression(model: Any) -> bool:
    if hasattr(model, "predict_proba"):
        return "classification"
    if hasattr(model, "predict"):
        return "regression"
    raise ValueError(
        "Cannot discern if model is classifier or regressor! Pass in `score_type`!"
    )


class Explainer(shap.Explainer):

    def __init__(self, model: object, *args, **kwargs):
        """Construct a SHAP-style explainer that also uploads to your TruEra deployment if supplied.

        Notes: 
            Because this class is primarily a wrapper, a large number of kwargs (described below) are available.
            All kwargs are noted described below by the function they are passed to, either in SHAP or TruEra.
            Please refer to (https://shap.readthedocs.io) or TruEra (https://docs.truera.com) documentation respectively for full description of use.

        Args:
            model: model object
            **connection_string: URL of the TruEra deployment. Defaults to None.
            **token: Authentication token to connect to TruEra deployment. Defaults to None.
            **masker: Argument needed for SHAP `Explainer`
            **link: Argument needed for SHAP `Explainer`
            **algorithm: Argument needed for SHAP `Explainer`
            **output_names: Argument needed for SHAP `Explainer`
            **feature_names: Argument needed for SHAP `Explainer`
            **linearize_link: Argument needed for SHAP `Explainer`
            **seed: Argument needed for SHAP `Explainer`
            **input_type: Argument needed for `add_project`
            **num_default_influences: Argument needed for `add_project`
            **pre_to_post_feature_map: Argument needed for `add_data_collection`
            **provide_transform_with_model: Argument needed for `add_data_collection`
            **additional_pip_dependencies: Argument needed for 'add_python_model`
            **additional_modules: Argument needed for `add_python_model`
            **classification_threshhold: Argument needed for `add_python_model`
            **train_split_name: Argument needed for `add_python_model`
            **train_parameters: Argument needed for `add_python_model`
            **verify_model: Argument needed for `add_python_model`
            **compute_predictions: Argument needed for `add_python_model`
            **compute_feature_influences: Argument needed for `add_python_model`
            **compute_for_all_splits: Argument needed for `add_python_model`
            **virtual_models: Argument needed for `upload_project`
            **upload_strategy: Argument needed for `upload_project`
            **upload_error_influences: Argument needed for `upload_project`
            **upload_partial_dependencies: Argument needed for `upload_project`
        """

        # Get shap explainer.
        shap_explainer_kwargs = _filter_kwargs(
            kwargs, [
                "masker", "link", "algorithm", "output_names", "feature_names",
                "linearize_link", "seed"
            ]
        )
        self.shap_explainer = shap.Explainer(
            model, *args, **shap_explainer_kwargs
        )

        # Set up TruEra.
        self.connection_string = kwargs.get("connection_string", None)
        self.token = kwargs.get("token", None)
        if self.connection_string is None or self.token is None:
            logging.warning(
                "`connection_string` or `token` not specified. Contact TruEra for help (support.truera.com)."
            )
        else:
            logging.info(
                f"Access your TruEra application at: {self.connection_string}"
            )

            # Create TrueraWorkspace.
            self.tru = TrueraWorkspace(
                self.connection_string,
                TokenAuthentication(self.token),
                # TODO: Remove ignore_version_mismatch when PyPi release up to date
                ignore_version_mismatch=True,
                log_level=logging.ERROR
            )
            self.tru.set_environment("local")

            # Add project.
            project = kwargs.get("project", f"project_{_id_generator()}")
            influence_type = kwargs.get("influence_type", "shap")
            score_type = kwargs.get("score_type", None)
            if score_type is None:
                output_type = _infer_classification_or_regression(model)
                score_type = "probits" if output_type == "classification" else "regression"
            add_project_kwargs = _filter_kwargs(
                kwargs, ["input_type", "num_default_influences"]
            )
            self.tru.add_project(
                project=project, score_type=score_type, **add_project_kwargs
            )
            self.tru.set_influence_type(influence_type)
            logging.info(f"added project: {project}")

            # Add data collection.
            data_collection_name = kwargs.get(
                "data_collection_name", f"data_collection_{_id_generator()}"
            )
            add_data_collection_kwargs = _filter_kwargs(
                kwargs,
                ["pre_to_post_feature_map", "provide_transform_with_model"]
            )
            self.tru.add_data_collection(
                data_collection_name=data_collection_name,
                **add_data_collection_kwargs
            )
            logging.info(f"added data collection: {data_collection_name}")

            # Add model.
            model_name = kwargs.get("model_name", None)
            if model_name is None:
                model_name = re.split(
                    r'[`!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?~]', str(model)
                )[0] + str("_") + _id_generator()
            add_python_model_kwargs = _filter_kwargs(
                kwargs, [
                    "additional_pip_dependencies", "additional_modules",
                    "classification_threshhold", "train_split_name",
                    "train_parameters", "verify_model", "compute_predictions",
                    "compute_feature_influences", "compute_for_all_splits"
                ]
            )
            self.tru.add_python_model(
                model_name=model_name, model=model, **add_python_model_kwargs
            )
            logging.info(f"added model: {model_name}")

            # Upload project.
            upload_project_kwargs = _filter_kwargs(
                kwargs, [
                    "virtual_models", "upload_strategy",
                    "upload_error_influences", "upload_partial_dependencies"
                ]
            )
            self.tru.upload_project(**upload_project_kwargs)
            logging.info(f"uploaded to: {self.connection_string}")

    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        """Get the shap values for a list of parallel iterable datasets using the model agnostic explainer. Also upload the first dataset in the list to TruEra if connection supplied.

        Notes:
            Because this class is primarily a wrapper, a large number of kwargs (described below) are available.
            All kwargs are noted described below by the function they are passed to, either in SHAP or TruEra.
            Please refer to SHAP (https://shap.readthedocs.io) or TruEra (https://docs.truera.com) documentation respectively for full description of use.

            If you pass more than one dataset using *args, post_data, outputs/label_data, and extra_data_df will not be added to TruEra.

        Args:
            *args: a list of parallel iterable datasets
            **max_evals: Argument needed for SHAP `__call__`
            **main_effects: Argument needed for SHAP `__call__`
            **error_bounds: Argument needed for SHAP `__call__`
            **batch_size: Argument needed for SHAP `__call__`
            **outputs: Argument needed for SHAP `__call__`, analagous to label_data
            **silent: Argument needed for SHAP `__call__`
            **post_data: Argument needed for `add_data_split`
            **label_col_name: Argument needed for `add_data_split`
            **id_col_name: Argument needed for `add_data_split`
            **extra_data_df: Argument needed for `add_data_split`
            **split_type: Argument needed for `add_data_split`
            **sample_count: Argument needed for `add_data_split`
            **sample_kind: Argument needed for `add_data_split`
            **seed: Argument needed for `add_data_split`
            **prediction_col_name: Argument needed for `add_data_split`
            **timestamp_col_name: Argument needed for `add_data_split`
            **split_time_range_begin: Argument needed for `add_data_split`
            **split_time_range_end: Argument needed for `add_data_split`
            **virtual_models: Argument needed for `upload_project`
            **upload_strategy: Argument needed for `upload_project`
            **upload_error_influences: Argument needed for `upload_project`
            **upload_partial_dependencies: Argument needed for `upload_project`
        """
        ret = []
        shap_explainer_shap_values_kwargs = _filter_kwargs(
            kwargs, [
                "max_evals", "main_effects", "error_bounds", "batch_size",
                "outputs", "silent"
            ]
        )
        for data in args:
            data_for_model = data.copy()
            id_col_name = kwargs.get("id_col_name", None)
            if id_col_name:
                data_for_model.drop(id_col_name, axis=1, inplace=True)

            ret.append(
                self.shap_explainer(
                    data_for_model, **shap_explainer_shap_values_kwargs
                )
            )
        ret = ret[0] if len(ret) == 1 else ret

        if self.connection_string is None or self.token is None:
            return ret

        if len(args) > 1:
            for curr in [
                "data_split_name", "post_data", "label_data", "y", "extra_data"
            ]:
                if curr in kwargs:
                    raise ValueError(
                        f"Argument `{curr}` cannot be specified when given multiple datasplits!"
                    )

        # data split
        data_split_name = kwargs.get(
            "data_split_name", f"data_split_{_id_generator()}"
        )
        data_split_kwargs = [
            "post_data",
            "y",  # using outputs instead of label_data, conforms to SHAP
            "label_col_name",
            "id_col_name",
            "extra_data_df",
            "split_type",
            "sample_count",
            "sample_kind",
            "seed",
            "prediction_col_name",
            "timestamp_col_name",
            "split_time_range_begin",
            "split_time_range_end"
        ]
        add_data_split_kwargs = _filter_kwargs(kwargs, data_split_kwargs)
        if "y" in kwargs:
            add_data_split_kwargs["label_data"] = add_data_split_kwargs.pop("y")

        if data_split_name in self.tru.get_data_splits():
            logging.info(f"{data_split_name} already exists, skipped")
        else:
            for data in args:
                if data_split_name is None:
                    data_split_name = f"data_split_{_id_generator()}"
                self.tru.add_data_split(
                    data_split_name=data_split_name,
                    pre_data=data,
                    **add_data_split_kwargs
                )
                logging.info(f"added data split: {data_split_name}")

        # Upload project.
        upload_project_kwargs = _filter_kwargs(
            kwargs, [
                "virtual_models", "upload_strategy", "upload_error_influences",
                "upload_partial_dependencies"
            ]
        )
        self.tru.upload_project(**upload_project_kwargs)
        logging.info(f"uploaded to: {self.connection_string}")
        return ret

    def get_truera_workspace(self) -> TrueraWorkspace:
        """Fetch the TruEra workspace associated with the `Explainer`.
        """
        return self.tru
