from langchain import PromptTemplate, LLMChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores.faiss import FAISS
from promt_templates import manager_template
from pprint import pprint
import configs
import os


os.environ["OPENAI_API_KEY"] = configs.OPENAI_KEY

callback_manager = BaseCallbackManager([StreamingStdOutCallbackHandler()])
llm = ChatOpenAI(model_name='gpt-3.5-turbo')
embeddings = OpenAIEmbeddings()
index = FAISS.load_local("./state_of_the_union_index", embeddings)


def similarity_search(query, index):
    matched_docs = index.similarity_search(query, k=4)
    sources = []
    for doc in matched_docs:
        sources.append(
            {
                "page_content": doc.page_content,
                "metadata": doc.metadata,
            }
        )
    return matched_docs, sources


def construct_prompt(query) -> PromptTemplate:
    matched_docs, _ = similarity_search(query, index)
    context = "\n".join([str(doc.metadata) for doc in matched_docs])
    return PromptTemplate(template=manager_template,
                          input_variables=["context", "question"]).partial(context=context)


if __name__ == "__main__":
    while True:
        query = input("Query: ")
        if query.lower() == 'exit':
            break
        prompt = construct_prompt(query)
        pprint(LLMChain(prompt=prompt, llm=llm).run(query))
