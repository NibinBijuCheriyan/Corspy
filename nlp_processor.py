import spacy

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

PIVOT_KEYWORDS = [
    "strategic pivot", "restructuring", "new vertical", "AI integration", 
    "generative AI", "market shift", "discontinue", "layoffs", "hiring freeze",
    "acquisition", "merger", "divestiture", "rebranding", "bankruptcy",
    "new product line", "R&D focus", "patent application", "executive change"
]

def calculate_pivot_score(text):
    """
    Calculates a 'pivot score' based on the presence of key terms and context.
    Returns a float between 0.0 and 1.0.
    """
    if not text:
        return 0.0
    
    doc = nlp(text.lower())
    score = 0.0
    
    # Keyword matching (basic implementation, could be enhanced with vector similarity)
    # We normalize score by length of text to avoid bias towards long documents,
    # but for now, let's just count occurrences and cap it.
    
    found_keywords = []
    for keyword in PIVOT_KEYWORDS:
        if keyword in text.lower():
            score += 0.2
            found_keywords.append(keyword)
    
    # Cap score at 1.0
    return min(score, 1.0)
