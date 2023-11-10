
# phonepe_project

## About phonepe pulse
    The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With over 45% market share, PhonePe's data is representative of the country's digital payment habits. The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.
## Introduction
    PhonePe has become a leader among digital payment platforms, serving millions of users for their daily transactions. Known for its easy-to-use design, fast and secure payment processing, and creative features, PhonePe has gained praise and recognition in the industry. The PhonePe Pulse Data Visualization and Exploration project aims to gather valuable information from PhonePe's GitHub repository, process the data, and present it using an interactive dashboard that's visually appealing. This is accomplished using Python, Streamlit, and Plotly.
## Key Technologies and Skills
```bash
* Github Cloning
* Python
* Pandas
* MYSQL
* Streamlit
* Plotly
```
## Programming hints
```http
Write the program to below content
1) Clone the repository: git clone https://github.com/gopiashokan/Phonepe-Pulse-Data-Visualization-and-Exploration.git

2)Install the required packages: pip install -r requirements.txt

3)Extract the data and store the data to MYSQL

4)Run the Streamlit app: streamlit run app.py

5)Access the app in your browser at http://localhost:8501
```

## Installation
Install need project packages

```bash
import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
import numpy as np
import mysql.connector
from sqlalchemy import create_engine

```
## Github clone
```bash
First need to clone phonepe pulse github Data to my local system

    git.Repo.clone_from("https://github.com/PhonePe/pulse.git", 'phonepe_pulse_git')
    ```


## Data extraction
In this step the JSON files that are available in the folders are converted into the readeable and understandable DataFrame format by using the for loop and iterating file by file and then finally the DataFrame is created.
##  Data storage
    The collected data can be stored in a variety of ways but In this project, we will use  
```http
* SQL-. SQL is a relational database that is well-suited for querying and analyzing structured data.
* First need to create the connection between python and mysql
* create the table queries
* Data inserted into MYSQL database
```
## Streamlit
```http
 The data can be analyzed using a variety of tools. In this project, we will use Streamlit. 
 Streamlit is a Python library that can be used to create interactive web applications.  
 We will use Streamlit to create a dashboard that allows users to visualize and analyze the data.
```
## Plotly
```bash
    Utilizing the power of Plotly, users can create various types of charts, including line charts, bar charts, scatter plots, pie charts, and more. These visualizations enhance the understanding of the data and make it easier to identify patterns, trends, and correlations.
    ```