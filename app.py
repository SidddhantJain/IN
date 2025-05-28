import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import create_table, add_item, get_inventory, update_item, delete_item

# Initialize database
create_table()

st.title("Inventory Management System")

# --- Add Item Form ---
with st.form("Add Item"):
    st.subheader("Add New Inventory Item")
    model = st.text_input("Model")
    purchased_qty = st.number_input("Purchased Qty", min_value=0)
    received_qty = st.number_input("Received Qty", min_value=0)
    client_orders = st.number_input("Client Orders", min_value=0)
    dispatched_qty = st.number_input("Dispatched Qty", min_value=0)
    submitted = st.form_submit_button("Add Item")
    if submitted:
        add_item(model, purchased_qty, received_qty, client_orders, dispatched_qty)
        st.success(f"{model} added to inventory!")

# --- Display Inventory ---
st.subheader("Current Inventory")
inventory_data = get_inventory()

if inventory_data:
    inventory_df = pd.DataFrame(inventory_data, columns=["ID", "Model", "Purchased Qty", "Received Qty", "Client Orders", "Dispatched Qty"])
    st.dataframe(inventory_df)

    selected_id = st.selectbox("Select Item ID to Edit or Delete", inventory_df["ID"])

    # --- Delete ---
    if st.button("Delete Item"):
        delete_item(selected_id)
        st.success("Item deleted successfully!")

    # --- Edit ---
    with st.expander("Edit Selected Item"):
        item = inventory_df[inventory_df["ID"] == selected_id].iloc[0]
        new_model = st.text_input("Model", item["Model"])
        new_purchased = st.number_input("Purchased Qty", value=int(item["Purchased Qty"]), min_value=0)
        new_received = st.number_input("Received Qty", value=int(item["Received Qty"]), min_value=0)
        new_orders = st.number_input("Client Orders", value=int(item["Client Orders"]), min_value=0)
        new_dispatched = st.number_input("Dispatched Qty", value=int(item["Dispatched Qty"]), min_value=0)
        if st.button("Update Item"):
            update_item(selected_id, new_model, new_purchased, new_received, new_orders, new_dispatched)
            st.success("Item updated successfully!")

# --- Visualizations ---
if inventory_data:
    st.subheader("Inventory Visualizations")
    inventory_df["Stock Balance"] = inventory_df["Received Qty"] - inventory_df["Dispatched Qty"]
    inventory_df["Status"] = inventory_df["Stock Balance"].apply(
        lambda x: "In Stock" if x >= 100 else "Low Stock" if x > 0 else "Out of Stock"
    )

    # Bar chart
    st.write("### Stock Balance by Model")
    fig1, ax1 = plt.subplots()
    ax1.bar(inventory_df["Model"], inventory_df["Stock Balance"], color="skyblue")
    ax1.set_xlabel("Model")
    ax1.set_ylabel("Stock Balance")
    ax1.set_title("Stock Balance by Model")
    st.pyplot(fig1)

    # Pie chart
    st.write("### Inventory Status Distribution")
    fig2, ax2 = plt.subplots()
    status_counts = inventory_df["Status"].value_counts()
    ax2.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=90)
    ax2.set_title("Inventory Status")
    st.pyplot(fig2)
else:
    st.info("No inventory data available. Add some items first.")
