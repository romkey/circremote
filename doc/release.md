# Releases

## Version number

Bump the version number appropriately in `circremote/version.py` where new version is `X.Y.Z`

## git tags

1. commit all needed files including `circremote/version.py`
2. `git tag -a vX.Y.Z -m "Release version X.Y.Z - short note"`
3. `git push origin vX.Y.Z`

## PyPI

This allows `pip install circremote` to work

API keys must be stored in ~/.pypirc

1. `rm dist/*`
2. `python -m build`
3. `twine upload dist/*`

## PyPI test

1. `rm dist/*`
2. `python -m build`
3. `twine upload --repository testpypi dist/*`

To test: `python3 -m pip install --index-url https://test.pypi.org/simple/ circremote`
