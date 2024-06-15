import os
from typing import List, Optional
from openai import OpenAI
from .scraper import scrape_result
from .google_urls import search
from settings import config

API_KEY = config['openai']['API_KEY']

def create_article_v2(subject: str, keywords: Optional[List[str]]):

    client = OpenAI(api_key=API_KEY)

    have_information = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Do you have any information about {subject}? Just say yes or no."
            }
        ],
        model="gpt-4o-2024-05-13",
    )

    no_information = "متاسفانه در مورد موضوع مورد نظر اطلاعی در دست نیست"
    if have_information.choices[0].message.content.lower().replace(".", "") == "no":
        return no_information

    main_text = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a blog writer assistant specialized in generating long, "
                    "SEO-optimized blog posts in Persian. Your task is to help users create "
                    "article text that is engaging, comprehensive, and rich in keywords to "
                    "enhance search engine visibility. Please submit the text you want formatted "
                    "for your HTML article. Ensure your submission includes potential headings, "
                    "and note that the final format will correct any spelling or grammatical "
                    "errors, apply HTML <h3> tags to headings."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Compose a detailed and engaging article about {subject}, ensuring it "
                    "is devoid of any spelling or grammatical errors. Begin with an attractive "
                    "heading followed by an introductory paragraph under the 'مقدمه' heading. "
                    f"Use the provided keywords: {keywords} as headings throughout the article, "
                    "but only where they can be used appropriately. If you lack information about "
                    "a keyword, ignore it. Should there be fewer than five suitable headings, "
                    "create additional appropriate headings based on your expertise. Each paragraph"
                    "must contain at least 300 word and the article must contain at least 1000 words"
                    "and be written in Persian. Conclude with a comprehensive summary under the "
                    "'نتیجه گیری' heading. Ensure the article is informative and uses a formal tone."
                )
            }
        ],
        model="gpt-4o-2024-05-13",
        temperature=0.7,
        max_tokens=3500,
    )

    article = main_text.choices[0].message.content

    return article
