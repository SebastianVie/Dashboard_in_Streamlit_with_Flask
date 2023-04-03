# Capstone2023
# My Capstone for H&M Web App

This is the README documentation for the My Capstone for H&M web app. This web app is designed to visualize and analyze customer transaction and article data.

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Features](#features)
- [H&M Business Data API](#hm-business-data-api)
- [Authors](#authors)

## Installation

To install the web app, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the web app using `streamlit run app.py`.

## Requirements

- Python 3.6 or higher
- SQLAlchemy==1.4.40
- Flask
- flask_restx
- pandas
- numpy
- streamlit
- plotly.express
- streamlit_authenticator
- altair
- pyyaml
- requests
- gunicorn
- PyMySQL==1.0.2

## Usage

After running the web app, you will be greeted with a login page. Enter your credentials to access the main dashboard.

## Features

The web app provides the following features:

1. **KPI Dashboard**: Displays key performance indicators such as the number of active customers, average age, club membership percentage, average articles purchased, total revenue, and average price of articles sold.
2. **Interactive Visualizations**: Several interactive visualizations are included to help you explore the data and identify trends and patterns. These visualizations include age distribution, club membership status, fashion news frequency, sales by sales channel, product type, department, color group, and more.
3. **Data Filtering**: The sidebar contains various filters that allow you to customize the data displayed in the visualizations. You can filter the data based on age, club membership status, fashion news frequency, sales channel, product type, department, and color group.
4. **Authentication**: The web app is protected by a login system to ensure only authorized users can access the data.

# **H&M Business Data API**

This API is designed to request and receive data from the H&M MySQL database. It is built using Flask and Flask-Restx.

## Table of Contents

* [Getting Started](#getting-started)
* [Prerequisites](#prerequisites)
* [API Key](#api-key)
* [API Endpoints](#api-endpoints)
  * [Customers](#customers)
  * [Transactions](#transactions)
  * [Articles](#articles)
  * [Merged Data](#merged-data)
* [Usage](#usage)
* [Authors](#authors)

## **Getting Started**

These instructions will guide you on how to use the H&M Business Data API.

### **Prerequisites**

To use the API, you will need the following dependencies:

- Flask
- Flask-RESTx
- SQLAlchemy
- PyMySQL

Install the required dependencies using **`pip`**:

```
pip install Flask Flask-RESTx SQLAlchemy PyMySQL
```

### **API Key**

An API key is required for authentication. The API key for this project is **`Capstone2023`**.

### **API Endpoints**

The API is organized into several namespaces, each with their own set of endpoints:

1. Customers
2. Transactions
3. Articles
4. Merged Data

### Customers

- **GET** **`/api/v1/customers/customers`**
    
    Retrieves a limited 10000 customer rows from the **`customers`** table.
    

### Transactions

- **GET** **`/api/v1/transactions/transactions`**
    
    Retrieves a limited 10000 transaction rows from the **`transactions`** table.
    

### Articles

- **GET** **`/api/v1/articles/articles`**
    
    Retrieves a limited 10000 article rows from the **`articles`** table.
    

### Merged Data

- **GET** **`/api/v1/merged/merged`**
    
    Retrieves a limited 10000 rows from the **`merged`** table.
    

### **Usage**

To use the API, include the **`X-API-KEY`** header with the value **`Capstone2023`** in your HTTP requests.

## **Authors**

- Sebastian Viehhofer - **[sebastian.viehhofer@student.ie.edu](mailto:sebastian.viehhofer@student.ie.edu)**

##
![image](https://user-images.githubusercontent.com/114749515/229496281-d911beae-6fa4-4c04-a91e-9499723f9097.png)
