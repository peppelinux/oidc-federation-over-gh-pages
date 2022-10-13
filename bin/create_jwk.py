from cryptojwt.jwk.rsa import new_rsa_key


DEFAULT_HASH_FUNC = "SHA-256"


def create_jwk(hash_func=None):
    key = new_rsa_key()
    thumbprint = key.thumbprint(hash_function=hash_func or DEFAULT_HASH_FUNC)
    jwk = key.to_dict()
    jwk["kid"] = thumbprint.decode()
    return jwk


if __name__ == '__main__':
    
    import json
    
    print(json.dumps(create_jwk()))
