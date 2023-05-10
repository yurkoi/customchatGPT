from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores.faiss import FAISS
import configs
import os

os.environ["OPENAI_API_KEY"] = configs.OPENAI_KEY


index_path = './state_of_the_union_index'
llm = ChatOpenAI(model_name='gpt-3.5-turbo')

embeddings = OpenAIEmbeddings()

index = FAISS.load_local(index_path, embeddings)
qa = ConversationalRetrievalChain.from_llm(llm, index.as_retriever(), max_tokens_limit=400)


chat_history = []
print("Welcome to the State of the Union chatbot! Type 'exit' to stop.")
while True:
    query = input("Please enter your question: ")
    if query.lower() == 'exit':
        break
    result = qa({"question": query, "chat_history": chat_history})

    print("Answer:", result['answer'])
