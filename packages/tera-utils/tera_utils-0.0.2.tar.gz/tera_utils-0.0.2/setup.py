from setuptools import setup, find_packages


VERSION = "0.0.2"
DESCRIPTION = "Utils for fun"
LONG_DESCRIPTION = "A package made for fun and education"

# Setting up
setup(
    name="tera_utils",
    version=VERSION,
    author="TeraGeek",
    # author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    # install_requires=[],
    keywords=["python"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
