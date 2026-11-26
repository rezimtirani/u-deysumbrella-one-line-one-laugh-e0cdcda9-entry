"""Upload main.py and README.md for the One Line, One Laugh entry.

Uses the GitHub Contents API: PUT creates the file when it does not
exist yet and updates it (with the current blob sha) when it does.
Credentials come from the `custom.github` surrogate — no token is
stored in this file.
"""

import base64
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request  # noqa: E402

OWNER = "rezimtirani"
REPO = "u-deysumbrella-one-line-one-laugh-e0cdcda9-entry"
API_ROOT = "https://api.github.com"
FOLDER = Path("/home/hatch/workspace/makefun/u-deysumbrella-one-line-one-laugh-e0cdcda9-entry")
TO_UPLOAD = ["main.py", "README.md"]


def call_github(method, url, payload=None):
    body = None
    headers = {"Accept": "application/vnd.github+json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, method=method, headers=headers)
    add_surrogate_to_request(request, "custom.github", allowed_hosts=["api.github.com"])
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def current_blob_sha(name):
    try:
        info = call_github("GET", f"{API_ROOT}/repos/{OWNER}/{REPO}/contents/{name}")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    return info.get("sha")


def push_one(name):
    local_path = FOLDER / name
    encoded = base64.b64encode(local_path.read_bytes()).decode("ascii")
    payload = {"message": f"Add {name} — One Line, One Laugh entry", "content": encoded}
    sha = current_blob_sha(name)
    if sha:
        payload["sha"] = sha
    result = call_github("PUT", f"{API_ROOT}/repos/{OWNER}/{REPO}/contents/{name}", payload)
    print(f"{name}: {result['commit']['sha']}")
    return result["commit"]["sha"]


def main():
    for name in TO_UPLOAD:
        push_one(name)
    print(f"Done: {OWNER}/{REPO}")


if __name__ == "__main__":
    main()
