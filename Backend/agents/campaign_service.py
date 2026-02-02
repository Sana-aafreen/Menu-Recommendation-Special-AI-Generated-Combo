# agents/campaign_service.py

class CampaignService:
    def __init__(self):
        self.active_offers = ["DINE10", "WELCOME50"]

    def get_active_campaigns(self):
        """Active marketing campaigns aur discounts return karta hai"""
        return {
            "campaigns": [
                {"id": "C1", "name": "Weekend Special", "discount": "10%"},
                {"id": "C2", "name": "Happy Hours", "discount": "15%"}
            ]
        }