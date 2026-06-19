# Source/app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from queries import SQLQueries

st.set_page_config(page_title="Food Wastage Management Platform", layout="wide", page_icon="🍲")

# Database Connection Engine Setup
DATABASE_URL = "postgresql://postgres:@localhost:5432/food_wastage"

@st.cache_resource
def get_db_engine():
    return create_engine(DATABASE_URL)

engine = get_db_engine()

def load_db_data(query, params=None):
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn, params=params)

# Sidebar Navigation Control
st.sidebar.title("🍲 Core Navigation")
page = st.sidebar.radio("Go to:", ["Dashboard & Filters", "Manage Listings (CRUD)", "Directory & Contact", "Analytical Queries"])

# ==========================================================
# PAGE 1: DASHBOARD & DYNAMIC FILTERS
# ==========================================================
if page == "Dashboard & Filters":
    st.title("📊 Food Donation Marketplace")
    st.subheader("Live Available and Filterable Surplus Inventory")

    # FIXED: Added double quotes around aliases so PostgreSQL preserves capital letters
    raw_listings = load_db_data("""
        SELECT f.*, p."Name" as "Provider_Name", p."Type" as "Provider_Type" 
        FROM food_listings f 
        JOIN providers p ON f."Provider_ID" = p."Provider_ID"
    """)

    # Filter Row Elements
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_loc = st.selectbox("📍 Filter Location/City", ["All"] + list(raw_listings['Location'].unique()))
    with col2:
        selected_provider = st.selectbox("🏢 Filter by Provider", ["All"] + list(raw_listings['Provider_Name'].unique()))
    with col3:
        selected_type = st.selectbox("🥦 Filter Diet Type", ["All"] + list(raw_listings['Food_Type'].unique()))

    # Apply filters dynamically
    filtered_df = raw_listings.copy()
    if selected_loc != "All":
        filtered_df = filtered_df[filtered_df['Location'] == selected_loc]
    if selected_provider != "All":
        filtered_df = filtered_df[filtered_df['Provider_Name'] == selected_provider]
    if selected_type != "All":
        filtered_df = filtered_df[filtered_df['Food_Type'] == selected_type]

    # Visual metrics summary cards
    m1, m2, m3 = st.columns(3)
    m1.metric("Filtered Listings Count", len(filtered_df))
    m2.metric("Total Food Units Offered", int(filtered_df['Quantity'].sum()) if len(filtered_df) > 0 else 0)
    m3.metric("Active Providers Engaged", filtered_df['Provider_ID'].nunique())

    st.dataframe(filtered_df, use_container_width=True)

# ==========================================================
# PAGE 2: MANAGE LISTINGS (FULL CRUD ACTIONS)
# ==========================================================
elif page == "Manage Listings (CRUD)":
    st.title("🛠️ Database Operations Control Panel")
    crud_action = st.tabs(["➕ Add New Listing", "✏️ Edit/Update Listing", "❌ Remove/Delete Listing"])

    with crud_action[0]:
        st.subheader("Post a New Surplus Food Listing")
        with st.form("add_listing_form"):
            f_id=st.number_input("Food ID", min_value=1,step=1,help="Enter a Unique Identifier for the Food item")
            f_name = st.text_input("Food Item Name (e.g., Bread, Salad)")
            f_qty = st.number_input("Quantity Available", min_value=1, step=1, value=10)
            f_exp = st.date_input("Expiry Date")
            f_prov = st.number_input("Valid Provider ID", min_value=1, step=1)
            f_loc = st.text_input("Fulfillment Location/City")
            f_type = st.selectbox("Food Class Category", ["Vegetarian", "Vegan", "Non-Vegetarian"])
            f_meal = st.selectbox("Meal Category", ["Breakfast", "Lunch", "Dinner", "Snacks"])

            submit_add = st.form_submit_button("Insert Record into Database")
            if submit_add:
                with engine.begin() as conn:
                    conn.execute(text("""
                        INSERT INTO food_listings ("Food_ID", "Food_Name", "Quantity", "Expiry_Date", "Provider_ID", "Location", "Food_Type", "Meal_Type")
                        VALUES (:id, :name, :qty, :exp, :prov, :loc, :type, :meal)
                    """), {"id":f_id, "name": f_name, "qty": f_qty, "exp": f_exp, "prov": f_prov, "loc": f_loc, "type": f_type, "meal": f_meal})
                st.success(f"Listing for {f_name} (ID: {f_id}) successfully added!")

    with crud_action[1]:
        st.subheader("Modify Existing Record Properties")
        target_id = st.number_input("Enter the Target Food_ID to update:", min_value=1, step=1)
        check_exist = load_db_data('SELECT * FROM food_listings WHERE "Food_ID" = :id', {"id": target_id})

        if not check_exist.empty:
            st.write("Current Properties:", check_exist)
            new_qty = st.number_input("New Updated Quantity Value", min_value=1, value=int(check_exist['Quantity'].iloc[0]))
            new_status = st.text_input("Update Location", value=str(check_exist['Location'].iloc[0]))

            if st.button("Commit Quantities Update"):
                with engine.begin() as conn:
                    conn.execute(text('UPDATE food_listings SET "Quantity" = :qty, "Location" = :loc WHERE "Food_ID" = :id'), 
                                 {"qty": new_qty, "loc": new_status, "id": target_id})
                st.success("Listing configurations successfully synchronized!")
        else:
            st.warning("No record found matching that specific target Food_ID.")

    with crud_action[2]:
        st.subheader("Purge a Listing Record")
        delete_id = st.number_input("Enter Target Food_ID to drop permanently:", min_value=1, step=1)

        if st.button("Permanently Execute Drop Action", type="primary"):
            with engine.begin() as conn:
                conn.execute(text('DELETE FROM food_listings WHERE "Food_ID" = :id'), {"id": delete_id})
            st.error(f"Record #{delete_id} deleted from your production schema.")

# ==========================================================
# PAGE 3: MAIN COMMUNICATIONS DIRECTORY
# ==========================================================
elif page == "Directory & Contact":
    st.title("📞 Matchmaking & Communications Directory")
    choice = st.radio("Select Target Entity Base:", ["Food Providers (Supply Base)", "Receivers (Demand Base - NGOs/Shelters)"])

    if choice == "Food Providers (Supply Base)":
        df_prov = load_db_data(SQLQueries.Q3_PROVIDER_CONTACTS)
        st.subheader("Active Supply Providers Mapping")
        st.dataframe(df_prov, use_container_width=True)
    else:
        df_rec = load_db_data('SELECT "Receiver_ID", "Name", "Type", "City", "Contact_Number" FROM receivers ORDER BY "City", "Name"')
        st.subheader("Registered Demand Receivers Directory")
        st.dataframe(df_rec, use_container_width=True)
    st.info("💡 **Direct Outreach Trigger:** Use the contact information displayed to coordinate immediate pick-ups.")

# ==========================================================
# PAGE 4: RUN ALL 15 CORE DATABASE ANALYTICS QUERIES LIVE
# ==========================================================
elif page == "Analytical Queries" :
    st.title("🧮 Core System Analytical Execution Matrix")
    st.markdown("Run your analytical queries interactively directly against your data model:")
    
    # 1. Fetch all queries from your utility method
    queries_map = SQLQueries.get_all_queries()
    query_labels = list(queries_map.keys())
    
    # NEW: Allow user to choose how they want to look up the query
    selection_mode = st.radio("Choose Selection Mode:", ["Select by Title Name", "Select by Query Number"])
    
    if selection_mode == "Select by Query Number":
        # Provide a number selector (1 to 18)
        query_num = st.number_input("Enter Query Number (1-18):", min_value=1, max_value=18, value=1, step=1)
        # Display the corresponding title to the user so they know what they selected
        selected_query_label = query_labels[query_num - 1]
        st.info(f"Selected Query: **{selected_query_label}**")
    else:
        # Fall back to the traditional descriptive dropdown selection
        selected_query_label = st.selectbox("Select Target Production Analytics Target Query:", query_labels)
        # Map the selected string back to its 1-indexed number position
        query_num = query_labels.index(selected_query_label) + 1

    if st.button("Run Target Query Against Live Database"):
        # 2. Pass the resolved query number to your second utility method
        target_sql = SQLQueries.get_query_by_number(query_num)
        
        if not target_sql:
            st.error("Invalid Query selection context.")
        else:
            st.markdown("**Executed Transaction String:**")
            st.code(target_sql, language="sql")
            
            output_df = load_db_data(target_sql)
            st.markdown("**Returned Matrix Output:**")
            
            if output_df.empty:
                st.info("Query successfully returned empty set matching standard operational expectations.")
            else:
                st.dataframe(output_df, use_container_width=True)
                
                # --- VISUAL CHART GENERATION LOGIC ---
                st.markdown("---")
                st.markdown("### 📊 Dynamic Query Visualization")
                
                layout_columns = output_df.columns.tolist()
                if len(layout_columns) >= 2:
                    x_axis = layout_columns[0]
                    y_axis = layout_columns[1]
                    
                    if query_num == 10: 
                        st.write("📈 **Status Breakdown Share:**")
                        st.bar_chart(data=output_df, x=x_axis, y=y_axis, use_container_width=True)
                    elif "city" in x_axis.lower() or "location" in x_axis.lower() or "provider_type" in x_axis.lower() or "food_type" in x_axis.lower():
                        st.write(f"📊 **Comparison of {y_axis.replace('_', ' ')} by {x_axis}:**")
                        st.bar_chart(data=output_df, x=x_axis, y=y_axis, use_container_width=True)
                    elif "name" in x_axis.lower():
                        st.write(f"🏅 **Leaderboard Summary Chart ({y_axis.replace('_', ' ')}):**")
                        st.bar_chart(data=output_df, x=x_axis, y=y_axis, use_container_width=True)
                    else:
                        st.write("📊 **Trend / General Metric Chart View:**")
                        st.bar_chart(data=output_df, x=x_axis, y=y_axis, use_container_width=True)
                else:
                    st.write("💡 Single-metric scalar outcome. (No chart required)")