from google import genai # Note the change in import
from app.core.config import settings
import json
import datetime

# Initialize the client with your API key
client = genai.Client(api_key=settings.GEMINI_API_KEY)


def classify_with_gemini(signals: dict):
    prompt = f"""
    Analyze these website signals for phishing risk:
    {json.dumps(signals, indent=2)}
    
    Return a JSON object with:
    - decision: "SAFE", "SUSPICIOUS", or "PHISHING"
    - confidence: "LOW", "MEDIUM", or "HIGH"
    - reasoning: A brief explanation.
    
    Return ONLY the raw JSON.
    """
    
    try:
        # Use the client to generate content with the correct model name
        response = client.models.generate_content(
            model="gemini-2.5-flash",  
            contents=prompt
        )
        
        # Clean the response text in case the LLM adds markdown backticks
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
        
    except Exception as e:
        return {
            "decision": "UNKNOWN",
            "confidence": "LOW",
            "reasoning": f"AI Analysis Failed: {str(e)}"
        }
