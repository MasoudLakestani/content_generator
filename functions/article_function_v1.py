import os
from typing import List, Optional
from openai import OpenAI
from .scraper import scrape_result
from .google_urls import search
from settings import config
from tokencost import calculate_completion_cost, calculate_prompt_cost, count_string_tokens

API_KEY = config['openai']['API_KEY']
model = "gpt-4o-2024-05-13"

def check_information(client, value):
    check_information_prompt = [
            {
                "role": "user",
                "content": f"Do you have any information about exact {value}? Just say yes or no. not nothing else"
            } 
        ]
    
    have_information = client.chat.completions.create(
        messages=check_information_prompt,
        model=model
    )
    information_completions = have_information.choices[0].message.content
    information_prompt_cost = calculate_prompt_cost(check_information_prompt, model)
    information_completions_cost = calculate_completion_cost(information_completions, model)
    information_cost = information_prompt_cost + information_completions_cost
    return information_completions.lower().replace(".", ""), information_cost

def create_article_v1(subject: str, keywords: Optional[List[str]], tone:int=1, brand_name:str=None):

    tone_dict = {
        1:"Use an informative tone for writing this article.",
        2:"Use an informative tone for writing this article.",
        3:"Use an informative tone for writing this article.",
        4:"Use a persuasive tone to write this article."
    }

    brand = None
    if brand_name:
        brand = f"Incorporate the brand name {brand_name} throughout the article to strategically promote and introduce the brand. "
        f"Note that {brand_name}' may not be the manufacturer but merely the seller or distributor; ensure the article."

    client = OpenAI(api_key=API_KEY)
    article = subject + "\n"

    used_information = ""
    retrieved_information = ""
    check = check_information(client, subject)[0][:2]
    check_cost = check_information(client, subject)[1]

    if check == "no":
        scrape_url = search(subject)
        counter = 0
        for url in scrape_url:
            google_information = scrape_result([url])
            if google_information[1] == 200:
                retrieved_information += google_information[0]
                counter += 1
            if counter >= 2:
                break

        used_information = (
            f"Use only the information provided: {retrieved_information}. Do not use your information."
                )

    main_text_prompt = [
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
                    f"Compose a detailed and engaging main body for an article about {subject}, "
                    f"ensuring it is devoid of any spelling or grammatical errors. {brand}. {used_information}"
                    "Find an attractive heading and begin with a paragraph "
                    f"about that heading. Then use these keywords: {', '.join(keywords)} as headings throughout "
                    f"the article, but only where they naturally fit the content. Ensure that the "
                    "keywords may include a question. Answer the question and utilize these as headings. "
                    "Exercise caution when incorporating question-based keywords into your article. It is crucial to use them in a manner that maintains the semantic integrity of the article. Ensure that these keywords blend seamlessly into the content, supporting and enhancing the overall structure without disrupting the flow or coherence of the text. "
                    "Should there be fewer than three suitable headings, draw upon your expertise to create "
                    "additional appropriate headings. The article must contain at least 800 words and be "
                    "written in Persian. Focus exclusively on delivering the main content without including "
                    "any introductory or concluding elements. Specifically, avoid any summarizing paragraphs "
                    f"or statements like 'نتیجه گیری' or 'جمع بندی' that could be interpreted as conclusions, "
                    f"ensuring the text consists only of substantive content without any introduction and "
                    f"conclusion. {tone_dict[tone]}"
                )
            }
        ]

    main_text = client.chat.completions.create(
        messages=main_text_prompt,
        model=model,
        temperature=0.7,
        max_tokens=2000,
    )
    main_text_completions = main_text.choices[0].message.content
    main_text_prompt_cost = calculate_prompt_cost(main_text_prompt, model)
    main_text_completions_cost = calculate_completion_cost(main_text_completions, model)
    main_text_cost = main_text_prompt_cost + main_text_completions_cost

    introduction_prompt = [
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
                    f"Generate an introduction for the provided main text. Main text: {main_text_completions}. "
                    "Avoid duplication in the introduction and main text. Use the word 'مفدمه' at the start of the introduction."
                )
            }
        ]
    introduction = client.chat.completions.create(
        messages=introduction_prompt,
        model=model,
        temperature=0.7,
        max_tokens=800,
    )
    introduction_completions = introduction.choices[0].message.content
    introduction_prompt_cost = calculate_prompt_cost(introduction_prompt, model)
    introduction_completions_cost = calculate_completion_cost(introduction_completions, model)
    introduction_cost = introduction_prompt_cost + introduction_completions_cost

    article = introduction_completions + "\n" + main_text_completions + "\n"


    conclusion_prompt = [
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
        ]
    conclusion = client.chat.completions.create(
        messages=conclusion_prompt,
        model=model,
        temperature=0.7,
        max_tokens=800,
    )
    conclusion_completions = conclusion.choices[0].message.content
    conclusion_prompt_cost = calculate_prompt_cost(conclusion_prompt, model)
    conclusion_completions_cost = calculate_completion_cost(conclusion_completions, model)
    conclusion_cost = conclusion_prompt_cost + conclusion_completions_cost

    article += conclusion_completions

    edit_prompt = [
            {
                "role": "system",
                "content": (
                    "You are assigned the role of a text editor. I will provide you with an article. "
                    "Your tasks include correcting any spelling or grammatical errors and removing any "
                    "duplicate content. This process involves identifying and removing any duplicate "
                    "sections within the document, such as multiple conclusions ('نتیجه گیری', ''). It also "
                    "ensures that the article is free from redundant information and avoids "
                    "repetitiveness across different parts of the content. Please use HTML <h2> tags to "
                    "designate section headings, and <p> tags for paragraphs to structure the document "
                    "appropriately. Use the <b> tag to embolden any of the following keywords in the "
                    f"article: {', '.join(keywords)}. Please note that you should not bold the words when they "
                    "appear in headings. Additionally, you should eliminate all unnecessary white spaces "
                    "and delete all blank lines to ensure the content is optimized for web presentation. "
                    "Ensure that the text is clear, concise, and well-organized to enhance readability "
                    "and SEO performance."
                )
            },
            {
                "role": "user",
                "content": f"Please edit and format the following article as specified: {article}"
            }
        ]


    edited_article = client.chat.completions.create(
        messages = edit_prompt ,
        model=model,
        temperature=0.7,
        max_tokens=3000,
    )
    edit_completions = edited_article.choices[0].message.content
    edit_prompt_cost = calculate_prompt_cost(edit_prompt, model)
    edit_completions_cost = calculate_completion_cost(edit_completions, model)
    edit_cost = edit_prompt_cost + edit_completions_cost

    cost = check_cost + main_text_cost + introduction_cost + conclusion_cost + edit_cost

    return {
        "article":edit_completions,
        "cost": float(cost)
        }
