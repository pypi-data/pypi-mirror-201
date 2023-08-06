import json
import logging
import os
import subprocess
from urllib.parse import urlparse

import keyring


class PlaintextKeyring(keyring.backend.KeyringBackend):
    priority = 9

    def set_password(self, servicename, username, password):
        raise NotImplementedError()

    def delete_password(self, servicename, username):
        raise NotImplementedError()

    def get_password(self, servicename, username):
        params = {
            "region": "KEYRING_AWS_CODEARTIFACT_REGION",
            "domain": "KEYRING_AWS_CODEARTIFACT_DOMAIN",
            "domain_owner": "KEYRING_AWS_CODEARTIFACT_DOMAIN_OWNER",
        }

        for k, v in params.items():
            val = os.environ.get(v)
            if val is None:
                logging.warning(f"{v} not set")
                return
            params[k] = val

        suffix = f"{params['domain']}-{params['domain_owner']}.d.codeartifact.{params['region']}.amazonaws.com"

        if not valid_service(servicename, suffix):
            return
        try:
            return get_token(params["domain"], params["domain_owner"], params["region"])
        except Exception as e:
            logging.warning(f"Failed to retrieve token: {e}")


def valid_service(servicename, suffix):
    if servicename.endswith(suffix):
        return True
    url = urlparse(servicename)
    if url.hostname is None:
        return False
    return url.hostname.endswith(suffix)


def get_token(domain, domain_owner, region):
    try:
        logging.warning("Trying to retrieve credentials from aws...")
        command = subprocess.run(
            [
                "aws",
                "codeartifact",
                "get-authorization-token",
                "--domain",
                domain,
                "--domain-owner",
                domain_owner,
                "--region",
                region,
            ],
            check=True,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
    except Exception as e:
        raise Exception(f"aws command exited with status: {e}")
    result = json.loads(command.stdout)
    return result.get("authorizationToken")
