import tempfile
from typing import Any, Dict, List, Tuple, cast

import mlflow
from loguru import logger
from playground.core.tracking.git_utils import get_branch_name, get_commit_hash, get_gitlab_path, get_repo_name


def flatten(d: Dict[str, Any], parent="", sep="/") -> Dict[str, float]:
    items: List[Tuple[str, float]] = []
    for k, v in d.items():
        new_key = parent + sep + k if parent else k
        if isinstance(v, dict):
            items.extend(flatten(d=v, parent=new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_git_tags() -> Dict[str, str]:
    tags = dict()
    commit = get_commit_hash()
    tags["mlflow.source.git.commit"] = commit
    tags["mlflow.source.git.branch"] = get_branch_name()
    tags["git.branch"] = get_branch_name()
    tags["git_repo"] = get_repo_name()
    tags["git.url"] = f"{get_gitlab_path()}/-/tree/{commit}"
    return tags


def get_experiment_id(experiment_name: str) -> str:
    exp = mlflow.get_experiment_by_name(name=experiment_name)
    if mlflow.get_experiment_by_name(name=experiment_name) is None:
        logger.info(f"experiment {experiment_name} is not found -> creating the experiment")
        exp_id = mlflow.create_experiment(name=experiment_name)
    else:
        exp_id = exp.experiment_id
    return cast(str, exp_id)


def submit_metrics(metrics: Dict[str, Any], parameters: Dict[str, Any]) -> None:
    metrics = flatten(d=metrics)
    parameters = flatten(d=parameters)
    mlflow.log_metrics(metrics=metrics)
    mlflow.log_params(params=parameters)


def submit_matplotlib_figures(figures: Dict):
    with tempfile.TemporaryDirectory() as tempd:
        for figure_name, figure in figures.items():
            local_path = f"{tempd}/{figure_name}.png"
            figure.savefig(local_path, bbox_inches="tight")
            mlflow.log_artifact(local_path, "img")
