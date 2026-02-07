import pandas as pd
import os

class OrderService:
    def __init__(self):
        # Aapka absolute path
        self.db_path = r"C:\Users\sumbu\Downloads\DineIQ-pre_main\DineIQ-pre_main\Backend\services\DineIQ_DB.xlsx"

    def track_order(self, order_id):
        """Asli logic jo 'Orders' sheet se status fetch karega"""
        try:
            if not os.path.exists(self.db_path):
                return "❌ Database file nahi mili!"

            # Excel ki 'Orders' sheet read karein
            df = pd.read_excel(self.db_path, sheet_name="Orders")
            
            # Order_ID match karein (Case insensitive aur string format mein)
            df['Order_ID'] = df['Order_ID'].astype(str).str.strip()
            order_data = df[df['Order_ID'].str.upper() == str(order_id).strip().upper()]
            
            if not order_data.empty:
                row = order_data.iloc[0]
                status = row.get('Order_Status', 'UNKNOWN')
                price = row.get('Order_Price', 0)
                customer = row.get('Customer_Name', 'Guest')
                
                # Sunder message return karein
                return f"Namaste {customer}! Aapka order {order_id} abhi '{status}' status par hai. Total bill ₹{price} hai."
            else:
                return f"⚠️ Order ID '{order_id}' hamare record mein nahi mili. Please sahi ID dalein."

        except Exception as e:
            print(f"❌ Order Service Error: {e}")
            return "Server busy hai, please thodi der mein track karein."

    def get_order_history(self, customer_id):
        """Customer ki purani orders ki list nikalna"""
        try:
            df = pd.read_excel(self.db_path, sheet_name="Orders")
            user_orders = df[df['Customer_ID'].astype(str) == str(customer_id)]
            return user_orders.to_dict(orient="records")
        except:
            return []