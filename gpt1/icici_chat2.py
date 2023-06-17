import numpy as np
import openai
import pandas as pd
import pickle
import tiktoken

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

df = pd.read_csv('FAQ_ICICI.csv')

# df["token"] = None
# for idx, r in df.iterrows():
# #     print(len(r.content))
# #     df["token"] = df[len(r.content)]
#     df.loc[idx,'token'] = len(r.content)

# "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" -- MLAI
# "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" -- MLAI
# "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" -- LP
def get_embedding(text: str, model: str=EMBEDDING_MODEL) -> list[float]:
    openai.api_key = "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"
    result = openai.Embedding.create(
      model=model,
      input=text
    )
    return result["data"][0]["embedding"]

# import time
# def compute_doc_embeddings(df: pd.DataFrame) -> dict[tuple[str, str], list[float]]:
#     embeddings = {}
#     for idx, r in df.iterrows():
#         print(idx)
# #         print(r)
#         embeddings[idx] = get_embedding(r.title)
#         time.sleep(5)  # Add a delay of 10 second between requests
#     return embeddings


def load_embeddings(fname: "str") -> dict[tuple[str, str], list[float]]:
    """
    Read the document embeddings and their keys from a CSV.

    fname is the path to a CSV with exactly these named columns:
        "title", "heading", "0", "1", ... up to the length of the embedding vectors.
    """

    df = pd.read_csv(fname, header=0)

    max_dim = max([int(c) for c in df.columns if c != "title"])
    return {
        (r.title): [r[str(i)] for i in range(max_dim + 1)] for _, r in df.iterrows()

    }

document_embeddings = load_embeddings("ICICI_faq_embed.csv")


def vector_similarity(x: list[float], y: list[float]) -> float:
    """
    Returns the similarity between two vectors.

    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(x), np.array(y))


def order_document_sections_by_query_similarity(query: str, contexts: dict[(str, str), np.array]) -> list[
    (float, (str, str))]:
    """
    Find the query embedding for the supplied query, and compare it against all of the pre-calculated document embeddings
    to find the most relevant sections.

    Return the list of document sections, sorted by relevance in descending order.
    """
    query_embedding = get_embedding(query)

    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in contexts.items()
    ], reverse=True)

    return document_similarities

# a = order_document_sections_by_query_similarity("Give me a list of icici credit crads  interest rate", document_embeddings)[:5]

MAX_SECTION_LEN = 7552
SEPARATOR = "\n* "
ENCODING = "gpt2"  # encoding for text-davinci-003

encoding = tiktoken.get_encoding(ENCODING)
separator_len = len(encoding.encode(SEPARATOR))

print(f"Context separator contains {separator_len} tokens")


def construct_prompt(question: str, context_embeddings: dict, df: pd.DataFrame) -> str:
    """
    Fetch relevant
    """
    most_relevant_document_sections = order_document_sections_by_query_similarity(question, context_embeddings)[:3]
    #     print(most_relevant_document_sections)
    chosen_sections = []
    chosen_sections_len = 0
    chosen_sections_indexes = []

    for _, section_index in most_relevant_document_sections:
        # Add contexts until we run out of space.
        #         print(section_index)
        document_section = df.loc[section_index]
        #         print(document_section)
        chosen_sections_len += document_section.token + separator_len
        if chosen_sections_len > MAX_SECTION_LEN:
            break

        chosen_sections.append(SEPARATOR + document_section.content.replace("\n", " "))
        chosen_sections_indexes.append(str(section_index))

    # Useful diagnostic information
    print(f"Selected {len(chosen_sections)} document sections:")
    print("\n".join(chosen_sections_indexes))
    # print(type("".join(chosen_sections) ))
    # header = """Answer the question as truthfully as possible using the provided Given Below Information and previous conversation, and if the answer is not contained within in both, say "I don't know.For more details call on our CUSTOMER CARE NO.1800 1080"\n\nGiven Below Information:"""
    header =  "please don't make answer if you can't find the answer simply say i don't know" + "".join(chosen_sections) + "Please help me find the answer to the following question:\n"+ f"{question}\n\n" + "please don't make answer if you can't find the answer simply say i don't know"

    return header 





# COMPLETIONS_API_PARAMS = {
#     # We use temperature of 0.0 because it gives the most predictable, factual answer.
#     "temperature": 0.0,
#     "max_tokens": 500,
#     "model": COMPLETIONS_MODEL,
# }


# def generate_response(input_text):
#     output_text = f"<a href={input_text}>{input_text}</a>"
#     return output_text


import re
import pandas as pd
import openai



# conversation=[]
def answer_query_with_context(
        query: str,
        df: pd.DataFrame,
        document_embeddings: document_embeddings,
        show_prompt: bool = False,
) -> str:
    conversation = []
    # Construct prompt to send to OpenAI API
    prompt = construct_prompt(
        query,
        document_embeddings,
        df,
        # conversation
    )
    
    # Print prompt if show_prompt is True
    if show_prompt:
        print(prompt)
     
    
    
    message = {"role": "system", "content": prompt}
    conversation.append(message) 
    # Send prompt to OpenAI API and get response
    while(True):
        # user_input = input("")     
        conversation.append({"role": "user", "content": query})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = conversation
        )

        conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        print("Conve",conversation)
        # print("\n" + response['choices'][0]['message']['content'] + "\n")
        
        text = response['choices'][0]['message']['content']
        # regex = r"(credit card)"
        # match = re.search(regex, text.lower())
        # print(match)
        # if match:
        #     text += " To know more, please visit https://www.icicibank.com/card/credit-cards/credit-card"

        # regex = r"(personal loan)"
        # match = re.search(regex, text.lower())
        # if match:
        #     text += " To know more, please visit https://www.icicibank.com/personal-banking/loans/personal-loan"

        # regex = r"(home loan)"
        # match = re.search(regex, text.lower())
        # if match:
        #     text += " To know more, please visit https://www.icicibank.com/personal-banking/loans/home-loan"

        # regex = r"(fixed deposit)"
        # match = re.search(regex, text.lower())
        # if match:
        #     text += " To know more, please visit https://www.icicibank.com/personal-banking/deposits/fixed-deposit"

        # regex = r"(demat account)|(trading account)"
        # match = re.search(regex, text.lower())
        # if match:
        #     text += " To know more, please visit https://www.icicibank.com/personal-banking/accounts/three-in-one-trading-account"
        # # Check if response contains a URL and generate response if so
        # regex = r"(?P<url>https?://[^\s]+)"
        # #     regex = r'https?://(?:www\.)?icicibank\.com/\S+(?:\?\S*)?(?:#\S*)?'
        # #     regex = r"https?://[^\s<>]+(?:\w/)?(?:[^\s()]*)"
        # match = re.search(regex, text)
        print(match)
        if match:
            url = match.group("url")
            text = text.replace(url, "")
            # link = generate_response(url)
            link = url
            #         print(link)
            return f"{text}, {link}"

        # Return response text
        return text

    
 
  

def inputdata(inpval: str) :
    response = answer_query_with_context(inpval, df, document_embeddings)
    if isinstance(response, tuple):
        text, url = response
        return text, url
    else:
        return response


# print(answer_query_with_context("Tell me about home loan", df, document_embeddings)[0].strip())
# def add_text(history, text):
#     history = history + [(text, None)]
#     return history, ""

# def inputdata(history) :
#     history2 = history[-1][0]


#     response = answer_query_with_context(history2, df, document_embeddings)
#     # if isinstance(response, tuple):
#     #     text, url = response
#     #     return text, url
#     # else:
#     history[-1][1] = response
#     print("History: ",history)
#     return history



# import os
# import openai
# openai.api_key = os.getenv("OPENAI_API_KEY") 
# openai.organization = os.getenv("OPENAI_ORGANIZATION") 
# def chatgpt(inpval:str)

#     conversation=[{"role": "system", "content": "You are a helpful assistant."}]

#     while(True):
#         user_input = input("")     
#         conversation.append({"role": "user", "content": user_input})

#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages = conversation
#         )

#         conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
#         print("\n" + response['choices'][0]['message']['content'] + "\n")