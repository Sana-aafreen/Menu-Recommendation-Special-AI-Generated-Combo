import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8002"

st.set_page_config(
    page_title="DineIQ | Order Now", 
    layout="wide", 
    page_icon="🍽️",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS - Food-Themed Warm Colors ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container - Warm cream background */
    .main {
        background: linear-gradient(180deg, #fff9f0 0%, #ffe8cc 50%, #ffd8a8 100%);
        background-attachment: fixed;
    }
    
    /* Header Styles - Tomato Red to Orange Gradient */
    .food-header {
        background: linear-gradient(135deg, #ff4757 0%, #ff6348 50%, #ff793f 100%);
        padding: 25px 40px;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 8px 32px rgba(255, 71, 87, 0.3);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    
    .food-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .header-title {
        color: white;
        font-size: 48px;
        font-weight: 800;
        margin: 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 18px;
        margin-top: 8px;
        position: relative;
        z-index: 1;
    }
    
    /* Section Headers - Orange gradient */
    .section-header {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #ff6348 0%, #ff9068 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 35px 0 25px 0;
        padding-left: 20px;
        border-left: 6px solid #ff6348;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Food Card Styles - White with warm shadows */
    .food-card {
        background: linear-gradient(145deg, #ffffff 0%, #fffbf7 100%);
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 4px 16px rgba(255, 99, 72, 0.12);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid transparent;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .food-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 32px rgba(255, 99, 72, 0.25);
        border-color: #ff6348;
    }
    
    .food-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #ff4757, #ff6348, #ffa502);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .food-card:hover::after {
        opacity: 1;
    }
    
    /* Veg/Non-Veg Indicators */
    .veg-indicator {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2.5px solid #38a169;
        border-radius: 4px;
        position: relative;
        vertical-align: middle;
        margin-right: 8px;
    }
    
    .veg-indicator::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 10px;
        height: 10px;
        background: #38a169;
        border-radius: 50%;
    }
    
    .non-veg-indicator {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2.5px solid #dc2626;
        border-radius: 4px;
        position: relative;
        vertical-align: middle;
        margin-right: 8px;
    }
    
    .non-veg-indicator::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 0;
        height: 0;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-bottom: 8px solid #dc2626;
        transform: translate(-50%, -50%) rotate(0deg);
    }
    
    .food-name {
        font-size: 19px;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 10px;
        line-height: 1.3;
    }
    
    .food-price {
        font-size: 24px;
        font-weight: 800;
        background: linear-gradient(135deg, #ff4757 0%, #ff6348 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 10px 0;
    }
    
    /* Tags with warm food colors */
    .food-tag {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        margin-top: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .bestseller-tag {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: #78350f;
        box-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
    }
    
    .premium-tag {
        background: linear-gradient(135deg, #ff6348 0%, #ff4757 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(255, 71, 87, 0.3);
    }
    
    .value-tag {
        background: linear-gradient(135deg, #68d391 0%, #48bb78 100%);
        color: #22543d;
        box-shadow: 0 2px 8px rgba(104, 211, 145, 0.3);
    }
    
    .favorite-tag {
        background: linear-gradient(135deg, #fca5a5 0%, #f87171 100%);
        color: #7f1d1d;
        box-shadow: 0 2px 8px rgba(252, 165, 165, 0.3);
    }
    
    /* Button Styles - Gradient red to orange */
    .stButton > button {
        background: linear-gradient(135deg, #ff4757 0%, #ff6348 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(255, 71, 87, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 14px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(255, 71, 87, 0.4);
        background: linear-gradient(135deg, #ff3838 0%, #ff5538 100%);
    }
    
    /* Recommendation Card - Orange cream gradient */
    .rec-card {
        background: linear-gradient(135deg, #fff4e6 0%, #ffe4cc 100%);
        border: 3px solid #ffa94d;
        border-radius: 20px;
        padding: 25px;
        margin: 25px 0;
        box-shadow: 0 8px 24px rgba(255, 169, 77, 0.2);
    }
    
    .rec-title {
        font-size: 26px;
        font-weight: 800;
        color: #c2410c;
        margin-bottom: 12px;
    }
    
    .rec-pitch {
        background: white;
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #ff6348;
        margin: 18px 0;
        font-size: 16px;
        color: #2d3748;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Combo Card - Golden yellow gradient */
    .combo-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 50%, #fcd34d 100%);
        border: 4px solid #f59e0b;
        border-radius: 24px;
        padding: 35px;
        margin: 25px 0;
        box-shadow: 0 12px 32px rgba(245, 158, 11, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .combo-card::before {
        content: '✨';
        position: absolute;
        top: 15px;
        right: 15px;
        font-size: 48px;
        opacity: 0.3;
    }
    
    .combo-title {
        font-size: 36px;
        font-weight: 800;
        color: #78350f;
        margin-bottom: 12px;
        font-family: 'Caveat', cursive;
        letter-spacing: 1px;
    }
    
    .combo-desc {
        font-size: 18px;
        color: #92400e;
        font-weight: 500;
        margin-bottom: 25px;
        line-height: 1.6;
    }
    
    /* Cart Badge - Red gradient */
    .cart-badge {
        background: linear-gradient(135deg, #ff4757 0%, #ff6348 100%);
        color: white;
        border-radius: 50%;
        padding: 6px 12px;
        font-size: 15px;
        font-weight: 800;
        box-shadow: 0 2px 8px rgba(255, 71, 87, 0.3);
    }
    
    /* Coupon Card - White with colorful borders */
    .coupon-card {
        background: white;
        border: 3px dashed #cbd5e1;
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .coupon-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 6px;
        background: linear-gradient(180deg, #ff4757, #ffa502);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .coupon-card:hover {
        border-color: #ff6348;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe8e5 100%);
        transform: translateX(5px);
    }
    
    .coupon-card:hover::before {
        opacity: 1;
    }
    
    .coupon-code {
        font-size: 20px;
        font-weight: 800;
        background: linear-gradient(135deg, #ff4757 0%, #ffa502 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Courier New', monospace;
        letter-spacing: 1px;
    }
    
    .coupon-available {
        border-color: #48bb78;
        background: linear-gradient(135deg, #f0fff4 0%, #e6ffec 100%);
    }
    
    .coupon-locked {
        opacity: 0.5;
        cursor: not-allowed;
    }
    
    /* Price Breakdown */
    .price-row {
        display: flex;
        justify-content: space-between;
        padding: 15px 0;
        border-bottom: 2px solid #fff7ed;
        font-size: 16px;
        font-weight: 500;
    }
    
    .price-total {
        font-size: 28px;
        font-weight: 800;
        padding: 25px 0;
        border-top: 3px solid #ff6348;
        color: #2d3748;
    }
    
    .discount-green {
        color: #38a169;
        font-weight: 700;
    }
    
    /* Loyalty Badge - Gradient styles */
    .loyalty-badge {
        display: inline-block;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: 800;
        font-size: 15px;
        margin: 8px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .bronze {
        background: linear-gradient(135deg, #d4a574 0%, #b08968 100%);
        color: white;
    }
    
    .silver {
        background: linear-gradient(135deg, #e5e7eb 0%, #cbd5e1 100%);
        color: #1e293b;
    }
    
    .gold {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: #78350f;
    }
    
    .platinum {
        background: linear-gradient(135deg, #c084fc 0%, #a855f7 100%);
        color: white;
    }
    
    /* Upsell Nudge - Yellow orange gradient */
    .upsell-nudge {
        background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
        border-left: 5px solid #f59e0b;
        padding: 18px 24px;
        border-radius: 12px;
        margin: 18px 0;
        font-size: 16px;
        font-weight: 700;
        color: #92400e;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 80px 20px;
    }
    
    .empty-icon {
        font-size: 100px;
        margin-bottom: 25px;
        filter: drop-shadow(0 4px 12px rgba(255, 99, 72, 0.2));
    }
    
    .empty-text {
        font-size: 24px;
        color: #4a5568;
        margin-bottom: 12px;
        font-weight: 700;
    }
    
    /* Category Badge */
    .category-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .cat-rice {
        background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
        color: #9a3412;
        border: 1px solid #fed7aa;
    }
    
    .cat-bread {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #78350f;
        border: 1px solid #fcd34d;
    }
    
    .cat-gravy {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #7f1d1d;
        border: 1px solid #fca5a5;
    }
    
    .cat-snacks {
        background: linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%);
        color: #9a3412;
        border: 1px solid #fdba74;
    }
    
    .cat-beverage {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #1e3a8a;
        border: 1px solid #93c5fd;
    }
    
    .cat-smoothie {
        background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
        color: #831843;
        border: 1px solid #f9a8d4;
    }
    
    /* Animation */
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    .animate-slide {
        animation: slideUp 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .animate-fade {
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .header-title {
            font-size: 32px;
        }
        .section-header {
            font-size: 24px;
        }
        .food-card {
            padding: 18px;
        }
    }
    
    /* Scrollbar - Orange theme */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #fff7ed;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #ff6348, #ffa502);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #ff4757, #ff7f50);
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'last_rec' not in st.session_state:
    st.session_state.last_rec = None
if 'page' not in st.session_state:
    st.session_state.page = "menu"
if 'show_combo' not in st.session_state:
    st.session_state.show_combo = False
if 'selected_coupon' not in st.session_state:
    st.session_state.selected_coupon = None
if 'show_rec_for_item' not in st.session_state:
    st.session_state.show_rec_for_item = None

# --- Helper Functions ---
def is_veg(item_name):
    """Check if item is vegetarian"""
    non_veg_keywords = ['chicken', 'mutton', 'egg', 'fish', 'meat', 'prawn', 'lamb']
    return not any(keyword in item_name.lower() for keyword in non_veg_keywords)

def get_veg_indicator(item_name):
    """Get veg/non-veg HTML indicator"""
    if is_veg(item_name):
        return '<span class="veg-indicator"></span>'
    else:
        return '<span class="non-veg-indicator"></span>'

def get_category_class(category):
    """Get CSS class for category badge"""
    category_lower = str(category).lower()
    if 'rice' in category_lower:
        return 'cat-rice'
    elif 'bread' in category_lower:
        return 'cat-bread'
    elif 'gravy' in category_lower:
        return 'cat-gravy'
    elif 'snack' in category_lower:
        return 'cat-snacks'
    elif 'beverage' in category_lower:
        return 'cat-beverage'
    elif 'smoothie' in category_lower:
        return 'cat-smoothie'
    return 'cat-rice'

def add_to_cart(item):
    st.session_state.cart.append(item)
    st.session_state.show_rec_for_item = item['Item_ID']

def remove_from_cart(index):
    st.session_state.cart.pop(index)

def go_to_checkout():
    st.session_state.page = "checkout"

def go_to_menu():
    st.session_state.page = "menu"
    st.session_state.show_rec_for_item = None

def calculate_cart_total():
    return sum(item.get('Current_Price', 0) for item in st.session_state.cart)

# --- TOP NAVIGATION BAR ---
col_logo, col_nav, col_cart = st.columns([2, 6, 2])

with col_logo:
    st.markdown('<h1 style="background: linear-gradient(135deg, #ff4757 0%, #ffa502 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; font-size: 36px; font-weight: 800;">🍽️ DineIQ</h1>', unsafe_allow_html=True)

with col_nav:
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        if st.button("🏠 Menu", use_container_width=True, type="secondary" if st.session_state.page == "checkout" else "primary"):
            go_to_menu()
            st.rerun()
    with nav_col2:
        if st.session_state.cart:
            cart_count = len(st.session_state.cart)
            if st.button(f"🛒 Cart ({cart_count})", use_container_width=True, type="primary" if st.session_state.page == "checkout" else "secondary"):
                go_to_checkout()
                st.rerun()

with col_cart:
    if st.session_state.cart:
        total = calculate_cart_total()
        st.markdown(f'<div style="text-align: right; padding: 10px;"><span style="font-size: 22px; font-weight: 800; background: linear-gradient(135deg, #ff4757, #ff6348); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">₹{total}</span></div>', unsafe_allow_html=True)

st.markdown("---")

# Email input
email = st.text_input("📧 Your Email", "parag.dubey@webisdom.com", label_visibility="collapsed", placeholder="Enter your email")

st.markdown("<br>", unsafe_allow_html=True)

# ==================== MENU PAGE ====================
if st.session_state.page == "menu":
    
    # Header
    st.markdown("""
    <div class="food-header animate-slide">
        <h1 class="header-title">🍕 Discover Delicious Food</h1>
        <p class="header-subtitle">🎯 Fresh, Hot & Personalized just for you</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Combo Section
    st.markdown('<div class="section-header">🎊 Special AI Combo</div>', unsafe_allow_html=True)
    
    if st.button("🤖 Generate My Perfect Combo", use_container_width=True, type="primary"):
        st.session_state.show_combo = True
        st.rerun()
    
    if st.session_state.show_combo:
        with st.spinner("🔮 AI Chef is preparing your personalized combo..."):
            try:
                combo_res = requests.post(f"{API_URL}/create-combo", json={"customer_email": email})
                
                if combo_res.status_code == 200:
                    combo_data = combo_res.json()
                    
                    if combo_data.get('status') == 'success':
                        combo = combo_data['combo']
                        
                        st.markdown(f"""
                        <div class="combo-card animate-slide">
                            <h2 class="combo-title">✨ {combo['combo_name']}</h2>
                            <p class="combo-desc">{combo['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Combo items in grid
                        item_cols = st.columns(len(combo['items']))
                        for idx, item in enumerate(combo['items']):
                            with item_cols[idx]:
                                veg_html = get_veg_indicator(item['Item_Name'])
                                cat_class = get_category_class(item.get('Item_Category', ''))
                                
                                st.markdown(f"""
                                <div class="food-card">
                                    {veg_html}
                                    <div class="food-name">{item['Item_Name']}</div>
                                    <div class="food-price">₹{item['Current_Price']}</div>
                                    <span class="category-badge {cat_class}">{item.get('Item_Category', 'Item')}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Pricing
                        price_col1, price_col2, price_col3 = st.columns(3)
                        with price_col1:
                            st.metric("Original Price", f"₹{combo['original_price']}", delta=None)
                        with price_col2:
                            st.metric("Combo Price", f"₹{combo['combo_price']}", delta=f"-₹{combo['savings']}")
                        with price_col3:
                            st.markdown(f'<div style="background: linear-gradient(135deg, #48bb78, #38a169); color: white; padding: 20px; border-radius: 12px; text-align: center; font-size: 20px; font-weight: 800;">{combo["discount_percent"]}% OFF 🎉</div>', unsafe_allow_html=True)
                        
                        col_btn1, col_btn2 = st.columns([3, 1])
                        with col_btn1:
                            if st.button("🛒 Add Entire Combo to Cart", type="primary", use_container_width=True):
                                for item in combo['items']:
                                    add_to_cart(item)
                                st.session_state.show_combo = False
                                st.success("✅ Combo added to cart!")
                                st.rerun()
                        with col_btn2:
                            if st.button("❌ Close", use_container_width=True):
                                st.session_state.show_combo = False
                                st.rerun()
                    else:
                        st.warning("⚠️ Could not create combo. Try again!")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Get Smart Menu
    try:
        menu_res = requests.post(f"{API_URL}/menu", json={"customer_email": email})
        
        if menu_res.status_code == 200:
            menu_data = menu_res.json()
            menu_sections = menu_data.get('menu', {}).get('menu_sections', {})
            
            # Define section order with food emojis
            section_order = [
                ("Your Favorites ⭐", "⭐", "favorite-tag"),
                ("Popular Items 🔥", "🔥", "bestseller-tag"),
                ("Premium Selection 👑", "👑", "premium-tag"),
                ("Budget Friendly 💰", "💰", "value-tag"),
                ("Recommended 👍", "👍", "food-tag")
            ]
            
            # Display ordered sections
            for section_name, icon, tag_class in section_order:
                if section_name in menu_sections:
                    items = menu_sections[section_name]
                    if items:
                        st.markdown(f'<div class="section-header">{section_name}</div>', unsafe_allow_html=True)
                        
                        # Show items in grid (4 columns)
                        cols = st.columns(4)
                        for idx, item in enumerate(items[:8]):  # Max 8 items per section
                            with cols[idx % 4]:
                                veg_html = get_veg_indicator(item['Item_Name'])
                                cat_class = get_category_class(item.get('Item_Category', ''))
                                tag_html = f'<span class="{tag_class}">{item.get("tag", "")}</span>' if item.get('tag') else ''
                                
                                st.markdown(f"""
                                <div class="food-card animate-fade">
                                    {veg_html}
                                    <div class="food-name">{item['Item_Name']}</div>
                                    <div class="food-price">₹{item['Current_Price']}</div>
                                    <span class="category-badge {cat_class}">{item.get('Item_Category', 'Item')}</span>
                                    {tag_html}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if st.button("➕ Add", key=f"add_{section_name}_{item['Item_ID']}_{idx}", use_container_width=True):
                                    add_to_cart(item)
                                    st.rerun()
                        
                        st.markdown("<br>", unsafe_allow_html=True)
            
            # Show category-wise items
            st.markdown('<div class="section-header">📂 Browse by Category</div>', unsafe_allow_html=True)
            
            # Get all category sections
            category_sections = {k: v for k, v in menu_sections.items() if k not in [s[0] for s in section_order]}
            
            for category, items in category_sections.items():
                if items:
                    with st.expander(f"🍴 {category} ({len(items)} items)", expanded=False):
                        cat_cols = st.columns(4)
                        for idx, item in enumerate(items[:12]):
                            with cat_cols[idx % 4]:
                                veg_html = get_veg_indicator(item['Item_Name'])
                                cat_class = get_category_class(item.get('Item_Category', ''))
                                
                                st.markdown(f"""
                                <div class="food-card">
                                    {veg_html}
                                    <div class="food-name">{item['Item_Name']}</div>
                                    <div class="food-price">₹{item['Current_Price']}</div>
                                    <span class="category-badge {cat_class}">{item.get('Item_Category', 'Item')}</span>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if st.button("➕ Add", key=f"cat_{category}_{item['Item_ID']}_{idx}", use_container_width=True):
                                    add_to_cart(item)
                                    st.rerun()
    
    except Exception as e:
        st.error(f"⚠️ Could not load menu. Please check if backend is running.")
        st.code(f"Error: {e}")
    
    # Show recommendations if item was just added
    if st.session_state.show_rec_for_item and st.session_state.cart:
        st.markdown('<br><div class="section-header">🤝 Perfect Pairings</div>', unsafe_allow_html=True)
        
        try:
            rec_res = requests.post(
                f"{API_URL}/item-addons",
                json={"customer_email": email, "item_id": st.session_state.show_rec_for_item}
            )
            
            if rec_res.status_code == 200:
                rec_data = rec_res.json()
                smart_recs = rec_data.get('smart_recommendations', {})
                
                # AI Pitch
                ai_pitch = smart_recs.get('ai_pitch', 'Complete your meal with these items!')
                st.markdown(f'<div class="rec-pitch">💡 {ai_pitch}</div>', unsafe_allow_html=True)
                
                # Recommendations
                add_ons = smart_recs.get('add_ons', [])
                if add_ons:
                    rec_cols = st.columns(min(len(add_ons), 3))
                    for i, addon in enumerate(add_ons[:3]):
                        with rec_cols[i]:
                            veg_html = get_veg_indicator(addon['Item_Name'])
                            cat_class = get_category_class(addon.get('Item_Category', ''))
                            tag_html = f'<span class="food-tag bestseller-tag">{addon.get("tag", "")}</span>' if addon.get('tag') else ''
                            
                            st.markdown(f"""
                            <div class="food-card animate-slide">
                                {veg_html}
                                <div class="food-name">{addon['Item_Name']}</div>
                                <div class="food-price">₹{addon['Current_Price']}</div>
                                <span class="category-badge {cat_class}">{addon.get('Item_Category', 'Item')}</span>
                                {tag_html}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button("➕ Add", key=f"rec_{i}_{addon['Item_ID']}", use_container_width=True):
                                add_to_cart(addon)
                                st.success("✅ Added to cart!")
                                st.rerun()
                
                col_dismiss1, col_dismiss2 = st.columns([3, 1])
                with col_dismiss2:
                    if st.button("✖️ Dismiss", use_container_width=True):
                        st.session_state.show_rec_for_item = None
                        st.rerun()
        
        except Exception as e:
            print(f"Recommendation error: {e}")

# ==================== CHECKOUT PAGE ====================
elif st.session_state.page == "checkout":
    
    st.markdown("""
    <div class="food-header animate-slide">
        <h1 class="header-title">💳 Checkout</h1>
        <p class="header-subtitle">Review your order & complete payment</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.markdown("""
        <div class="empty-state animate-slide">
            <div class="empty-icon">🛒</div>
            <div class="empty-text">Your cart is empty!</div>
            <p style="color: #718096; font-size: 16px;">Add some delicious items to get started 🍕</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🍴 Browse Menu", type="primary", use_container_width=True):
            go_to_menu()
            st.rerun()
        st.stop()
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Order Items
        st.markdown('<div class="section-header">📦 Your Order</div>', unsafe_allow_html=True)
        
        for i, item in enumerate(st.session_state.cart):
            item_col1, item_col2, item_col3 = st.columns([5, 2, 1])
            
            with item_col1:
                veg_html = get_veg_indicator(item['Item_Name'])
                cat_class = get_category_class(item.get('Item_Category', ''))
                
                st.markdown(f"""
                <div style="padding: 12px 0; border-bottom: 2px solid #fff7ed;">
                    {veg_html}
                    <span style="font-size: 17px; font-weight: 700; color: #2d3748;">{item['Item_Name']}</span>
                    <div style="margin-top: 5px;">
                        <span class="category-badge {cat_class}">{item.get('Item_Category', 'Item')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with item_col2:
                st.markdown(f'<div style="padding: 20px 0; font-size: 20px; font-weight: 800; background: linear-gradient(135deg, #ff4757, #ff6348); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">₹{item["Current_Price"]}</div>', unsafe_allow_html=True)
            
            with item_col3:
                if st.button("🗑️", key=f"del_{i}"):
                    remove_from_cart(i)
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Frequently Ordered Together
        try:
            if st.session_state.cart:
                cart_item_ids = [item['Item_ID'] for item in st.session_state.cart]
                cart_rec_res = requests.post(
                    f"{API_URL}/cart-suggestions",
                    json={"customer_email": email, "cart_items": cart_item_ids}
                )
                
                if cart_rec_res.status_code == 200:
                    cart_suggestions = cart_rec_res.json().get('suggestions', {})
                    suggest_items = cart_suggestions.get('cart_suggestions', [])
                    
                    if suggest_items:
                        st.markdown('<div class="section-header">🔄 Frequently Ordered Together</div>', unsafe_allow_html=True)
                        
                        suggest_cols = st.columns(min(len(suggest_items), 3))
                        for idx, sugg_item in enumerate(suggest_items[:3]):
                            with suggest_cols[idx]:
                                veg_html = get_veg_indicator(sugg_item['Item_Name'])
                                cat_class = get_category_class(sugg_item.get('Item_Category', ''))
                                
                                st.markdown(f"""
                                <div class="food-card animate-fade">
                                    {veg_html}
                                    <div class="food-name">{sugg_item['Item_Name']}</div>
                                    <div class="food-price">₹{sugg_item['Current_Price']}</div>
                                    <span class="category-badge {cat_class}">{sugg_item.get('Item_Category', 'Item')}</span>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if st.button("➕ Add", key=f"cart_sugg_{idx}", use_container_width=True):
                                    add_to_cart(sugg_item)
                                    st.success("✅ Added!")
                                    st.rerun()
        except Exception as e:
            print(f"Cart suggestions error: {e}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Also Try Section - Get recommendations for last added item
        try:
            if st.session_state.cart:
                last_item = st.session_state.cart[-1]  # Get last added item
                
                also_try_res = requests.post(
                    f"{API_URL}/item-addons",
                    json={"customer_email": email, "item_id": last_item['Item_ID']}
                )
                
                if also_try_res.status_code == 200:
                    also_try_data = also_try_res.json()
                    smart_recs = also_try_data.get('smart_recommendations', {})
                    also_try_items = smart_recs.get('add_ons', [])
                    
                    if also_try_items:
                        st.markdown('<div class="section-header">✨ Also Try</div>', unsafe_allow_html=True)
                        
                        # AI Pitch
                        ai_pitch = smart_recs.get('ai_pitch', 'Complete your meal!')
                        st.markdown(f'<div class="rec-pitch">💡 {ai_pitch}</div>', unsafe_allow_html=True)
                        
                        also_cols = st.columns(min(len(also_try_items), 3))
                        for idx, also_item in enumerate(also_try_items[:3]):
                            with also_cols[idx]:
                                veg_html = get_veg_indicator(also_item['Item_Name'])
                                cat_class = get_category_class(also_item.get('Item_Category', ''))
                                tag_html = f'<span class="food-tag bestseller-tag">{also_item.get("tag", "Recommended")}</span>'
                                
                                st.markdown(f"""
                                <div class="food-card animate-fade">
                                    {veg_html}
                                    <div class="food-name">{also_item['Item_Name']}</div>
                                    <div class="food-price">₹{also_item['Current_Price']}</div>
                                    <span class="category-badge {cat_class}">{also_item.get('Item_Category', 'Item')}</span>
                                    {tag_html}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if st.button("➕ Add", key=f"also_try_{idx}", use_container_width=True):
                                    add_to_cart(also_item)
                                    st.success("✅ Added to cart!")
                                    st.rerun()
        except Exception as e:
            print(f"Also try error: {e}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Popular Items Section - Show trending items
        try:
            popular_menu_res = requests.post(f"{API_URL}/menu", json={"customer_email": email})
            
            if popular_menu_res.status_code == 200:
                menu_data = popular_menu_res.json()
                menu_sections = menu_data.get('menu', {}).get('menu_sections', {})
                
                # Get popular items
                popular_items = menu_sections.get('Popular Items 🔥', [])
                
                if popular_items:
                    # Filter out items already in cart
                    cart_item_ids = [item['Item_ID'] for item in st.session_state.cart]
                    available_popular = [item for item in popular_items if item['Item_ID'] not in cart_item_ids]
                    
                    if available_popular:
                        st.markdown('<div class="section-header">🔥 Popular Right Now</div>', unsafe_allow_html=True)
                        
                        popular_cols = st.columns(min(len(available_popular), 4))
                        for idx, pop_item in enumerate(available_popular[:4]):
                            with popular_cols[idx]:
                                veg_html = get_veg_indicator(pop_item['Item_Name'])
                                cat_class = get_category_class(pop_item.get('Item_Category', ''))
                                
                                st.markdown(f"""
                                <div class="food-card animate-fade">
                                    {veg_html}
                                    <div class="food-name">{pop_item['Item_Name']}</div>
                                    <div class="food-price">₹{pop_item['Current_Price']}</div>
                                    <span class="category-badge {cat_class}">{pop_item.get('Item_Category', 'Item')}</span>
                                    <span class="food-tag bestseller-tag">Bestseller</span>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if st.button("➕ Add", key=f"popular_{idx}", use_container_width=True):
                                    add_to_cart(pop_item)
                                    st.success("✅ Added!")
                                    st.rerun()
        except Exception as e:
            print(f"Popular items error: {e}")
    
    with col_right:
        # Bill Details
        st.markdown('<div class="section-header">💰 Bill Details</div>', unsafe_allow_html=True)
        
        try:
            payload = {
                "customer_email": email,
                "cart_items": [
                    {
                        "dish_id": item.get('Item_ID'),
                        "price": float(item.get('Current_Price', 0)),
                        "quantity": 1,
                        "category": item.get('Item_Category', '')
                    }
                    for item in st.session_state.cart
                ]
            }
            
            checkout_res = requests.post(f"{API_URL}/checkout", json=payload)
            
            if checkout_res.status_code == 200:
                checkout_data = checkout_res.json()
                pricing = checkout_data.get('pricing', {})
                
                # Price breakdown
                subtotal = pricing.get('subtotal', 0)
                discount_info = pricing.get('discount_applied', {})
                discount_amt = discount_info.get('discount_amount', 0)
                final_total = pricing.get('final_total', 0)
                
                st.markdown(f"""
                <div class="price-row">
                    <span>Subtotal</span>
                    <span style="font-weight: 700;">₹{subtotal}</span>
                </div>
                """, unsafe_allow_html=True)
                
                if discount_amt > 0:
                    st.markdown(f"""
                    <div class="price-row">
                        <span>{discount_info.get('name', 'Discount')}</span>
                        <span class="discount-green">-₹{discount_amt}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="price-total">
                    <div style="display: flex; justify-content: space-between;">
                        <span>Grand Total</span>
                        <span style="background: linear-gradient(135deg, #ff4757, #ffa502); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">₹{final_total}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Upsell nudge
                upsell = pricing.get('upsell_nudge', {})
                if upsell and upsell.get('show'):
                    st.markdown(f'<div class="upsell-nudge">🎯 {upsell.get("message", "")}</div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Coupons Section
                st.markdown('<div class="section-header">🎫 Coupons</div>', unsafe_allow_html=True)
                
                coupons = pricing.get('available_coupons', [])
                for coupon in coupons[:4]:
                    is_available = "Available" in coupon.get('status', '') or "Unlocked" in coupon.get('status', '')
                    is_locked = "Locked" in coupon.get('status', '')
                    
                    card_class = "coupon-card"
                    if is_available:
                        card_class += " coupon-available"
                    elif is_locked:
                        card_class += " coupon-locked"
                    
                    icon = "✅" if is_available else "🔒"
                    
                    st.markdown(f"""
                    <div class="{card_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div class="coupon-code">{coupon['code']}</div>
                                <div style="font-size: 14px; color: #718096; margin-top: 6px; font-weight: 600;">{coupon.get('discount', '')}</div>
                            </div>
                            <div style="font-size: 28px;">{icon}</div>
                        </div>
                        <div style="font-size: 13px; color: #a0aec0; margin-top: 10px; font-weight: 500;">{coupon.get('status', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Loyalty Status
                st.markdown('<div class="section-header">⭐ Loyalty</div>', unsafe_allow_html=True)
                
                loyalty = pricing.get('loyalty_status', {})
                rewards = pricing.get('reward_points', {})
                
                tier = loyalty.get('current_tier', 'Bronze')
                tier_class = tier.lower()
                
                st.markdown(f'<div class="loyalty-badge {tier_class}">{tier} Member</div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="margin-top: 18px; padding: 18px; background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%); border-radius: 12px; border: 2px solid #fed7aa;">
                    <div style="font-size: 14px; color: #9a3412; margin-bottom: 6px; font-weight: 600;">Points on this order</div>
                    <div style="font-size: 28px; font-weight: 800; background: linear-gradient(135deg, #ff6348, #ffa502); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🎉 {rewards.get('earned', 0)} pts</div>
                </div>
                """, unsafe_allow_html=True)
                
                next_tier = loyalty.get('next_tier')
                orders_to_next = loyalty.get('orders_to_next', 0)
                if next_tier:
                    st.markdown(f'<div style="margin-top: 12px; padding: 12px; background: linear-gradient(135deg, #fef3c7, #fde68a); border-radius: 10px; font-size: 14px; font-weight: 600; color: #78350f;">📈 {orders_to_next} more orders to {next_tier}!</div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Place Order Button
                if st.button("🚀 Place Order", type="primary", use_container_width=True):
                    try:
                        order_res = requests.post(f"{API_URL}/recommendation-strategy", json=payload)
                        
                        if order_res.status_code == 200:
                            st.balloons()
                            st.success("✅ Order placed successfully!")
                            st.markdown('<div style="background: linear-gradient(135deg, #d1fae5, #a7f3d0); padding: 15px; border-radius: 10px; text-align: center; font-weight: 700; color: #065f46; margin: 15px 0;">🎉 You\'ll receive confirmation email shortly!</div>', unsafe_allow_html=True)
                            
                            # Show order details
                            with st.expander("📋 Order Details"):
                                st.json(order_res.json())
                            
                            # Clear cart
                            st.session_state.cart = []
                            st.session_state.show_rec_for_item = None
                            
                            # Redirect after delay
                            import time
                            time.sleep(2)
                            go_to_menu()
                            st.rerun()
                        else:
                            st.error(f"❌ Order failed: {order_res.text}")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            else:
                st.error(f"Failed to get pricing: {checkout_res.status_code}")
        
        except Exception as e:
            st.error(f"Checkout error: {e}")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 25px; background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%); border-radius: 15px; margin-top: 20px;">
    <p style="margin: 0; font-size: 16px; font-weight: 700;">
        🍽️ <span style="background: linear-gradient(135deg, #ff4757, #ffa502); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 20px;">DineIQ</span> - Smart Restaurant Ordering
    </p>
    <p style="margin: 8px 0 0 0; font-size: 13px; color: #78350f; font-weight: 500;">Powered by AI & Groq | Made with ❤️ in India 🇮🇳</p>
</div>
""", unsafe_allow_html=True)