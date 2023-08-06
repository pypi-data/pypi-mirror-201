# Data Augmentation Library for Portuguese (Brazil)

Research project developed in conjunction with the [GASPLN](https://wp.ufpel.edu.br/gaspln/) research group of the Federal University of Pelotas (UFPel) to create a Python library for Data Augmentation in Portuguese (Brazil).

## Installation

The package is available on PyPI and can be installed with pip:

```bash
pip install data_augmentation_GASPLN
```

## How to use

***THIS PROJECT IS STILL UNDER CONSTRUCTION AND NOT READY FOR USE***

With that said, there are some functions in test that can be used, as shown below.

You can import the library as follows:

```python
import data_augmentation_GASPLN.functions as da
```

### Synonym Replacement

```python
da.synonyms_replacement("Data augmentation é uma técnica de aprendizado de máquina que aumenta o número de dados de treinamento, alterando os dados existentes de alguma forma a fim de criar novos dados.", 0.5)
```

Where the first parameter is the text to be augmented, and the second parameter is the amount of words to be replaced by synonyms (0.5 = 50% of the words in the text), if they are found in the synonym dictionary.

### Back Translation

```python
da.back_translation("Data augmentation é uma técnica de aprendizado de máquina que aumenta o número de dados de treinamento, alterando os dados existentes de alguma forma a fim de criar novos dados.", 2)
```

Where the first parameter is the text to be augmented, and the second parameter is the number of translations to be made. As for now, there are two options available for the second parameter, 1 or 2, where:

- 1 = Portuguese > English > Portuguese
- 2 = Portuguese > Spanish > English > Portuguese
