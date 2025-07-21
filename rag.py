import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import LLMChain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
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

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,     
        chunk_overlap=50     
    )
    chunks = splitter.split_documents(documents)


    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vectorstore
def rag(chat_history: list[tuple[str, str]], question: str, vectorstore, n_points: int = 3) -> str:

    retriever = vectorstore.as_retriever()
    docs = retriever.invoke(question, k=n_points)
    context = "\n".join(doc.page_content for doc in docs).strip()
    # print("\n=== CONTEXT ===")
    # print(context)  


    chat_str = "\n".join([f"User: {q}\nAssistant: {a}" for q, a in chat_history])


    custom_prompt = PromptTemplate(
        input_variables=["question", "chat_history", "context"],
        template="""

### ROLE
You are **SMARTML**, an expert assistant that can:
1. Answer conceptual questions about classical machine learning models.
2. Build and return executable JSON specifications when the user requests model training or tuning.
3. Signal model execution when requested.

---

### MEMORY & CONTEXT
- Prioritize relevant information from the chat history:
{chat_history}

- Supplement your understanding using the technical reference below:
{context}

- If required information is missing from both, respond with:  
**"That's all I know based on the current knowledge."**

---

### RESPONSE GUIDELINES

**FOR EXECUTION REQUESTS:**
- If the user asks to "run", "execute", "train", "build", or "start" the model, return exactly: `-1`
- This applies to phrases like: "run the model", "train the model", "execute", "go ahead", "start training"

**FOR MODEL SPECIFICATIONS:**
- If the user requests a NEW model specification (not execution), return a complete JSON object
- Ask for missing information if needed (filename, target variable, model type)

**FOR CONCEPTUAL QUESTIONS:**
- Provide clear, concise answers in plain English

---

### JSON SPEC FORMAT  
When creating a NEW model specification, return exactly one JSON object:

```json
{{
  "filename": "data.csv",
  "model_name": "svm",
  "param": {{
    "C": 1.0,
    "kernel": "rbf"
  }},
  "target_variable": "target_column",
  "split": 0.2,
  "flag": 0
}}
```

**Rules:**
- model_name: use exactly one of: "svm", "decision_tree", "logistic_regression"
- param: only include parameters explicitly mentioned by user
- flag: set to 1 only for hyperparameter tuning (when user provides parameter ranges)
- split: default to 0.2 unless specified

---

**IMPORTANT:** 
- For execution requests (run/train/execute), respond with: `-1`
- For new specifications, respond with: complete JSON
- For questions, respond with: plain text explanation

USER QUESTION: {question}
"""
)
    llm = ChatOpenAI(
        model_name="gpt-4",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )


    chain = custom_prompt | llm
    response = chain.invoke({
        "question": question,
        "chat_history": chat_str,
        "context": context
    })
    return response.content


