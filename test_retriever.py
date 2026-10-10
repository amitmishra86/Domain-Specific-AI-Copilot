'''
from retriever import load_documents

documents = load_documents()

for name, text in documents.items():

    print(name)

    print(text)

    print("-" * 40)
    '''
from retriever import retrieve
while True:
    text=input("Enter your search..")
    if(text!='again'):
       # text=input("Enter your search again..")
        filename, content = retrieve(text)

        print(filename)

        print()

        print(content)
        continue
    else:
        break