# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import urllib.request
from pathlib import Path

# We're downloading this dataset from the MHPP repo.
URL = "https://raw.githubusercontent.com/SparksofAGI/MHPP/main/data/MHPP.jsonl"

# Data Format
#
# Required:
#   - question (problem statement)
#   - prompt (model input)


if __name__ == "__main__":
    data_folder = Path(__file__).absolute().parent
    original_file = str(data_folder / f"original_test.jsonl")
    data_folder.mkdir(exist_ok=True)
    output_file = str(data_folder / f"test.jsonl")

    if not os.path.exists(original_file):
        urllib.request.urlretrieve(URL, original_file)

    with open(original_file, "rt", encoding="utf-8") as fin:
        data = [json.loads(line) for line in fin]

    with open(output_file, "wt", encoding="utf-8") as fout:
        for problem in data:
            # somehow models like tabs more than spaces
            problem['question'] = problem['question'].replace('    ', '\t')
            # dropping inputs which are large and are not needed, since they are re-downloaded during eval anyway
            fout.write(json.dumps(problem) + "\n")
