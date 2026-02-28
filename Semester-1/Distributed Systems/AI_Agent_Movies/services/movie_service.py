import requests
import os
from typing import Dict, Any, List

class MovieService:
    def __init__(self):
        self.api_key = os.environ.get("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"
        if not self.api_key:
             raise ValueError("Eroare: Cheia TMDB_API_KEY nu este setată.")

    def search_movie(self, query: str) -> List[Dict[str, Any]]:
        if not query:
            return []

        # Suport pentru multiple titluri separate de |
        if "|" in query:
            queries = [q.strip() for q in query.split("|")]
        else:
            queries = [query]

        all_results = []
        
        for q in queries:
            url = f"{self.base_url}/search/multi"
            params = {
                "api_key": self.api_key,
                "query": q,
                "language": "ro-RO",
                "page": 1,
                "include_adult": "false"
            }
            
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                raw_results = data.get("results", [])
                
                # Luăm doar primul rezultat relevant pentru fiecare titlu căutat
                for item in raw_results:
                    media_type = item.get('media_type')
                    if media_type in ['movie', 'tv']:
                        all_results.append(item)
                        break
                    elif media_type == 'person':
                        known_for = item.get('known_for', [])
                        for k in known_for:
                            if k.get('media_type') in ['movie', 'tv']:
                                all_results.append(k)
                        break

            except requests.exceptions.RequestException as e:
                print(f"Eroare TMDB pentru '{q}': {e}")
                continue

        return all_results

class MovieParser:
    """Formatează datele în HTML vizual"""
    
    @staticmethod
    def process_and_format_html(items: List[Dict[str, Any]]) -> str:
        if not items:
            return "<p><i>Nu am găsit niciun film sau serial potrivit.</i></p>"

        # Eliminăm duplicatele
        seen = set()
        unique_items = []
        for x in items:
            if x['id'] not in seen:
                unique_items.append(x)
                seen.add(x['id'])

        top_items = unique_items[:5]
        html_out = f"<p>🔍 Iată ce am găsit:</p>"
        
        for item in top_items:
            title = item.get('title') or item.get('name') or 'Titlu Necunoscut'
            date_str = item.get('release_date') or item.get('first_air_date')
            year = date_str[:4] if date_str else 'N/A'
            rating = item.get('vote_average', 0)
            m_type = "📺 Serial" if item.get('media_type') == 'tv' else "🎬 Film"
            overview = item.get('overview', 'Fără descriere în limba română.')
            if not overview: overview = "Descriere indisponibilă."

            # Imaginea cu Placeholder
            poster_path = item.get('poster_path')
            if poster_path:
                img_url = f"https://image.tmdb.org/t/p/w200{poster_path}"
            else:
                img_url = "https://via.placeholder.com/100x150/444654/FFFFFF?text=No+Image"

            img_td = f"<td width='110' valign='top'><img src='{img_url}' width='100' style='border-radius:6px;'></td>"

            card = f"""
            <br>
            <div style="background-color: #2b2c36; border: 1px solid #444; border-radius: 8px; padding: 10px;">
                <table width="100%" border="0" cellspacing="0" cellpadding="5">
                    <tr>
                        {img_td}
                        <td valign="top">
                            <div style="font-size: 10px; color: #aaa;">{m_type}</div>
                            <h3 style="margin: 2px 0 5px 0; color: #4facfe; font-size: 16px;">{title}</h3>
                            <div style="color: #ddd; font-size: 12px; margin-bottom: 8px;">
                                📅 {year} &nbsp; ⭐ {rating:.1f}
                            </div>
                            <div style="font-size: 13px; color: #eee; line-height: 1.4;">
                                {overview}
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
            """
            html_out += card
            
        return html_out