import os
import csv
import gzip
import pandas as pd
import typing as t
from sentence_transformers import util
from contextlib import contextmanager

ALLNLI_DATASET_URL = "https://sbert.net/datasets/AllNLI.tsv.gz"
STS_BENCHMARK_DATASET_URL = "https://sbert.net/datasets/stsbenchmark.tsv.gz"


def download_dataset(url: str, download_path: str) -> None:
    """Download dataset from given url to download_path.

    Args:
        url (str): Dataset URL.
        download_path (str): Path to download.
    """
    if not os.path.exists(download_path):
        util.http_get(url, download_path)


@contextmanager
def open_dataset(dataset_path: str) -> t.Generator[csv.DictReader, None, None]:
    """Open dataset within a context manager.

    Args:
        dataset_path (str): Path to dataset file.

    Yields:
        Iterator[t.Generator[csv.DictReader, None, None]]: CSV reader.
    """
    file = gzip.open(dataset_path, "rt", encoding="utf8")
    reader = csv.DictReader(file, delimiter="\t", quoting=csv.QUOTE_NONE)
    yield reader
    file.close()


def read_as_dataframe(dataset_path: str) -> pd.DataFrame:
    """Read from given dataset path as DataFrame."""
    with open_dataset(dataset_path) as reader:
        columns = reader.fieldnames
        lines = [[row[field] for field in columns] for row in reader]
        return pd.DataFrame(lines, columns=columns)
