# NBDT_datasets
## A Comprehensive Library for Research Paper Recommendation and Dataset Management

# Installation

For installation, you can run the following code in the command line/terminal:
```python
git clone https://github.com/nbdt-journal/nbdt_lib.git
pip install ./nbdt_lib

```

# Load Datasets

Currently the library has 5 datasets ready to use:

`arxiv`: Has nearly 3.5k papers

`bioarxiv`: Has 29k papers from Bioarxiv

`plos_one`: Has 18k papers from PLOS_ONE

`medline_small`: Has 105k papers from the top 200 journals in the neuroscience field

`medline_large`: Has 200k papers from MEDLINE

To load your dataset use the following code:

```python
from nbdt.datasets import load_dataset
load_dataset(dataset_name = 'arxiv', destination_path = 'arxiv.csv', start_year = 2018, end_year = 2023)

```
- If `destination_path` is not specified, the dataset will be loaded as a pandas DataFrame to the specified variable.
- If `start_year` and `end_year` are not specified, the entire dataset is returned by default.
- Only papers with a publishing year from 2018 to 2023 are available in all specified datasets.

# Update Datasets

To update your dataset, use the following code:
```python
from nbdt.update import update_dataset
update_dataset(dataset_name, start_date, end_date, destination_path, update)

# Examples
update_dataset(dataset_name='plos_one', start_date='06-2023', end_date = '08-2023', destination_path='plos_one_new.csv', update=True)
update_dataset(dataset_name='bioarxiv', end_date = '08-2023', destination_path='bioarxiv_new.csv') # Here as 'update' and 'start_date' is not specified, their respective default values are applied, e.g False and 01-01-2023.


```
`dataset_name`:   Currently only `arxiv`, `bioarxiv`, and `plos_one` datasets are available for updation.


`start_date` and `end_date`:   The input of both the parameters should be in `MM-YYYY`, any other format will return an error. By default all the datasets are updated to a predefined start date:

- `arxiv`: 31-05-2023
            
- `bio_arxiv`: 01-01-2023
               
- `plos_one`: 31-05-2023

`destination_path`: Specify the destination path as required, for example: `'/content/arxiv.csv'` (Note: The file format should be in CSV)

`update`: By default, this parameter is `False`, but if `update=True` is passed then the source dataset along with the updated data of the mentioned period will be returned to the specified destination path.

Note: The parameters `dataset_name`, `destination_path`, and `end_date` should be atleast specified to return any data.
