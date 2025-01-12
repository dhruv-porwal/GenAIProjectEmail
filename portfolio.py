import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path="/Users/dhruvporwal/Desktop/testFolder/project-genai-cold-email-generator/app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        # Check if the collection is empty
        if not self.collection.count():
            # Iterate over the rows in the DataFrame
            for _, row in self.data.iterrows():
                # Add each document to the collection
                self.collection.add(
                    documents=row["Techstack"],        # The document to add
                    metadatas={"links": row["Links"]},  # Metadata for the document
                    ids=[str(uuid.uuid4())]            # Unique ID for the document
                )

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
