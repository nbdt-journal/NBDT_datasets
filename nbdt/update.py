from dateutil import parser
from datetime import timedelta
import requests
import json
import pandas as pd
import csv
import urllib.request
import io




def update_dataset(dataset_name, end_date, destination_path, start_date=None, update=False):
    """
    Update the dataset with new papers from the specified source.

    Args:
        dataset_name (str): Name of the dataset.
        end_date (str): End date for collecting papers in the format "dd-mm-yyyy".
        destination_path (str): File path to store the updated dataset.
        start_date (str, optional): Start date for collecting papers in the format "dd-mm-yyyy". Default is None.
        update (bool, optional): Flag indicating whether to update the source dataset. Default is False.
    """
    if update != False and update != True:
      raise ValueError("update should be either True or False (by default it is False)")


    date_obj = parser.parse(end_date, dayfirst=True)
    last_day = date_obj.replace(day=1, month=date_obj.month + 1) - timedelta(days=1)
    c_date = last_day.strftime("%Y-%m-%d")

    if start_date is not None:
        date_obj2 = parser.parse(start_date, dayfirst=True)
        last_day2 = date_obj2.replace(day=1, month=date_obj2.month + 1) - timedelta(days=1)
        c_date2 = last_day2.strftime("%Y-%m-%d")

    if dataset_name == 'bioarxiv':
        if start_date is None:
            bioarxiv(c_date, destination_path, update)
        else:
            bioarxiv(c_date, destination_path, update, c_date2)

    elif dataset_name == 'plos_one':
        if start_date is None:
            plos_one(c_date, destination_path, update)
        else:
            plos_one(c_date, destination_path, update, c_date2)

    elif dataset_name == 'arxiv':
        if start_date is None:
            arxiv(c_date, destination_path, update)
        else:
            arxiv(c_date, destination_path, update, c_date2)


    else:
        raise ValueError("The given dataset is not available! Check Documentation")


def bioarxiv(a1, d1, update, b1='2023-01-01'):
    """
    Collect papers from the bioarxiv source and update the dataset.

    Args:
        a1 (str): End date for collecting papers.
        d1 (str): File path to store the updated dataset.
        update (bool): Flag indicating whether to update the source dataset.
        b1 (str, optional): Start date for collecting papers. Default is '2023-01-01'.
    """
    dataset_url = 'https://huggingface.co/datasets/PenguinMan/ARXIV/resolve/main/bioarxiv_final.csv'
    url = 'https://api.biorxiv.org/details/biorxiv/{}/{}/{}/json?category=neuroscience'.format(b1, a1, '{}')
    results1 = requests.get(url.format(0)).json()
    total = results1['messages'][0]['total']

    print("Total number of papers:", total)

    if total >= 100 and total <= 10000:
        print("Collecting Papers... Estimated Time: ~6 mins")
    elif total > 10000:
        print("Collecting Papers... Estimated Time: 10 mins to 30 mins")
    elif total >= 50000:
        print("Collecting Papers... Estimated Time: 30 mins to 1 hr")

    if total >= 100:
        url = 'https://api.biorxiv.org/details/biorxiv/{}/{}/{}/json?category=neuroscience'.format(b1, a1, '{}')
        articles1 = []
        cursor = 0
        count = 0
        while len(results1['collection']) != 0:
            results1 = requests.get(url.format(cursor)).json()
            articles1 += results1['collection']
            count += len(results1['collection'])
            cursor += 100

        with open('neuroscience_articles_1.json', 'w') as f:
            json.dump(articles1, f)

    one = pd.read_json('neuroscience_articles_1.json')
    neuro = one[one.category == 'neuroscience']
    neuro_2 = neuro[['doi', 'title', 'abstract', 'authors', 'author_corresponding', 'date', 'jatsxml']] \
        .rename(columns={'doi': 'ID', 'jatsxml': 'URL'})
    neuro_3 = neuro_2.drop_duplicates(subset=['abstract'], keep='last')
    print("Total number of papers collected:", neuro_3.shape[0])

    if not update:
        neuro_3.to_csv(d1, index=False)
        print("Updated papers stored as: ", d1)

    if update:
        print("Updating source dataset...")
        response = urllib.request.urlopen(dataset_url)
        dataset_content = response.read().decode('utf-8')
        dataset_dataframe = pd.read_csv(io.StringIO(dataset_content))
        new = dataset_dataframe[['doi', 'title', 'abstract', 'authors', 'author_corresponding', 'date', 'jatsxml']] \
            .rename(columns={'doi': 'ID', 'jatsxml': 'URL'})

        combined_dataset = pd.concat([new, neuro_3], ignore_index=True)
        combined_dataset2 = combined_dataset.drop_duplicates(subset=['abstract'], keep='last')

        combined_dataset2.to_csv(d1, index=False)
        print("Source dataset updated!")


def plos_one(c_date, destination_path, update, b2='2023-05-31'):
    """
    Collects articles from the PLOS ONE journal in the field of neuroscience within a specified date range.

    Args:
        c_date (str): The end date of the date range in the format 'YYYY-MM-DD'.
        destination_path (str): The file path to store the collected data.
        update (bool): Whether to update an existing dataset or create a new one.
        b2 (str, optional): The start date of the date range in the format 'YYYY-MM-DD'. Default is '2023-05-31'.
    """

    query = "neuroscience"
    fields = "title,author,abstract,journal,subject_facet,publication_date"
    filter = "publication_date:[2019-01-01T00:00:00Z TO 2023-12-31T23:59:59Z], subject_facet:\"/Neuroscience/\""
    n_filter = filter.replace('2019-01-01T00:00:00Z', f'{b2}T00:00:00Z').replace('2023-12-31T23:59:59Z', f'{c_date}T23:59:59Z')
    start = 0
    rows = 100

    # Construct the query URL
    url = f"http://api.plos.org/search?q={query}&fl={fields}&fq={n_filter}&start={start}&rows={rows}"

    # Send the request and get the response
    response = requests.get(url)

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the response as JSON
        data = response.json()
        num = data['response']['numFound']
        if num > 100 and num <= 10000:
            print('Collecting Papers........ Est time: ~2mins')
        elif num > 10000:
            print('Collecting Papers........ Est time: ~5mins')
    else:
        # Print an error message
        print(f"Request failed with status code {response.status_code}")

    articles = []  # Define an empty list to store articles

    for i in range(0, num, 100):
        # Define the query parameters
        query = "neuroscience"
        fields = "title,author,abstract,journal,subject_facet,accepted_date,id"
        filter2 = n_filter
        start = i
        rows = 100

        # Construct the query URL
        url2 = f"http://api.plos.org/search?q={query}&fl={fields}&fq={filter}&start={start}&rows={rows}"

        # Send the request and get the response
        response = requests.get(url2)

        # Check if the response is successful
        if response.status_code == 200:
            # Parse the response as JSON
            data = response.json()

            # Append the articles from this page to the list
            articles.extend(data['response']['docs'])
        else:
            # Print an error message
            print(f"Request failed with status code {response.status_code}")

    with open("neuroscience_articles.csv", mode="w", newline="") as file:
        # Create a CSV writer
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["ID", "title", "author", "abstract", "journal", "subject", "date"])

        # Loop over the articles and write the data to the CSV file
        for article in articles:
            writer.writerow([
                article.get("id", ""),
                article.get("title", ""),
                article.get("author", ""),
                article.get("abstract", ""),
                article.get("journal", ""),
                article.get("subject_facet", ""),
                article.get("accepted_date", "")
            ])

    plos_one_update = pd.read_csv("neuroscience_articles.csv")

    plos_one_update2 = plos_one_update.drop_duplicates(subset=['abstract'], keep='last')
    plos_one_update3 = plos_one_update2.dropna()

    print("New Papers collected: ", plos_one_update3.shape[0])

    # Print the total number of articles collected
    if not update:
        plos_one_update3.to_csv(destination_path, index=False)
        print("The data is stored as: ", destination_path)

    if update:
        # Need to add error handling
        print("Updating source dataset.............")
        plos_one_url = "https://huggingface.co/datasets/PenguinMan/ARXIV/resolve/main/plos_one_final2.csv"
        response = urllib.request.urlopen(plos_one_url)
        dataset_content2 = response.read().decode('utf-8')
        dataset_dataframe2 = pd.read_csv(io.StringIO(dataset_content2))
        plos_new = dataset_dataframe2[['ID', 'Title', 'Author', 'Abstract', 'Journal', 'Subject', 'Accepted_Date']] \
            .rename(columns={'Title': 'title', 'Author': 'author', 'Abstract': 'abstract', 'Journal': 'journal',
                             'Subject': 'subject', 'Accepted_Date': 'date'})

        plos_combined = pd.concat([plos_new, plos_one_update3], ignore_index=True)
        plos_combined2 = plos_combined.drop_duplicates(subset=['abstract'], keep='last')
        plos_combined3 = plos_combined2.dropna()
        plos_combined3.to_csv(destination_path, index=False)

        print("Source dataset Updated!!")
        print("The data is stored as: ", destination_path)


import arxiv


def arxiv(c_date, destination_path, update, c_date2='2023-05-31'):
    import arxiv

    # Perform the arXiv search with date filtering
    search = arxiv.Search(
        query='brain',
        max_results=20000,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    # Create an empty list to store the extracted data
    data = []
    print("Collecting Papers........ Est Time: 10 mins")
    # Iterate over the search results
    for result in search.results():
        # Extract the desired information from each result
        entry_id = result.entry_id
        submitter = ""
        if result.authors:
            submitter = result.authors[0].name
        authors = [author.name for author in result.authors]
        title = result.title
        journal_ref = result.journal_ref if result.journal_ref else ""
        categories = [result.primary_category]
        abstract = result.summary
        versions = len(result.comment) if result.comment else 0
        update_date = result.updated
        authors_parsed = []

        # Append the extracted data to the list
        data.append({
            'id': entry_id,
            'submitter': submitter,
            'authors': authors,
            'title': title,
            'categories': categories,
            'abstract': abstract,
            'versions': versions,
            'update_date': update_date
        })

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data)
    df['update_date'] = pd.to_datetime(df['update_date'])

    # Define the start and end dates for filtering


    # Filter the DataFrame based on the date range
    filtered_df = df[(df['update_date'] >= c_date2) & (df['update_date'] <= c_date)]
    arxiv_2 = filtered_df.drop_duplicates(subset=['abstract'], keep='last')
    arxiv_final = arxiv_2.dropna()
    if not update:
       arxiv_final.to_csv(destination_path, index=False)
    

    if update:
      arxiv_url = 'https://huggingface.co/datasets/PenguinMan/ARXIV/resolve/main/arxiv2.csv'
      print("Updating Source Dataset...............")
      response3 = urllib.request.urlopen(arxiv_url)
      dataset_content3 = response3.read().decode('utf-8')
      dataset_dataframe3 = pd.read_csv(io.StringIO(dataset_content3))
      arxiv_new = dataset_dataframe3[['id', 'submitter', 'authors', 'title', 'categories', 'abstract', 'versions', 'update_date']]
      arxiv_new2 = arxiv_new.drop_duplicates(subset=['abstract'], keep='last')
      arxiv_new3 = arxiv_new2.dropna()                             
            

      arxiv_new3.to_csv(destination_path, index=False)
      print("The source dataset is updated and is stored at:", destination_path)
