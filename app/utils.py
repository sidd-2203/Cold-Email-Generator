import re

def clean_text(text):
    #Remove HTML Tags
    text=re.sub(r'<[^>]*?>','',text)
    
    #Remove Urls
    text=re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',text)
    
    #Remove special characters
    text=re.sub(r'[^a-zA-Z0-9]','',text)

    #Replace multiple spaces with a single space
    text=re.sub(r'\s{2,}','',text)
    
    #Trim leading and trailing whitespaces
    text=text.strip()
    #Remove extra whitespaces
    text=' '.join(text.split())
    return text

