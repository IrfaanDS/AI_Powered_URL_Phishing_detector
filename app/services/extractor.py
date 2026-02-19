import whois
import dns.resolver
import tldextract
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

def extract_all_signals(url: str):
    signals = {}
    
    # 1. Domain Extraction
    try:
        ext = tldextract.extract(url)
        domain = f"{ext.domain}.{ext.suffix}"
        signals['domain'] = domain
    except Exception as e:
        signals['domain_error'] = str(e)
        domain = None

    if domain:
        # 2. WHOIS
        try:
            w = whois.whois(domain)
            signals['creation_date'] = str(w.creation_date)
            signals['registrar'] = w.registrar
        except Exception as e:
            signals['whois_error'] = str(e)

        # 3. DNS
        try:
            signals['dns_a'] = [r.to_text() for r in dns.resolver.resolve(domain, 'A')]
        except Exception:
            signals['dns_a'] = []
            
        try:
            signals['dns_mx'] = [r.to_text() for r in dns.resolver.resolve(domain, 'MX')]
        except Exception:
            signals['dns_mx'] = []
            
        try:
            signals['dns_ns'] = [r.to_text() for r in dns.resolver.resolve(domain, 'NS')]
        except Exception:
            signals['dns_ns'] = []

    # 4. Content Scraping
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        signals['title'] = soup.title.string if soup.title else "No Title"
        signals['text_content'] = soup.get_text()[:1000] # First 1000 chars
    except Exception as e:
        signals['scraping_error'] = str(e)

    return signals
