
import os
import json

#Dataframe of aggregated Transactions
def aggregated_transaction():
   # Specify the base path
    base_path = r'C:\pythan\phonpe project\pulse\data\aggregated\transaction\country\india\state'

    # Initialize a dictionary to store data
    columns1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],
                'Transaction_amount': []}
    
    # Iterate through states
    for state in os.listdir(base_path):
        cur_state = os.path.join(base_path, state)  # Use os.path.join for path concatenation
        if not os.path.isdir(cur_state):
            continue  # Skip if it's not a directory

        # Iterate through years
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)  # Use os.path.join for path concatenation
            if not os.path.isdir(cur_year):
                continue  # Skip if it's not a directory

            for file in os.listdir(cur_year):
                if file.endswith(".json"):
                    cur_file = os.path.join(cur_year, file)  # Use os.path.join for path concatenation
                    with open(cur_file, 'r') as data_file:
                        A = json.load(data_file)
                    
                    for i in A['data']['transactionData']:
                        name = i['name']
                        count = i['paymentInstruments'][0]['count']
                        amount = i['paymentInstruments'][0]['amount']
                        columns1['Transaction_type'].append(name)
                        columns1['Transaction_count'].append(count)
                        columns1['Transaction_amount'].append(amount)
                        columns1['State'].append(state)
                        columns1['Year'].append(year)
                        columns1['Quarter'].append(int(file.strip('.json')))
                    
                    

    return columns1

def aggregated_user():
    # Specify the base path using raw string
    base_path = r'C:\pythan\phonpe project\pulse\data\aggregated\user\country\india\state'

    # Initialize a dictionary to store data
    columns2 = {'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'Count': [],
                'Percentage': []}

    # Iterate through states
    for state in os.listdir(base_path):
        cur_state = os.path.join(base_path, state)  # Use os.path.join for path concatenation
        if not os.path.isdir(cur_state):
            continue  # Skip if it's not a directory

        # Iterate through years
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)  # Use os.path.join for path concatenation
            if not os.path.isdir(cur_year):
                continue  # Skip if it's not a directory

            # Iterate through JSON files
            for file in os.listdir(cur_year):
                if file.endswith(".json"):
                    cur_file = os.path.join(cur_year, file)  # Use os.path.join for path concatenation
                    with open(cur_file, 'r') as data_file:
                        B = json.load(data_file)
                    try:
                        for i in B["data"]["usersByDevice"]:
                            brand_name = i["brand"]
                            counts = i["count"]
                            percents = i["percentage"]
                            columns2["Brands"].append(brand_name)
                            columns2["Count"].append(counts)
                            columns2["Percentage"].append(percents)
                            columns2["State"].append(state)
                            columns2["Year"].append(year)
                            columns2["Quarter"].append(int(file.strip('.json')))
                    except:
                        pass
                    
    return columns2

def map_transaction():
    # Specify the base path using raw string
    base_path = r'C:\pythan\phonpe project\pulse\data\map\transaction\hover\country\india\state'

    # Initialize a dictionary to store data
    columns3 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Count': [],
                'Amount': []}

    # Iterate through states
    for state in os.listdir(base_path):
        cur_state = os.path.join(base_path, state)  # Use os.path.join for path concatenation
        if not os.path.isdir(cur_state):
            continue  # Skip if it's not a directory

        # Iterate through years
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)  # Use os.path.join for path concatenation
            if not os.path.isdir(cur_year):
                continue  # Skip if it's not a directory

            # Iterate through JSON files
            for file in os.listdir(cur_year):
                if file.endswith(".json"):
                    cur_file = os.path.join(cur_year, file)  # Use os.path.join for path concatenation
                    with open(cur_file, 'r') as data_file:
                        C = json.load(data_file)
                    
                    for i in C["data"]["hoverDataList"]:
                        district = i["name"]
                        count = i["metric"][0]["count"]
                        amount = i["metric"][0]["amount"]
                        columns3["District"].append(district)
                        columns3["Count"].append(count)
                        columns3["Amount"].append(amount)
                        columns3['State'].append(state)
                        columns3['Year'].append(year)
                        columns3['Quarter'].append(int(file.strip('.json')))
    return columns3

def map_user():
    # Specify the base path using raw string
    base_path = r'C:\pythan\phonpe project\pulse\data\map\user\hover\country\india\state'

    # Initialize a dictionary to store data
    columns4 = {"State": [], "Year": [], "Quarter": [], "District": [],
                "RegisteredUser": [], "AppOpens": []}

    # Iterate through states
    for state in os.listdir(base_path):
        cur_state = os.path.join(base_path, state)  # Use os.path.join for path concatenation
        if not os.path.isdir(cur_state):
            continue  # Skip if it's not a directory

        # Iterate through years
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)  # Use os.path.join for path concatenation
            if not os.path.isdir(cur_year):
                continue  # Skip if it's not a directory

            # Iterate through JSON files
            for file in os.listdir(cur_year):
                if file.endswith(".json"):
                    cur_file = os.path.join(cur_year, file)  # Use os.path.join for path concatenation
                    with open(cur_file, 'r') as data_file:
                        D = json.load(data_file)
                    
                    for district, data in D["data"]["hoverData"].items():
                        registereduser = data["registeredUsers"]
                        appOpens = data['appOpens']
                        columns4["District"].append(district)
                        columns4["RegisteredUser"].append(registereduser)
                        columns4["AppOpens"].append(appOpens)
                        columns4['State'].append(state)
                        columns4['Year'].append(year)
                        columns4['Quarter'].append(int(file.strip('.json')))
    return columns4


def top_transaction_district():
    # Specify the base path using a raw string
    base_path = r'C:\pythan\phonpe project\pulse\data\top\transaction\country\india\state'
    # Initialize a dictionary to store data
    columns5 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Transaction_count': [],
                'Transaction_amount': []}

    # Iterate through states
    for state in os.listdir(base_path):
        cur_state = os.path.join(base_path, state)  # Use os.path.join for path concatenation
        if not os.path.isdir(cur_state):
            continue  # Skip if it's not a directory

        # Iterate through years
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)  # Use os.path.join for path concatenation
            if not os.path.isdir(cur_year):
                continue  # Skip if it's not a directory

            # Iterate through JSON files
            for file in os.listdir(cur_year):
                if file.endswith(".json"):
                    cur_file = os.path.join(cur_year, file)  # Use os.path.join for path concatenation
                    with open(cur_file, 'r') as data_file:
                        E = json.load(data_file)
                    
                    for i in E['data']['districts']:
                        name = i['entityName']
                        count = i['metric']['count']
                        amount = i['metric']['amount']
                        columns5['District'].append(name)
                        columns5['Transaction_count'].append(count)
                        columns5['Transaction_amount'].append(amount)
                        columns5['State'].append(state)
                        columns5['Year'].append(year)
                        columns5['Quarter'].append(int(file.strip('.json')))
    return columns5


def top_transaction_pincode():
    # Specify the base path using a raw string
    base_path = r'C:\pythan\phonpe project\pulse\data\top\transaction\country\india\state'

    # Initialize a dictionary to store data
    columns6 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Transaction_count': [],
                'Transaction_amount': []}

    # Iterate through states
    for state in os.listdir(base_path):
        cur_state = os.path.join(base_path, state)  # Use os.path.join for path concatenation
        if not os.path.isdir(cur_state):
            continue  # Skip if it's not a directory

        # Iterate through years
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)  # Use os.path.join for path concatenation
            if not os.path.isdir(cur_year):
                continue  # Skip if it's not a directory

            # Iterate through JSON files
            for file in os.listdir(cur_year):
                if file.endswith(".json"):
                    cur_file = os.path.join(cur_year, file)  # Use os.path.join for path concatenation
                    with open(cur_file, 'r') as data_file:
                        F = json.load(data_file)
                    
                    for i in F['data']['pincodes']:
                        name = i['entityName']
                        count = i['metric']['count']
                        amount = i['metric']['amount']
                        columns6['Pincode'].append(name)
                        columns6['Transaction_count'].append(count)
                        columns6['Transaction_amount'].append(amount)
                        columns6['State'].append(state)
                        columns6['Year'].append(year)
                        columns6['Quarter'].append(int(file.strip('.json')))
    return columns6



def top_user_district():
    # Specify the base path using a raw string
    base_path = r'C:\pythan\phonpe project\pulse\data\top\user\country\india\state'
    # Initialize a dictionary to store data
    columns7 = {'State': [], 'Year': [], 'Quarter': [], 'District': [],
                'RegisteredUsers': []}

    # Iterate through states
    for state in os.listdir(base_path):
        cur_state = os.path.join(base_path, state)  # Use os.path.join for path concatenation
        if not os.path.isdir(cur_state):
            continue  # Skip if it's not a directory

        # Iterate through years
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)  # Use os.path.join for path concatenation
            if not os.path.isdir(cur_year):
                continue  # Skip if it's not a directory

            # Iterate through JSON files
            for file in os.listdir(cur_year):
                if file.endswith(".json"):
                    cur_file = os.path.join(cur_year, file)  # Use os.path.join for path concatenation
                    with open(cur_file, 'r') as data_file:
                        G = json.load(data_file)
                    
                    for i in G['data']['districts']:
                        name = i['name']
                        registeredUsers = i['registeredUsers']
                        columns7['District'].append(name)
                        columns7['RegisteredUsers'].append(registeredUsers)
                        columns7['State'].append(state)
                        columns7['Year'].append(year)
                        columns7['Quarter'].append(int(file.strip('.json')))
    return columns7


def top_user_pincode():
    # Specify the base path using a raw string
    base_path = r'C:\pythan\phonpe project\pulse\data\top\user\country\india\state'

    # Initialize a dictionary to store data
    columns8 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [],
                'RegisteredUsers': []}

    # Iterate through states
    for state in os.listdir(base_path):
        cur_state = os.path.join(base_path, state)  # Use os.path.join for path concatenation
        if not os.path.isdir(cur_state):
            continue  # Skip if it's not a directory

        # Iterate through years
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)  # Use os.path.join for path concatenation
            if not os.path.isdir(cur_year):
                continue  # Skip if it's not a directory

            # Iterate through JSON files
            for file in os.listdir(cur_year):
                if file.endswith(".json"):
                    cur_file = os.path.join(cur_year, file)  # Use os.path.join for path concatenation
                    with open(cur_file, 'r') as data_file:
                        H = json.load(data_file)
                    
                    for i in H['data']['pincodes']:
                        name = i['name']
                        registeredUsers = i['registeredUsers']
                        columns8['Pincode'].append(name)
                        columns8['RegisteredUsers'].append(registeredUsers)
                        columns8['State'].append(state)
                        columns8['Year'].append(year)
                        columns8['Quarter'].append(int(file.strip('.json')))
    return columns8