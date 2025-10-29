import streamlit as st
import sqlite3
import os

DB_PATH = 'rental.db'  # cesta k SQLite DB

# --- Funkce pro inicializaci DB ---
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        # Vytvořit tabulky
        cur.execute('''CREATE TABLE clients (
            id INTEGER PRIMARY KEY,
            company_name TEXT,
            address TEXT,
            ico TEXT,
            discount REAL,
            contact_person TEXT
        )''')
        cur.execute('''CREATE TABLE machines (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            price_per_day REAL,
            available INTEGER
        )''')
        # Naplnit ukázkovými daty
        clients_data = [
            (1,"Stavební s.r.o.","Ulice 12, Město","12345678",0.10,"Jan Novák"),
            (2,"Developer a.s.","Projektová 5, Město","87654321",0.05,"Petra Malá"),
            (3,"ABC Konstrukce","Hlavní 1, Město","11223344",0.15,"Karel Doležal"),
        ]
        machines_data = [
            (1,"Bagr CAT 320","Střední pásový bagr",1500,1),
            (2,"Nakladač JCB 3CX","Kolový nakladač",1200,0),
            (3,"Zhutňovač Wacker","Zhutňovač zeminy",600,1),
        ]
        cur.executemany('INSERT INTO clients VALUES (?,?,?,?,?,?)', clients_data)
        cur.executemany('INSERT INTO machines VALUES (?,?,?,?,?)', machines_data)
        conn.commit()
        conn.close()

# --- Funkce pro načtení dat z DB ---
def load_clients():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT company_name, discount FROM clients ORDER BY company_name")
    clients = cur.fetchall()
    conn.close()
    return clients

def load_machines():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name, price_per_day, available FROM machines ORDER BY name")
    machines = cur.fetchall()
    conn.close()
    return machines

# --- Inicializace DB ---
init_db()

# --- Načtení dat ---
clients = load_clients()
machines = load_machines()

# --- Streamlit UI ---
st.title("Půjčovna stavebních strojů")

# Dropdown pro klienty
client_names = [c[0] for c in clients]
selected_client = st.selectbox("Vyberte klienta:", client_names)

# Dropdown pro stroje (jen dostupné)
machines_available = [m for m in machines if m[2] == 1]
machine_names = [m[0] for m in machines_available]
selected_machine = st.selectbox("Vyberte stroj:", machine_names)

# Počet dní
num_days = st.number_input("Počet dní:", min_value=1, max_value=365, value=1)

# --- Výpočet ---
if st.button("Vypočítat"):
    # najít data pro klienta a stroj
    discount = next((c[1] for c in clients if c[0] == selected_client), 0)
    price_per_day = next((m[1] for m in machines if m[0] == selected_machine), 0)
    total = price_per_day * num_days * (1 - discount)

    st.success(f"Celková cena: {total:,.2f} Kč (sleva {discount*100:.0f}%)")
