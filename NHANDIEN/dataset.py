# dataset.py
from huggingface_hub import hf_hub_download
import pandas as pd

def tai_dataset():
    repo_id = "fptudsc/face-celeb-vietnamese"
    filename = "data/train-00000-of-00001-e97e83ad56524b9c.parquet"
    file_path = hf_hub_download(repo_id=repo_id, filename=filename, repo_type="dataset")
    df = pd.read_parquet(file_path)
    return df
