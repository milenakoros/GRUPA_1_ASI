"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 1.0.0
"""

from kedro.pipeline import Node, Pipeline  # noqa
from . import nodes

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        Node(
            func=nodes.load_raw,
            inputs="raw_data",
            outputs="used_cars_raw",
            name="load_raw",
        ),
        Node(
            func=nodes.basic_clean,
            inputs="used_cars_raw",
            outputs="clean_data",
            name="basic_clean"
        )
    ])
