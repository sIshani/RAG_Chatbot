from flask import Flask, request, jsonify, render_template     #doubt   
import os
from langchain import hub
from dotenv import load_dotenv  
from langchain_community.vectorstores import Chroma  
from langchain_openai import ChatOpenAI, OpenAIEmbeddings 
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.document_loaders import WebBaseLoader 
from langchain_core.output_parsers import StrOutputParser  
from langchain_core.runnables import RunnablePassthrough    
from langchain_core.prompts import PromptTemplate                          


app=Flask(__name__)   
load_dotenv() 
openai_api_key=os.getenv("OPENAI_API_KEY")    

def response(user_query, user_url):  
    loader=WebBaseLoader(
        web_paths=(user_url,) 

        #web_paths=("https://www.ibm.com/topics/chatbots",)   
    )  
    docs=loader.load() 

    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,                      #number of characters in each chunk
        chunk_overlap=200,                    #number of overlapping characters between chunks
        #length_function=len,                          #to measure length of string to be split in chunks
        )
    splits=text_splitter.split_documents(docs) 
    vectorstore=Chroma.from_documents(documents=splits,embedding=OpenAIEmbeddings())   
    #embedding=OpenAIEmbeddings()   


    retriever = vectorstore.as_retriever(search_type="similarity")                             #creates a retriever object to carry out similarity searches
    prompt=hub.pull("rlm/rag-prompt") 
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2, openai_api_key=openai_api_key)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs) 

    template = """Use the following pieces of context to answer the question at the end.
    Say that you don't know when asked a question you don't know, do not make up an answer. Be precise and concise in your answer.

    {context}

    Question: {question}
    Helpful Answer:"""    

    custom_rag_prompt= PromptTemplate.from_template(template) 

    rag_chain=( 
        {"context": retriever | format_docs, "question": RunnablePassthrough()} 
        | custom_rag_prompt
        | llm 
        | StrOutputParser() 
    )

    return rag_chain.invoke(user_query)      

