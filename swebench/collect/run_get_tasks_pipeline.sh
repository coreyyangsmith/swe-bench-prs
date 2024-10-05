#!/usr/bin/env bash

# If you'd like to parallelize, do the following:
# * Create a .env file in this folder
# * Declare GITHUB_TOKENS=token1,token2,token3...

python ./collect/get_tasks_pipeline.py \
    --repos 'conan-io/conan' 'conda/conda' 'dagster-io/dagster' 'huggingface/transformers'\
    --path_prs './collect/path_prs' \
    --path_tasks './collect/path_tasks'