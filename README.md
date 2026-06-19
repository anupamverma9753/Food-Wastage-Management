# 🍲 Food Wastage Management Platform

An interactive, SQL-powered data analytics and CRUD platform built using **Streamlit**, **PostgreSQL**, and **Python**. This application serves as a bridge between surplus food providers (supermarkets, restaurants, caterers) and receivers (NGOs, shelters, charities) to streamline surplus food redistribution and track wastage velocity.

---

## 🚀 Key Features

* **Interactive Dashboard:** Complete oversight of existing surplus inventory across different locations with customizable search filters.
* **Full CRUD Operational Control:** Easily insert new listings with unique identifiers, update quantities or fulfillment locations, and safely purge expired items from the active database.
* **Communications Directory:** Direct outreach tracking matrices for both active supply providers and registered demand receivers (NGOs).
* **Deep-Dive SQL Analytics Engine:** 15+ complex production analytical queries visualized dynamically into responsive **Pie Charts** and **Bar Charts** powered by Plotly Express.

---

## 📊 Core Analytics Insights Provided

1. **Top Contributing Food Providers:** Identifies the highest frequency contributors driving the supply chain and total item counts.
2. **High-Demand Fulfillment Locations:** Visualizes transaction hotspots based on claim frequencies to improve distribution routes.
3. **Food Wastage & Distribution Trends:** Flags expired vs. successfully saved items across specific food categories (Vegan, Vegetarian, Non-Vegetarian) to measure efficiency rates.

---

## 📂 Project Directory Structure

```text
Food-Wastage-Management/
│
├── .gitignore                      # Blocks python cache, notebooks checkpoints, and secrets
├── requirements.txt                # Lists external python dependencies for Streamlit Cloud
├── README.md                       # Documentation of the project framework
│
├── Data/                           # Local directory hosting the pipeline datasets
│   ├── claims_cleaned.csv
│   ├── food_listings_cleaned.csv
│   ├── providers_cleaned.csv
│   └── recevers_cleaned.csv
│
└── Source/                         # Source application engine scripts
    ├── app.py                      # Main Streamlit interface entry point
    └── queries.py                  # Core SQLQueries utility library class
