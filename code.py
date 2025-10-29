import streamlit as st

# --- Ukázková data přímo v kódu ---
clients = [
    {"company_name": "Stavební s.r.o.", "discount": 0.10},
    {"company_name": "Developer a.s.", "discount": 0.05},
    {"company_name": "ABC Konstrukce", "discount": 0.15},
]

machines = [
    {"name": "Bagr CAT 320", "price_per_day": 1500, "available": True, "description": "Střední pásový bagr"},
    {"name": "Nakladač JCB 3CX", "price_per_day": 1200, "available": False, "description": "Kolový nakladač"},
    {"name": "Zhutňovač Wacker", "price_per_day": 600, "available": True, "description": "Zhutňovač zeminy"},
]

# --- Streamlit UI ---
st.title("Půjčovna stavebních strojů")

# Layout dvě kolony
col1, col2 = st.columns([2,3])

with col1:
    st.subheader("Formulář výpočtu půjčovného")
    # Dropdown pro klienty
    client_names = [c['company_name'] for c in clients]
    selected_client = st.selectbox("Vyberte klienta:", client_names)

    # Dropdown pro stroje (jen dostupné)
    machines_available = [m for m in machines if m['available']]
    machine_names = [m['name'] for m in machines_available]
    selected_machine = st.selectbox("Vyberte stroj:", machine_names)

    # Počet dní
    num_days = st.number_input("Počet dní:", min_value=1, max_value=365, value=1)

    # --- Výpočet ---
    if st.button("Vypočítat"):
        # najít data pro klienta a stroj
        discount = next(c['discount'] for c in clients if c['company_name'] == selected_client)
        price_per_day = next(m['price_per_day'] for m in machines if m['name'] == selected_machine)
        total = price_per_day * num_days * (1 - discount)

        st.success(f"Celková cena: {total:,.2f} Kč (sleva {discount*100:.0f}%)")

with col2:
    st.subheader("Seznam všech strojů")
    # Připravit data do tabulky
    table_data = [
        {
            "Název": m['name'],
            "Popis": m['description'],
            "Cena za den (Kč)": m['price_per_day'],
            "Dostupnost": "Ano" if m['available'] else "Ne"
        }
        for m in machines
    ]
    st.table(table_data)
