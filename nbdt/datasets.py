import pandas as pd
import urllib.request
import io
from datetime import datetime

def load_dataset(dataset_name, start_year=None, end_year=None, destination_path=None):
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

        response = urllib.request.urlopen(dataset_url)
        dataset_content = response.read().decode('utf-8')
        dataset_dataframe = pd.read_csv(io.StringIO(dataset_content))
        
        if destination_path is None and start_year is None and end_year is None:
               response = urllib.request.urlopen(dataset_url)
               dataset_content = response.read().decode('utf-8')
               dataset_dataframe = pd.read_csv(io.StringIO(dataset_content))
               print('Dataset downloaded successfully.') # print confirmation
               return dataset_dataframe
        elif destination_path != None and start_year is None and end_year is None:
               response = urllib.request.urlopen(dataset_url)
               dataset_content = response.read().decode('utf-8')
               dataset_dataframe = pd.read_csv(io.StringIO(dataset_content))
               dataset_dataframe.to_csv(destination_path, index=False)
               print(f'Dataset downloaded successfully and saved to "{destination_path}".')
        elif destination_path != None and start_year and end_year:
                response = urllib.request.urlopen(dataset_url)
                dataset_content = response.read().decode('utf-8')
                dataset_dataframe = pd.read_csv(io.StringIO(dataset_content))
                dataset_dataframe = filter(start_year, end_year, dataset_name, dataset_dataframe)
                dataset_dataframe.to_csv(destination_path, index=False)
                print(f'Dataset downloaded successfully and saved to "{destination_path}".')
        elif destination_path is None and start_year and end_year:
               response = urllib.request.urlopen(dataset_url)
               dataset_content = response.read().decode('utf-8')
               dataset_dataframe = pd.read_csv(io.StringIO(dataset_content))
               dataset_dataframe = filter(start_year, end_year, dataset_name, dataset_dataframe)
               print('Dataset downloaded successfully.') # print confirmation
               return dataset_dataframe

               
    else:
        print(f'Dataset "{dataset_name}" is not available.')

def filter(start_year, end_year, dataset_name, dataset_dataframe):
    if start_year in range(2018, 2024) and end_year in range(2018, 2024):
             
             if dataset_name == 'arxiv' and start_year and end_year:
                       dataset_dataframe = dataset_dataframe[
                             (pd.to_datetime(dataset_dataframe['update_date']).dt.year >= start_year) &
                             (pd.to_datetime(dataset_dataframe['update_date']).dt.year <= end_year)
                                  ]
             elif dataset_name == 'bioarxiv' and start_year and end_year:
                        dataset_dataframe = dataset_dataframe[
                             (pd.to_datetime(dataset_dataframe['date']).dt.year >= start_year) &
                             (pd.to_datetime(dataset_dataframe['date']).dt.year <= end_year)
                                  ]
             elif dataset_name == 'plos_one' and start_year and end_year:
                        dataset_dataframe = dataset_dataframe[
                              ((pd.to_datetime(dataset_dataframe['Publication Date'], format="%Y-%m-%dT%H:%M:%SZ")).dt.year >= start_year) &
                              ((pd.to_datetime(dataset_dataframe['Publication Date'], format="%Y-%m-%dT%H:%M:%SZ")).dt.year <= end_year)
                                  ]
             elif (dataset_name in ['medline_large', 'medline_small']) and start_year and end_year:

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




