# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import os
from unittest.mock import MagicMock, patch

import pytest
import wget

os.environ["IRIS_DEBUG"] = "True"  # set debug variable for iris

from iris.sdk import download, get, login, logout, post, pull
from iris.sdk.exception import (
    BadRequestError,
    DownloadLinkExpiredError,
    EndpointNotFoundError,
    InvalidCommandError,
    InvalidLoginError,
)

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                     Test Module                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


# --------------------------------------       iris post    -------------------------------------- #


# --------------------------------------       iris get     -------------------------------------- #


@patch("requests.get")
def test_iris_get_with_401_response(mock_get):
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 401
    mock_get.return_value = mock_response

    with pytest.raises(InvalidLoginError):
        get()


@patch("requests.get")
def test_iris_get_with_404_response(mock_get):
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(EndpointNotFoundError):
        get()


# --------------------------------------    iris download   -------------------------------------- #


def test_iris_download_with_invalid_experiment_cmd():
    with pytest.raises(InvalidCommandError) as exc:
        download("invalid")


@patch("requests.get")
def test_download_with_bad_request_error(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "failure"}
    mock_get.return_value = mock_response

    with pytest.raises(BadRequestError):
        download("experiment_id:job_tag")


# --------------------------------------      iris pull     -------------------------------------- #


def test_iris_pull_with_invalid_experiment_cmd():
    with pytest.raises(InvalidCommandError):
        pull("invalid")
