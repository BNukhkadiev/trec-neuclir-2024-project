## Done by Baga


import ir_datasets
import pandas as pd
import csv


def save_as_csv(path, data):
    """
    write data to .csv file with \t as separator
    """
    with open(path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        # Write the header
        writer.writerow(("doc_id", "doc_title", "doc_text"))
        # Write the data
        writer.writerows(data)
        print(f"Data has been saved to {path}")


def import_clir_dataset():
    return ir_datasets.load("neuclir/1/ru/trec-2023")


def get_qrels_queries():
    """
    returns queries and qrels and lists.
    """
    dataset = import_clir_dataset()
    english_queries = [(query.query_id, query.title) for query in dataset.queries_iter()]
    qrels = [(qrel.query_id, qrel.doc_id, qrel.relevance) for qrel in dataset.qrels_iter()]
    return english_queries, qrels


def sample_documents_set(filename):
    """
    Selects small subset of documents that only appear in qrels
    """
    import csv


    dataset = import_clir_dataset()
    qrels_df = pd.DataFrame(qrels, columns=['query_id', 'doc_id', 'relevance_class'])

    unique_qrel_docs = qrels_df['doc_id'].nunique()
    counter = 0
    filename = 'data/documents_subset.csv'

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(("doc_id", "doc_title", "doc_text"))
        for doc in dataset.docs_iter():
            if doc.doc_id in qrels_df['doc_id'].values:
                writer.writerow((doc.doc_id, doc.title, doc.text))
                counter += 1
                if counter == unique_qrel_docs:
                    break
    print('data has been saved to', filename)
