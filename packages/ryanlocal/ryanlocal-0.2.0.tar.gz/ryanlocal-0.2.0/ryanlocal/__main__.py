from pathlib import Path

import requests

URL = "https://api.sandbox1.unit21.com/v1/imports/pre-signed-url/create"
API_KEY = "b361917de20a0c9b18f15f2134dc59ccf45297862f5e80561ae0abdf41"
STREAM_HAME = "ryanlocal"


def get_and_post_presigned_url(file_path):
    # get presigned url
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "u21-key": API_KEY,
    }

    body = {"stream_name": "ryanlocal", "file_name": file_path.name}
    response = requests.post(URL, headers=headers, json=body)
    response.raise_for_status()
    resp_json = response.json()
    print(resp_json)

    # upload file to the presigned url
    upload_response = requests.post(
        # the url from the previous call
        resp_json.get("url"),
        # dictionary from previous call used as form params
        data=resp_json.get("form_fields"),
        # file descriptor dictionary of the actual file
        files={"file": file_path.open("rb")},
    )
    upload_response.raise_for_status()
    print(f"success for {file_path}")


get_and_post_presigned_url(Path("../entity_1.csv"))
get_and_post_presigned_url(Path("../event_1.csv"))
get_and_post_presigned_url(Path("../instrument_1.csv"))
