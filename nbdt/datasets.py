import pandas as pd
import urllib.request
import io

def load_dataset(dataset_name, start_year=None, end_year=None, destination_path=None):
    """
    Loads a dataset by name and optionally filters it based on start_year and end_year.
    Saves the filtered dataset to a destination_path if provided.

    Args:
        dataset_name (str): The name of the dataset to load.
        start_year (int, optional): The start year for filtering the dataset. Defaults to None.
        end_year (int, optional): The end year for filtering the dataset. Defaults to None.
        destination_path (str, optional): The file path to save the filtered dataset. Defaults to None.

    Returns:
        pd.DataFrame or None: The loaded dataset as a DataFrame if destination_path is not provided, otherwise None.
    """
    # Mapping of dataset names to dataset URLs
    dataset_mapping = {
        'arxiv': 'https://huggingface.co/datasets/PenguinMan/ARXIV/resolve/main/arxiv2.csv',
        'bioarxiv': 'https://huggingface.co/datasets/PenguinMan/ARXIV/resolve/main/bioarxiv%20(1).csv',
        'plos_one': 'https://huggingface.co/datasets/PenguinMan/ARXIV/resolve/main/plos_one_new.csv',
        'medline_small': 'https://huggingface.co/datasets/PenguinMan/ARXIV/resolve/main/MEDLINE_Journal_Recommend2.csv',
        'medline_large': 'https://huggingface.co/datasets/PenguinMan/ARXIV/resolve/main/MEDLINE_COMPLETE.csv' 
        # Add more dataset mappings as needed
    }

    if dataset_name in dataset_mapping:
        dataset_url = dataset_mapping[dataset_name]

        with urllib.request.urlopen(dataset_url) as response:
            dataset_content = response.read().decode('utf-8')
        
        dataset_dataframe = pd.read_csv(io.StringIO(dataset_content))
        
        if start_year is not None and end_year is not None:
            dataset_dataframe = filter_dataset(dataset_name, start_year, end_year, dataset_dataframe)

        if destination_path is not None:
            dataset_dataframe.to_csv(destination_path, index=False)
            print(f'Dataset downloaded successfully and saved to "{destination_path}".')
        else:
            print('Dataset downloaded successfully.')
            return dataset_dataframe
    else:
        print(f'Dataset "{dataset_name}" is not available.')


def filter_dataset(dataset_name, start_year, end_year, dataset_dataframe):
    """
    Filters the dataset based on start_year and end_year.

    Args:
        dataset_name (str): The name of the dataset being filtered.
        start_year (int): The start year for filtering.
        end_year (int): The end year for filtering.
        dataset_dataframe (pd.DataFrame): The dataset to filter.

    Returns:
        pd.DataFrame: The filtered dataset.
    """
    if start_year in range(2018, 2024) and end_year in range(2018, 2024):
        if dataset_name == 'arxiv':
            dataset_dataframe = dataset_dataframe[
                (pd.to_datetime(dataset_dataframe['update_date']).dt.year >= start_year) &
                (pd.to_datetime(dataset_dataframe['update_date']).dt.year <= end_year)
            ]
        elif dataset_name == 'bioarxiv':
            dataset_dataframe = dataset_dataframe[
                (pd.to_datetime(dataset_dataframe['date']).dt.year >= start_year) &
                (pd.to_datetime(dataset_dataframe['date']).dt.year <= end_year)
            ]
        elif dataset_name == 'plos_one':
            dataset_dataframe = dataset_dataframe[
                ((pd.to_datetime(dataset_dataframe['Publication Date'], format="%Y-%m-%dT%H:%M:%SZ")).dt.year >= start_year) &
                ((pd.to_datetime(dataset_dataframe['Publication Date'], format="%Y-%m-%dT%H:%M:%SZ")).dt.year <= end_year)
            ]
        elif dataset_name in ['medline_large', 'medline_small']:
            dataset_dataframe['Year'] = dataset_dataframe['P_Date'].str.split(' ', expand=True)[0]
            dataset_dataframe['Month'] = dataset_dataframe['P_Date'].str.split(' ', expand=True)[1]
            dataset_dataframe['Year'] = pd.to_numeric(dataset_dataframe['Year'], errors='coerce')
            dataset_dataframe['Month'] = pd.to_datetime(dataset_dataframe['Month'], format='%b', errors='coerce').dt.month
            dataset_dataframe = dataset_dataframe[
                (dataset_dataframe['Year'] >= start_year) &
                (dataset_dataframe['Year'] <= end_year)
            ]

        print(f'Dataset "{dataset_name}" loaded and filtered based on date selection.')
        return dataset_dataframe
    else:
        print('The selected filters are not available.')
        return None




