import setuptools
import os

__local__ = os.path.abspath(os.path.dirname(__file__))

f_version = os.path.join(__local__, "greasepaint", "_version.py")
exec(open(f_version).read())

# Get the long description from the relevant file
long_description = """greasepaint
=================================
A python library to manipulate the faces. Think snapchat but weirder.
"""

setuptools.setup(
    name="greasepaint",
    packages=setuptools.find_packages(),
    # Include package data...
    include_package_data=True,
    description="A python library to manipulate the faces. Think snapchat but weirder.",
    long_description=long_description,
    version=__version__,
    # The project's main homepage.
    url="https://github.com/thoppe/greasepaint",

    # Author details
    author="Travis Hoppe",
    author_email="travis.hoppe+greasepaint@gmail.com",

    # Choose your license
    license="CC-SA",
    install_requires=[
        "face_recognition",
        "pixelhouse>=0.5.3",
        "opencv-python",
        "numpy",
    ],
    
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5  -Production/Stable
        "Development Status :: 3 - Alpha",

        # Indicate who your project is intended for
        "Intended Audience :: Developers",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.6",
    ],
    
    # What does your project relate to?
    keywords="art",
)
