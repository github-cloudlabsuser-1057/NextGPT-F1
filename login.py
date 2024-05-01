import streamlit as st
import azure.cosmos.cosmos_client as cosmos_client

# Azure Cosmos DB details
cosmosdb_endpoint = "https://nextgptcosmosdb.documents.azure.com:443/"
cosmosdb_key = "QPUJCqbq8M1QcdZty8lMdORK0rPPK9YUWYIJbiDNcc9cb8eRb0UHidOMIMuqUEm2gwlgElDrcApfACDbDipKTA=="
database_name = "nextgptcosmosdb"
container_name = "ToDoList"

# Initialize Cosmos DB client
client = cosmos_client.CosmosClient(url_connection=cosmosdb_endpoint, auth={'masterKey': cosmosdb_key})
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Streamlit UI
st.title("Login/Signup Page")

# Login Form
def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Query Cosmos DB to check if the user exists
        query = f"SELECT * FROM c WHERE c.username = '{username}' AND c.password = '{password}'"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))

        if items:
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

# Signup Form
def signup():
    st.subheader("Signup")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Signup"):
        # Check if username already exists
        query = f"SELECT * FROM c WHERE c.username = '{new_username}'"
        existing_user = list(container.query_items(query=query, enable_cross_partition_query=True))

        if existing_user:
            st.error("Username already exists. Please choose a different one.")
        else:
            # Add new user to Cosmos DB
            new_user = {"id": new_username, "username": new_username, "password": new_password}
            container.create_item(body=new_user)
            st.success("Signup successful! Please login.")

# Main function
def main():
    login()
    signup()

if __name__ == "__main__":
    main()
