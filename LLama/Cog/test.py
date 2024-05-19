import json
from groq import Groq
import dotenv
import os
import csv

with open("Book1.csv", "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    titles = []
    for row in reader:
        title = row[0]
        titles.append(title)

dotenv.load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")


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
    return response_text.strip()


def generate_content_for_titles(titles):
    data = []
    for title in titles:
        # Generate content for each item using separate prompts
        description_prompt = f"Write a compelling description for the title: {title}"
        description = get_llama_assistance(description_prompt)

        toc_prompt = f"Create a table of contents for a document titled: {title}"
        toc = get_llama_assistance(toc_prompt)

        meta_title_prompt = f"Generate a catchy meta title for a document titled: {title}"
        meta_title = get_llama_assistance(meta_title_prompt)

        meta_description_prompt = f"Write a concise meta description for a document titled: {title}"
        meta_description = get_llama_assistance(meta_description_prompt)

        meta_keywords_prompt = f"Suggest relevant meta keywords for a document titled: {title}"
        meta_keywords = get_llama_assistance(meta_keywords_prompt)

        # Create a dictionary with the generated content
        content = {
            "title": title,
            "description": description,
            "table_of_contents": toc,
            "meta_title": meta_title,
            "meta_description": meta_description,
            "meta_keywords": meta_keywords,
        }

        data.append(content)

    # Save the data to a JSON file
    with open("content.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


if __name__ == "__main__":
    # Replace this with your actual list of titles
    titles = [titles[:10]]
    generate_content_for_titles(titles)
    print("Content generation complete! Check content.json for the results.")
