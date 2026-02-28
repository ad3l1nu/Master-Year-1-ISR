# AI Movie Assistant
### Asistentul Inteligent pentru Pasionații de Filme

---

## 1. Descrierea Aplicației
AI Movie Assistant este o aplicație desktop modernă care rezolvă problema alegerii unui film. Spre deosebire de o simplă căutare pe Google, această aplicație integrează Inteligența Artificială (Google Gemini) pentru a înțelege preferințele utilizatorului și baze de date globale (TMDB) pentru a oferi informații verificate în timp real.

Aplicația oferă un sistem de conturi securizat în Cloud (Firebase), permițând utilizatorilor să își salveze istoricul conversațiilor și să reia discuțiile de unde au rămas.

### Principalele Funcționalități:
1.  **Recomandări AI Conversaționale:** Poți discuta cu asistentul virtual (ex: "Vreau un film psihologic din anii 90 similar cu Seven"), iar acesta va înțelege contextul.
2.  **Date în Timp Real:** Preia automat postere, note (rating), anul lansării și descrieri oficiale folosind un API public.
3.  **Istoric Cloud:** Salvează automat conversația în baza de date online (Google Firestore) pentru utilizatorii autentificați.
4.  **Autentificare Securizată:** Sistem de Login / Înregistrare / Mod Oaspete.

---

## 2. Arhitectura Tehnică
Acest proiect demonstrează competențe de integrare a sistemelor distribuite:

* **Limbaj de programare:** Python 3.10+
* **Interfață Grafică (GUI):** PyQt6
* **Componentă Cloud (Back-end as a Service):**
    * **Google Firebase Authentication:** Gestionarea utilizatorilor.
    * **Google Firestore:** Bază de date NoSQL pentru stocarea istoricului de chat.
* **Web Services & API:**
    * **TMDB API (The Movie Database):** Sursă de date pentru filme (REST API).
    * **Google Gemini API:** LLM pentru procesarea limbajului natural.

---

## 3. Ghid de Instalare

### Pasul 1: Cerințe preliminare
Asigurați-vă că aveți instalat Python (versiunea 3.8 sau mai nouă).

### Pasul 2: Structura fișierelor
Proiectul este organizat modular:
* `main.py` (Fișierul principal)
* `firebase_config.json` & `serviceAccountKey.json` (Configurări)
* Folderul `services/` (conține logica de business: Gemini, TMDB, Firebase)
* Folderul `ui/` (conține interfața grafică)

### Pasul 3: Instalarea dependențelor
Deschideți terminalul în folderul proiectului și rulați comanda:

```bash
pip install PyQt6 requests firebase-admin pyrebase4 google-generativeai google-cloud-firestore python-dotenv
```

### Pasul 4: Configurarea Variabilelor de Mediu (.env)

1. **Copiați fișierul template:**
   ```bash
   cp .env.example .env
   ```

2. **Editați `.env` și completați cu cheile voastre:**
   ```
   GEMINI_API_KEY=your_actual_gemini_key_here
   TMDB_API_KEY=your_actual_tmdb_key_here
   ```

#### Cum să obțineți cheile API:

**a) GEMINI_API_KEY:**
- Accesați: https://makersuite.google.com/app/apikey
- Creați o nouă API key
- Copiați-o în `.env`

**b) TMDB_API_KEY:**
- Accesați: https://www.themoviedb.org/settings/api
- Creați un cont și solicitați o API key
- Copiați-o în `.env`

### Pasul 5: Configurarea Firebase

1. **Creați un Firebase Project:**
   - Accesați: https://console.firebase.google.com/
   - Creați un nou proiect
   - Activați Authentication (Email/Password)
   - Activați Firestore Database

2. **Descarcați `serviceAccountKey.json`:**
   - În Firebase Console → Project Settings → Service Accounts
   - Generați o nouă cheie privată
   - Salvați-o în folderul proiectului ca `serviceAccountKey.json`

3. **Creați `firebase_config.json`:**
   - Copiați configurația din Firebase Console → Project Settings
   - Salvați-o ca `firebase_config.json`

**⚠️ IMPORTANT:** 
- Fișierele `firebase_config.json` și `serviceAccountKey.json` sunt în `.gitignore` și NU vor fi uploadate pe GitHub
- Sunt fișiere sensibile - nu le partajați cu alții!

### Pasul 6: Pornirea Aplicației
Rulați comanda:

```bash
python main.py
```

**Notă:** La prima rulare, aplicația va verifica existența variabilelor de mediu și va afișa o eroare dacă lipsesc cheile din `.env`.

---

## 4. Ghid de Utilizare

### A. Autentificare
La deschidere, aplicatia solicita autentificarea.
* Puteti crea un cont nou folosind un email si o parola.
* Puteti intra in modul "Oaspete" pentru o testare rapida (fara salvarea datelor in Cloud).

### B. Cautare si Chat
* In fereastra de chat, puteti scrie titlul unui film pentru a vedea detalii.
* Puteti cere recomandari complexe (ex: "Filme cu Brad Pitt de actiune").
* Aplicatia va afisa un card cu posterul filmului, descrierea si nota acestuia.

### C. Istoric Sincronizat
* Utilizatorii autentificați vor regăsi conversația anterioară la fiecare logare.
* Datele fiind încărcate din Firestore.
---

## 5. Intrebari Frecvente (Q&A)

**I: De ce sunt cheile API în `.env` și nu în cod?**
R: Siguranță. Fișierele `.env` sunt în `.gitignore` și nu se urcă pe GitHub. Dacă cheile erau în cod, ar fi exponerate publicului și cineva ar putea abuza de API-urile tale.

**I: Ce fac cu `.env.example`?**
R: Este un template pentru alți utilizatori care clonează repo-ul. Ei vor copia `.env.example` în `.env` și vor completa cu propriile chei.

**I: Cum comunica Python cu baza de date?**
R: Folosesc libraria `firebase-admin` (SDK oficial Google) si `pyrebase`. Datele sunt transmise securizat sub format JSON catre serverele Firestore.

**I: De ce s-au folosit doua API-uri (Gemini si TMDB)?**
R: Gemini este folosit pentru intelegerea limbajului natural (NLP) si intentia utilizatorului, in timp ce TMDB este sursa de date factuale (an, actori, imagini), eliminand riscul de "halucinatii" AI.

**I: Ce se intampla daca nu exista conexiune la internet?**
R: Fiind o aplicatie de tip Cloud Client care depinde de API-uri externe, functionalitatea va fi restrictionata. Interfata va ramane activa, dar nu va putea prelua date noi.

**I: Care este diferența între `.env` și `firebase_config.json`?**
R: `.env` conține cheile API simple (strings), în timp ce `firebase_config.json` este configurația proiectului Firebase. Ambele sunt sensibile și trebuie protejate.