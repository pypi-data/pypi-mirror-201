from setuptools import setup, find_packages

VERSION = "1.0.2"
DESCRIPTION = "Utilities with FastAPI"

# Setting up
setup(
    name="py-ke-utils-fastapi",
    version=VERSION,
    author="KE",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["flask", "redis", "deepdiff"],
    keywords=["python", "fastapi", "JWT", "decorator", "token"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
)
