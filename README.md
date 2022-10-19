# OpenID Connect Federation over Github Pages

PoC of a OpenID Federation Trust Anchor that works entirely on Github Pages.


## Intro

This project propose a deploy mechanism on CDN for the Trust Anchor's Federation endpoints.

The Federation Trust Anchor is an An Entity that represents the trusted third party, needed to build a Federation,
as defined in [OpenID Connect Federation 1.0](https://openid.net/specs/openid-connect-federation-1_0.html).

## General  Architecture
<img src="https://user-images.githubusercontent.com/1297620/195827852-014e6a15-37d0-4260-8a5a-16e3c1e67cd4.png" alt="" data-canonical-src="https://user-images.githubusercontent.com/1297620/195827852-014e6a15-37d0-4260-8a5a-16e3c1e67cd4.png" width="320"/>

1. The git repository implements CI and CD to validate and publish the contents in one or more CDNs. The Federation private key is stored in a GitHub secret. This can only be deleted or updated.
2. A pool of HTTPd Frontends resolved to a single hostname make reverse proxy and rewrite rules for the Federation endpoints that require URL parameters, like the Fetch endpoint for the retrieval of the entity statements. 


> Implementation note: The HTTP Frontends can be hosted on different organizations and these should only serve the Fetch endpoint. The TA's entity configuration should be always taken directly from the CDN, without any intermediary. In this way the intermediaris that manages the frontend can't change the TA's entity configuration, and they can only serve the entity statements issued and signed by the TA's.


## General workflow

Every time a commit occur in the main branch,
a GitHub action uses the scripts configured in `bin/` 
to update the storage of the TA and deploy its content on GitHub Page.

The branch for the github page deployment is `gh-trust-anchor`.

## Onboarding

The OnBoarding should be done with a traditional review process, made by a team, 
on the PRs that want to update the master branch.
The master branch should be protected with a quorum of reviewers.

The git commits on [federation/descendants](federation/descendants) must create a
JSON file, containing a JSON Objects with at least three attributes as given in the example below:

````
{
    "entity_id": "https://hostna.me",
    "jwks": { "keys": [.. leaf's entity configuration jwks ...]},
    "leaf_entity_types": ["openid_provider"]

}
````
The name of the file must be the url encoding of the `entity_id` value.

The validation CI on the pull requests should:

1. fetch the leaf's entity configuration from the URL given by `entity_id`.
2. validate the signature of the leaf's entity configuration using one of the keys given in `jwks`.
3. validate the leaf's entity configuration, following the given json-schema and the entity types given in the commit.

The CI would let the reviewers to approve the pull request and merge it on the main branch.
A CI action should be triggered to create and deploy on CDN the entity statements related to the onboarded Leaf.

## TA's endpoints

#### Entity Configuration

The file [federation/.well-known/openid-federation.json](federation/.well-known)
is the unsigned Entity Configuration of the Trust Anchor. Every time a commit occur in the main branch,
a GitHub action uses `bin/create_jwt.py` to parse `openid-federation.json`,
update the claims `iat`, `exp` and `jwks` and then create a signed JWT.

The private key used for signature operations is stored in the github secrets.

The Entity Configuration once deployed will be available at 
[this url](https://peppelinux.github.io/oidc-federation-over-gh-pages/.well-known/openid-federation).


#### TA's Listing

> TODO

The file [federation/list.json](federation/list.json) contains JSON array with all the 
URLs of the participants. Every time an onboarding action is merged in the main branch, like create, update or delete, 
this file is edited by the scripts configured in the `bin/` directory.

#### Entity Statements

> TODO: see onboarding.


## Open Points

To be converted in issues?

- The URL parameters with the char`?` doesn't work in gh pages, so the fetch of entity statements using the HTTP GET method doesn't work: 
        https://peppelinux.github.io/oidc-federation-over-gh-pages/entity-statements/fetch?sub%3Dhttps%253A%252F%252Ftrust.me
        
- this instead works, but it's not compliant: 
        https://peppelinux.github.io/oidc-federation-over-gh-pages/entity-statements/fetch%3Fsub%3Dhttps%253A%252F%252Ftrust.me

- solution: put an nginx frontend that does reverse proxy
  - requirements: keep entity configuration updated with the FQDN of the frontend


## Local setup

If you want to run the action script by your own:
````
pip install -r requirements.txt
````


