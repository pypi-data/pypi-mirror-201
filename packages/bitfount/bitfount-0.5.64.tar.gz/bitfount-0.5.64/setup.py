"""This file enables the github repo to be packaged into a wheel using `setuptools`."""
from collections import defaultdict
from os import PathLike
from pprint import pprint
import re
import runpy
from typing import DefaultDict, List, Tuple, Union

from setuptools import find_packages, setup

# The order of the operations is important because we want to check for "<="
# before "< etc.
_REQ_OPERATIONS = ("<=", ">=", "<", ">", "~=", "!=", "==")
_REQ_OP_REGEX = re.compile("|".join(re.escape(op) for op in _REQ_OPERATIONS))


def _load_reqs(file: Union[str, PathLike]) -> List[str]:
    """Load a requirements or constraints file.

    Will remove comments, -c and -r lines and return a list of solely the
    requirements and version constraints.
    """
    with open(file) as f:
        return [
            line.split("#")[0].strip()
            for line in f.read().splitlines()
            if not line.startswith(("#", "-c", "-r")) and line != ""
        ]


def _extract_package_info(line: str) -> Tuple[str, List[str]]:
    """Extract package and constraint info from requirements line.

    Will extract the package name and list of version constraints.

    For example:
        `ipython>=5,<10,!=8.5`
    becomes:
        `("ipython", [">=5", "<10", "!=8.5"])`

    """
    package_name: str
    constraints: List[str]

    # Split on commas to handle multiple version constraints
    first_constraint: str
    rest: List[str]
    first_constraint, *rest = line.split(",")

    # Extract package name (string before first operation)
    package_name, _ = re.split(_REQ_OP_REGEX, first_constraint)
    first_constraint = first_constraint.lstrip(package_name)

    constraints = [first_constraint] + rest
    return package_name.strip(), [c.strip() for c in constraints]


def _combine_reqs(*reqs: List[str]) -> List[str]:
    """Combines the package version constraints from several sources together.

    For a group of requirements (each a list of raw requirement lines), this function
    will produce a single line per package which contains all the constraints applied.

    Note, it does not do any condensing (e.g. <5,<8 becoming <5) or validity checking
    (e.g. <4,>5 being impossible). These are deferred to pip to handle.
    """
    # Find duplicated package names and their version constraints. These must be
    # combined into a single line.
    packages: DefaultDict[str, List[str]] = defaultdict(list)

    for r in reqs:
        for line in r:
            # Raise an error if the line doesn't contain any of the operations
            if not any(op in line for op in _REQ_OPERATIONS):
                raise ValueError(f"Unknown version constraint: {line}")

            # Skip platform-specific requirements
            if "platform_system" in line:
                # TODO: [BIT-2637] This should be removed once 'platform_system' is
                # removed from the requirements files.
                continue

            package_name, package_constraints = _extract_package_info(line)
            packages[package_name].extend(package_constraints)

    # Combine the lists of constraints into a single constrained string for each package
    return sorted(
        [
            f"{p_name}{','.join(p_constraints)}"
            for p_name, p_constraints in packages.items()
        ]
    )


# Import version information into current namespace
file_globals = runpy.run_path("bitfount/__version__.py")

# Get constraints
compat_constraints = _load_reqs("requirements/constraints-compatibility.txt")
direct_constraints = _load_reqs("requirements/constraints-direct.txt")
security_constraints = _load_reqs("requirements/constraints-security.txt")
dp_constraints = _load_reqs("requirements/differential_privacy/constraints-dp.txt")

# Get install requirements
install_reqs_in = _load_reqs("requirements/requirements.in")
dp_reqs_in = _load_reqs("requirements/differential_privacy/requirements-dp.in")

# Combine requirements with relevant constraints
install_reqs = _combine_reqs(
    install_reqs_in, compat_constraints, direct_constraints, security_constraints
)
dp_reqs = _combine_reqs(
    dp_reqs_in,
    dp_constraints,
    install_reqs_in,
    compat_constraints,
    direct_constraints,
    security_constraints,
)

# Remove any duplicate reqs in dp_reqs
dp_reqs = sorted(set(dp_reqs) - set(install_reqs))

# These will only be shown if pip installed with `-v` option, but helpful for debug
print("## INSTALL REQS ##")
pprint(install_reqs)

print("## DP REQS ##")
pprint(dp_reqs)

# Get other requirements where we can be more strict and just use the compiled
# .txt files
tutorial_reqs = _load_reqs("requirements/requirements-tutorial.txt")
tests_reqs = _load_reqs("requirements/requirements-test.txt")
# This is temporarily removed whilst we rely on a mypy fork
# dev_reqs = _load_reqs("requirements/requirements-dev.txt")

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    author=file_globals["__author__"],
    author_email=file_globals["__author_email__"],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description=file_globals["__description__"],
    entry_points={
        "console_scripts": [
            "bitfount = scripts.script_runner:main",
        ]
    },
    extras_require={
        "tests": tests_reqs,
        # This is temporarily removed whilst we rely on a mypy fork
        # "dev": dev_reqs,
        "tutorials": tutorial_reqs,
        "dp": dp_reqs,
    },
    install_requires=install_reqs,
    keywords=["federated learning", "privacy", "AI", "machine learning"],
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name=file_globals["__title__"],
    packages=find_packages(),
    package_data={"bitfount": ["py.typed"]},
    project_urls={
        "Documentation": "https://docs.bitfount.com/",
        "Homepage": "https://bitfount.com",
        "Source Code": "https://github.com/bitfount/bitfount/",
        "Hub": "https://hub.bitfount.com",
    },
    python_requires=">=3.8,<3.10,!=3.9.7",
    url=file_globals["__url__"],
    version=file_globals["__version__"],
)
