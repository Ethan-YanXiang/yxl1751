from langchain_community.llms.ollama import Ollama


def llama3_summary(url):
    model = 'llama3.1'
    llm = Ollama(model=model)

    prompt = f'Please summarize the following news article in a concise summary of no more than 100 words: {url}'
    response = llm.invoke(prompt)  # summa
    return response


def llama3_sentiment(url):
    model = 'llama3.1'
    llm = Ollama(model=model)

    prompt = f'Please analyze the sentiment of the following news article and determine whether the overall sentiment is positive, negative, or neutral: {url}'
    response = llm.invoke(prompt)
    return response
