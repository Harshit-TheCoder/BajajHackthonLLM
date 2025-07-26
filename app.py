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
import google.generativeai as genai
from LLMS.PolicyNames.bajaj_policy_names import bajaj_policy
from LLMS.PolicyNames.edelweiss_policy_names import edelweiss_policy
from LLMS.PolicyNames.hdfc_policy_names import hdfc_policy
from LLMS.PolicyNames.kotak_policy_names import kotak_policy
from LLMS.PolicyNames.lic_policy_names import lic_policy
from LLMS.PolicyNames.starhealth_policy_names import starhealth_policy
# from googleapiclient import discovery
# import json
from dotenv import load_dotenv
load_dotenv()
import os

company_rag_chains = {
    "edelweiss" : edelweiss_rag_chain,
    "hdfc" : hdfc_rag_chain,
    "lic" : lic_rag_chain,
    "kotak" : kotak_rag_chain,
    "starhealth" : starhealth_rag_chain,
    "bajaj" : bajaj_rag_chain
}

company_policy_names = {
    "edelweiss" : edelweiss_policy,
    "hdfc" : hdfc_policy,
    "lic" : lic_policy,
    "kotak" : kotak_policy,
    "starhealth" : starhealth_policy,
    "bajaj" : bajaj_policy
}

company_policy_keys = [
"edelweiss_policy",
"hdfc_policy",
"lic_policy",
"kotak_policy",
"starhealth_policy",
"bajaj_policy"
]

hdfc_policy_string = "\n".join(f"- {p}" for p in hdfc_policy)
edelweiss_policy_string = "\n".join(f"- {p}" for p in edelweiss_policy)
bajaj_policy_string = "\n".join(f"- {p}" for p in bajaj_policy)
lic_policy_string = "\n".join(f"- {p}" for p in lic_policy)
kotak_policy_string = "\n".join(f"- {p}" for p in kotak_policy)
starhealth_policy_string = "\n".join(f"- {p}" for p in starhealth_policy)
# API_KEY = os.getenv("PERSPECTIVE_AI_API_KEY")

# client = discovery.build(
#     "commentanalyzer",
#     "v1alpha1",
#     developerKey=API_KEY,
#     discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
#     static_discovery=False,
# )
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")
# response = model.generate_content("Explain insurance claim process for a knee surgery")

company_name = ""
def get_target_chain():
    company_input = input("Enter the insurance company (Edelweiss, HDFC, LIC, KOTAK, StarHealth, Bajaj or 'any') ").strip().lower()
    target_chain = []
    global company_name
    company_name = company_input
    if company_input == "any":
        for company_key in company_rag_chains:
            target_chain.append(company_rag_chains[company_key])
    elif company_input in company_rag_chains:
        target_chain.append(company_rag_chains[company_input])
    else:
        print("Invalid company name. Try again.")

    target_policy_names = []
    if company_input == "any":
        for company_key in company_policy_names:
            target_policy_names.append(company_policy_names[company_key])
    elif company_input in company_policy_names:
        target_policy_names.append(company_policy_names[company_input])
    else:
        print("Invalid company name")

    return target_chain, target_policy_names

def translate_text(text, src_lang, dest_lang):
    try:
        if not text or len(text) > 4900:
            print("Translation skipped: text too long or empty.")
            return text
        return GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
    except Exception as e:
        print("Translation error:", text, "-->", e)
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
    message_lower = str(message).lower()

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
    target_chain, target_policy_names = get_target_chain()
    SESSION_ID = "default_session"
    if len(target_chain) > 1:
        while True:
            question = input("\nYou: ")
            # question = str(TextBlob(question).correct()) ## corrected english 
            if question.strip().lower() == "exit":
                break
            # question = translate_text(question, src_lang=lang, dest_lang="english")
            if is_abusive(question):
                print("Assistant: Please be respectful. Let's keep this conversation helpful and professional.")
                continue

            # if is_vague(question):
            #     print("It seems your question is a bit vague or lacking in context. Can you describe your question properly")
            #     continue

            prompt = f"""
                You are an insurance query normalizer.
                Your task is to take a raw insurance query from a user and turn it into a clear, full English question with structured context.
                Raw input: "{question}"
                These are the policies covered by HDFC RAG LLM: "{hdfc_policy_string}"
                These are the policies covered by Edelweiss RAG LLM: "{edelweiss_policy_string}"
                These are the policies covered by Bajaj RAG LLM: "{bajaj_policy_string}"
                These are the policies covered by KOTAK RAG LLM: "{kotak_policy_string}"
                These are the policies covered by LIC RAG LLM: "{lic_policy_string}"
                These are the policies covered by Star Health RAG LLM: "{starhealth_policy_string}"
                Return a **rephrased natural language question** that includes:
                - Age (if available)
                - Gender (if available)
                - Medical procedure
                - Location
                - Policy duration (if mentioned)
                - Context (e.g., whether asking about coverage, claim approval, or payout)
                ⚠️ If the user is asking “what is” or “tell me about” a specific policy name, instruct the RAG LLM to look up and return that exact policy's details.
                ⚠️ Encourage the RAG LLM to **search all available policy names and return relevant matching policy names** that may cover the user’s context (age, condition, etc.)..
                Make sure the result is a single, complete sentence or paragraph understandable by a retrieval/LLM system.
            """

            response = model.generate_content(prompt)
            question = response.text.strip()
            print(question)

            final_response = []
            for i in range(len(target_chain)):
                company_key = list(company_rag_chains.keys())[i]  # e.g., "hdfc"
                policy_key = f"{company_key}_policy"

                response = target_chain[i].invoke(
                    {"input": question, policy_key: "\n".join(f"- {p}" for p in target_policy_names[i])},
                    config={"configurable": {"session_id": SESSION_ID}}
                )

                # response = translate_text(response, src_lang="english", dest_lang=lang)
                final_response.append(response)
            
            print("Assistant:", response['answer'])
            print("\nWould you like to exit or ask question for a specific company? Then Type 'exit' else enter the question in selected language")
    else:
        single_chain = target_chain[0]
        policy_list = target_policy_names[0]

        while True:
            question = input("\nYou: ")
            if question.strip().lower() == "exit":
                break
            if is_abusive(question):
                print("Assistant: Please be respectful. Let's keep this conversation helpful and professional.")
                continue
            # if is_vague(question):
            #     print("It seems your question is a bit vague or lacking in context. Can you describe your question properly")
            #     continue

            prompt = f"""
                You are an insurance query normalizer.
                Your task is to take a raw insurance query from a user and turn it into a clear, full English question with structured context.
                Raw input: "{question}"
                These are the policies covered by HDFC RAG LLM: "{hdfc_policy_string}"
                These are the policies covered by Edelweiss RAG LLM: "{edelweiss_policy_string}"
                These are the policies covered by Bajaj RAG LLM: "{bajaj_policy_string}"
                These are the policies covered by KOTAK RAG LLM: "{kotak_policy_string}"
                These are the policies covered by LIC RAG LLM: "{lic_policy_string}"
                These are the policies covered by Star Health RAG LLM: "{starhealth_policy_string}"
                Return a **rephrased natural language question** that includes:
                - Age (if available)
                - Gender (if available)
                - Medical procedure
                - Location
                - Policy duration (if mentioned)
                - Context (e.g., whether asking about coverage, claim approval, or payout)
                ⚠️ If the user is asking “what is” or “tell me about” a specific policy name, instruct the RAG LLM to look up and return that exact policy's details.
                ⚠️ Always instruct the LLM to return the response in **JSON format**.
                ⚠️ Encourage the RAG LLM to **search all available policy names and return relevant matching policy names** that may cover the user’s context (age, condition, etc.)..
                Make sure the result is a single, complete sentence or paragraph understandable by a retrieval/LLM system.
            """

            response = model.generate_content(prompt)
            question = response.text.strip()
            print(question)

            response = single_chain.invoke(
                {
                    "input": question,
                    f"{company_name}_policy": "\n".join(f"- {p}" for p in policy_list)
                },
                config={"configurable": {"session_id": SESSION_ID}}
            )

            print("Assistant:", response['answer'])

        print("\nWould you like to exit or change company? Then Type 'exit' else enter the question in selected language")
    
    choice = input("\nWould you like to exit?yes/no?")
    if(choice == "yes"): break

