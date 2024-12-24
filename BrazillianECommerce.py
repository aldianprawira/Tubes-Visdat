import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import plotly.express as px
from streamlit_folium import st_folium
import pandas as pd


# Load data frame menggunakan pickle
with open("top5_purchased_products.pkl", "rb") as file:
    top5_purchased_products = pickle.load(file)

with open("top5_produced_products.pkl", "rb") as file:
    top5_produced_products = pickle.load(file)

with open("top5_spending_state.pkl", "rb") as file:
    total_spending_state = pickle.load(file)

# Sidebar untuk navigasi
page = st.sidebar.radio("Navigation", ("Main Dashboard", "Top 5 Purchased Products", "Top 5 Produced Products", "Total Spending State", "Top Sellers"))

# Page 1: Dashboard Utama
if page == "Main Dashboard":
    st.title("Dashboard E-commerce Brazil")
    st.header("Deskripsi Dataset")
    st.write(
        """
This dataset is public e-commerce data from Brazil, provided by Olist, the largest department store in the Brazilian market. Olist connects small businesses from across Brazil to various sales channels effortlessly with a single contract. Merchants can sell their products through Olist Store and ship them directly to customers using Olist's logistics partners.

    

After a customer purchases a product from Olist Store, the seller is notified to fulfill the order. Once the customer receives the product or the estimated delivery date has arrived, the customer receives a satisfaction survey via email, where they can rate their shopping experience and leave some comments.

    """
    )

    # Title for the section
    st.header("Data Table")

    # Display the datasets with descriptions
    datasets = {
        "olist_customers_dataset.csv": "Contains customer information, including customer IDs, geographical details, and other demographic data.",
        "olist_geolocation_dataset.csv": "Holds geographical information for each customer, including latitude and longitude, enabling location-based analysis.",
        "olist_order_items_dataset.csv": "Includes details about the items in each order, such as product IDs, order IDs, and quantities ordered.",
        "olist_order_payments_dataset.csv": "Captures payment information for each order, detailing payment methods, statuses, and transaction values.",
        "olist_order_reviews_dataset.csv": "Features customer reviews for products, including ratings and review comments, which can be useful for sentiment analysis.",
        "olist_orders_dataset.csv": "Contains overall order data, including order IDs, customer IDs, order statuses, and timestamps for order placements.",
        "olist_products_dataset.csv": "Lists all products available for sale, with attributes such as product IDs, names, categories, and prices.",
        "olist_sellers_dataset.csv": "Provides information about sellers, including seller IDs, names, and associated geographical details.",
        "product_category_name_translation.csv": "Translates product category names into English for easier analysis and reporting.",
    }

    # Display each dataset and its description
    for dataset, description in datasets.items():
        st.subheader(dataset)
        st.write(description)

    st.write(
        """
On this dashboard, you can analyze sales, production, and total spending by each state during the rainy and dry seasons. You can further explore the data through the following pages.
    - Top 5 Purchased Products
    - Top 5 Produced Products
    - Total Spending State
    """
    )


# Page 2: Top 5 Purchased Products
elif page == "Top 5 Purchased Products":
    st.title("Top 5 Purchased Products")
    st.header("Most Purchased Products on Wet and Dry Seasons for each State")
    st.write(
        "The provided code processes sales data by merging several DataFrames to extract relevant information about customer orders, including customer location and product categories. Initially, it combines orders, customers, order items, products, and product category translations to create a comprehensive DataFrame that includes the necessary details. It also converts the purchase timestamps to datetime format and extracts the month to classify each order into either "
        "Wet Season"
        " or "
        "Dry Season,"
        " based on predefined month ranges."
    )

    st.write(
        "After preparing the data, the code groups the merged DataFrame by customer state, season, and product category to count the number of purchases for each category. Finally, it identifies the top five most purchased products for each customer state and season by applying a filter to the grouped data, resulting in a new DataFrame that highlights the most popular products within different regions and seasonal contexts."
    )

    st.dataframe(top5_purchased_products)

    # Peta singkatan state ke nama asli
    state_names = {
        "AC": "Acre",
        "AL": "Alagoas",
        "AP": "Amapá",
        "AM": "Amazonas",
        "BA": "Bahia",
        "CE": "Ceará",
        "DF": "Distrito Federal",
        "ES": "Espírito Santo",
        "GO": "Goiás",
        "MA": "Maranhão",
        "MT": "Mato Grosso",
        "MS": "Mato Grosso do Sul",
        "MG": "Minas Gerais",
        "PA": "Pará",
        "PB": "Paraíba",
        "PR": "Paraná",
        "PE": "Pernambuco",
        "PI": "Piauí",
        "RJ": "Rio de Janeiro",
        "RN": "Rio Grande do Norte",
        "RS": "Rio Grande do Sul",
        "RO": "Rondônia",
        "RR": "Roraima",
        "SC": "Santa Catarina",
        "SP": "São Paulo",
        "SE": "Sergipe",
        "TO": "Tocantins",
    }

    # Dropdown untuk memilih state
    selected_state = st.selectbox("Pilih State:", list(state_names.keys()), format_func=lambda x: state_names[x])

    # Filter data berdasarkan state yang dipilih
    subset_wet = top5_purchased_products[(top5_purchased_products["customer_state"] == selected_state) & (top5_purchased_products["season"] == "Wet Season")]
    subset_dry = top5_purchased_products[(top5_purchased_products["customer_state"] == selected_state) & (top5_purchased_products["season"] == "Dry Season")]

    bar_width = 0.35
    indices_dry = np.arange(len(subset_dry))
    indices_wet = np.arange(len(subset_wet)) + len(subset_dry)

    plt.figure(figsize=(12, 6))
    plt.bar(indices_dry, subset_dry["purchase_count"], width=bar_width, label="Dry Season", color="orange", align="center")
    plt.bar(indices_wet, subset_wet["purchase_count"], width=bar_width, label="Wet Season", color="skyblue", align="center")

    plt.xlabel("Product Category")
    plt.ylabel("Purchase Count")
    plt.title(f"Top Products in {state_names[selected_state]} (Dry on Left and Wet on Right)")

    all_categories = np.concatenate([subset_dry["product_category_name_english"].values, subset_wet["product_category_name_english"].values])
    plt.xticks(np.concatenate([indices_dry, indices_wet]), all_categories, rotation=45, ha="right")
    plt.legend()

    st.pyplot(plt)  # Tampilkan visualisasi di Streamlit

    # Penjelasan berdasarkan state yang dipilih
    st.subheader(f"Analysis for State: {state_names[selected_state]}")

    if selected_state == "AC":
        st.header("Key Findings")
        st.write(
            """
        Key Findings:
        The most popular product categories in Acre shift between dry and wet seasons. Furniture & decor and sports & leisure lead in the dry season, likely due to favorable weather for outdoor activities and home improvement. In the wet season, computers & accessories and housewares see increased demand, potentially reflecting more indoor time and cleaning needs. Telephony and auto remain relatively stable year-round.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """Weather plays a significant role, with dry conditions encouraging outdoor activities and wet weather driving indoor pursuits. Seasonal lifestyle changes, cultural factors, and regional preferences could also influence product demand."""
        )

    elif selected_state == "AL":
        st.header("Key Findings")

        st.write(
            """The data reveals a clear seasonal pattern in product preferences in Alagoas. During the dry season, health & beauty and computers & accessories are the most popular categories, likely due to increased outdoor activities and indoor pursuits. In the wet season, watches & gifts and furniture & decor see a rise in demand, potentially reflecting gift-giving occasions and home improvement projects.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
        Weather plays a significant role, with dry conditions encouraging outdoor activities and personal care, while wet weather drives indoor activities and home comfort needs. Cultural and regional factors may also influence these trends.
        """
        )

    elif selected_state == "AP":
        st.header("Key Findings")

        st.write(
            """The provided chart illustrates the top-selling products in Amapá during dry and wet seasons. During the dry season, health & beauty and bed_bath_table emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories, electronics, and fixed_telephony.

        It's interesting to observe that certain categories like watches_gifts, computers_accessories, and sports_leisure showed relatively stable purchase counts across both seasons. This suggests a consistent demand for these products throughout the year, regardless of weather conditions.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
        The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

        On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for products like computers, electronics, and fixed telephony, as people seek indoor activities and communication tools. Furthermore, the increased need for home comfort and entertainment during rainy weather could contribute to the popularity of items like bed_bath_table.
        """
        )
    elif selected_state == "AM":
        st.header("Key Findings")

        st.write(
            """
        The provided chart illustrates the top-selling products in Amazonas during dry and wet seasons. During the dry season, health & beauty, computers_accessories, and sports_leisure emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories and health_beauty.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
        The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

        On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories and health_beauty products, as people seek indoor activities and personal care options. Furthermore, the increased need for home comfort and entertainment during rainy weather could contribute to the popularity of certain items.
        """
        )
    elif selected_state == "BA":
        st.header("Key Findings")

        st.write(
            """
        The provided chart illustrates the top-selling products in Bahia during dry and wet seasons. During the dry season, health & beauty, sports_leisure, and bed_bath_table emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories and telephony.


        """
        )

        st.header("Potential Explanations")
        st.write(
            """
        The provided chart illustrates the top-selling products in Bahia during dry and wet seasons. During the dry season, health & beauty, sports_leisure, and bed_bath_table emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories and telephony.


        """
        )
    elif selected_state == "CE":
        st.header("Key Findings")

        st.write(
            """
        The provided chart illustrates the top-selling products in Ceará during dry and wet seasons. During the dry season, health & beauty, watches_gifts, and sports_leisure emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for health_beauty, watches_gifts, and telephony.


        """
        )

        st.header("Potential Explanations")
        st.write(
            """
        The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

        On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for health_beauty, watches_gifts, and telephony, as people seek indoor activities and communication tools. Furthermore, the increased need for home comfort and entertainment during rainy weather could contribute to the popularity of certain items.
        """
        )
    elif selected_state == "DF":
        st.header("Key Findings")

        st.write(
            """
        The provided chart illustrates the top-selling products in Distrito Federal during dry and wet seasons. During the dry season, health & beauty, sports_leisure, and bed_bath_table emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories, furniture_decor, and health_beauty.


        """
        )

        st.header("Potential Explanations")
        st.write(
            """
        The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

        On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, furniture_decor, and health_beauty, as people seek indoor activities, home improvement projects, and personal care options. Furthermore, the increased need for home comfort and entertainment during rainy weather could contribute to the popularity of certain items.
        """
        )
    elif selected_state == "ES":
        st.header("Key Findings")

        st.write(
            """
        The provided chart illustrates the top-selling products in Espírito Santo during dry and wet seasons. During the dry season, bed_bath_table, health_beauty, and sports_leisure emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories and bed_bath_table.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
        """
        )
    elif selected_state == "GO":
        st.header("Key Findings")

        st.write(
            """
        The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health_beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

        On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories and bed_bath_table, as people seek indoor activities and home comfort options. Furthermore, the increased need for home entertainment and relaxation during rainy weather could contribute to the popularity of certain items.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
        """
        )
    elif selected_state == "MA":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Maranhão during dry and wet seasons. During the dry season, health & beauty, computers_accessories, and watches_gifts emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for sports_leisure, health_beauty, and computers_accessories.

        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, health_beauty, and sports_leisure, as people seek indoor activities, personal care options, and entertainment. Furthermore, the increased need for home comfort and relaxation during rainy weather could contribute to the popularity of certain items.

        """
        )
    elif selected_state == "MT":
        st.header("Key Findings")

        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for bed_bath_table, sports_leisure, and telephony, as people seek indoor activities, home comfort options, and communication tools. Furthermore, the increased need for home entertainment and relaxation during rainy weather could contribute to the popularity of certain items.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
        """
        )
    elif selected_state == "MS":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Mato Grosso do Sul during dry and wet seasons. During the dry season, health & beauty, sports_leisure, and bed_bath_table emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories, furniture_decor, and health_beauty.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, furniture_decor, and health_beauty, as people seek indoor activities, home improvement projects, and personal care options. Furthermore, the increased need for home comfort and entertainment during rainy weather could contribute to the popularity of certain items.
        """
        )
    elif selected_state == "MG":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Minas Gerais during dry and wet seasons. During the dry season, bed_bath_table, health_beauty, and sports_leisure emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories, furniture_decor, and health_beauty.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health_beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, furniture_decor, and health_beauty, as people seek indoor activities, home improvement projects, and personal care options. Furthermore, the increased need for home comfort and entertainment during rainy weather could contribute to the popularity of certain items.
        """
        )
    elif selected_state == "PA":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Pará during dry and wet seasons. During the dry season, health & beauty, computers_accessories, and watches_gifts emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for sports_leisure, health_beauty, and telephony.

        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, health_beauty, and telephony, as people seek indoor activities, personal care options, and communication tools. Furthermore, the increased need for home comfort and entertainment during rainy weather could contribute to the popularity of certain items.

        """
        )
    elif selected_state == "PB":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Paraíba during dry and wet seasons. During the dry season, health & beauty, computers_accessories, and furniture_decor emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for sports_leisure, health_beauty, and computers_accessories.

        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, health_beauty, and sports_leisure, as people seek indoor activities, personal care options, and entertainment. Furthermore, the increased need for home comfort and relaxation during rainy weather could contribute to the popularity of certain items.

        """
        )
    elif selected_state == "PR":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Paraná during dry and wet seasons. During the dry season, furniture_decor, sports_leisure, and bed_bath_table emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories, furniture_decor, and health_beauty.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for sports_leisure and health_beauty products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, furniture_decor, and health_beauty, as people seek indoor activities, home improvement projects, and personal care options. Furthermore, the increased need for home comfort and entertainment during rainy weather could contribute to the popularity of certain items.

        """
        )
    elif selected_state == "PE":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Pernambuco during dry and wet seasons. During the dry season, health & beauty, watches_gifts, and sports_leisure emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for health_beauty, telephony, and sports_leisure.

        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for health_beauty, telephony, and sports_leisure, as people seek indoor activities, personal care options, and entertainment. Furthermore, the increased need for home comfort and relaxation during rainy weather could contribute to the popularity of certain items.

        """
        )
    elif selected_state == "PI":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Piauí during dry and wet seasons. During the dry season, health & beauty, telephony, and watches_gifts emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for sports_leisure, health_beauty, and bed_bath_table.

        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for health_beauty, bed_bath_table, and sports_leisure, as people seek indoor activities, personal care options, and entertainment. Furthermore, the increased need for home comfort and relaxation during rainy weather could contribute to the popularity of certain items.

        """
        )
    elif selected_state == "RJ":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Rio de Janeiro during dry and wet seasons. During the dry season, bed_bath_table, health_beauty, and furniture_decor emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories, furniture_decor, and sports_leisure.

        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health_beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, furniture_decor, and sports_leisure, as people seek indoor activities, home improvement projects, and entertainment. Furthermore, the increased need for home comfort and relaxation during rainy weather could contribute to the popularity of certain items.

        """
        )
    elif selected_state == "RN":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Rio Grande do Norte during dry and wet seasons. During the dry season, health & beauty, watches_gifts, and housewares emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for health_beauty, watches_gifts, and books_general_interest.

        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for books_general_interest, health_beauty, and watches_gifts, as people seek indoor activities, personal care options, and entertainment. Furthermore, the increased need for home comfort and relaxation during rainy weather could contribute to the popularity of certain items.

        """
        )
    elif selected_state == "RS":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Rio Grande do Sul during dry and wet seasons. During the dry season, bed_bath_table, furniture_decor, and housewares emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories, furniture_decor, and sports_leisure.

        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health_beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, furniture_decor, and sports_leisure, as people seek indoor activities, home improvement projects, and entertainment. Furthermore, the increased need for home comfort and relaxation during rainy weather could contribute to the popularity of certain items.

        """
        )
    elif selected_state == "RO":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Rondônia during dry and wet seasons. During the dry season, health & beauty, telephony, and computers_accessories emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for sports_leisure, computers_accessories, and bed_bath_table.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, bed_bath_table, and sports_leisure, as people seek indoor activities, home improvement projects, and entertainment. Furthermore, the increased need for home comfort and relaxation during rainy weather could contribute to the popularity of certain items.

        """
        )
    elif selected_state == "RR":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Roraima during dry and wet seasons. During the dry season, furniture_decor, sports_leisure, and health_beauty emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories, telephony, and baby products.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for sports_leisure and health_beauty products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, telephony, and baby products, as people seek indoor activities, communication tools, and family-related items. Furthermore, the increased need for home comfort and entertainment during rainy weather could contribute to the popularity of certain items.
        """
        )
    elif selected_state == "SC":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Santa Catarina during dry and wet seasons. During the dry season, sports_leisure, furniture_decor, and bed_bath_table emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories, furniture_decor, and health_beauty.

        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for sports_leisure and health_beauty products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories and furniture_decor, as people seek indoor activities, home improvement projects, and entertainment. Furthermore, the increased need for home comfort and relaxation during rainy weather could contribute to the popularity of certain items.
        """
        )
    elif selected_state == "SP":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in São Paulo during dry and wet seasons. During the dry season, bed_bath_table, health_beauty, and housewares emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for computers_accessories, furniture_decor, and sports_leisure.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health_beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, furniture_decor, and sports_leisure, as people seek indoor activities, home improvement projects, and entertainment. Furthermore, the increased need for home comfort and relaxation during rainy weather could contribute to the popularity of certain items.
        """
        )
    elif selected_state == "SE":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Sergipe during dry and wet seasons. During the dry season, health & beauty, computers_accessories, and sports_leisure emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for sports_leisure, computers_accessories, and furniture_decor.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, furniture_decor, and sports_leisure, as people seek indoor activities, home improvement projects, and entertainment. Furthermore, the increased need for home comfort and relaxation during rainy weather could contribute to the popularity of certain items.
        """
        )
    elif selected_state == "TO":
        st.header("Key Findings")

        st.write(
            """
The provided chart illustrates the top-selling products in Tocantins during dry and wet seasons. During the dry season, health & beauty, watches_gifts, and furniture_decor emerged as the most popular categories. In contrast, during the wet season, there was a notable increase in demand for sports_leisure, health_beauty, and computers_accessories.
        """
        )

        st.header("Potential Explanations")
        st.write(
            """
The seasonal fluctuations in product demand can be attributed to several factors. The dry season, with its warmer temperatures and lower rainfall, might encourage outdoor activities and personal care, leading to increased demand for health & beauty and sports_leisure products. Additionally, the availability of more daylight hours during this season could boost demand for items related to home and leisure.

On the other hand, the wet season, characterized by higher rainfall and cooler temperatures, might drive people indoors. This could explain the surge in demand for computers_accessories, health_beauty, and sports_leisure, as people seek indoor activities, personal care options, and entertainment. Furthermore, the increased need for home comfort and relaxation during rainy weather could contribute to the popularity of certain items.
        """
        )

    # Tambahkan penjelasan untuk state lain sesuai kebutuhan
    else:
        st.write(
            """
            Negara bagian ini menunjukkan pola pembelian yang unik, yang dipengaruhi oleh berbagai faktor seperti iklim lokal, budaya, dan ketersediaan produk.
            Data pembelian selama musim kering dan musim hujan menunjukkan adanya preferensi yang berbeda pada setiap musim, yang dapat membantu dalam memahami kebutuhan konsumen setempat.
        """
        )


# Page 3: Top 5 Produced Products
elif page == "Top 5 Produced Products":
    st.title("Top 5 Produced Products")
    st.header("Data Produk yang Paling Banyak Diproduksi tiap State")
    st.write(
        "The provided code processes e-commerce sales data by merging multiple DataFrames—orders, order items, products, sellers, and customers—into a comprehensive dataset. It selects relevant columns that include product IDs, categories, order status, timestamps, and seller states. The code then enriches the dataset by merging with a translation DataFrame to obtain English names for product categories, replacing the original category names with these translations. Unnecessary columns are removed, and the order timestamps are converted to a datetime format."
    )

    st.write(
        "To analyze the data seasonally, the code defines a function that categorizes orders into either "
        "wet"
        " or "
        "dry"
        " seasons based on the month of the order date. It adds this seasonal information to the DataFrame and calculates the count of products sold by seller state and season. Finally, the code identifies the top five most produced products for each seller state during both wet and dry seasons, resulting in a refined DataFrame that highlights the most popular products based on seasonal sales across different states."
    )

    st.dataframe(top5_produced_products)

    # Peta singkatan state ke nama asli
    state_names = {
        "AC": "Acre",
        "AL": "Alagoas",
        "AP": "Amapá",
        "AM": "Amazonas",
        "BA": "Bahia",
        "CE": "Ceará",
        "DF": "Distrito Federal",
        "ES": "Espírito Santo",
        "GO": "Goiás",
        "MA": "Maranhão",
        "MT": "Mato Grosso",
        "MS": "Mato Grosso do Sul",
        "MG": "Minas Gerais",
        "PA": "Pará",
        "PB": "Paraíba",
        "PR": "Paraná",
        "PE": "Pernambuco",
        "PI": "Piauí",
        "RJ": "Rio de Janeiro",
        "RN": "Rio Grande do Norte",
        "RS": "Rio Grande do Sul",
        "RO": "Rondônia",
        "RR": "Roraima",
        "SC": "Santa Catarina",
        "SP": "São Paulo",
        "SE": "Sergipe",
        "TO": "Tocantins",
    }

    # Dropdown untuk memilih state
    selected_state = st.selectbox("Pilih State:", list(state_names.keys()), format_func=lambda x: state_names[x])

    # Filter data berdasarkan state yang dipilih
    subset_wet = top5_produced_products[(top5_produced_products["seller_state"] == selected_state) & (top5_produced_products["season"] == "wet")]
    subset_dry = top5_produced_products[(top5_produced_products["seller_state"] == selected_state) & (top5_produced_products["season"] == "dry")]

    # Buat array untuk posisi batang
    bar_width = 0.35
    indices_dry = np.arange(len(subset_dry))  # Posisi untuk dry season
    indices_wet = np.arange(len(subset_wet)) + len(subset_dry)  # Posisi untuk wet season, offset dengan panjang dry season

    # Plot batang
    plt.figure(figsize=(12, 6))

    plt.bar(indices_dry, subset_dry["count"], width=bar_width, label="Dry Season", color="orange", align="center")
    plt.bar(indices_wet, subset_wet["count"], width=bar_width, label="Wet Season", color="skyblue", align="center")

    # Set label, judul, dan sumbu x
    plt.xlabel("Product Category")
    plt.ylabel("Produced Count")
    plt.title(f"Top Products in {state_names[selected_state]} (Dry on Left and Wet on Right)")

    # Gabungkan kategori produk untuk kedua musim dan atur ticks
    all_categories = np.concatenate([subset_dry["product_category_name"].values, subset_wet["product_category_name"].values])
    plt.xticks(np.concatenate([indices_dry, indices_wet]), all_categories, rotation=45, ha="right")

    # Tampilkan legenda
    plt.legend()

    # Tampilkan grafik di Streamlit
    st.pyplot(plt)

    # Menutup figura setelah menampilkan untuk menghindari plot bertumpuk
    plt.close()

    # Penjelasan berdasarkan state yang dipilih
    explanations = {
        "AL": "Alagoas is renowned for its agricultural products, particularly in the fields of food and beverages. The state’s fertile land and favorable climate enable the cultivation of various crops, contributing significantly to its economy. Alagoas is also famous for its beautiful beaches and vibrant culture, making it a popular tourist destination. Traditional dishes, such as sururu (a local shellfish) and various seafood preparations, reflect the state's rich culinary heritage.",
        "AC": "Acre, located in the Amazon region, is known for its rich forest resources and agricultural products. The state is characterized by its vast rainforests and diverse ecosystems, which support a variety of wildlife. Acre’s economy is largely driven by sustainable logging, rubber tapping, and agriculture. The local culture is heavily influenced by indigenous traditions, and festivals celebrating the region's natural heritage are commonly held.",
        "AP": "Amapá is rich in forest resources and agricultural products due to its tropical climate. The state is home to diverse flora and fauna, contributing to its ecological significance. Amapá has a vibrant culture influenced by indigenous communities, reflected in its art, music, and local cuisine. The people of Amapá take pride in their traditional practices and celebrate their heritage through various festivals throughout the year.",
        "AM": "Amazonas is famous for its vast tropical rainforest and diverse wildlife, producing products like timber and raw materials. The state plays a crucial role in Brazil's ecological balance and offers a wealth of natural resources. The economy is centered around sustainable practices, including eco-tourism and traditional agriculture. The culture of Amazonas is rich with indigenous influences, and festivals often celebrate the unique relationship between the people and the Amazon rainforest.",
        "BA": "Bahia is known for its rich cultural heritage and distinctive food and drink production, including cachaça, a popular Brazilian spirit. The state boasts a blend of African, Indigenous, and Portuguese influences, evident in its music, dance, and culinary traditions. Bahia’s coastal cities are famous for their beautiful beaches and lively festivals, which attract both local and international tourists.",
        "CE": "Ceará is famous for its textile industry and agricultural products, particularly fruits and vegetables. The state features a diverse landscape, from sandy beaches to lush valleys, providing a variety of agricultural opportunities. Ceará is also known for its cultural richness, with vibrant music, dance, and festivals that showcase the local traditions. Signature dishes include seafood and traditional northeastern foods.",
        "DF": "Distrito Federal is the center of government in Brazil and boasts a range of local products influenced by its diverse population. The area is characterized by its modern architecture and urban planning, creating a unique cultural atmosphere. Although smaller in size, the Distrito Federal has a dynamic economy supported by various sectors, including services and trade. The local cuisine features a mix of traditional Brazilian dishes and contemporary culinary innovations.",
        "ES": "Espírito Santo is recognized for its coffee production and agricultural products. The state has a strong agricultural sector, with coffee being a significant export. Espírito Santo is also known for its beautiful coastline and diverse ecosystems, attracting tourists with its natural beauty. The local culture is rich, with culinary traditions that include dishes like moqueca (a fish stew) and various seafood preparations.",
        "GO": "Goiás is known for its agricultural output, particularly in the production of corn and soybeans. The state is characterized by its vast farmlands and rich natural resources. Goiás has a rich cultural heritage, celebrated through festivals that highlight traditional music, dance, and culinary specialties. The local cuisine includes typical dishes like pamonha (a corn dish) and pequi (a native fruit).",
        "MA": "Maranhão is famous for its rice production and other agricultural products. The state features a diverse landscape, including the Lençóis Maranhenses National Park, known for its stunning sand dunes and lagoons. Maranhão has a vibrant culture, influenced by indigenous and African traditions, which is reflected in its music, dance, and festivals. Traditional dishes include rice and various seafood specialties.",
        "MT": "Mato Grosso is recognized as one of the largest agricultural producers in Brazil. The state is a major contributor to the national economy, producing soybeans, corn, and cattle. Mato Grosso is home to diverse ecosystems, including the Pantanal wetlands, which support a rich array of wildlife. The local culture is vibrant, with traditional festivals celebrating the agricultural heritage and natural beauty of the region.",
        "MS": "Mato Grosso do Sul produces a wide variety of agricultural and livestock products. The state is known for its rich natural resources, including the Pantanal, which is one of the world's largest tropical wetlands. Mato Grosso do Sul has a diverse culture influenced by indigenous peoples, and its culinary traditions include regional dishes that showcase local ingredients. The state also promotes eco-tourism, attracting visitors interested in its natural landscapes.",
        "MG": "Minas Gerais is celebrated for its agricultural products and mineral resources. The state has a rich history in mining and is known for its delicious food, including traditional dishes like pão de queijo (cheese bread) and feijão tropeiro (a bean dish). Minas Gerais boasts beautiful landscapes and a rich cultural heritage, with numerous festivals celebrating music, art, and local traditions.",
        "PA": "Pará is known for its forest resources and agricultural products, particularly those sourced from the Amazon. The state features a unique blend of cultures, with strong indigenous influences evident in its cuisine and traditions. Pará is famous for dishes like tacacá and açaí, which are integral to its culinary identity. The state's economy relies on sustainable practices, balancing environmental preservation with resource exploitation.",
        "PB": "Paraíba produces various agricultural products, including peanuts and corn. The state features a vibrant culture, known for its music, dance, and artistic expressions. Paraíba is also home to beautiful coastal areas, attracting tourists to its beaches and cultural events. Traditional festivals celebrate local folklore and cuisine, contributing to the region's cultural richness.",
        "PR": "Paraná is renowned for its agricultural production, especially soybeans and corn. The state has a diverse landscape, including the Iguaçu Falls, a UNESCO World Heritage site. Paraná’s economy is bolstered by agriculture and industry, with a focus on sustainability and innovation. The local culture reflects a mix of influences, with festivals celebrating regional traditions and culinary specialties.",
        "PE": "Pernambuco is known for its agricultural products and rich cultural heritage. The state is famous for its vibrant music scene, particularly in the genres of frevo and maracatu, and hosts numerous cultural festivals throughout the year. Traditional dishes like bolo de rolo (a rolled cake) and various seafood preparations showcase the local cuisine. Pernambuco's beautiful beaches and historical cities attract tourists from around the world.",
        "PI": "Piauí is recognized for its agricultural output, including peanuts and cotton. The state features a diverse landscape, with natural parks and historical sites that reflect its rich cultural heritage. Piauí is home to vibrant traditions, including music and dance, and celebrates various festivals that highlight local cuisine and customs. Traditional dishes often feature local ingredients, celebrating the state's agricultural bounty.",
        "RJ": "Rio de Janeiro is famous for its tourism industry and local products. The state boasts beautiful beaches, mountains, and a vibrant cultural scene, making it a popular destination for both locals and tourists. Rio de Janeiro is also known for its culinary diversity, with a mix of international and traditional Brazilian cuisines. The local culture is rich, influenced by music, dance, and the arts, with events like Carnival attracting global attention.",
        "RN": "Rio Grande do Norte is a state located in northeastern Brazil, known for its salt production and agricultural products. This region boasts beautiful beaches, and its ecosystems support various tourism activities. The local community celebrates traditions and cultures with festivals showcasing music, dance, and handicrafts. Signature dishes from Rio Grande do Norte include a variety of seafood and fresh agricultural produce.",
        "RS": "Rio Grande do Sul is situated in southern Brazil, recognized for its livestock farming, particularly cattle, as well as wine production. This region has a rich culture influenced by European immigrants, especially Germans and Italians, which is reflected in its cuisine and local festivals. The people of Rio Grande do Sul are famous for their tradition of churrasco (Brazilian barbecue) and unique handicrafts. Additionally, the area features stunning natural landscapes, including mountains and lakes.",
        "RO": "Rondônia is a state located in western Brazil, known for its rich natural resources and agriculture. This region encompasses vast rainforests and is part of the Amazon ecosystem. The people of Rondônia are committed to developing sustainable agricultural practices while preserving their rich cultural traditions. Agricultural products such as soybeans and coffee play a significant role in the local economy.",
        "RR": "Roraima is situated in northern Brazil, known for its natural beauty and ethnic diversity. This region features extensive rainforests and a rich local culture, including indigenous communities that maintain their traditions and way of life. Roraima is renowned for its unique agricultural products and forest resources, as well as its growing nature tourism sector. Cultural festivals are frequently held to celebrate the heritage of the local communities and the region's biodiversity.",
        "SC": "Santa Catarina is located in southern Brazil, recognized for its agricultural output, including vegetables and fruits, as well as seafood production. This state boasts beautiful beaches and stunning mountains, making it a popular tourist destination. Santa Catarina also has a rich cultural heritage, influenced by German and Italian immigrants, evident in its cuisine, crafts, and local festivals. Signature dishes such as churrasco and cuca are highly celebrated in this region.",
        "SP": "São Paulo is the most populous state and the economic center of Brazil. Known for its strong industry and commerce, São Paulo has a wide variety of products, including coffee, sugar and agricultural products. Additionally, the city of São Paulo is a dynamic cultural center with numerous festivals, museums and performing arts. The people of São Paulo have a rich and varied culinary tradition, reflecting the existing ethnic and cultural diversity.",
        "SE": "Sergipe adalah negara bagian terkecil di Brasil yang terletak di bagian timur laut. Dikenal dengan hasil pertanian, termasuk padi dan buah-buahan tropis, Sergipe juga memiliki pantai-pantai yang indah dan kebudayaan yang kaya. Masyarakat di sini merayakan berbagai festival, termasuk festival folkor yang menampilkan musik dan tarian lokal. Hidangan khas seperti caranguejo (kepiting) dan berbagai makanan laut sangat populer di daerah ini.",
        "TO": "Tocantins adalah negara bagian yang terletak di bagian tengah Brasil, dikenal dengan keanekaragaman hayati dan produk pertanian yang melimpah. Wilayah ini memiliki hutan dan sungai yang menakjubkan, serta merupakan bagian dari ekosistem yang penting. Masyarakat di Tocantins merayakan tradisi lokal melalui festival budaya dan seni, serta menjaga hubungan yang kuat dengan alam. Produk pertanian, seperti jagung dan kedelai, menjadi bagian penting dari perekonomian lokal.",
    }

    # Tampilkan penjelasan berdasarkan state yang dipilih
    st.subheader(f"Detailed Description about {state_names[selected_state]}")
    st.write(explanations[selected_state])


# Page 4: Total Spending State
elif page == "Total Spending State":

    # Halaman Streamlit
    st.header("Total Spending State")

    # Mengelompokkan pengeluaran per customer_state
    spending_per_state = total_spending_state.groupby("customer_state")["payment_value"].sum().reset_index()

    # Mengubah inisial state menjadi nama sebenarnya
    state_names = {
        "AC": "Acre",
        "AL": "Alagoas",
        "AP": "Amapá",
        "AM": "Amazonas",
        "BA": "Bahia",
        "CE": "Ceará",
        "DF": "Distrito Federal",
        "ES": "Espírito Santo",
        "GO": "Goiás",
        "MA": "Maranhão",
        "MT": "Mato Grosso",
        "MS": "Mato Grosso do Sul",
        "MG": "Minas Gerais",
        "PA": "Pará",
        "PB": "Paraíba",
        "PR": "Paraná",
        "PE": "Pernambuco",
        "PI": "Piauí",
        "RJ": "Rio de Janeiro",
        "RN": "Rio Grande do Norte",
        "RS": "Rio Grande do Sul",
        "RO": "Rondônia",
        "RR": "Roraima",
        "SC": "Santa Catarina",
        "SP": "São Paulo",
        "SE": "Sergipe",
        "TO": "Tocantins",
    }

    # Mengganti inisial dengan nama negara bagian lengkap
    spending_per_state["customer_state"] = spending_per_state["customer_state"].map(state_names)

    # Visualisasi menggunakan treemap
    fig = px.treemap(
        spending_per_state,
        path=["customer_state"],  # Label untuk tiap state
        values="payment_value",
        title="Total Spending by State",
        color="payment_value",
        color_continuous_scale="Blues",
        labels={"customer_state": "State", "payment_value": "Total Spending"},
        height=1000,  # Meningkatkan tinggi untuk menampung lebih banyak informasi
        width=3000,  # Meningkatkan lebar untuk nama yang lebih panjang
    )

    # Menyesuaikan ukuran teks agar lebih besar dan lebih jelas
    fig.update_traces(textfont=dict(size=16))

    # Menampilkan visualisasi di Streamlit
    st.plotly_chart(fig)

    st.write(
        """
    São Paulo has the highest total spending among Brazilian states, largely due to its position as the economic powerhouse of Brazil. As the state with the largest GDP, São Paulo serves as the main hub for industry, commerce, and services, driving significant economic activity. The large population, which is the highest in Brazil, naturally leads to greater consumption of goods and services. This combination of economic prominence and a large number of consumers results in higher overall expenditure.
    """
    )

    st.write(
        """
    Additionally, São Paulo benefits from being the center of trade, business, and diverse economic activities. The presence of national and international companies boosts business spending, while better infrastructure and services make it a desirable place for both residents and businesses. With higher average income levels and diverse opportunities for consumption, São Paulo's residents have greater purchasing power, further driving up the state's total spending.
    """
    )

# Page 5: Top Sellers
elif page == "Top Sellers":
    # Caching the data loading and merging process
    @st.cache_data
    def load_and_merge_data(top_n):
        # Load datasets
        df_geolocation = pd.read_csv("dataset/olist_geolocation_dataset.csv")
        df_sellers = pd.read_csv("dataset/olist_sellers_dataset.csv")
        df_order_items = pd.read_csv("dataset/olist_order_items_dataset.csv")

        # Group by seller_id and count the number of unique order_ids
        seller_order_count = df_order_items.groupby("seller_id")["order_id"].count().reset_index()

        # Rename the columns for better readability
        seller_order_count.rename(columns={"order_id": "order_count"}, inplace=True)

        # Sort sellers by order_count in descending order and select the top N
        top_sellers = seller_order_count.sort_values(by="order_count", ascending=False).head(top_n)

        # Perform a left join between top_sellers and df_sellers
        top_sellers_with_info = pd.merge(top_sellers, df_sellers, how="left", on="seller_id")

        # Perform an inner join on seller_zip_code_prefix
        df_sellers_geolocation = pd.merge(top_sellers_with_info, df_geolocation, how="inner", left_on="seller_zip_code_prefix", right_on="geolocation_zip_code_prefix")

        # Group by seller_id and take the first latitude and longitude for each seller
        df_sellers_first_location = df_sellers_geolocation.groupby("seller_id").first().reset_index()

        # Select relevant columns for the new DataFrame
        df_sellers_first_location = df_sellers_first_location[["seller_id", "order_count", "seller_zip_code_prefix", "geolocation_lat", "geolocation_lng", "seller_city", "seller_state"]]

        # Renaming columns
        df_sellers_first_location.rename(columns={"geolocation_lat": "lat", "geolocation_lng": "lon"}, inplace=True)

        return df_sellers_first_location

    st.header("Top Sellers Brazilian E-Commerce")

    # Create slider to select top N sellers
    top_n = st.slider("Select the number of top sellers to display:", 1, 100, 10)

    # Load and merge data
    df_sellers_geolocation = load_and_merge_data(top_n)

    # Sort the DataFrame by order_count in descending order
    df_sellers_geolocation = df_sellers_geolocation.sort_values(by="order_count", ascending=False)

    # Center coordinates for the map
    CONNECTICUT_CENTER = (-15.793889, -47.882778)
    map = folium.Map(location=CONNECTICUT_CENTER, zoom_start=5)

    # Add markers to the map
    for index, row in df_sellers_geolocation.iterrows():
        location = row["lat"], row["lon"]
        popup_text = f"Seller ID: {row['seller_id']}<br>Order Count: {row['order_count']}"
        folium.Marker(location, popup=popup_text).add_to(map)

    st_folium(map, width=700)

    # Display the sorted table of top N sellers
    st.subheader(f"Top {top_n} Sellers (Sorted by Order Count)")
    st.dataframe(df_sellers_geolocation)
