from LLMS.Edelweiss import conversational_rag_chain as edelweiss_rag_chain
from LLMS.HDFC import conversational_rag_chain as hdfc_rag_chain
from LLMS.LIC import conversational_rag_chain as lic_rag_chain
from LLMS.KOTAK import conversational_rag_chain as kotak_rag_chain
from LLMS.StarHealth import conversational_rag_chain as starhealth_rag_chain
from LLMS.Bajaj import conversational_rag_chain as bajaj_rag_chain
from textblob import TextBlob
from deep_translator import GoogleTranslator
from cuss_words import abusive_words
from vague_sentences import vague_words
from vague_sentences import vague_phrases
import re
# from googleapiclient import discovery
# import json
# from dotenv import load_dotenv
# load_dotenv()
# import os

company_rag_chains = {
    "edelweiss" : edelweiss_rag_chain,
    "hdfc" : hdfc_rag_chain,
    "lic" : lic_rag_chain,
    "kotak" : kotak_rag_chain,
    "starhealth" : starhealth_rag_chain,
    "bajaj" : bajaj_rag_chain
}

# API_KEY = os.getenv("PERSPECTIVE_AI_API_KEY")

# client = discovery.build(
#     "commentanalyzer",
#     "v1alpha1",
#     developerKey=API_KEY,
#     discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
#     static_discovery=False,
# )

def get_target_chain():
    company_input = input("Enter the insurance company (Edelweiss, HDFC, LIC, KOTAK, StarHealth, Bajaj or 'any') ").strip().lower()
    target_chain = []
    if company_input == "any":
        for company_key in company_rag_chains:
            target_chain.append(company_rag_chains[company_key])
    elif company_input in company_rag_chains:
        target_chain.append(company_rag_chains[company_input])
    else:
        print("Invalid company name. Try again.")
    return target_chain

def translate_text(text, src_lang, dest_lang):
    try:
        return GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
    except Exception as e:
        print("Translation error:", e)
        return text
        
def get_user_language():
    print("Please select your preferred language:")
    print("Examples: english, hindi, tamil, telugu, french, german, arabic, urdu, etc.")
    lang = input("Language: ").strip().lower()
    return lang

def is_abusive(message):
    message_words = message.lower().split()

    # Check if any abusive word is in the message
    for word in message_words:
        if word in abusive_words:
            return True
    return False

def is_vague(message):
    message_lower = message.lower()

    # Word match
    for word in vague_words:
        if re.search(r'\b' + re.escape(word) + r'\b', message_lower):
            return True

    # Phrase match
    for pattern in vague_phrases:
        if re.search(pattern, message_lower):
            return True

    return False

print("Welcome to Insurance Q&A Chatbot")
lang = get_user_language()

while True:
    target_chain = get_target_chain()
    SESSION_ID = "default_session"
    if len(target_chain) > 0:
        while True:
            question = input("\nYou: ")
            question = TextBlob(question).correct() ## corrected english 
            if question.lower() == "exit":
                break
            question = translate_text(question, src_lang=lang, dest_lang="english")
            if is_abusive(question):
                print("Assistant: Please be respectful. Let's keep this conversation helpful and professional.")
                continue

            if is_vague(question):
                print("It seems your question is a bit vague or lacking in context. Can you describe your question properly")
                continue

            final_response = []
            for target in target_chain:
                response = target.invoke(
                    {"input": question},
                    config={"configurable": {"session_id": SESSION_ID}}
                )
                response = translate_text(response, src_lang="english", dest_lang=lang)
                final_response.append(response)
            
            print("Assistant:", response['answer'])
            print("\nWould you like to exit? Then Type 'exit' else enter the question in selected language")
    else:
        while True:
            question = input("\nYou: ")
            question = TextBlob(question).correct() ## corrected english 
            if question.lower() == "exit":
                break
            question = translate_text(question, src_lang=lang, dest_lang="english")
            if is_abusive(question):
                print("Assistant: Please be respectful. Let's keep this conversation helpful and professional.")
                continue

            if is_vague(question):
                print("It seems your question is a bit vague or lacking in context. Can you describe your question properly")
                continue
            response = target_chain.invoke(
                {"input": question},
                config={"configurable": {"session_id": SESSION_ID}}
            )
            response = translate_text(response, src_lang="english", dest_lang=lang)
            print("Assistant:", response['answer'])

        print("\nWould you like to exit? Then Type 'exit' else enter the question in selected language")

