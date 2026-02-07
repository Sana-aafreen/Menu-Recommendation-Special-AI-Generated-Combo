import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Step 1: Fix Path for nested directories
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Step 2: Load Environment
load_dotenv()

try:
    from agents.recommendation_agent import RecommendationAgent
except ImportError:
    # Fallback if running from a different directory
    sys.path.append(os.path.dirname(current_dir))
    from agents.recommendation_agent import RecommendationAgent

def run_test():
    print("--- 🔍 Initializing DineIQ System Check ---")
    agent = RecommendationAgent()
    
    # 3. Create Dummy Menu (Matches your Google Sheets structure)
    menu_data = pd.DataFrame([
        {'ID': 'M1', 'Name': 'Paneer Tikka', 'Cuisine': 'Punjabi', 'Category': 'Starter', 'Dietary': 'Veg', 'Tags': 'Spicy, Grilled', 'Price': 300},
        {'ID': 'M2', 'Name': 'Butter Chicken', 'Cuisine': 'North Indian', 'Category': 'Main', 'Dietary': 'Non-Veg', 'Tags': 'Creamy', 'Price': 450},
        {'ID': 'M3', 'Name': 'Dal Makhani', 'Cuisine': 'Punjabi', 'Category': 'Main', 'Dietary': 'Veg', 'Tags': 'Rich', 'Price': 250},
        {'ID': 'M4', 'Name': 'Masala Dosa', 'Cuisine': 'South Indian', 'Category': 'Breakfast', 'Dietary': 'Veg', 'Tags': 'Light', 'Price': 150}
    ])

    # 4. Scenario: User "Sumit" with Veg Punjabi preference
    user_prefs = {'diet': 'Veg', 'cuisine': 'Punjabi'}
    
    # 5. Get ML Results
    # Mocking interaction: User previously added Dal Makhani to cart
    mock_history = {'M3': 5} 
    
    results = agent.get_recommendations(user_prefs, menu_data, interaction_history=mock_history, top_n=2)
    
    print("\n✅ ML Recommendation Success:")
    for idx, row in results.iterrows():
        print(f"- Item: {row['Name']} | Rank Score: {row['final_score']:.2f}")

    # 6. Get LLM Message
    rec_names = results['Name'].tolist()
    message = agent.generate_hinglish_reason("Sumit", rec_names)
    
    print("\n✅ Groq LLM Response (Hinglish):")
    print(message)

if __name__ == "__main__":
    run_test()