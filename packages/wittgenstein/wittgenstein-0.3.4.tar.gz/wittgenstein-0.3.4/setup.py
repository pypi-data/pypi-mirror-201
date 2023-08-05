import setuptools

setuptools.setup(
    name="wittgenstein",
    version="0.3.4",
    # license="MIT",
    description="Ruleset covering algorithms for explainable machine learning",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ilan Moscovitz",
    author_email="ilan.moscovitz@gmail.com",
    url="https://github.com/imoscovitz/wittgenstein",
    keywords=[
        "Classification",
        "Decision Rule",
        "Machine Learning",
        "Explainable Machine Learning",
        "Data Science",
        "Machine Learning Interpretability",
        "Transparent Machine Learning",
        "ML",
        "Ruleset"
    ],
    packages=setuptools.find_packages(),
    install_requires=["pandas", "numpy"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    package_data={"": ["data/*.csv"]},
)
