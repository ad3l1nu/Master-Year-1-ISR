# Echo Server - Documentație

## Descriere Proiect

Acest proiect implementează un sistem client-server bazat pe socket-uri TCP. Serverul acceptă conexiuni multiple de la clienți și răspunde cu aceleași mesaje primite (echo). Proiectul demonstrează conceptele de bază ale programării distribuite: comunicarea TCP/IP, multithreading și protocoale personalizate.

---

## Structura Proiectului

```
DS_P1/
├── echo_server_multi.py      # Server multithr-thread care acceptă mai mulți clienți
├── echo_client_improved.py   # Client simplu pentru testare
├── echo_client_multi.py       # Client avansat cu interfață interactivă
└── echo_protocol.py           # Protocol personalizat de comunicare
```

---

## Componente

### 1. **echo_protocol.py**
Definește protocolul de comunicare dintre client și server.

**Caracteristici:**
- `PORT = 5000` - Portul pe care se comunică
- `MSG_DELIM = '\0'` - Delimitator de mesaje (caracter null)
- `BUFFER_SIZE = 1024` - Dimensiunea buffer-ului de recepție

**Clasa SocketWrapper:**
- Wrapper peste socket-ul brut pentru gestionarea trimiterii și primirii de mesaje
- **`send_msg(msg)`** - Trimite un mesaj cu delimitator
- **`recv_msg()`** - Primește un mesaj complet
- **`has_buffered_msg()`** - Verifică dacă sunt mesaje în buffer
- Gestionează automaticamente mesajele fragmentate sau multiple în buffer

---

### 2. **echo_server_multi.py**
Server TCP care ascultă pe portul 5000 și gestionează mai mulți clienți simultan.

**Caracteristici:**
- Acceptă conexiuni de la mai mulți clienți
- Creează un thread separat pentru fiecare client
- Utilizează `SO_REUSEADDR` pentru a permite reluarea portului
- Echitează (returnează) fiecare mesaj primit

**Flux de execuție:**
1. Creează socket TCP și se leagă de 127.0.0.1:5000
2. Intră în buclă infinită de așteptare a conexiunilor
3. Pentru fiecare client acceptat, creează un thread daemon
4. Thread-ul citește mesaje și le returnează înapoi (echo)

---

### 3. **echo_client_improved.py**
Client simplu care testează comunicarea cu serverul.

**Caracteristici:**
- Conectare la server
- Trimiterea și primirea de mesaje
- Demonstrație de trimiterea multiplelor mesaje

**Flux:**
1. Se conectează la server (127.0.0.1:5000)
2. Trimite 3 mesaje ("Hello there!", "Some more", "messages")
3. Primește și afișează răspunsurile
4. Închide conexiunea

---

### 4. **echo_client_multi.py** (Versiunea Avansat)
Client interactiv cu interfață CLI și gestionare de erori.

**Caracteristici:**
- Interfață interactivă cu prompt `> `
- Timeout de 5 secunde pentru conexiune
- Gestionare de erori: server oprit, conexiune pierdută
- Comandă `exit` pentru a încheia
- Mesaje de informare utilizator în limba română

**Flux:**
1. Conectare cu timeout la server
2. Citire input utilizator în buclă
3. Trimitere mesaj și așteptare răspuns
4. Gestionare situații de eroare

---

## Cum se Folosește

### Pornirea Serverului

```bash
cd DS_P1
python3 echo_server_multi.py
```

**Output așteptat:**
```
Welcome to Echo Server!
Ready to accept a client connection.
```

### Rularea Clientului (într-un alt terminal)

#### Opțiunea 1: Client Simplu
```bash
python3 echo_client_improved.py
```

#### Opțiunea 2: Client Interactiv
```bash
python3 echo_client_multi.py
```

Apoi scrie mesaje și apasă Enter. Scrie `exit` pentru a ieși.

---

## Exemple de Utilizare

### Client Simplu (echo_client_improved.py)
```
Welcome to Echo Client!
received: Hello there!
received: Some more
received: messages
```

### Client Avansat (echo_client_multi.py)
```
--- Echo Client Pro v1.0 ---
Conectat cu succes la 127.0.0.1:5000
Scrie mesajul tau (sau 'exit' pentru a inchide):
> salut
Serverul a raspuns: salut
> test socket
Serverul a raspuns: test socket
> exit
Conexiune inchisa. La revedere!
```

---

## Concepte Demonstrate

1. **Socket-uri TCP** - Comunicarea în rețea între client și server
2. **Multithreading** - Gestionarea multiplilor clienți simultan
3. **Protocol Personalizat** - Implementarea unui protocol de mesaje cu delimitator
4. **Gestionare Buffer** - Tratarea mesajelor fragmentate sau aggregate
5. **Gestionare Erori** - Tratarea cazurilor de eroroare (timeout, conexiune pierdută)
6. **Opțiuni Socket** - Utilizarea `SO_REUSEADDR` pentru reutilizarea portului

---

## Probleme și Soluții

### Eroare: "Address already in use"
**Cauză:** Port-ul este deja ocupat de o instanță anterioară  
**Soluție:** Server-ul utilizează `SO_REUSEADDR` pentru a permite reutilizarea. Dacă persistă, așteptați 30-60 de secunde sau schimbați portul.

### Eroare: "Connection refused"
**Cauză:** Server-ul nu rulează  
**Soluție:** Porniți mai întâi serverul în alt terminal

### Timeout în client
**Cauză:** Server-ul nu răspunde în timp  
**Soluție:** Utilizați client-ul avansat care are gestionare timeout (5 secunde)

---

## Note Tehnice

- **IP:** 127.0.0.1 (localhost) - Comunicare pe aceeași mașină
- **Protocol:** TCP (Transmission Control Protocol) - Comunicare fiabilă
- **Thread-uri Daemon:** Server-ul folosește thread-uri daemon pentru ca procesul să poată fi oprit cu Ctrl+C
- **Encoding:** UTF-8 pentru mesaje text
- **Delimitator:** `\0` (null byte) pentru a marca sfârșitul mesajelor

---

## Concluzii

Acest proiect este o introducere practică în programarea distribuită cu Python, demonstrând interacțiunile client-server și gestionarea concurenței prin thread-uri.
