import os
from langchain_community.document_loaders import TextLoader
from langchain_community.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv; load_dotenv()


def load_text_docs():
    documents = []
    for fname in os.listdir("Documents"):
        if fname.endswith(".txt"):
            loader = TextLoader(os.path.join("Documents", fname))
            docs = loader.load()
            documents.extend(docs)
    return documents


def build_vectorstore(documents):
    # 1. Split each long document into smaller overlapping chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,     
        chunk_overlap=50     
    )
    chunks = splitter.split_documents(documents)

    # 2. Create OpenAI embedding model
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # 3. Store embeddings in Chroma (in-memory vector database)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vectorstore

def build_qa_chain(vectorstore):
    # Create OpenAI chat model
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",  
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Create the RAG chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True  
    )

    return qa_chain

