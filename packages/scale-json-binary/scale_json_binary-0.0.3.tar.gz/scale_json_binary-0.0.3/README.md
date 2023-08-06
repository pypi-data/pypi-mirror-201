# json-binary

Implementation of codecs used for sensor fusion scenes


## Setup

Install [poetry](https://python-poetry.org/docs/#installation)

Make sure you have a python version >= 3.8 or you may run into version issues

[TODO] add a better documentation

### Codeartifact setup

```
source "${SCALEAPI_REPO}/bin/codeartifact.bash" # <-- add this to your ~/.bashrc
maybe_refresh_codeartifact_token_python
```


## Publishing package

### Configure poetry to publish to internal repo

Run
```
poetry config repositories.scale-pypi https://scale-307185671274.d.codeartifact.us-west-2.amazonaws.com/pypi/scale-pypi/
bash utils/refresh_auth.sh
poetry publish --build --repository scale-pypi
```
