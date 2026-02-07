import pandas as pd

class DataFetcher:
    def __init__(self):
        # File names as per your DB
        self.menu_path = "DineIQ_DB.xlsx - Menu.csv"
        self.pref_path = "DineIQ_DB.xlsx - Customer_Preferences.csv"
        self.orders_path = "DineIQ_DB.xlsx - Orders.csv"
        self.items_path = "DineIQ_DB.xlsx - Order_Items.csv"
        self.chats_path = "DineIQ_DB.xlsx - Chats.csv"

    def get_user_context(self, email, cust_id):
        # 1. Get Base Preferences
        prefs = pd.read_csv(self.pref_path)
        user_row = prefs[prefs['Email'] == email].iloc[0]
        
        # 2. Get Chat Intent (latest 2 messages)
        chats = pd.read_csv(self.chats_path)
        user_chats = chats[chats['Customer_ID'] == cust_id]
        chat_intent = " ".join(user_chats['Chat_Session_Text'].tail(2).astype(str))

        # 3. Get Feedback History (Orders = 5 points)
        orders = pd.read_csv(self.orders_path)
        order_items = pd.read_csv(self.items_path)
        
        user_orders = orders[orders['Customer_ID'] == cust_id]['Order_ID']
        past_items = order_items[order_items['Order_ID'].isin(user_orders)]
        
        history = {}
        for item_id in past_items['Item_ID']:
            history[item_id] = history.get(item_id, 0) + 5
            
        return {
            'prefs': {
                'diet': user_row['Dietary'],
                'cuisine': user_row['Main Course'],
                'chat_intent': chat_intent
            },
            'history': history,
            'name': user_row.get('Customer_Name', 'Guest')
        }

    def get_menu(self):
        return pd.read_csv(self.menu_path)