from __future__ import annotations

from dataclasses import dataclass
import logging
import os
from typing import Optional

from tqdm import tqdm

from chateval.kernels.openai import OpenAIChat, OpenAIChatConfig
from chateval.metrics.metric import Metric, MetricConfig
from chateval.metrics.protocols.utils import PROTOCOLS_PATH
from chateval.utils.prompt_utils import format_necessary
from chateval.utils.py_util import (
    dict_to_str,
    get_answer_from_data,
    list_to_str,
    load_yaml,
    NO_ANSWER,
)

logging.basicConfig(level=logging.ERROR)


@dataclass
class GPTScoreConfig(MetricConfig):
    name: str
    protocol_config_path: str
    criteria: Optional[str] = None
    eval_model_config: OpenAIChatConfig = OpenAIChatConfig(
        model_name="gpt-3.5-turbo",
    )

    def __post_init__(self):
        self.protocol_config = load_yaml(self.protocol_config_path)


class GPTScore(Metric):
    def __init__(self, config: GPTScoreConfig):
        self.config = config
        self.evaluator = OpenAIChat(config.eval_model_config)

    def compute_sample(self, sample: dict, prediction: str) -> dict:

        prompt = self.config.protocol_config["prompt"]
        prompt_args = {}
        # instantiate prompt with criteria
        if self.config.criteria is not None:
            if self.config.criteria not in self.config.protocol_config["criteria"]:
                raise ValueError(
                    f"Criteria {self.config.criteria} not found in protocol config."
                )
            criteria_content = self.config.protocol_config["criteria"][
                self.config.criteria
            ]
            # likert protocol
            if self.config.protocol_config["eval_type"] == "cot_likert":
                criteria_content = dict_to_str(criteria_content)
                prompt_args["choices"] = ", ".join(
                    list(self.config.protocol_config["choice_scores"].keys())
                )

            prompt_args["criteria"] = criteria_content
        # instantiate prompt with input and completion
        # TODO(pfliu-nlp): the for loop is problematic
        for input_slot_name, output_slot_name in self.config.protocol_config[
            "input_outputs"
        ].items():
            prompt_args[input_slot_name] = sample[input_slot_name]
            prompt_args[output_slot_name] = prediction

        prompt_instantiated = format_necessary(prompt, **prompt_args)
        result = self.evaluator.execute(
            [
                {"role": "user", "content": prompt_instantiated},
            ]
        )

        extracted_result = get_answer_from_data(
            result, list(self.config.protocol_config["choice_scores"].keys())
        )

        if extracted_result in self.config.protocol_config["choice_scores"]:
            return {
                "value": self.config.protocol_config["choice_scores"][extracted_result],
                "detail": {
                    "prompt": prompt_instantiated,
                    "judgment": result,
                },
            }
        else:
            return {
                "value": -1,
                "detail": {
                    "prompt": prompt_instantiated,
                    "judgment": result,
                },
            }

    def compute(self, dataset: list[dict], predictions: list[str]) -> dict:
        results = []
        for sample, prediction in zip(tqdm(dataset), predictions):
            try:
                out = self.compute_sample(sample, prediction)
            except Exception as e:
                logging.warning(f"Error in computing GPTScore: {e}")
                out = None
            results.append(out)
        scores = [result["value"] if result is not None else None for result in results]
        details = [
            result["detail"] if result is not None else None for result in results
        ]

        value = 0
        no_score = 0
        for score in scores:
            if score is not None and score >= 0:
                value += score
            else:
                no_score += 1

        value = 0 if len(scores) - no_score == 0 else value / (len(scores) - no_score)
        return {
            "value": value,
            "no_score": no_score,
            "sample_values": scores,
            "details": details,
        }

    def compare(
        self, dataset: list[dict], predictions_1: list[str], predictions_2: list[str]
    ) -> dict:
        results = []
        for sample, prediction_1, predictions_2 in zip(
            tqdm(dataset), predictions_1, predictions_2
        ):
            try:
                out = self.compare_sample(sample, prediction_1, predictions_2)
            except (ValueError, TypeError, RuntimeError) as e:
                logging.warning(f"Error in computing GPTScore: {e}")
                out = None
            results.append(out)
        scores = [result["value"] if result is not None else None for result in results]
        details = [
            result["detail"] if result is not None else None for result in results
        ]

        value = 0
        no_score = 0
        for score in scores:
            if score is not None and score >= 0:
                value += score
            else:
                no_score += 1
        value = value / (len(scores) - no_score)
        return {
            "value": value,
            "no_score": no_score,
            "sample_values": scores,
            "details": details,
        }

    def compare_sample(
        self, sample: dict, prediction_1: str, prediction_2: str
    ) -> dict:

        prompt = self.config.protocol_config["prompt"]
        prompt_args = {}
        # instantiate prompt with criteria
        if self.config.criteria is not None:
            if self.config.criteria not in self.config.protocol_config["criteria"]:
                raise ValueError(
                    f"Criteria {self.config.criteria} not found in protocol config."
                )

            criteria_content = self.config.protocol_config["criteria"][
                self.config.criteria
            ]
            prompt_args["criteria"] = criteria_content

        # instantiate prompt with input and completion
        # TODO(pfliu-nlp): the for loop is problematic

        for input_slot_name, output_slot_names in self.config.protocol_config[
            "input_outputs"
        ].items():
            prompt_args[input_slot_name] = sample[input_slot_name]
            prompt_args[output_slot_names[0]] = prediction_1
            prompt_args[output_slot_names[1]] = prediction_2

        prompt_instantiated = format_necessary(prompt, **prompt_args)
        result = self.evaluator.execute(
            [
                {"role": "user", "content": prompt_instantiated},
            ]
        )

        extracted_result = get_answer_from_data(
            result, list(self.config.protocol_config["choice_scores"].keys())
        )

        if extracted_result in self.config.protocol_config["choice_scores"]:
            return {
                "value": self.config.protocol_config["choice_scores"][extracted_result],
                "detail": {
                    "prompt": prompt_instantiated,
                    "judgment": result,
                },
            }
        else:
            return {
                "value": -1,
                "detail": {
                    "prompt": prompt_instantiated,
                    "judgment": result,
                },
            }

    def rank(
        self,
        dataset: list[dict],
        predictions_list: list[list[str]],
    ) -> dict:
        results = []
        for sample, predictions in zip(tqdm(dataset), predictions_list):
            try:
                out = self.rank_sample(sample, predictions)
            except (ValueError, TypeError, RuntimeError) as e:
                logging.warning(f"Error in computing GPTScore: {e}")
                out = None
            results.append(out)
        scores = [result["value"] if result is not None else None for result in results]
        details = [
            result["detail"] if result is not None else None for result in results
        ]

        dict_sys_choice = {}
        no_score = 0
        for score in scores:
            if score is not None and score != NO_ANSWER:
                if score not in dict_sys_choice:
                    dict_sys_choice[score] = 1
                else:
                    dict_sys_choice[score] += 1
            else:
                no_score += 1

        # get the most frequent choice
        value = max(dict_sys_choice, key=dict_sys_choice.get)

        return {
            "value": value,
            "no_score": no_score,
            "sample_values": scores,
            "details": details,
        }

    def rank_sample(self, sample: dict, predictions: list[str]) -> dict:

        prompt = self.config.protocol_config["prompt"]
        prompt_args = {}
        # instantiate prompt with criteria
        if self.config.criteria is not None:
            if self.config.criteria not in self.config.protocol_config["criteria"]:
                raise ValueError(
                    f"Criteria {self.config.criteria} not found in protocol config."
                )

            criteria_content = self.config.protocol_config["criteria"][
                self.config.criteria
            ]
            prompt_args["criteria"] = criteria_content

        for input_slot_name, output_slot_name in self.config.protocol_config[
            "input_outputs"
        ].items():
            prompt_args[input_slot_name] = sample[input_slot_name]
            prompt_args[output_slot_name] = list_to_str(predictions)

        prompt_args["n"] = len(predictions)

        prompt_instantiated = format_necessary(prompt, **prompt_args)
        result = self.evaluator.execute(
            [
                {"role": "user", "content": prompt_instantiated},
            ]
        )

        choices = [str(i + 1) for i in range(len(predictions))]
        extracted_result = get_answer_from_data(result, choices)

        if extracted_result in choices:
            return {
                "value": extracted_result,
                "detail": {
                    "prompt": prompt_instantiated,
                    "judgment": result,
                },
            }
        else:
            return {
                "value": NO_ANSWER,
                "detail": {
                    "prompt": prompt_instantiated,
                    "judgment": result,
                },
            }


_GPT_METRICS: [str, Metric] = {
    "generic_bool/relevance": GPTScore(
        GPTScoreConfig(
            name="generic_bool/relevance",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_bool.yaml"),
            criteria="relevance",
        ),
    ),
    "generic_bool/coherence": GPTScore(
        GPTScoreConfig(
            name="generic_bool/coherence",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_bool.yaml"),
            criteria="coherence",
        ),
    ),
    "generic_bool/helpfulness": GPTScore(
        GPTScoreConfig(
            name="generic_bool/helpfulness",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_bool.yaml"),
            criteria="helpfulness",
        ),
    ),
    "generic_bool/grammar": GPTScore(
        GPTScoreConfig(
            name="generic_bool/grammar",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_bool.yaml"),
            criteria="grammar",
        ),
    ),
    "generic_bool/harmlessness": GPTScore(
        GPTScoreConfig(
            name="generic_bool/harmlessness",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_bool.yaml"),
            criteria="harmlessness",
        ),
    ),
    "generic_likert/helpfulness": GPTScore(
        GPTScoreConfig(
            name="generic_likert/helpfulness",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_likert.yaml"),
            criteria="helpfulness",
        ),
    ),
    "generic_likert/relevance": GPTScore(
        GPTScoreConfig(
            name="generic_likert/relevance",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_likert.yaml"),
            criteria="relevance",
        ),
    ),
    "generic_likert/coherence": GPTScore(
        GPTScoreConfig(
            name="generic_likert/coherence",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_likert.yaml"),
            criteria="coherence",
        ),
    ),
    "generic_likert/harmlessness": GPTScore(
        GPTScoreConfig(
            name="generic_likert/harmlessness",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_likert.yaml"),
            criteria="harmlessness",
        ),
    ),
    "generic_pairwise/helpfulness": GPTScore(
        GPTScoreConfig(
            name="generic_pairwise/coherence",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_pairwise.yaml"),
            criteria="helpfulness",
        ),
    ),
    "generic_pairwise/relevance": GPTScore(
        GPTScoreConfig(
            name="generic_pairwise/relevance",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_pairwise.yaml"),
            criteria="relevance",
        ),
    ),
    "generic_pairwise/coherence": GPTScore(
        GPTScoreConfig(
            name="generic_pairwise/coherence",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_pairwise.yaml"),
            criteria="coherence",
        ),
    ),
    "generic_pairwise/harmlessness": GPTScore(
        GPTScoreConfig(
            name="generic_pairwise/harmlessness",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_pairwise.yaml"),
            criteria="harmlessness",
        ),
    ),
    "generic_rank/helpfulness": GPTScore(
        GPTScoreConfig(
            name="generic_rank/helpfulness",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_rank.yaml"),
            criteria="helpfulness",
        ),
    ),
    "generic_rank/relevance": GPTScore(
        GPTScoreConfig(
            name="generic_rank/relevance",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_rank.yaml"),
            criteria="relevance",
        ),
    ),
    "generic_rank/coherence": GPTScore(
        GPTScoreConfig(
            name="generic_rank/coherence",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_rank.yaml"),
            criteria="coherence",
        ),
    ),
    "generic_rank/harmlessness": GPTScore(
        GPTScoreConfig(
            name="generic_rank/harmlessness",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "generic_rank.yaml"),
            criteria="harmlessness",
        ),
    ),
    "llama_likert/helpfulness": GPTScore(
        GPTScoreConfig(
            name="lama_likert/helpfulness",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "llama_likert.yaml"),
            criteria="helpfulness",
        ),
    ),
    "debate_overall/relevance": GPTScore(
        GPTScoreConfig(
            name="debate_overall/relevance",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "debate_overall.yaml"),
            criteria="relevance",
        ),
    ),
    "debate_overall/persuasiveness": GPTScore(
        GPTScoreConfig(
            name="debate_overall/persuasiveness",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "debate_overall.yaml"),
            criteria="persuasiveness",
        ),
    ),
    "debate_overall/responsiveness": GPTScore(
        GPTScoreConfig(
            name="debate_overall/responsiveness",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "debate_overall.yaml"),
            criteria="responsiveness",
        ),
    ),
    "debate_overall/coherence": GPTScore(
        GPTScoreConfig(
            name="debate_overall/coherence",
            protocol_config_path=os.path.join(PROTOCOLS_PATH, "debate_overall.yaml"),
            criteria="coherence",
        ),
    ),
}
