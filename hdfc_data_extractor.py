import os
import json
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="Gemma2-9b-It")
parser = StrOutputParser()

# Prompt Template to extract only preamble
preamble_prompt = PromptTemplate.from_template("""
You are a policy parser. From the given policy document content, extract all the **Standard Definitions** section.

Return a JSON in the following format:
{{
  "Standard Definitions": "<definitions text here>"
}}

If definitions is not found, return:
{{ "Standard Definitions": "" }}

Only return valid JSON and nothing else.

CONTENT:
--------
{content}
""")

# Paths
pdf_root = "documents/HDFC"
output_json_path = "structured_standard_definitions.json"

# Final aggregated results
results = []

# Walk through subfolders and files
for root, dirs, files in os.walk(pdf_root):
    for file in files:
        if file.endswith(".pdf"):
            pdf_path = os.path.join(root, file)
            print(f"Processing: {pdf_path}")

            try:
                # Load PDF
                loader = PyMuPDFLoader(pdf_path)
                pages = loader.load()
                text = "\n\n".join([p.page_content for p in pages])

                # Split content into chunks (just to avoid large inputs)
                splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
                chunks = splitter.split_text(text)
                doc_text = chunks[0]

                # Run prompt
                prompt = preamble_prompt.format(content=doc_text[:2000])
                response_str = (llm | parser).invoke(prompt)
                response_json = json.loads(response_str)

                # Build record
                policy_data = {
                    "policy_name": file.replace(".pdf", "").replace("_", " ").replace("-", " ").title(),
                    "policy_type": os.path.basename(root),
                    "definitions": response_json.get("Standard Definitions", "")
                }

                results.append(policy_data)
                print(f"✅ Extracted preamble from: {file}")

            except Exception as e:
                print(f"❌ Failed for {file}: {e}")
                continue

# Save all results to a single JSON file
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n🎯 All preambles saved to: {output_json_path}")
