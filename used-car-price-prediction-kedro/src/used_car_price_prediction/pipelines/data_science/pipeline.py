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
        ),
        Node(
            func=nodes.split_to_train_test,
            inputs=['clean_data', 'params:split.test_size', 'params:split.random_state'],
            outputs=['X_train', 'X_test', 'y_train', 'y_test'],
            name='split_to_train_test'
        ),
        Node(
            func=nodes.train_autogluon,
            inputs=['X_train', 'y_train', 'params:autogluon', 'params:model.random_state'],
            outputs='model_autogluon',
            name='train_autogluon'
        ),
        Node(
            func=nodes.evaluate_autogluon,
            inputs=['model_autogluon', 'X_test', 'y_test', 'params:autogluon'],
            outputs='metrics_autogluon',
            name='evaluate_autogluon'
        )
    ])

"""
Node(
    func=nodes.train_baseline,
    inputs=['X_train', 'y_train', 'params:model'],
    outputs='model_baseline',
    name='train_baseline'
),
Node(
    func=nodes.evaluate,
    inputs=['model_baseline', 'X_test', 'y_test'],
    outputs='metrics_baseline',
    name='evaluate'
)
"""
