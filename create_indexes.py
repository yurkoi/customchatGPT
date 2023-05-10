from langchain.document_loaders import JSONLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
import configs
import os

os.environ["OPENAI_API_KEY"] = configs.OPENAI_KEY


def metadata_func(record: dict, metadata: dict) -> dict:
    metadata['name'] = record.get("name")
    metadata["description"] = record.get("description")
    metadata["technical_characteristics"] = record.get("technical_characteristics")
    metadata["price"] = record.get("price")
    metadata["quantity"] = record.get("quantity")
    return metadata


def split_chunks(sources):
    chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=32)
    for chunk in splitter.split_documents(sources):
        chunks.append(chunk)
    return chunks


def create_index(chunks):
    embeddings = OpenAIEmbeddings()
    texts = [doc.page_content for doc in chunks]
    metadatas = [doc.metadata for doc in chunks]
    search_index = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    return search_index


if __name__ == "__main__":

    loader = JSONLoader(
        file_path='./data/products.json',
        jq_schema='.products[]',
        content_key="name",
        metadata_func=metadata_func
    )

    save_to = 'state_of_the_union_index'
    docs = loader.load()
    chunks = split_chunks(docs)
    index = create_index(chunks)
    index.save_local(save_to)
    if index is not None:
        print(f"Indexes are created and saved in {save_to}")
