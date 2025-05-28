import streamlit as st
import pandas as pd
import numpy as np

# Initialize an empty DataFrame to store inventory data
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=["Model", "Purchased Qty", "Received Qty", "Client Orders", "Dispatched Qty", "Stock Balance", "Order Balance", "Status"])

# Function to calculate stock balance and status
def calculate_stock(row):
    stock_balance = row['Received Qty'] - row['Dispatched Qty']
    order_balance = row['Client Orders'] - row['Dispatched Qty']
    status = "In Stock" if stock_balance >= 100 else "Low Stock" if stock_balance > 0 else "Out of Stock"
    return pd.Series([stock_balance, order_balance, status])

# Streamlit app layout
st.title("Inventory Management System")

# Input form for adding new inventory items
with st.form(key='inventory_form'):
    model = st.text_input("Model", required=True)
    purchased_qty = st.number_input("Purchased Qty", min_value=0, required=True)
    received_qty = st.number_input("Received Qty", min_value=0, required=True)
    client_orders = st.number_input("Client Orders", min_value=0, required=True)
    dispatched_qty = st.number_input("Dispatched Qty", min_value=0, required=True)
    
    submit_button = st.form_submit_button("Add Item")

    if submit_button:
        new_item = {
            "Model": model,
            "Purchased Qty": purchased_qty,
            "Received Qty": received_qty,
            "Client Orders": client_orders,
            "Dispatched Qty": dispatched_qty,
        }
        st.session_state.inventory = st.session_state.inventory.append(new_item, ignore_index=True)
        st.success(f"Added {model} to inventory!")

# Calculate stock balance and status for each item
if not st.session_state.inventory.empty:
    st.session_state.inventory[["Stock Balance", "Order Balance", "Status"]] = st.session_state.inventory.apply(calculate_stock, axis=1)

# Display the inventory table
st.subheader("Current Inventory")
st.dataframe(st.session_state.inventory)

# Option to clear inventory
if st.button("Clear Inventory"):
    st.session_state.inventory = pd.DataFrame(columns=["Model", "Purchased Qty", "Received Qty", "Client Orders", "Dispatched Qty", "Stock Balance", "Order Balance", "Status"])
    st.success("Inventory cleared!")
