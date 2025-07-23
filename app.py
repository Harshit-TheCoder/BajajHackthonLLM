from LLMS.Edelweiss import conversational_rag_chain as edelweiss_rag_chain
from LLMS.HDFC import conversational_rag_chain as hdfc_rag_chain
from LLMS.LIC import conversational_rag_chain as lic_rag_chain
# from LLMS.KOTAK import conversational_rag_chain as kotak_rag_chain
from LLMS.StarHealth import conversational_rag_chain as starhealth_rag_chain
from LLMS.Bajaj import conversational_rag_chain as bajaj_rag_chain

company_rag_chains = {
    "edelweiss" : edelweiss_rag_chain,
    "hdfc" : hdfc_rag_chain,
    "lic" : lic_rag_chain,
    # "kotak" : kotak_rag_chain,
    "starhealth" : starhealth_rag_chain,
    "bajaj" : bajaj_rag_chain
}

def get_target_chain():
    company_input = input("Enter the insurance company (Edelweiss, HDFC, LIC, KOTAK, StarHealth, Bajaj or 'any') ").strip().lower()
    target_chain = []
    if company_input == "any":
        for company_key in company_rag_chains:
            target_chain.append(company_rag_chains[company_key])
    else:
        target_chain.append(company_rag_chains[company_input])
    return target_chain
        

print("Welcome to Insurance Q&A Chatbot")
while True:
    target_chain = get_target_chain()
    SESSION_ID = "default_session"
    if len(target_chain) > 0:
        while True:
            question = input("\nYou: ")
            if question.lower() == "exit":
                break
            final_response = []
            for target in target_chain:
                response = target.invoke(
                    {"input": question},
                    config={"configurable": {"session_id": SESSION_ID}}
                )
                final_response.append(response)
            
            print("Assistant:", response['answer'])
            print("\nWould you like to ask questions related to a specific company? or exit? Then Type 'exit' ")
    else:
        while True:
            question = input("\nYou: ")
            if question.lower() == "exit":
                break
            response = target_chain.invoke(
                {"input": question},
                config={"configurable": {"session_id": SESSION_ID}}
            )
            print("Assistant:", response['answer'])

        print("\nWould you like to ask questions for another company or for all companies in general or exit? Then Type 'exit' ")

