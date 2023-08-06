[<img src="https://img.shields.io/pypi/v/flowui-project?color=%231BA331&label=PyPI&logo=python&logoColor=%23F7F991%20">](https://pypi.org/project/flowui-project/)
[<img src="https://img.shields.io/docker/v/taufferconsulting/flowui-backend?label=Backend&logo=docker&style=flat">](https://hub.docker.com/r/taufferconsulting/flowui-backend)
[<img src="https://img.shields.io/docker/v/taufferconsulting/flowui-frontend?label=Frontend&logo=docker&style=flat">](https://hub.docker.com/r/taufferconsulting/flowui-frontend)
[<img src="https://img.shields.io/readthedocs/flowui?color=%23799194&label=Docs&logo=Read%20the%20Docs&logoColor=white">](link)




# Domino Project
Domino is an open source workflow management platform, containing:

- an intuitive Graphical User Interface that facilitates creating, editing and supervising any type of Workflows (e.g. data processing, machine learning, etc...)
- a REST API that controls a running Apache Airflow instance
- a standard way of writing Operators which follows good practices for data typing, documentation and distribution

<br>

# Domino Infrastructure

Per Platform:
- Frontend service
- Backend service
- Database
- Airflow services
- Github repository for GitSync of Workflows

<br>


## Shared storage structure:
Shared workflow data could be stored in a remote source (e.g. S3 bucket) or locally (for dev and tests only).

```
/shared_storage
..../{dag-id}
......../{run-id}
............/{task-id}
................/results
..................../log.txt
..................../result.npy
..................../result.html
................/report
................/xcom_out
..................../xcom_out.json


```

<br>

## Operators
Each Operator will have:
- A `operator.py` file with the source code to be executed, as the `piece_function()`
- A `models.py` file containing the Pydantic models that define the input, output and secrets for the Operator
- A `metadata.json` file containing the Operators metadata, including frontend node style

Each dependency group from an Operators repository will build an independent Docker image. This dependency group image has the following basic file struture within `/home`:
```
# This path holds the source code from the Operators repository, it comes built in the Image
/operators_repository
..../config.toml
..../operators
......../{OPERATOR-NAME}
............/metadata.json    # OPTIONAL
............/model.py         # REQUIRED
............/operator.py      # REQUIRED
..../.flowui
......../dependencies_map.json
......../compiled_metadata.json
..../dependencies
......../requirements.txt     # If dependency group was defined with a requirements.txt file
```