import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SkeletonP",
    version="0.0.1",
    author="Arnaud tauveron",
    author_email="https://www.linkedin.com/in/arnaud-tauveron/",
    description="The skeleton for *Your* data science project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "competition_project\strategies_utils"},
    packages=setuptools.find_packages(where="competition_project\strategies_utils"),
    python_requires=">=3.6",
)
