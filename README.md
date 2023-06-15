# nbdt_lib


# Installation

For installation you can run the following code in the command line/terminal:
```python
git clone https://github.com/nbdt-journal/nbdt_lib.git
pip install ./nbdt_lib

```

# Load Datasets

Currently the library has 4 datasets ready to use:

`arxiv`: Has nearly 3.5k papers

`bioarxiv`: Has 29k papers from Bioarxiv

`plos_one`: Has 18k papers from PLOS_ONE

`medline`: Has 105k papers from the top 200 journals in the neuroscience field

To load your dataset use the following code:

```python

data = load_dataset(dataset_name = 'arxiv', destination_path = 'arxiv.csv', start_year = 2018, end_year = 2023)

```
- If `destination_path` is not specified, then the dataset will be loaded as a pandas DataFrame to the specified variable.
- If `start_year` and `end_year` is not specified, then by default the entire dataset is returned.
- In all specified datasets, only papers with a publishing year from 2018 to 2023 are available.
