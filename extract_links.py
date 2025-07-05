import os
import re
from pathlib import Path
from pypdf import PdfReader

def extract_links_from_pdfs():
    """Extract links from all PDFs in the documents folder"""
    documents_path = Path("data/documents")
    
    if not documents_path.exists():
        print("❌ Documents folder not found")
        return
    
    all_links = []
    
    for pdf_file in documents_path.glob("*.pdf"):
        print(f"\n📄 Processing: {pdf_file.name}")
        try:
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            # Find URLs in the text
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            links = re.findall(url_pattern, text)
            
            if links:
                print(f"🔗 Found {len(links)} links:")
                for i, link in enumerate(links, 1):
                    print(f"  {i}. {link}")
                    all_links.append({
                        'file': pdf_file.name,
                        'link': link
                    })
            else:
                print("  No links found")
                
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"Total links found: {len(all_links)}")
    print(f"Files with links: {len(set(item['file'] for item in all_links))}")
    
    return all_links

if __name__ == "__main__":
    print("🔍 Extracting links from PDF documents...")
    links = extract_links_from_pdfs()
    
    if links:
        print(f"\n💡 Recommendation:")
        print("Consider manually saving important linked content as PDFs")
        print("and adding them to the data/documents/ folder for better AI coverage.") 