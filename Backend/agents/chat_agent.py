import os
from groq import Groq

class ChatAgent:
    def __init__(self):
        # Aapki provided Groq API Key
        self.api_key = "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" 
        self.client = Groq(api_key=self.api_key)

    def process_message(self, customer_id, message, history):
        try:
            # System prompt ko aur friendly banaya gaya hai
            system_prompt = (
                f"You are a friendly and smart AI Waiter for DineIQ restaurant. "
                f"The customer you are talking to is {customer_id}. "
                "Always respond in natural Hinglish (Hindi + English mix). "
                "Keep your responses short, helpful, and slightly witty. "
                "If the user is confused, suggest the 'Mix Vegetables' or 'Aloo Baingan' from our menu."
            )
            
            # Context build karne ke liye messages ki list
            messages = [{"role": "system", "content": system_prompt}]
            
            # Purani baatein (History) add karna
            for msg in history[-3:]:  # Sirf last 3 baatein yaad rakhega
                messages.append({"role": "user", "content": str(msg)})
                
            # Current message add karna
            messages.append({"role": "user", "content": message})
            
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.8, # Thoda creative banane ke liye
                max_tokens=150
            )
            
            return completion.choices[0].message.content

        except Exception as e:
            print(f"❌ Groq Error: {e}")
            return f"Arre {customer_id} ji, lagta hai mera net thoda slow hai. Par aap chinta mat kijiye, hamara Mix Veg ekdam fresh hai, wahi order kar dein?"

    def get_latest_intent(self, customer_id):
        # Default intent
        return "General Query"