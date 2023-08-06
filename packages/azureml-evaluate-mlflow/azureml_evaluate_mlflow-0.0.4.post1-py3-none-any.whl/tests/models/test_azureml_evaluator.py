# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
# flake8: noqa
import ast

from azureml.metrics.azureml_regression_metrics import AzureMLRegressionMetrics
from azureml.metrics.azureml_classification_metrics import AzureMLClassificationMetrics
import matplotlib.pyplot as plt
from unittest import mock
import numpy as np
import json
import pandas as pd
import pytest
import sklearn
from contextlib import nullcontext as does_not_raise
from azureml.metrics import compute_metrics, constants
import azureml.evaluate.mlflow as mlflow

from mlflow.exceptions import MlflowException
from azureml.evaluate.mlflow.models.evaluation import evaluate
from azureml.evaluate.mlflow.models.evaluation.default_evaluator import (
    _get_classifier_global_metrics,
    _infer_model_type_by_labels,
    _extract_raw_model,
    _extract_predict_fn,
    _get_regressor_metrics,
    _get_binary_sum_up_label_pred_prob,
    _get_classifier_per_class_metrics,
    _gen_classifier_curve,
    _evaluate_custom_metric,
    _compute_df_mode_or_mean,
    _CustomMetric,
)
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.datasets import load_iris

from tempfile import TemporaryDirectory
from os.path import join as path_join
from PIL import Image, ImageChops
import io

# noqa: F811
from .utils import (  # noqa: F811
    get_run_data,
    linear_regressor_model_uri,
    diabetes_dataset,
    multiclass_logistic_regressor_model_uri,
    iris_dataset,
    get_iris,
    newsgroup_dataset,
    newsgroup_dataset_text_pair,
    arxiv_dataset,
    multiclass_llm_model_uri,
    summarization_llm_model_uri,
    qna_llm_model_uri,
    translation_llm_model_uri,
    billsum_dataset,
    squad_qna_dataset,
    opus_dataset,
    multilabel_llm_model_uri,
    y_transformer_arxiv,
    ner_dataset,
    get_connll_dataset,
    ner_llm_model_uri
)
from mlflow.models.utils import plot_lines


def assert_dict_equal(d1, d2, rtol):
    for k in d1:
        assert k in d2
        assert np.isclose(d1[k], d2[k], rtol=rtol)


def test_regressor_evaluation(linear_regressor_model_uri, diabetes_dataset):  # noqa: F811
    '''
    format of result needs to be changed
    2) non-scalar metrics should be part of metrics? -> residuals, predicted_true
    '''
    # mlflow.set_tracking_uri("azureml://eastus2.api.azureml.ms/mlflow/v1.0/subscriptions/72c03bf3-4e69-41af-9532"
    #                         "-dfcdc3eefef4/resourceGroups/shared-model-evaluation-rg/providers/Microsoft"
    #                         ".MachineLearningServices/workspaces/aml-shared-model-evaluation-ws")
    with mlflow.start_run() as run:
        result = evaluate(
            linear_regressor_model_uri,
            diabetes_dataset._constructor_args["data"],
            model_type="regressor",
            targets=diabetes_dataset._constructor_args["targets"],
            dataset_name=diabetes_dataset.name,
            evaluators="azureml",
        )

    _, metrics, tags, artifacts = get_run_data(run.info.run_id)

    model = mlflow.aml.load_model(linear_regressor_model_uri, model_type="regressor")

    y = diabetes_dataset.labels_data
    y_pred = model.predict(diabetes_dataset.features_data)
    metric = AzureMLRegressionMetrics()
    expected_metrics = metric.compute(y_test=y, y_pred=y_pred)
    for metric_key in expected_metrics:
        if np.isscalar(expected_metrics[metric_key]):
            assert np.isclose(
                expected_metrics[metric_key],
                result.metrics[metric_key],
                rtol=1e-3,
            )


def test_regressor_evaluation_mlflow_model(linear_regressor_model_uri,
                                           diabetes_dataset):  # noqa: F811
    '''
    format of result needs to be changed
    2) non-scalar metrics should be part of metrics? -> residuals, predicted_true
    '''
    linear_regressor_model_mlflow = mlflow.aml.load_model(linear_regressor_model_uri)
    with mlflow.start_run() as run:
        result = evaluate(
            linear_regressor_model_mlflow,
            diabetes_dataset._constructor_args["data"],
            model_type="regressor",
            targets=diabetes_dataset._constructor_args["targets"],
            dataset_name=diabetes_dataset.name,
            evaluators="azureml",
        )

    _, metrics, tags, artifacts = get_run_data(run.info.run_id)

    y = diabetes_dataset.labels_data
    y_pred = linear_regressor_model_mlflow.predict(diabetes_dataset.features_data)
    expected_metrics = compute_metrics(task_type=constants.Tasks.REGRESSION, y_test=y, y_pred=y_pred)
    for metric_key in expected_metrics:
        if np.isscalar(expected_metrics[metric_key]):
            assert np.isclose(
                expected_metrics[metric_key],
                result.metrics[metric_key],
                rtol=1e-3,
            )


def test_multi_classifier_evaluation(multiclass_logistic_regressor_model_uri,
                                     iris_dataset):  # noqa: F811
    metrics_args = {
        "class_labels": np.unique(iris_dataset.labels_data),
        "train_labels": np.unique(iris_dataset.labels_data)
    }
    with mlflow.start_run() as run:
        result = evaluate(
            multiclass_logistic_regressor_model_uri,
            iris_dataset._constructor_args["data"],
            model_type="classifier",
            targets=iris_dataset._constructor_args["targets"],
            dataset_name=iris_dataset.name,
            evaluators="azureml",
            evaluator_config=metrics_args
        )

    _, metrics, tags, artifacts = get_run_data(run.info.run_id)

    model = mlflow.aml.load_model(multiclass_logistic_regressor_model_uri, "classifier")

    y = iris_dataset.labels_data
    y_pred = model.predict(iris_dataset.features_data)
    y_probs = model.predict_proba(iris_dataset.features_data)

    expected_metrics = compute_metrics(task_type=constants.Tasks.CLASSIFICATION, y_test=y, y_pred=y_pred,
                                       y_pred_proba=y_probs, **metrics_args)
    for metric_key in expected_metrics:
        if np.isscalar(expected_metrics[metric_key]):
            assert np.isclose(
                expected_metrics[metric_key],
                result.metrics[metric_key],
                rtol=1e-3,
            )


def test_multiclass_llm_evaluation(multiclass_llm_model_uri, newsgroup_dataset):  # noqa: F811
    metrics_args = {
        "class_labels": np.unique(newsgroup_dataset.labels_data),
        "train_labels": np.unique(newsgroup_dataset.labels_data)
    }
    with mlflow.start_run() as run:
        result = evaluate(
            multiclass_llm_model_uri,
            newsgroup_dataset._constructor_args["data"],
            model_type="classifier",
            targets=newsgroup_dataset._constructor_args["targets"],
            dataset_name=newsgroup_dataset.name,
            evaluators="azureml",
            evaluator_config=metrics_args
        )

    _, metrics, tags, artifacts = get_run_data(run.info.run_id)

    model = mlflow.aml.load_model(multiclass_llm_model_uri, "classifier")

    y = newsgroup_dataset.labels_data
    y_pred = model.predict(newsgroup_dataset.features_data)
    y_probs = model.predict_proba(newsgroup_dataset.features_data)
    y_pred_numpy = model.predict(newsgroup_dataset.features_data.to_numpy())
    assert all(np.isclose(y_pred[y_pred.columns[0]].to_numpy(), y_pred_numpy, rtol=1e-3))
    expected_metrics = compute_metrics(task_type=constants.Tasks.CLASSIFICATION, y_test=y, y_pred=y_pred,
                                       y_pred_proba=y_probs, **metrics_args)
    for metric_key in expected_metrics:
        if np.isscalar(expected_metrics[metric_key]):
            assert np.isclose(
                expected_metrics[metric_key],
                result.metrics[metric_key],
                rtol=1e-3,
            )


def test_multiclass_llm_evaluation_text_pair(multiclass_llm_model_uri, newsgroup_dataset_text_pair):  # noqa: F811
    metrics_args = {
        "class_labels": np.unique(newsgroup_dataset_text_pair.labels_data),
        "train_labels": np.unique(newsgroup_dataset_text_pair.labels_data)
    }
    with mlflow.start_run() as run:
        result = evaluate(
            multiclass_llm_model_uri,
            newsgroup_dataset_text_pair._constructor_args["data"],
            model_type="classifier",
            targets=newsgroup_dataset_text_pair._constructor_args["targets"],
            dataset_name=newsgroup_dataset_text_pair.name,
            evaluators="azureml",
            evaluator_config=metrics_args
        )

    _, metrics, tags, artifacts = get_run_data(run.info.run_id)

    model = mlflow.aml.load_model(multiclass_llm_model_uri, "classifier")

    y = newsgroup_dataset_text_pair.labels_data
    y_pred = model.predict(newsgroup_dataset_text_pair.features_data)
    y_probs = model.predict_proba(newsgroup_dataset_text_pair.features_data)
    y_pred_numpy = model.predict(newsgroup_dataset_text_pair.features_data.to_numpy())
    assert all(np.isclose(y_pred[y_pred.columns[0]].to_numpy(), y_pred_numpy, rtol=1e-3))
    expected_metrics = compute_metrics(task_type=constants.Tasks.CLASSIFICATION, y_test=y, y_pred=y_pred,
                                       y_pred_proba=y_probs, **metrics_args)
    for metric_key in expected_metrics:
        if np.isscalar(expected_metrics[metric_key]):
            assert np.isclose(
                expected_metrics[metric_key],
                result.metrics[metric_key],
                rtol=1e-3,
            )


def test_multilabel_llm_evaluation(multilabel_llm_model_uri, arxiv_dataset,
                                   y_transformer_arxiv):  # noqa: F811
    metrics_args = {
        # "class_labels": np.array(y_transformer_arxiv.classes_),
        # "train_labels": np.array(y_transformer_arxiv.classes_),
        "multilabel": True
        # "y_transformer": y_transformer_arxiv
    }
    with mlflow.start_run() as run:
        result = evaluate(
            multilabel_llm_model_uri,
            arxiv_dataset._constructor_args["data"],
            model_type="classifier-multilabel",
            targets=arxiv_dataset._constructor_args["targets"],
            dataset_name=arxiv_dataset.name,
            evaluators="azureml",
            evaluator_config=metrics_args
        )

    _, metrics, tags, artifacts = get_run_data(run.info.run_id)

    model = mlflow.aml.load_model(multilabel_llm_model_uri, "classifier")

    y = np.array(list(map(lambda x: ast.literal_eval(x), arxiv_dataset.labels_data)))
    y_pred = model.predict(arxiv_dataset.features_data)
    y_pred = np.array(list(map(lambda x: ast.literal_eval(x), y_pred[y_pred.columns[0]].to_numpy())))
    y_probs = model.predict_proba(arxiv_dataset.features_data)
    expected_metrics = compute_metrics(task_type=constants.Tasks.TEXT_CLASSIFICATION, y_test=y,
                                       y_pred=y_pred, y_pred_proba=y_probs, **metrics_args)
    for metric_key in expected_metrics:
        if np.isscalar(expected_metrics[metric_key]):
            assert np.isclose(
                expected_metrics[metric_key],
                result.metrics[metric_key],
                rtol=1e-3,
            )


def test_ner_llm_evaluation(ner_llm_model_uri, ner_dataset):  # noqa: F811
    _, _, labels_list = get_connll_dataset()
    metrics_args = {
        'train_label_list': labels_list,
        'label_list': labels_list
    }
    with mlflow.start_run() as run:
        result = evaluate(
            ner_llm_model_uri,
            ner_dataset._constructor_args["data"],
            model_type="ner",
            targets=ner_dataset._constructor_args["targets"],
            dataset_name=ner_dataset.name,
            evaluators="azureml",
            evaluator_config=metrics_args
        )

    _, metrics, tags, artifacts = get_run_data(run.info.run_id)

    model = mlflow.aml.load_model(ner_llm_model_uri, "ner")
    preds = model.predict(ner_dataset.features_data)
    y_pred = list(map(lambda x: ast.literal_eval(x), preds[preds.columns[0]].values.tolist()))
    y_test = list(map(lambda x: ast.literal_eval(x), list(ner_dataset.labels_data)))
    expected_metrics = compute_metrics(task_type=constants.Tasks.TEXT_NER, y_test=y_test, y_pred=y_pred,
                                       **metrics_args)
    for metric_key in expected_metrics:
        if np.isscalar(expected_metrics[metric_key]):
            assert np.isclose(
                expected_metrics[metric_key],
                result.metrics[metric_key],
                rtol=1e-3,
            )


def test_parse_aml_tracking_uri():
    current_tracking_uri = mlflow.get_tracking_uri()
    mlflow.set_tracking_uri("azureml://eastus2.api.azureml.ms/mlflow/v1.0/subscriptions/72c03bf3-4e69-41af-9532"
                            "-dfcdc3eefef4/resourceGroups/shared-model-evaluation-rg/providers/Microsoft"
                            ".MachineLearningServices/workspaces/aml-shared-model-evaluation-ws")
    from azureml.evaluate.mlflow.models.evaluation.azureml.azureml_evaluator import AzureMLEvaluator
    azureml_evaluator = AzureMLEvaluator()
    workspace, resource_group, subscription = azureml_evaluator._parse_aml_tracking_uri()
    assert workspace == "aml-shared-model-evaluation-ws"
    assert resource_group == "shared-model-evaluation-rg"
    assert subscription == "72c03bf3-4e69-41af-9532-dfcdc3eefef4"
    mlflow.set_tracking_uri(current_tracking_uri)


def test_summarization_llm_evaluation(summarization_llm_model_uri, billsum_dataset):  # noqa: F811
    metrics_args = {

    }
    with mlflow.start_run() as run:
        result = evaluate(
            summarization_llm_model_uri,
            billsum_dataset._constructor_args["data"],
            model_type="summarization",
            targets=billsum_dataset._constructor_args["targets"],
            dataset_name=billsum_dataset.name,
            evaluators="azureml",
            evaluator_config=metrics_args
        )

    _, metrics, tags, artifacts = get_run_data(run.info.run_id)

    model = mlflow.aml.load_model(summarization_llm_model_uri)

    y = billsum_dataset.labels_data
    y_test = np.reshape(y, (-1, 1))
    y_pred = model.predict(billsum_dataset.features_data)
    y_pred = y_pred[y_pred.columns[0]].to_numpy().tolist()
    expected_metrics = compute_metrics(task_type=constants.Tasks.SUMMARIZATION, y_test=y_test.tolist(), y_pred=y_pred,
                                       **metrics_args)
    for metric_key in expected_metrics:
        if np.isscalar(expected_metrics[metric_key]):
            assert np.isclose(
                expected_metrics[metric_key],
                result.metrics[metric_key],
                rtol=1e-3,
            )


def test_translation_llm_evaluation(translation_llm_model_uri, opus_dataset):  # noqa: F811
    metrics_args = {

    }
    with mlflow.start_run() as run:
        result = evaluate(
            translation_llm_model_uri,
            opus_dataset._constructor_args["data"],
            model_type="translation",
            targets=opus_dataset._constructor_args["targets"],
            dataset_name=opus_dataset.name,
            evaluators="azureml",
            evaluator_config=metrics_args
        )

    _, metrics, tags, artifacts = get_run_data(run.info.run_id)

    model = mlflow.aml.load_model(translation_llm_model_uri)

    y = opus_dataset.labels_data
    y_test = np.reshape(y, (-1, 1))
    y_pred = model.predict(opus_dataset.features_data)
    y_pred = y_pred[y_pred.columns[0]].to_numpy().tolist()
    expected_metrics = compute_metrics(task_type=constants.Tasks.TRANSLATION, y_test=y_test.tolist(), y_pred=y_pred,
                                       **metrics_args)
    for metric_key in expected_metrics:
        if np.isscalar(expected_metrics[metric_key]):
            assert np.isclose(
                expected_metrics[metric_key],
                result.metrics[metric_key],
                rtol=1e-3,
            )


def test_qna_llm_evaluation(qna_llm_model_uri, squad_qna_dataset):  # noqa: F811
    metrics_args = {

    }
    with mlflow.start_run() as run:
        result = evaluate(
            qna_llm_model_uri,
            squad_qna_dataset._constructor_args["data"],
            model_type="question-answering",
            targets=squad_qna_dataset._constructor_args["targets"],
            dataset_name=squad_qna_dataset.name,
            evaluators="azureml",
            evaluator_config=metrics_args
        )

    _, metrics, tags, artifacts = get_run_data(run.info.run_id)

    model = mlflow.aml.load_model(qna_llm_model_uri)

    y = squad_qna_dataset.labels_data
    # y_test = np.reshape(y, (-1, 1))
    y_pred = model.predict(squad_qna_dataset.features_data)
    y_pred = y_pred[y_pred.columns[0]].to_numpy().tolist()
    expected_metrics = compute_metrics(task_type=constants.Tasks.QUESTION_ANSWERING, y_test=y.tolist(), y_pred=y_pred,
                                       **metrics_args)
    for metric_key in expected_metrics:
        if np.isscalar(expected_metrics[metric_key]):
            assert np.isclose(
                expected_metrics[metric_key],
                result.metrics[metric_key],
                rtol=1e-3,
            )


def test_load_model():
    pass


def test_log_predictions():
    pass
