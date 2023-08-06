# Package squatting

To squat an internal package on pipy, first 

```bash
PIP_IGNORE_INSTALL_PACKAGE_ERROR=1 python setup.py sdist
PIP_IGNORE_INSTALL_PACKAGE_ERROR=1 python setup.py bdist_wheel
twine check dist/*
twine upload dist/dabacus-0.0.0.tar.gz
```
