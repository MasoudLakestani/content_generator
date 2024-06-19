import os
from typing import List, Optional
from openai import OpenAI
from .scraper import scrape_result
from .google_urls import search
from settings import config

API_KEY = config['openai']['API_KEY']

def create_article_v1(subject: str, keywords: Optional[List[str]]):
    persuasive_mode = (
        f"Use persuasive language to engage the reader, presenting compelling "
        f"arguments and evidence to support your viewpoints on the {subject}. "
        f"The article should not only inform but also persuade the reader of the "
        f"significance and relevance of the topic."
    )

    informative_mode = (
        f"Use clear and precise language to present information comprehensively "
        f"about the {subject}. Include relevant data, facts, and figures to support "
        f"your explanations, ensuring the article is both informative and engaging. "
        f"Aim to educate the reader on the significance and details of the topic, while "
        f"utilizing the keywords effectively as headings to improve SEO and readability."
    )

    client = OpenAI(api_key=API_KEY)
    article = subject + "\n"

    have_information = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Do you have any information about {subject}? Just say yes or no."
            }
        ],
        model="gpt-4o-2024-05-13",
    )

    used_information = ""
    if have_information.choices[0].message.content.lower().replace(".", "") == "no":
        scrape_url = search(subject)[:6 - len(keywords)]
        for key in keywords:
            scrape_url.append(search(key)[0])
        google_information = scrape_result(scrape_url)
        used_information = (
            f"Use only the information provided: {google_information}. Do not use your information."
        )

    main_text = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a blog writer assistant specialized in generating long, "
                    "SEO-optimized blog posts in Persian. Your task is to help users create "
                    "main text that is engaging, comprehensive, and rich in keywords to enhance "
                    "search engine visibility."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Compose a detailed and engaging main body for an article about {subject}, ensuring it "
                    f"is devoid of any spelling or grammatical errors. {used_information} Find an attractive "
                    f"heading and begin with a paragraph about that heading. Then use these keywords: {keywords} "
                    f"as headings throughout the article, but only where they naturally fit the content. Should there "
                    f"be fewer than three suitable headings, draw upon your expertise to create additional appropriate "
                    f"headings. The article must contain at least 800 words and be written in Persian. Focus exclusively "
                    f"on delivering the main content without including any introductory or concluding elements. Specifically, "
                    f"avoid any summarizing paragraphs or statements like 'نتیجه گیری' or 'جمع بندی' that could be interpreted "
                    f"as conclusions, ensuring the text consists only of substantive content without any introduction and conclusion. {informative_mode}"
                )
            }
        ],
        model="gpt-4o-2024-05-13",
        temperature=0.7,
        max_tokens=2000,
    )

    introduction = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a blog writer assistant specialized in generating long, SEO-optimized blog posts in Persian. "
                    "Your primary responsibility involves carefully analyzing the provided main content to craft a detailed and "
                    "well-aligned introduction. This introduction should seamlessly introduce the main themes and prepare readers "
                    "for the in-depth exploration that follows in the main body of the text."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Generate an introduction for the provided main text. Main text: {main_text.choices[0].message.content}. "
                    "Avoid duplication in the introduction and main text. Use the word 'مفدمه' at the start of the introduction."
                )
            }
        ],
        model="gpt-4o-2024-05-13",
        temperature=0.7,
        max_tokens=800,
    )

    article = introduction.choices[0].message.content + "\n" + main_text.choices[0].message.content + "\n"

    conclusion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a blog writer assistant specialized in generating long, SEO-optimized blog posts in Persian. "
                    "Your primary responsibility involves carefully analyzing the provided article to craft a detailed and well-aligned "
                    "conclusion. This conclusion should be complete and comprehensive, encapsulating the key points and main arguments "
                    "presented in the article. It should effectively summarize the content while providing a clear, conclusive statement that "
                    "reinforces the article's main themes and leaves the reader with a strong impression of the overall message."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Generate a conclusion for the provided article. Main article: {article}. Avoid duplication. Use the word "
                    "'نتیجه گیری' at the start of the conclusion."
                )
            }
        ],
        model="gpt-4o-2024-05-13",
        temperature=0.7,
        max_tokens=800,
    )
    article += conclusion.choices[0].message.content

    edited_article = client.chat.completions.create(
        messages = [
            {
                "role": "system",
                "content": (
                    "You are assigned the role of a text editor. I will provide you with an article "
                    "Your tasks include correcting any spelling or grammatical errors and removing any duplicate "
                    "content. Please use HTML <h2> tags to designate section headings. "
                    "Additionally, you should eliminate all unnecessary white spaces and delete "
                    "all blank lines to ensure the content is optimized for web presentation. "
                    "Ensure that the text is clear, concise, and well-organized to enhance "
                    "readability and SEO performance."
                )
            },
            {
                "role": "user",
                "content": f"Please edit and format the following article as specified: {article}"
            }
        ],
        model="gpt-4o-2024-05-13",
        temperature=0.7,
        max_tokens=3000,
    )

    return {"article":edited_article.choices[0].message.content}
