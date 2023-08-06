from typing import Optional
import requests
import json
import os


class Api:
    def __init__(
        self, token: Optional[str] = None, url: str = "https://tune.activeloop.dev"
    ):
        self.token = token or os.environ["ACTIVETUNE_TOKEN"]
        self.url = url

    def set_openai_key(self, key: str):
        return requests.get(
            self.url + "/api/set_openai_key", {"token": self.token, "key": key}
        ).json()

    def create_dataset(self, name: str, description: str = ""):
        return requests.get(
            self.url + "/api/create_dataset",
            {"token": self.token, "name": name, "description": description},
        ).text

    def list_datasets(self):
        return requests.get(
            self.url + "/api/get_datasets", {"token": self.token}
        ).json()

    def add_sample(
        self,
        dataset_id: str,
        input: str = "",
        model_output: str = "",
        model_id: str = "",
        expected_output: str = "",
        feedback=0,
        meta={},
    ):
        return requests.get(
            self.url + "/api/add_sample",
            {
                "token": self.token,
                "dataset_id": dataset_id,
                "input": input,
                "model_output": model_output,
                "model_id": model_id,
                "expected_output": expected_output,
                "feedback": feedback,
                "meta": json.dumps(meta),
            },
        ).text

    def get_data(self, dataset_id: str):
        return requests.get(
            self.url + "/api/get_data", {"token": self.token, "dataset_id": dataset_id}
        ).json()

    def set_feedback(self, sample_id: str, value: int):
        return requests.get(
            self.url + "/api/set_feedback",
            {"token": self.token, "sample_id": sample_id, "value": self},
        )

    def set_meta(self, sample_id: str, meta):
        return requests.get(
            self.url + "/api/set_meta",
            {
                "token": self.token,
                "sample_id": sample_id,
                "meta_json": json.dumps(meta),
            },
        )

    def update_meta(self, sample_id: str, meta):
        return requests.get(
            self.url + "/api/update_meta",
            {
                "token": self.token,
                "sample_id": sample_id,
                "meta_json": json.dumps(meta),
            },
        )

    def add_meta_column(self, dataset_id: str, column_name: str):
        return requests.get(
            self.url + "/api/add_meta_column",
            {"token": self.token, "dataset_id": dataset_id, "column_name": column_name},
        )
