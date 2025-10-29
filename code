import streamlit as st
import sqlite3

DB_PATH = 'rental.db'  # cesta k SQLite DB

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
