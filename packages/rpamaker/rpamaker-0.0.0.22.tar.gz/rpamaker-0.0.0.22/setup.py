from setuptools import setup, find_packages

VERSION = '0.0.0.22'
DESCRIPTION = 'RPAMAKER - RPA Maker'
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="rpamaker",
    version=VERSION,
    author="RPAMAKER",
    author_email="<nicolas@rpamaker.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'python-decouple',
        'fastapi',
        'uvicorn',
        'requests',
        'python-dotenv',
    ],
    keywords=['python', 'rpa', 'robotframework', 'rpamaker'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
