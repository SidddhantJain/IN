import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import create_table, add_item, get_inventory, update_item, delete_item

# Initialize the database
create_table()

# App title
st.title("📦 Inventory Management System")

# Input form to add a new item
with st.form(key='inventory_form'):
    model = st.text_input("Model")
    purchased_qty = st.number_input("Purchased Qty", min_value=0)
    received_qty = st.number_input("Received Qty", min_value=0)
    client_orders = st.number_input("Client Orders", min_value=0)
    dispatched_qty = st.number_input("Dispatched Qty", min_value=0)

    submit_button = st.form_submit_button("Add Item")

    if submit_button:
        if not model:
            st.error("Model name is required.")
        else:
            add_item(model, purchased_qty, received_qty, client_orders, dispatched_qty)
            st.success(f"✅ Added '{model}' to inventory.")

# Show inventory table
st.subheader("📋 Current Inventory")
inventory_data = get_inventory()

if inventory_data:
    inventory_df = pd.DataFrame(inventory_data, columns=[
        "ID", "Model", "Purchased Qty", "Received Qty", "Client Orders", "Dispatched Qty"
    ])
    st.dataframe(inventory_df)

    # Select an item to edit or delete
    selected_id = st.selectbox("Select an Item ID to Edit or Delete", inventory_df["ID"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Delete Item"):
            delete_item(selected_id)
            st.success("Item deleted successfully!")
    with col2:
        if st.button("✏️ Edit Item"):
            item = inventory_df[inventory_df["ID"] == selected_id].iloc[0]
            with st.form(key='edit_form'):
                model = st.text_input("Model", value=item["Model"])
                purchased_qty = st.number_input("Purchased Qty", value=item["Purchased Qty"], min_value=0)
                received_qty = st.number_input("Received Qty", value=item["Received Qty"], min_value=0)
                client_orders = st.number_input("Client Orders", value=item["Client Orders"], min_value=0)
                dispatched_qty = st.number_input("Dispatched Qty", value=item["Dispatched Qty"], min_value=0)
                update_btn = st.form_submit_button("Update Item")
                if update_btn:
                    update_item(selected_id, model, purchased_qty, received_qty, client_orders, dispatched_qty)
                    st.success("Item updated successfully!")

    # Inventory Visualizations
    st.subheader("📊 Inventory Visualizations")
    inventory_df["Stock Balance"] = inventory_df["Received Qty"] - inventory_df["Dispatched Qty"]
    inventory_df["Status"] = inventory_df["Stock Balance"].apply(
        lambda x: "In Stock" if x >= 100 else "Low Stock" if x > 0 else "Out of Stock"
    )

    # Bar Chart: Stock Balance
    st.subheader("📦 Stock Balance by Model")
    plt.figure(figsize=(10, 4))
    plt.bar(inventory_df["Model"], inventory_df["Stock Balance"], color='skyblue')
    plt.xlabel("Model")
    plt.ylabel("Stock Balance")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

    # Pie Chart: Status Distribution
    st.subheader("📈 Inventory Status Distribution")
    status_counts = inventory_df["Status"].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title("Status Distribution")
    st.pyplot(plt)

else:
    st.info("No inventory data available. Add items to get started.")
