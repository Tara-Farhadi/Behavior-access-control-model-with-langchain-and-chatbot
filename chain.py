from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()


def load_documents():
    """Load all PDF documents from the Uploaded_pdfs folder"""
    pdf_folder = os.path.join(os.getcwd(), "Uploaded_pdfs")
    loader = PyPDFDirectoryLoader(pdf_folder)
    documents = loader.load()
    print(f"Loaded {len(documents)} document pages")
    return documents

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks
def create_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")
    print("Created vector store")
    return vectorstore

def create_qa_chain(vectorstore):
    """Create QA chain using modern LCEL approach"""
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    
    # Create a prompt template
    template = """Answer the question based only on the following context:
{context}

Question: {question}

Answer:"""
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create the chain using LCEL - compatible with LangServe
    from langchain_core.runnables import RunnableLambda
    from operator import itemgetter
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    qa_chain = (
    {
        "context": itemgetter("input") | retriever | RunnableLambda(format_docs), 
        "question": itemgetter("input")
    }
    | prompt
    | llm
    )
    
    print("Created QA chain")
    return qa_chain

def get_qa_chain():
    """Main function to create the complete QA chain"""
    # TODO: Write the code that:
    # 1. Calls load_documents()
    # 2. Calls split_documents() with the documents
    # 3. Calls create_vectorstore() with the chunks
    # 4. Calls create_qa_chain() with the vectorstore
    # 5. Returns the final chain
    documents = load_documents()
    chunks = split_documents(documents)
    vectorstore = create_vectorstore(chunks)
    qa_chain = create_qa_chain(vectorstore)
    return qa_chain