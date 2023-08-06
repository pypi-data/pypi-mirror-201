# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.evaluate.mlflow.models.evaluation.azureml._classifier_evaluator import ClassifierEvaluator
from azureml.evaluate.mlflow.models.evaluation.azureml._classifier_multilabel_evaluator import \
    ClassifierMultilabelEvaluator
from azureml.evaluate.mlflow.models.evaluation.azureml._regressor_evaluator import RegressorEvaluator
from azureml.evaluate.mlflow.models.evaluation.azureml._translation_evaluator import TranslationEvaluator
from azureml.evaluate.mlflow.models.evaluation.azureml._qna_evaluator import QnAEvaluator
from azureml.evaluate.mlflow.models.evaluation.azureml._summarization_evaluator import SummarizationEvaluator
from azureml.evaluate.mlflow.models.evaluation.azureml._ner_evaluator import NerEvaluator


class EvaluatorFactory:

    def __init__(self):
        self._evaluators = {
            "classifier": ClassifierEvaluator,
            "classifier-multilabel": ClassifierMultilabelEvaluator,
            "multiclass": ClassifierEvaluator,
            "regressor": RegressorEvaluator,
            "ner": NerEvaluator,
            "text-ner": NerEvaluator,
            "text-classifier": ClassifierEvaluator,
            'text-classifier-multilabel': ClassifierMultilabelEvaluator,
            "translation": TranslationEvaluator,
            "summarization": SummarizationEvaluator,
            "question-answering": QnAEvaluator
        }

    def get_evaluator(self, model_type):
        return self._evaluators[model_type]()

    def register(self, name, obj):
        self._evaluators[name] = obj
