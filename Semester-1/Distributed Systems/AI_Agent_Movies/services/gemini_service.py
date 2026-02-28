import os
import json
import google.generativeai as genai
from typing import Dict, Any, Optional, Union

class GeminiService:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Eroare: Cheia API Gemini nu este setată.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')

    def interpret_user_request(self, user_prompt: str) -> Union[Dict[str, Any], str]:
        """Transformă cererea utilizatorului într-o căutare structurată."""
        
        system_instruction = """
        Ești un asistent expert în filme.
        
        REGULI STRICTE PENTRU CĂUTARE:
        Trebuie să returnezi STRICT un JSON în formatul: {"search_query": "..."}
        
        1. CĂUTARE EXACTĂ (Nume de film/actor):
           - Dacă userul scrie un nume greșit, corectează-l.
           - Ex: "brad pi" -> "Brad Pitt"
           
        2. CĂUTARE DUPĂ GEN, AN sau DESCRIERE (Recomandare):
           - Dacă userul cere "filme cu mașini", "comedii 2023", "filme de groază", NU returna genul.
           - Gândește-te la 3 cele mai relevante/populare titluri pentru acea descriere.
           - Returnează titlurile separate prin simbolul "|".
           - Ex User: "filme cu mașini" -> JSON: {"search_query": "Fast & Furious|Ford v Ferrari|Cars"}

        3. CONVERSAȚIE NORMALĂ:
           - Dacă userul spune "salut", "ce faci", răspunde text normal (fără JSON).
        """

        try:
            full_prompt = f"{system_instruction}\n\nUser: {user_prompt}"
            response = self.model.generate_content(full_prompt)
            text_response = response.text.strip()
            
            clean_text = text_response.replace("```json", "").replace("```", "").strip()

            if "{" in clean_text and "search_query" in clean_text:
                try:
                    data = json.loads(clean_text)
                    return data
                except json.JSONDecodeError:
                    pass
            
            return text_response
            
        except Exception as e:
            return f"Eroare Gemini: {e}"