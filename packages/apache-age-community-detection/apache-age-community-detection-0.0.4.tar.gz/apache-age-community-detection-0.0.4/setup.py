from setuptools import setup
from age_community_detection import VERSION

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name             = 'apache-age-community-detection',
    version          = VERSION.VERSION,
    description      = 'Detection of Community by maximizing modularity',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author           = 'Moontasir Mahmood',
    author_email     = 'moontasir042@gmail.com',
    url              = 'https://github.com/Munmud/Community-Detection-Modularity',
    license          = 'Apache2.0',
    install_requires = ['numpy'],
    packages         = ['age_community_detection'],
    keywords         = ['Community-Detection', 'Modularity', 'Reichardt and Bornholdt','Newman', 'partition network', 'k means cluster'],
    python_requires  = '>=3.9',
    classifiers      = [
        'Programming Language :: Python :: 3.9'
    ]
)