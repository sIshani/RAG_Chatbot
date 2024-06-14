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
load_dotenv()                                   #loads environment variables from env file into environment
os.environ["USER_AGENT"] = "YourAppName/1.0"    #to identify the application when it makes requests to web servers  

def response(user_query):                       #to handle user queries
    #print(f"Received URL: {user_url}")   
    #print(f"Received Query: {user_query}") 

    # Load environment and get your openAI api key
    load_dotenv()                                       #reloads the variables
    openai_api_key = os.getenv("OPENAI_API_KEY")        #retrieves the OpenAI API key from the environment variables


    # Select a webpage to load the context information from
    loader = WebBaseLoader(                       # to load the content of a specified web page
        #web_paths=(user_url,),  
        #web_paths=("https://www.techtarget.com/searchenterpriseai/tip/9-top-AI-and-machine-learning-trends/",), 
        #web_paths=("https://www.investopedia.com/terms/c/chatbot.asp#:~:text=A%20chatbot%20is%20a%20computer,through%20any%20major%20messaging%20application/",),
        web_paths=("https://www.linkedin.com/pulse/insights-post-pandemic-economy-our-2024-global-market-rob-sharps-jcnmc/",),
    )
    docs = loader.load()                     #loads the documents in docs variable


    # Restructure to process the info in chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)        #splits the document into smaller chunks of 1000 characters each, with a 200-character overlap between chunks
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())       #creates a vector store from the split documents, using OpenAI embeddings to convert the text into vectors that can be used for similarity searches


    # Retrieve info from chosen source
    retriever = vectorstore.as_retriever(search_type="similarity")                            #creates a retriever object to carry out similarity searches
    prompt = hub.pull("rlm/rag-prompt")                                                       #pulls a specific prompt template from langchainhub
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)    #initializes an LLM for generating responses

    def format_docs(docs):   
        return "\n\n".join(doc.page_content for doc in docs)                      #formats the document chunks to a single string by joining the content



    template = """Use the following pieces of context to answer the question at the end.
    Say that you don't know when asked a question you don't know, do not make up an answer. Be precise and concise in your answer.

    {context}

    Question: {question}
    Helpful Answer:"""                                             #how the question and context should be formatted

    # Add the context to your user query
    custom_rag_prompt = PromptTemplate.from_template(template)      #creates a prompt template from the template string

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}           #retrives and formats the text, passes user query
        | custom_rag_prompt                                                               #adds context to user query
        | llm                                                                             #uses llm to generate response
        | StrOutputParser()                                                               #parses the response into a string format
    )

    return rag_chain.invoke(user_query)                             #executes the chain with user query and returns the response