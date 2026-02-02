# Backend/services/auth_service.py

class AuthService:
    def authenticate(self, email, password):
        # Temporary logic for testing
        if email and password:
            return {"Customer_ID": "Cust_0001", "Customer_Name": "Guest User"}
        return None