import json
import logging
import os

from cryptojwt.jwk.jwk import key_from_jwk_dict
from cryptojwt.jws.jws import JWS


logger = logging.getLogger(__name__)


def create_jws(payload: dict, jwk_dict: dict, alg: str = "RS256", **kwargs) -> str:

    _key = key_from_jwk_dict(jwk_dict)
    _signer = JWS(payload, alg=alg, **kwargs)

    jwt = _signer.sign_compact([_key])
    return jwt


if __name__ == '__main__':
    
    from datetime import datetime, timedelta
    
    with open(".well-known/openid-federation.json") as f:
        ec_dict = json.loads(f.read())
    
    _private_key = json.loads(
        os.getenv("PRIVATE_JWK")
    )
    
    ec_dict["iat"] = int(datetime.now().timestamp())
    ec_dict["exp"] = int((datetime.now() + timedelta(hours=24)).timestamp())
    
    print(
        create_jws(ec_dict, _private_key)
    )
