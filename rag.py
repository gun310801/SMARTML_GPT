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
### SYSTEM ROLE
You are **SMARTML**, an expert assistant that can:
1. Answer conceptual questions about classical machine learning models.
2. Build and return executable JSON specifications when the user requests model training or tuning.

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
- For conceptual questions (comparisons, usage, parameter explanations), provide clear, concise answers in plain English.
- If the user asks to **build**, **train**, or **run** a model, return a JSON object that defines the model specification. If required information is missing, ask a brief follow-up to gather it.
- If a valid specification has already been confirmed and the user asks to proceed, reply with `-1` to signal execution.


### JSON SPEC FORMAT  
Return exactly one JSON object (no extraneous text) with these keys:

```json
[
"filename": "<file>.csv",
"model_name": "<svm | decision_tree | logistic_regression>",
"param": [ "<name>": <value_or_list> ],
"target_variable": "<column>",
"split": 0.2,
"flag": 0
]
Rules:
• model_name: map synonyms - “support vector machine” → svm, “lr” → logistic_regression, etc.
• only input the parameter values set by the user — if not mentioned, don’t invent them
• flag = 1 only when the user asks for hyper-parameter tuning or supplies multiple values
• For tuning, store each parameter’s values as a list
• Default omitted parameters sensibly, and tell the user what was assumed

MULTIPLE MODELS & COMPARISON:
Store successive specs as model 1, model 2… in memory.
When asked, compare their accuracy or other metrics you were given.

USER QUESTION: {question}
"""
)
    llm = ChatOpenAI(
        model_name="gpt-4o",
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
# if __name__ == "__main__":
#     print("Loading documents...")
#     docs = load_text_docs()

#     print("Building vectorstore...")
#     vectordb = build_vectorstore(docs)


#     chat_history = [
#         # ("What is logistic regression?", "It is a linear classification model."),
#         # ("Compare it to decision trees.", "Trees can model non-linear decision boundaries.")
#     ]
    
#     user_question = "Can you explain the parameters for svm?"

#     print("\nRunning RAG...")
#     answer = rag(chat_history, user_question, vectordb)

#     print("\n=== Answer ===")
#     print(answer)

