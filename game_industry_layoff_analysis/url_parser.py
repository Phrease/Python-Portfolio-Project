import spacy
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    """
    Fetches a URL and extracts the text content from paragraphs tags.

    Args:
         url (str): The URL of the article to scrape.

    Returns:
        str: The extracted content of the article, or None if fetching fails.
    """
    try:
        # Set a user-agent header to mimic a browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to fetch {url} (Status code: {response.status_code})")
            return None

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all paragraph tags and join their text
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])

        return article_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_layoffs_data(urls_to_process):
    """
    Parses a list of article texts to extract layoff data.
    (This function is the same as the one in the previous version)
    """
    nlp = spacy.load("en_core_web_sm")
    layoffs_keywords = ['layoff', 'laid off', 'lay offs', 'job cuts', 'cuts', 'workforce reduction', 'shut down', 'closure', 'affected',
                        'impacted', 'let go', 'streamline', 'restructuring', 'downsizing', 'exit', 'jobs list']
    all_extracted_data = []

    for url in urls_to_process:
        print(f"Processing: {url}")
        text = extract_text_from_url(url)

        if not text:
            print(f"--> Skipping URL due to fetch error or empty content. \n")
            continue

        doc = nlp(text)
        found_in_article = False

        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in layoffs_keywords):
                company, layoff_count, date = None, None, None

                # Attempt to find the most prominent company in the article
                doc_orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
                if doc_orgs:
                    for org in doc_orgs:
                        if len(org.strip()) > 3 and "Kotaku" not in org:
                            company = org.strip()
                            break
                    if not company: company = doc_orgs[0]

                # Refine search within the specific sentence
                for ent in sent.ents:
                    if ent.label_ == "ORG":
                        company = ent.text
                    if ent.label == "CARINDAL" and any(char.isdigit() for char in ent.text) and not layoff_count:
                        num_search = re.search(r'\d[\d,]*', ent.text)
                        if num_search:
                            layoff_count = int(num_search.group().replace(',', ''))
                    if ent.label_ == "DATE" and not date:
                        if not ent.text.isdigit() or len(ent.text) != 4:
                            date = ent.text

                if company:
                    layoff_value = layoff_count if layoff_count else "Review Manually"

                    all_extracted_data.append({
                        'Company': company,
                        'Layoffs': layoff_value,
                        'Date': date if date else "Not found",
                        'SourceURL': url,
                        'SourceText': sent.text.strip().replace('\n', ' ')
                    })
                    found_in_article = True
                    break # Success! Move to the next URL.

        if not found_in_article:
            print(f"--> No specific layoff sentence found in {url}.\n")
        else:
            print("--> Data extracted successfully.\n")

    return pd.DataFrame(all_extracted_data)

# Paste the full text of each article into this list.
# Each article should be enclosed in triple quotes
article_texts_to_process = [
    """
    placeholder
    """
]

# Run the main function
final_df = parse_layoffs_data(article_texts_to_process)

# Save and print the results
output_filename = "extracted_layoffs_from_text_final.csv"
final_df.to_csv(output_filename, index=False)

print(f"** Process Complete **")
print(f"Data extraction finished. Results saved to '{output_filename}'")
print("\n** Extracted Data **")
print(final_df)