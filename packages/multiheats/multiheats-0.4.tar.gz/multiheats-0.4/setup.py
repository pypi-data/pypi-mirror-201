from setuptools import setup, find_packages

setup(
    name="multiheats",
    version="0.4",
    packages=find_packages("src"),
    package_dir={"": "src"},
    readme="README.md",
    description="MultIHeaTS is a Multi-layered Implicit Heat Transfer Solver.",
    install_requires=[
        "wheel",
        "ipython",
        "pytest",
        "numpy",
        "matplotlib",
        "scipy",
        "pandas",
        "tqdm",
        "xlrd",
    ],
)
