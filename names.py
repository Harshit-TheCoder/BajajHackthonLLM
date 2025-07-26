import os

folder_path = 'documents/StarHealth'

pdf_names = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.pdf'):
            name_without_ext = os.path.splitext(file)[0]
            pdf_names.append(name_without_ext)

print(pdf_names)
