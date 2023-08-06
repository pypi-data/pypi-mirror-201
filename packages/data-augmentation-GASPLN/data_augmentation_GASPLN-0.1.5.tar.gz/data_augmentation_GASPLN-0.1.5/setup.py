from setuptools import setup, find_packages

setup(
    name='data_augmentation_GASPLN',
    version='0.1.5',
    author='Artur Melchiori Cerri',
    author_email='arturmelchiori@gmail.com',
    description='Data augmentation for Portuguese language',
    install_requires=[
        "spacy",
        "nltk",
        "pandas",
        "pyarrow",
        "numpy",
        "translators",
        "setuptools",
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={'' : ['data/synonyms_pt_BR.parquet']},
)