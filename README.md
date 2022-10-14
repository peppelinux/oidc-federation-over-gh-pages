# OpenID Connect Federation over Github Pages

PoC of a OpenID Federation Trust Anchor that works entirely on github pages.


## Intro

This project propose a deploy mechanism for the Federation endpoints of Trust Anchor.

The Federation Trust Anchor is an An Entity that represents a trusted third party, needed to build a Federation,
as defined in [OpenID Connect Federation 1.0](https://openid.net/specs/openid-connect-federation-1_0.html).


## How does it work

Every time a commit occur in the main branch,
a GitHub action uses the scripts configured in `bin/` 
to update the storage of the TA and deploy it on GitHub page.

The branch for the github page deployment is `gh-trust-anchor`.


## TA's endpoints

#### Entity Configuration

The file [federation/.well-known/openid-federation.json](federation/.well-known)
is the unsigned Entity Configuration of the Trust Anchor. Every time a commit occur in the main branch,
a GitHub action uses `bin/create_jwt.py` to parse `openid-federation.json`,
update the claims `iat`, `exp` and `jwks` and then create a signed JWT.

the private key used for signature operations is stored in the github secrets.

the Entity Configuration once deployed will be available at 
[this url](https://peppelinux.github.io/oidc-federation-over-gh-pages/.well-known/openid-federation).


## TA's Listing

> TODO

The file [federation/list.json](federation/list.json) contains JSON array with all the 
URLs of the participants. Every time this file is edited with a git commit,
the scripts in the `bin/` directory create, update or remove, 
the Entity Statements of the participants.

For doing that the action scripts fetches the Entity Configuration of each new/modified participant,
validate it, and then stores the signed entity statements related to this.

The commit on [federation/list.json](federation/list.json) should be coupled with the public jwk that
would match to the one published in the participants Entity Configuration.

The result will contain only the verified Entities for which the 
Entity Statement have been produced.


## Entity Statements

> TODO


### Open Points

To be converted in issues?

- The URL parameters with the char`?` doesn't work in gh pages, so the fetch of entity statements using the HTTP GET method doesn't work: 
        https://peppelinux.github.io/oidc-federation-over-gh-pages/entity-statements/fetch?sub%3Dhttps%253A%252F%252Ftrust.me
        
- this instead works, but it's not compliant: 
        https://peppelinux.github.io/oidc-federation-over-gh-pages/entity-statements/fetch%3Fsub%3Dhttps%253A%252F%252Ftrust.me

- solution: put an nginx frontend that does the rewrite rules
  - requirements: keep entity configuration updated with the FQDN of the frontend

- the actions should be scheduled, see [schedule](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule).


## Local setup

If you want to run the action script by your own:
````
pip install -r requirements.txt
````


