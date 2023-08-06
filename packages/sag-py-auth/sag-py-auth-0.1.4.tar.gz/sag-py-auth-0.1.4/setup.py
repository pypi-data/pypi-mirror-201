import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

with open("requirements.txt", "r") as fin:
    REQS = fin.read().splitlines()

setuptools.setup(
    name="sag-py-auth",
    version="0.1.4",
    description="Keycloak authentication for python projects",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/SamhammerAG/sag_py_auth",
    author="Samhammer AG",
    author_email="support@samhammer.de",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development",
    ],
    keywords="auth, fastapi, keycloak",
    packages=setuptools.find_packages(exclude=["tests"]),
    package_data={"sag_py_auth": ["py.typed"]},
    python_requires=">=3.8",
    install_requires=REQS,
    extras_require={"dev": ["pytest"]},
    project_urls={
        "Documentation": "https://github.com/SamhammerAG/sag_py_auth",
        "Bug Reports": "https://github.com/SamhammerAG/sag_py_auth/issues",
        "Source": "https://github.com/SamhammerAG/sag_py_auth",
    },
)
