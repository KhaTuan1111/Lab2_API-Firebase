import streamlit as st
import requests
import json
import datetime

# ==========================================
# 1. CONFIGURATION
# ==========================================
FIREBASE_WEB_API_KEY = "AIzaSyDgzahCsU-8w5q1QAkdjiaTP5W5jib0F-I" 
FASTAPI_BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Note App", page_icon="📝", layout="centered")

# ==========================================
# 2. CUSTOM CSS FOR RICH AESTHETICS
# ==========================================
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers & Text */
    h1 {
        background: -webkit-linear-gradient(45deg, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        padding-bottom: 20px;
    }
    
    /* Fix Text Input Colors */
    div[data-testid="stTextInput"] input {
        border-radius: 8px !important;
        background-color: #1e293b !important; /* Solid dark background */
        color: #ffffff !important; /* White text */
        border: 1px solid #475569 !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #a855f7 !important;
        box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.4) !important;
    }
    
    /* Fix Button Colors */
    div[data-testid="stFormSubmitButton"] button, div[data-testid="stButton"] button {
        background-color: #3b82f6 !important; /* Nice blue */
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        transition: background-color 0.2s;
    }
    div[data-testid="stFormSubmitButton"] button:hover, div[data-testid="stButton"] button:hover {
        background-color: #2563eb !important; /* Darker blue on hover */
    }
    
    /* Prevent button text wrapping and ensure text is white */
    div[data-testid="stButton"] button p, div[data-testid="stFormSubmitButton"] button p {
        color: #ffffff !important;
        white-space: nowrap !important;
        margin: 0 !important;
    }
    
    /* Note Container styling wrapper */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 5px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SESSION STATE INITIALIZATION
# ==========================================
if 'user_token' not in st.session_state:
    st.session_state.user_token = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'edit_note_id' not in st.session_state:
    st.session_state.edit_note_id = None

# ==========================================
# 4. FIREBASE AUTHENTICATION LOGIC
# ==========================================
def login_firebase(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("idToken"), data.get("email")
        else:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            st.error(f"Login failed: {error_msg}")
            return None, None
    except Exception as e:
        st.error(f"Network error: {e}")
        return None, None

def register_firebase(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("idToken"), data.get("email")
        else:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            st.error(f"Registration failed: {error_msg}")
            return None, None
    except Exception as e:
        st.error(f"Network error: {e}")
        return None, None

def logout():
    st.session_state.user_token = None
    st.session_state.user_email = None
    st.session_state.edit_note_id = None
    st.rerun()

# ==========================================
# 5. UI & APP FLOW
# ==========================================
st.markdown("<h1>✨ Note App Pro</h1>", unsafe_allow_html=True)

# --- LOGIN / REGISTER SCREEN ---
if not st.session_state.user_token:
    st.markdown("<h3 style='text-align: center; color: #cbd5e1;'>Welcome! Please Login or Register</h3>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if FIREBASE_WEB_API_KEY == "YOUR_FIREBASE_WEB_API_KEY":
                    st.error("⚠️ Please configure FIREBASE_WEB_API_KEY in frontend/app.py first!")
                elif email and password:
                    with st.spinner("Logging in..."):
                        token, user_email = login_firebase(email, password)
                        if token:
                            st.session_state.user_token = token
                            st.session_state.user_email = user_email
                            st.success("Login successful!")
                            st.rerun()

    with tab2:
        with st.form("register_form"):
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_button = st.form_submit_button("Register")
            
            if reg_button:
                if FIREBASE_WEB_API_KEY == "YOUR_FIREBASE_WEB_API_KEY":
                    st.error("⚠️ Please configure FIREBASE_WEB_API_KEY in frontend/app.py first!")
                elif reg_email and reg_password:
                    with st.spinner("Registering..."):
                        token, user_email = register_firebase(reg_email, reg_password)
                        if token:
                            st.session_state.user_token = token
                            st.session_state.user_email = user_email
                            st.success("Registration successful!")
                            st.rerun()

# --- MAIN APP SCREEN ---
else:
    # Header Info
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<div style='padding-top: 10px; font-size: 1.1rem; color: #cbd5e1;'>👤 Welcome, <b>{st.session_state.user_email}</b></div>", unsafe_allow_html=True)
    with col2:
        if st.button("Logout 🚪", use_container_width=True):
            logout()
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    
    # Add Note Form
    st.markdown("### ✍️ Create a new note")
    with st.form("add_note_form", clear_on_submit=True):
        new_note = st.text_input("What's on your mind?", placeholder="Type your note here...")
        add_btn = st.form_submit_button("✨ Add Note")
        
        if add_btn and new_note:
            headers = {"Authorization": f"Bearer {st.session_state.user_token}"}
            try:
                res = requests.post(f"{FASTAPI_BACKEND_URL}/notes", json={"content": new_note}, headers=headers)
                if res.status_code == 200:
                    st.toast("Note added successfully!", icon="✅")
                    st.rerun()
                else:
                    st.error(f"Failed to add note: {res.text}")
            except Exception as e:
                st.error(f"Backend connection error: {e}. Is FastAPI running?")
                
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    
    # Display Notes Header with Sort
    c_head1, c_head2 = st.columns([2, 1])
    with c_head1:
        st.markdown("### 📚 Your Notes")
    with c_head2:
        sort_order = st.selectbox("Sort by time", ["Newest First 🔽", "Oldest First 🔼"], label_visibility="collapsed")
        sort_param = "desc" if "Newest" in sort_order else "asc"

    headers = {"Authorization": f"Bearer {st.session_state.user_token}"}
    
    with st.spinner("Fetching notes..."):
        try:
            res = requests.get(f"{FASTAPI_BACKEND_URL}/notes?sort_order={sort_param}", headers=headers)
            if res.status_code == 200:
                notes = res.json()
                if not notes:
                    st.info("No notes found. Create your first note above! 🚀")
                else:
                    for note in notes:
                        # Render Note using native Container to support buttons
                        with st.container(border=True):
                            # Formatting date
                            try:
                                date_obj = datetime.datetime.fromisoformat(note['created_at'])
                                formatted_date = date_obj.strftime("%d %b %Y • %I:%M %p")
                            except:
                                formatted_date = note['created_at']
                                
                            # If this note is in edit mode
                            if st.session_state.edit_note_id == note['id']:
                                with st.form(key=f"edit_form_{note['id']}"):
                                    edit_content = st.text_input("Edit your note", value=note['content'])
                                    col_save, col_cancel = st.columns(2)
                                    with col_save:
                                        if st.form_submit_button("✅ Save"):
                                            if edit_content != note['content']:
                                                update_res = requests.put(f"{FASTAPI_BACKEND_URL}/notes/{note['id']}", json={"content": edit_content}, headers=headers)
                                                if update_res.status_code == 200:
                                                    st.toast("Note updated successfully!", icon="✅")
                                                else:
                                                    st.error("Failed to update note.")
                                            st.session_state.edit_note_id = None
                                            st.rerun()
                                    with col_cancel:
                                        if st.form_submit_button("❌ Cancel"):
                                            st.session_state.edit_note_id = None
                                            st.rerun()
                            # View Mode
                            else:
                                st.markdown(f"<div style='font-size: 1.15rem; font-weight: 500; margin-bottom: 0.5rem;'>{note['content']}</div>", unsafe_allow_html=True)
                                st.markdown(f"<div style='font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;'>🕒 {formatted_date}</div>", unsafe_allow_html=True)
                                
                                c1, c2, c3 = st.columns([6, 2, 2])
                                with c2:
                                    if st.button("✏️ Edit", key=f"edit_{note['id']}", use_container_width=True):
                                        st.session_state.edit_note_id = note['id']
                                        st.rerun()
                                with c3:
                                    if st.button("🗑️ Del", key=f"del_{note['id']}", use_container_width=True):
                                        del_res = requests.delete(f"{FASTAPI_BACKEND_URL}/notes/{note['id']}", headers=headers)
                                        if del_res.status_code == 200:
                                            st.toast("Note deleted!", icon="🗑️")
                                            st.rerun()
                                        else:
                                            st.error("Failed to delete note.")
            elif res.status_code == 401:
                st.error("Session expired. Please login again.")
                logout()
            else:
                st.error(f"Failed to fetch notes: {res.text}")
        except Exception as e:
            st.error(f"Cannot connect to backend: {e}. Please make sure your FastAPI server is running at {FASTAPI_BACKEND_URL}")
