from langchain_community.llms.ollama import Ollama


def llama3_summary(url):
    model = 'llama3.1'
    llm = Ollama(model=model)

    prompt = f'Summarize the article content at the following URL: {url}'
    response = llm.invoke(prompt)  # summa
    return response


def llama3_sentiment(url):
    model = 'llama3.1'
    llm = Ollama(model=model)

    prompt = (f'Analyze the overall sentiment of the news article content at the following URL without any explanation: {url}'
              f'Choose one word reply from: (Positive/Negative/Neutral) to represent the most likely overall sentiment')
    response = llm.invoke(prompt)
    return response.strip('.').lower()
