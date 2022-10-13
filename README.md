# OpenID Connect Federation over Github Pages

PoC of a OpenID Federation Trust Anchor that works entirely on github pages


# Local setup

````
pip install -r requirements.txt
````

# open points

- ? doesn't work in gh pages, entity statements GET doesnt works: 
        https://peppelinux.github.io/oidc-federation-over-gh-pages/entity-statements/fetch?sub%3Dhttps%253A%252F%252Ftrust.me
- this works: 
        https://peppelinux.github.io/oidc-federation-over-gh-pages/entity-statements/fetch%3Fsub%3Dhttps%253A%252F%252Ftrust.me
