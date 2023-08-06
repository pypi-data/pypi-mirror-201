import setuptools

readme = open("README.md").read()

setuptools.setup(
    name="flake8_iw",
    license="MIT",
    version="0.0.17",
    description="A plugin to show lint errors for IW",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Smit",
    author_email="smitpatel@instawork.com",
    url="http://github.com/Instawork/flake8-iw",
    py_modules=["flake8_iw"],
    entry_points={
        "flake8.extension": [
            "IW = flake8_iw:Plugin",
        ],
    },
    install_requires=["flake8"],
    extras_require={"testing": ["pytest", "ipython", "astpretty", "build", "twine"]},
    tests_require=["pytest", "flake8", "astpretty"],
    classifiers=[
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Quality Assurance",
        "Operating System :: OS Independent",
    ],
)
