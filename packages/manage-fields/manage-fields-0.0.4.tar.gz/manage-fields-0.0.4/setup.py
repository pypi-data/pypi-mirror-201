from setuptools import setup, find_packages

VERSION = "0.0.4"
DESCRIPTION = "Manage fields by request params"


def read(f):
    return open(f, "r", encoding="utf-8").read()


# Setting up
setup(
    name="manage-fields",
    version=VERSION,
    author="Maxmudov Asliddin",
    author_email="<asliddin750750@gmail.com>",
    description=DESCRIPTION,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(include=[
        "manage_fields"
    ]),
    include_package_data=True,
    install_requires=["Django", "djangorestframework"],
    keywords=["python", "field", "serializer", "manage fields"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
