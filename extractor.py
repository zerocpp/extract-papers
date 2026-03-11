import re
import csv
from pathlib import Path
from bs4 import BeautifulSoup

def extract_papers(html_file: str, output_csv: str):
    """Extract paper information from HTML and save to CSV."""
    
    # Read HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all paper divs
    papers = soup.find_all('div', class_='panel paper')
    
    papers_data = []
    
    for paper in papers:
        try:
            # Extract index
            index_span = paper.find('span', class_='index notranslate')
            index = index_span.text.strip('#') if index_span else None
            
            # Extract or_id and keywords from div
            or_id = paper.get('id', '').replace('@OpenReview', '')
            keywords = paper.get('keywords', '')
            or_url = f"https://openreview.net/forum?id={or_id}" if or_id else None
            
            # Extract title
            title_link = paper.find('a', {'id': f'title-{or_id}@OpenReview'})
            title = title_link.text if title_link else None
            
            # Extract PDF URL
            pdf_link = paper.find('a', {'id': f'pdf-{or_id}@OpenReview'})
            pdf_url = pdf_link.get('data') if pdf_link else None
            
            # Extract summary
            summary_p = paper.find('p', {'id': f'summary-{or_id}@OpenReview'})
            summary = summary_p.text if summary_p else None
            
            # Extract venue information
            venue_link = paper.find('a', class_='subject-1')
            venue = None
            year = None
            pub_type = None
            
            if venue_link:
                venue_text = venue_link.text
                match = re.match(r'(ICLR)\.(\d+)\s+-\s+(.+)', venue_text)
                if match:
                    venue, year, pub_type = match.groups()
            
            papers_data.append({
                'index': index,
                'or_id': or_id,
                'or_url': or_url,
                'keywords': keywords,
                'title': title,
                'pdf_url': pdf_url,
                'summary': summary,
                'venue': venue,
                'year': year,
                'type': pub_type
            })
        
        except Exception as e:
            print(f"Error parsing paper: {e}")
            continue
    
    # Write to CSV
    if papers_data:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['index', 'or_id', 'or_url', 'keywords', 'title', 'pdf_url', 'summary', 'venue', 'year', 'type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(papers_data)
        print(f"Extracted {len(papers_data)} papers to {output_csv}")

if __name__ == '__main__':
    extract_papers('data/ICLR.2026 | Cool Papers - Immersive Paper Discovery.html', 'output/iclr26_papers.csv')