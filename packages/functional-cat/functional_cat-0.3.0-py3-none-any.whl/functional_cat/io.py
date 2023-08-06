import base64
import hashlib
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import requests
from tqdm import tqdm

MODELS_CACHE_PATH = Path.home() / ".functional-cat"
os.makedirs(MODELS_CACHE_PATH, exist_ok=True)


def download_file(url: str, out_path: str) -> None:
    print(f"Downloading to {out_path}")
    with requests.get(url, stream=True) as r:
        total_length = r.headers.get("content-length")
        r.raise_for_status()
        chunk_size = 8192

        with open(out_path, "wb") as f:
            for chunk in tqdm(
                r.iter_content(chunk_size=chunk_size),
                total=math.ceil(int(total_length) / chunk_size)
                if total_length is not None
                else None,
                bar_format="{bar}{l_bar} [{elapsed}<{remaining}]",
            ):
                f.write(chunk)


def calculate_md5(fpath: str, chunk_size: int = 1024 * 1024) -> str:
    # taken from
    # https://github.com/pytorch/vision/blob/f82a4675a4fb9645246c777932c11b69d2bf3dc7/torchvision/datasets/utils.py
    if sys.version_info >= (3, 9):
        md5 = hashlib.md5(usedforsecurity=False)
    else:
        md5 = hashlib.md5()
    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            md5.update(chunk)
    return md5.hexdigest()


@dataclass
class FileFromURL:
    url: str
    md5: str

    def download(self, out_path: str) -> None:
        download_file(url=self.url, out_path=out_path)

    @property
    def file_name(self) -> str:
        return self.url.split("/")[-1]


@dataclass
class FileFromGithubLFS:
    organisation: str
    repo: str
    path: str
    md5: str

    def download(self, out_path: str) -> None:
        """c.f. https://gist.github.com/fkraeutli/66fa741d9a8c2a6a238a01d17ed0edc5"""

        resp = requests.get(
            f"https://api.github.com/repos/{self.organisation}/{self.repo}/contents/{self.path}"
        )
        content = resp.json()["content"]
        content = base64.b64decode(content).decode()
        lines = content.split("\n")

        if not lines[1].startswith("oid") or not lines[2].startswith("size"):
            raise RuntimeError("Error downloading file.")

        sha = lines[1][11:]
        size = int(lines[2][5:])

        payload = {
            "operation": "download",
            "transfer": ["basic"],
            "objects": [{"oid": sha, "size": size}],
        }

        resp = requests.post(
            f"https://github.com/{self.organisation}/{self.repo}.git/info/lfs/objects/batch",
            json=payload,
            headers={"Accept": "application/vnd.git-lfs+json"},
        )

        url = resp.json()["objects"][0]["actions"]["download"]["href"]

        download_file(url, out_path)

    @property
    def file_name(self) -> str:
        return self.path.split("/")[-1]


def download_to_cache(
    file: Union[FileFromURL, FileFromGithubLFS],
    verify_hash: bool = True,
    file_name: str = None,
) -> str:
    file_name = file_name or file.file_name
    out_path = str(MODELS_CACHE_PATH / file_name)
    if os.path.exists(out_path):
        print("file exists")
    else:
        file.download(out_path)

    if verify_hash:
        print("verifying hash")
        md5 = calculate_md5(out_path)
        if md5 != file.md5:
            raise RuntimeError(
                f"md5 mismatch: hash of {out_path} is {md5} but expected {file.md5}."
            )
        print("hash matches!")
    return out_path
