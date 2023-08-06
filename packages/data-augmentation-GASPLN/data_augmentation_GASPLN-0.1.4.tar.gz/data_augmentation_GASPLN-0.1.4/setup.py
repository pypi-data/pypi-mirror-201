from setuptools import setup, find_packages

setup(
    name='data_augmentation_GASPLN',
    version='0.1.4',
    author='Artur Melchiori Cerri',
    author_email='arturmelchiori@gmail.com',
    description='Data augmentation for Portuguese language',
    install_requires=[
        "nltk",
        "pandas",
        "pyarrow",
        "numpy",
        "translators",
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={'' : ['data/synonyms_pt_BR.parquet']},
)