# Spark

[![Build](https://img.shields.io/travis/masmu/spark.svg?style=flat-square)](https://travis-ci.org/masmu/spark)
[![Coverage](https://img.shields.io/coveralls/masmu/spark.svg?style=flat-square)](https://coveralls.io/r/masmu/spark)

Spark is a Python3 project pattern. It can be considered as a starting point for new Python3 applications using state-of-the-art technologies.

## Features

  - Runnable as python *virtual env* and *system wide*
  - Unit-Tests (using _tox_, _unittest_)
  - Code coverage
  - CI-Support (Travis CI)
  - Debian packaging
  - Documentation generation
  - Git version awareness

# Setup

## Requirements

The only requirement for building the application is

- *python3.5*
- *curl*

Everything else is being downloaded automatic to a Python virtual environment.

## Clone the sources
```bash
$ git clone https://github.com/masmu/spark.git
$ cd spark/
```
## Build the application
```bash
$ make
```

# Usage

## Run the application
```bash
$ bin/spark
```
## Run unit tests
```bash
$ make test
```
The test suite includes unit tests, linting, code coverage and manifest checking.
You can find a HTML coverage report in the  `htmlcov/` folder.

## Generate documentation
```bash
$ make docs
```
You can find the generated documentation in the `docs/` folder of the source
directory.

## Build Debian packages

You need to setup the debian packaging environment before:
On Ubuntu you can do this via:

```bash
$ sudo apt-get install pbuilder debootstrap devscripts lintian
$ sudo pbuilder create --debootstrapopts --variant=buildd
```

After that you should enable [Universe support](https://wiki.ubuntu.com/PbuilderHowto#Universe_support) for *pbuilder*.
For that add the following to your ` ~/.pbuilderrc`
```
COMPONENTS="main restricted universe multiverse"

if [ "$DIST" == "squeeze" ]; then
    echo "Using a Debian pbuilder environment because DIST is $DIST"
    COMPONENTS="main contrib non-free"
fi
```

After adding those new sources run the following command to update *pbuilder*:
```bash
$ sudo pbuilder update --override-config
```

Now you should be able to create Debian packages via:
```bash
$ make deb
```
