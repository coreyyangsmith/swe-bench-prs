# Example call for getting versions by building the repo locally
python get_versions.py \
    --instances_path "../collect/gpt4o_runs/gpt4o_Qiskit_qiskit.json" \
    --retrieval_method github \
    --conda_env "gpt_qiskit" \
    --num_workers 2 \
    --path_conda "/Users/corey/anaconda3" \
    --testbed "../collect/testbed"

# Example call for getting versions from github web interface
# python get_versions.py \
#     --path_tasks "<path to sphinx task instances>" \
#     --retrieval_method github \
#     --num_workers 25 \
#     --output_dir "<path to folder to save versioned task instances to>"