import os
import dotenv
import uvicorn
from groq import Groq
from fastapi import FastAPI, Body

dotenv.load_dotenv(); api_key = os.environ.get("GROQ_API_KEY")
if not api_key: raise ValueError("GROQ_API_KEY environment variable not set")

def get_llama_assistance(prompt):
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
            {
                "role": "assistant",
                "content": "",
            },
        ],
        temperature=1.4,
        max_tokens=8192,
        top_p=1,
        stream=True,
        stop=None,
    )
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""
    return response_text


def generate_content(title):  # Accepts a single title for processing
    data = dict()
    content_dict = {"title": title}
    constraint = "(You're an professional Market Research Analyst, and you only have to answer what's been told, without adding 'Here is the-(info). Just begin with what's been tasked')"
    content_dict["description"] = get_llama_assistance(
        f"{constraint}. Write a compelling description for the title: {title}"
    )
    content_dict["table_of_contents"] = get_llama_assistance(
        f"{constraint}. Generate a table of contents for content related to: {title}"
    )
    content_dict["meta_title"] = get_llama_assistance(
        f"{constraint}. Create a meta title for content about: {title}"
    )
    content_dict["meta_description"] = get_llama_assistance(
        f"{constraint}. Write a meta description summarizing content on: {title}"
    )
    content_dict["meta_keywords"] = get_llama_assistance(
        f"{constraint}. Suggest relevant meta keywords for content related to: {title}"
    )
    data[title] = content_dict
    return data


app = FastAPI()
@app.post("/generate_content")
async def generate_content_from_title(title: str = Body(...)):
    generated_data = generate_content(title)
    return generated_data


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000)