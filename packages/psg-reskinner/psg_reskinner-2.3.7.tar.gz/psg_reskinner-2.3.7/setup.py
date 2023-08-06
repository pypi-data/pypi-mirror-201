from setuptools import setup
from psg_reskinner import __version__ as VERSION

def desc():
    with open('DESCRIPTION.md', 'r') as desc_file:
        desc = desc_file.read()
    return desc

REQUIRED_PACKAGES = ['PySimpleGUI', 'colour']

setup(
    name="psg_reskinner",
    version=str(VERSION),
    author="Divine U. Afam-Ifediogor",
    author_email="divineafam@gmail.com",
    license="MIT License",
    description="Instantaneous theme changing for PySimpleGUI windows.",
    long_description=desc(),
    long_description_content_type="text/markdown",
    url="https://github.com/definite-d/psg_reskinner/",
    packages = ['psg_reskinner'],
    project_urls={
        "Bug Tracker": "https://github.com/definite-d/psg_reskinner/issues/",
    },
    install_requires=REQUIRED_PACKAGES,
    python_requires=">=3.6",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ]
)