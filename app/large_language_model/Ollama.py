from langchain_ollama import OllamaLLM


def llama3_summary(url):
    model = "llama3.2"
    llm = OllamaLLM(model=model)

    prompt = f"Summarize the content: {url}"
    response = llm.invoke(prompt)
    return response


def llama3_sentiment(url):
    model = "llama3.2"
    llm = OllamaLLM(model=model)

    prompt = (
        f"Analyze the overall sentiment of the news article content at the following URL without any explanation: {url}"
        f"Choose one word reply from: (Positive/Negative/Neutral) to represent the most likely overall sentiment"
    )
    response = llm.invoke(prompt)
    return response.strip(".").lower()
