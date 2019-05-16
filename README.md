# Greasepaint

A python library to manipulate the faces. Think snapchat but weirder.



## Examples

![](docs/images/eyes0.jpg)
![](docs/images/eyes1.jpg)
![](docs/images/eyes2.jpg)
![](docs/images/eyes3.jpg)
![](docs/images/eyes4.jpg)
![](docs/images/eyes5.jpg)

![org](docs/images/tessa1_src.jpg)  ![ThirdEye](docs/images/tessa1_third_eye.png) 

### Dev Notes:

+ Update the version number in `greasepaint/_version.py`
+ Test release, check coverage, and lint
+ Push the release to [pypi live](https://pypi.org/project/pixelhouse/)

    fab lint
    fab test
    rm dist/ -rvf && python setup.py sdist
    twine upload -r test dist/*
    twine upload dist/*