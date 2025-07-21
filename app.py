
# import streamlit as st
# import os
# import json
# from rag import rag, build_vectorstore, load_text_docs
# from runner import runner
# import time

# # === Page Configuration ===
# st.set_page_config(
#     page_title="SMARTML Assistant",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # === Custom CSS Styling ===
# st.markdown("""
# <style>
#     /* Import Google Fonts */
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
#     /* Root variables for consistent theming */
#     :root {
#         --primary-color: #6366f1;
#         --primary-dark: #4f46e5;
#         --secondary-color: #ec4899;
#         --accent-color: #06b6d4;
#         --success-color: #10b981;
#         --warning-color: #f59e0b;
#         --error-color: #ef4444;
#         --text-primary: #1f2937;
#         --text-secondary: #6b7280;
#         --bg-primary: #ffffff;
#         --bg-secondary: #f8fafc;
#         --bg-tertiary: #f1f5f9;
#         --border-color: #e5e7eb;
#         --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
#         --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
#         --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
#         --gradient-primary: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
#         --gradient-secondary: linear-gradient(135deg, var(--accent-color) 0%, var(--primary-color) 100%);
#     }
    
#     /* Hide default Streamlit elements */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
    
#     /* Main app styling */
#     .main .block-container {
#         padding-top: 2rem;
#         padding-bottom: 2rem;
#         max-width: 1200px;
#     }
    
#     /* Custom title styling */
#     .main-title {
#         background: var(--gradient-primary);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         font-family: 'Inter', sans-serif;
#         font-weight: 700;
#         font-size: 3.5rem;
#         text-align: center;
#         margin-bottom: 0.5rem;
#         animation: fadeInUp 0.8s ease-out;
#     }
    
#     .subtitle {
#         color: var(--text-secondary);
#         text-align: center;
#         font-size: 1.2rem;
#         font-weight: 400;
#         margin-bottom: 2rem;
#         animation: fadeInUp 0.8s ease-out 0.2s both;
#     }
    
#     /* Sidebar styling */
#     .css-1d391kg {
#         background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
#     }
    
#     .sidebar .sidebar-content {
#         background: var(--bg-secondary);
#         border-radius: 1rem;
#         padding: 1.5rem;
#         margin: 1rem;
#         box-shadow: var(--shadow-lg);
#     }
    
#     /* Card styling */
#     .custom-card {
#         background: var(--bg-primary);
#         border-radius: 1rem;
#         padding: 1.5rem;
#         box-shadow: var(--shadow-md);
#         border: 1px solid var(--border-color);
#         margin-bottom: 1.5rem;
#         transition: all 0.3s ease;
#         position: relative;
#         overflow: hidden;
#     }
    
#     .custom-card:hover {
#         box-shadow: var(--shadow-lg);
#         transform: translateY(-2px);
#     }
    
#     .custom-card::before {
#         content: '';
#         position: absolute;
#         top: 0;
#         left: 0;
#         right: 0;
#         height: 4px;
#         background: var(--gradient-primary);
#     }
    
#     /* Chat message styling */
#     .user-message {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 1rem 1.5rem;
#         border-radius: 1.5rem 1.5rem 0.5rem 1.5rem;
#         margin: 0.5rem 0 0.5rem 2rem;
#         max-width: 70%;
#         margin-left: auto;
#         box-shadow: var(--shadow-md);
#         animation: slideInRight 0.3s ease-out;
#         font-weight: 500;
#     }
    
#     .assistant-message {
#         background: var(--bg-primary);
#         color: var(--text-primary);
#         padding: 1rem 1.5rem;
#         border-radius: 1.5rem 1.5rem 1.5rem 0.5rem;
#         margin: 0.5rem 2rem 0.5rem 0;
#         max-width: 70%;
#         border: 1px solid var(--border-color);
#         box-shadow: var(--shadow-md);
#         animation: slideInLeft 0.3s ease-out;
#         position: relative;
#     }
    
#     .assistant-message::before {
#         content: '🤖';
#         position: absolute;
#         top: -0.5rem;
#         left: -0.5rem;
#         background: var(--gradient-primary);
#         width: 2rem;
#         height: 2rem;
#         border-radius: 50%;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 1rem;
#         box-shadow: var(--shadow-md);
#     }
    
#     /* Input styling */
#     .stTextInput > div > div > input {
#         background: var(--bg-primary);
#         border: 2px solid var(--border-color);
#         border-radius: 1rem;
#         padding: 1rem 1.5rem;
#         font-size: 1rem;
#         font-family: 'Inter', sans-serif;
#         transition: all 0.3s ease;
#     }
    
#     .stTextInput > div > div > input:focus {
#         border-color: var(--primary-color);
#         box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
#         outline: none;
#     }
    
#     /* Button styling */
#     .stButton > button {
#         background: var(--gradient-primary);
#         color: white;
#         border: none;
#         border-radius: 1rem;
#         padding: 0.75rem 2rem;
#         font-weight: 600;
#         font-family: 'Inter', sans-serif;
#         transition: all 0.3s ease;
#         box-shadow: var(--shadow-md);
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: var(--shadow-lg);
#     }
    
#     /* Success/Error messages */
#     .element-container .stAlert {
#         border-radius: 1rem;
#         border: none;
#         box-shadow: var(--shadow-md);
#     }
    
#     .stAlert[data-baseweb="notification"] {
#         background: linear-gradient(135deg, #10b981 0%, #059669 100%);
#         color: white;
#     }
    
#     /* Code blocks */
#     .stCode {
#         border-radius: 1rem;
#         box-shadow: var(--shadow-md);
#         border: 1px solid var(--border-color);
#     }
    
#     /* Spinner styling */
#     .stSpinner {
#         text-align: center;
#     }
    
#     /* File uploader */
#     .uploadedFile {
#         background: var(--bg-secondary);
#         border-radius: 0.5rem;
#         padding: 0.5rem;
#         border: 1px solid var(--border-color);
#     }
    
#     /* Metrics styling */
#     .metric-card {
#         background: var(--bg-primary);
#         border-radius: 1rem;
#         padding: 1.5rem;
#         text-align: center;
#         box-shadow: var(--shadow-md);
#         border: 1px solid var(--border-color);
#         transition: all 0.3s ease;
#     }
    
#     .metric-card:hover {
#         transform: scale(1.02);
#         box-shadow: var(--shadow-lg);
#     }
    
#     .metric-value {
#         font-size: 2.5rem;
#         font-weight: 700;
#         background: var(--gradient-primary);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         font-family: 'Inter', sans-serif;
#     }
    
#     .metric-label {
#         color: var(--text-secondary);
#         font-size: 0.9rem;
#         font-weight: 500;
#         text-transform: uppercase;
#         letter-spacing: 0.5px;
#     }
    
#     /* Animations */
#     @keyframes fadeInUp {
#         from {
#             opacity: 0;
#             transform: translateY(30px);
#         }
#         to {
#             opacity: 1;
#             transform: translateY(0);
#         }
#     }
    
#     @keyframes slideInLeft {
#         from {
#             opacity: 0;
#             transform: translateX(-30px);
#         }
#         to {
#             opacity: 1;
#             transform: translateX(0);
#         }
#     }
    
#     @keyframes slideInRight {
#         from {
#             opacity: 0;
#             transform: translateX(30px);
#         }
#         to {
#             opacity: 1;
#             transform: translateX(0);
#         }
#     }
    
#     @keyframes pulse {
#         0%, 100% {
#             opacity: 1;
#         }
#         50% {
#             opacity: 0.7;
#         }
#     }
    
#     .pulse {
#         animation: pulse 2s infinite;
#     }
    
#     /* Responsive design */
#     @media (max-width: 768px) {
#         .main-title {
#             font-size: 2.5rem;
#         }
        
#         .user-message, .assistant-message {
#             max-width: 85%;
#             margin-left: 1rem;
#             margin-right: 1rem;
#         }
#     }
    
#     /* Loading animation */
#     .loading-dots {
#         display: inline-block;
#         position: relative;
#         width: 80px;
#         height: 80px;
#     }
    
#     .loading-dots div {
#         position: absolute;
#         top: 33px;
#         width: 13px;
#         height: 13px;
#         border-radius: 50%;
#         background: var(--primary-color);
#         animation-timing-function: cubic-bezier(0, 1, 1, 0);
#     }
    
#     .loading-dots div:nth-child(1) {
#         left: 8px;
#         animation: loading1 0.6s infinite;
#     }
    
#     .loading-dots div:nth-child(2) {
#         left: 8px;
#         animation: loading2 0.6s infinite;
#     }
    
#     .loading-dots div:nth-child(3) {
#         left: 32px;
#         animation: loading2 0.6s infinite;
#     }
    
#     .loading-dots div:nth-child(4) {
#         left: 56px;
#         animation: loading3 0.6s infinite;
#     }
    
#     @keyframes loading1 {
#         0% { transform: scale(0); }
#         100% { transform: scale(1); }
#     }
    
#     @keyframes loading3 {
#         0% { transform: scale(1); }
#         100% { transform: scale(0); }
#     }
    
#     @keyframes loading2 {
#         0% { transform: translate(0, 0); }
#         100% { transform: translate(24px, 0); }
#     }
# </style>
# """, unsafe_allow_html=True)

# # === Setup folders ===
# os.makedirs("Datasets", exist_ok=True)
# os.makedirs("JSONs", exist_ok=True)

# # === Sidebar with beautiful styling ===
# with st.sidebar:
#     st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
#     st.markdown("# 🚀 Control Panel")
#     st.markdown("</div>", unsafe_allow_html=True)
    
#     # Upload section
#     st.markdown("---")
#     st.markdown("### 📁 Dataset Upload")
#     uploaded_file = st.file_uploader("Choose a CSV file", type="csv", help="Upload your dataset for training")
    
#     if uploaded_file:
#         file_path = os.path.join("Datasets", uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         st.success(f"✅ Saved: `{uploaded_file.name}`")
#         st.balloons()
    
#     # Vectorstore section
#     st.markdown("---")
#     st.markdown("### 🔄 Vector Database")
    
#     @st.cache_resource
#     def init_vectorstore():
#         with st.spinner("🔧 Building knowledge base..."):
#             docs = load_text_docs()
#             return build_vectorstore(docs)
    
#     if st.button("🔁 Rebuild Vectorstore", help="Refresh the AI knowledge base"):
#         init_vectorstore.clear()
#         st.success("🎯 Vectorstore refreshed!")
#         st.rerun()
    
#     # Chat management
#     st.markdown("---")
#     st.markdown("### 💬 Chat Management")
    
#     if st.button("🗑️ Clear History", help="Clear all chat history"):
#         st.session_state.chat = []
#         st.success("🧹 Chat cleared!")
#         st.rerun()
    
#     # Statistics
#     if "chat" in st.session_state and st.session_state.chat:
#         st.markdown("---")
#         st.markdown("### 📊 Session Stats")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Messages", len(st.session_state.chat))
#         with col2:
#             json_count = sum(1 for _, response in st.session_state.chat if response.strip().startswith("{"))
#             st.metric("JSON Specs", json_count)

# # Initialize vectorstore
# vectorstore = init_vectorstore()

# # === Main App Header ===
# st.markdown('<h1 class="main-title">SMARTML Assistant</h1>', unsafe_allow_html=True)
# st.markdown('<p class="subtitle">🧠 Your AI-powered machine learning companion for intelligent model development</p>', unsafe_allow_html=True)


# # === Session Chat Memory ===
# if "chat" not in st.session_state:
#     st.session_state.chat = []

# if "quick_question" not in st.session_state:
#     st.session_state.quick_question = ""

# # === Chat Interface ===
# st.markdown("---")
# st.markdown("### 💭 Ask SMARTML Anything")

# # Use quick question if available
# default_value = st.session_state.quick_question if st.session_state.quick_question else ""
# if st.session_state.quick_question:
#     st.session_state.quick_question = ""  # Clear after using

# user_input = st.text_input(
#     "Your question", 
#     value=default_value,
#     placeholder="Ask about ML concepts Or request model builds...",
#     help="Type your question or request. I can explain concepts, generate JSON specs, and run models!"
# )

# if user_input:
#     history = st.session_state.chat
    
#     # Beautiful thinking animation
#     with st.container():
#         thinking_placeholder = st.empty()
#         thinking_placeholder.markdown(
#             '<div style="text-align: center; padding: 2rem;"><div class="loading-dots"><div></div><div></div><div></div><div></div></div><p style="margin-top: 1rem; color: #6b7280;">🧠 SMARTML is thinking...</p></div>',
#             unsafe_allow_html=True
#         )
        
#         # Get response
#         response = rag(history, user_input, vectorstore)
#         thinking_placeholder.empty()
    
#     # Validate response
#     if not response or response.strip() == "undefined":
#         response = "I couldn't generate a proper response. Please try again with a different question."
    
#     # Save to chat history
#     history.append((user_input, response))
#     st.session_state.chat = history
    
#     # === Response Handling ===
#     response_clean = response.strip()
    
#     # Check for execution signal
#     execution_triggers = [
#         response_clean == "-1",
#         response_clean.lower() == "run_model",
#         "run_model" in response_clean.lower(),
#         "-1" in response_clean,
#         ("json" in response_clean.lower() and ("-1" in response_clean or "run" in response_clean.lower())),
#         (response_clean.startswith("{") and "command" in response_clean.lower())
#     ]
    
#     if any(execution_triggers):
#         st.markdown('<div class="custom-card">', unsafe_allow_html=True)
#         st.success("🚀 **Model Execution Initiated!**")
        
#         progress_bar = st.progress(0)
#         status_text = st.empty()
        
#         try:
#             # Simulate loading progress
#             for i in range(100):
#                 progress_bar.progress(i + 1)
#                 if i < 30:
#                     status_text.text("🔧 Loading model configuration...")
#                 elif i < 60:
#                     status_text.text("⚡ Training model...")
#                 elif i < 90:
#                     status_text.text("📊 Evaluating performance...")
#                 else:
#                     status_text.text("✨ Generating insights...")
#                 time.sleep(0.02)
            
#             result = runner("sample.json", "model_parameters.json")
#             progress_bar.empty()
#             status_text.empty()
            
#             if "error" in result:
#                 st.error(f"❌ **Model Execution Failed:** {result['error']}")
#             else:
#                 # Success animation
#                 st.balloons()
                
#                 # Display results with beautiful cards
#                 st.markdown("### 🎯 Model Performance Results")
                
#                 # Metrics in beautiful cards
#                 col1, col2, col3 = st.columns(3)
                
#                 with col1:
#                     st.markdown(f'''
#                     <div class="metric-card">
#                         <div class="metric-value">{result['acc']:.1%}</div>
#                         <div class="metric-label">Accuracy</div>
#                     </div>
#                     ''', unsafe_allow_html=True)
                
#                 with col2:
#                     # Extract precision from classification report if available
#                     precision = "N/A"
#                     if 'cr' in result and result['cr']:
#                         lines = result['cr'].split('\n')
#                         for line in lines:
#                             if 'weighted avg' in line or 'macro avg' in line:
#                                 parts = line.split()
#                                 if len(parts) >= 2:
#                                     try:
#                                         precision = f"{float(parts[1]):.1%}"
#                                         break
#                                     except:
#                                         pass
                    
#                     st.markdown(f'''
#                     <div class="metric-card">
#                         <div class="metric-value">{precision}</div>
#                         <div class="metric-label">Precision</div>
#                     </div>
#                     ''', unsafe_allow_html=True)
                
#                 with col3:
#                     st.markdown(f'''
#                     <div class="metric-card">
#                         <div class="metric-value">✅</div>
#                         <div class="metric-label">Status</div>
#                     </div>
#                     ''', unsafe_allow_html=True)
                
#                 # Detailed results in expandable sections
#                 with st.expander("📊 **Detailed Classification Report**", expanded=False):
#                     st.code(result['cr'], language="text")
                
#                 with st.expander("🔢 **Confusion Matrix**", expanded=False):
#                     st.write(result['cm'])
                
#                 # Get AI explanation
#                 user_summary = (
#                     f"Explain the following model training results:\n\n"
#                     f"Accuracy: {result['acc']:.4f}\n"
#                     f"Classification Report:\n{result['cr']}\n"
#                     f"Confusion Matrix: {result['cm']}\n"
#                     f"Used Parameters: {result['paramters']}"
#                 )
                
#                 with st.spinner("🤖 Generating AI insights..."):
#                     explanation = rag(st.session_state.chat, user_summary, vectorstore)
                
#                 st.markdown("### 🧠 SMARTML Analysis")
#                 st.markdown(f'<div class="assistant-message" style="max-width: 100%; margin: 1rem 0;">{explanation}</div>', unsafe_allow_html=True)
                
#                 # Save explanation to chat history
#                 st.session_state.chat.append(("Explain the model training results", explanation))
        
#         except Exception as e:
#             progress_bar.empty()
#             status_text.empty()
#             st.error(f"❌ **Execution Error:** {str(e)}")
        
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     elif response_clean.startswith("{") and response_clean.endswith("}"):
#         st.markdown('<div class="custom-card">', unsafe_allow_html=True)
#         st.markdown("### 📋 **Generated JSON Specification**")
#         st.code(response_clean, language="json")
        
#         # Save JSON spec
#         try:
#             parsed = json.loads(response_clean)
#             with open("JSONs/sample.json", "w") as f:
#                 json.dump(parsed, f, indent=2)
#             st.success("✅ **Specification saved** to `JSONs/sample.json`")
#         except Exception as e:
#             st.error(f"⚠️ **JSON Save Error:** {e}")
        
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     else:
#         # Regular response
#         st.markdown(f'<div class="assistant-message" style="max-width: 100%; margin: 1rem 0; padding-left: 3rem;">{response_clean}</div>', unsafe_allow_html=True)

# # === Beautiful Conversation History ===
# if st.session_state.chat:
#     st.markdown("---")
#     st.markdown("### 💬 Conversation History")
    
#     # Reverse order to show latest first
#     for i, (q, a) in enumerate(reversed(st.session_state.chat)):
#         with st.container():
#             # User message
#             st.markdown(f'<div class="user-message"><strong>You:</strong> {q}</div>', unsafe_allow_html=True)
            
#             # Clean response
#             cleaned_response = a.strip() if a else ""
            
#             # Assistant response with appropriate formatting
#             execution_check = [
#                 cleaned_response == "-1",
#                 "json-1" in cleaned_response.lower(),
#                 "-1" in cleaned_response,
#                 ("json" in cleaned_response.lower() and ("-1" in cleaned_response or "run" in cleaned_response.lower())),
#                 "run_model" in cleaned_response.lower(),
#                 (cleaned_response.startswith("{") and "command" in cleaned_response.lower())
#             ]
            
#             if any(execution_check):
#                 st.markdown('<div class="assistant-message" style="max-width: 100%; margin: 1rem 0; padding-left: 3rem;"><em>🚀 SMARTML executed model pipeline</em></div>', unsafe_allow_html=True)
#             elif cleaned_response.startswith("{") and cleaned_response.endswith("}"):
#                 st.markdown('<div class="assistant-message" style="max-width: 100%; margin: 1rem 0; padding-left: 3rem;"><strong>🤖 SMARTML:</strong> Generated JSON specification</div>', unsafe_allow_html=True)
#                 with st.expander(f"View JSON Spec #{len(st.session_state.chat) - i}", expanded=False):
#                     st.code(cleaned_response, language="json")
#             elif cleaned_response and cleaned_response != "undefined":
#                 st.markdown(f'<div class="assistant-message" style="max-width: 100%; margin: 1rem 0; padding-left: 3rem;"><strong>🤖 SMARTML:</strong> {cleaned_response}</div>', unsafe_allow_html=True)
#             else:
#                 st.markdown('<div class="assistant-message" style="max-width: 100%; margin: 1rem 0; padding-left: 3rem;"><em>⚠️ No response generated</em></div>', unsafe_allow_html=True)
            
#             st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)

# # === Footer ===
# st.markdown("---")
# st.markdown(
#     '<div style="text-align: center; color: #6b7280; padding: 2rem;"><p>🧠 Powered by SMARTML AI • Built with ❤️ using Streamlit</p></div>',
#     unsafe_allow_html=True
# )

import streamlit as st
import os
import json
from rag import rag, build_vectorstore, load_text_docs
from runner import runner
import time

# === Page Configuration ===
st.set_page_config(
    page_title="SMARTML Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === Custom CSS Styling ===
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-color: #6366f1;
        --primary-dark: #4f46e5;
        --secondary-color: #ec4899;
        --accent-color: #06b6d4;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-tertiary: #f1f5f9;
        --border-color: #e5e7eb;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        --gradient-primary: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        --gradient-secondary: linear-gradient(135deg, var(--accent-color) 0%, var(--primary-color) 100%);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main app styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Custom title styling */
    .main-title {
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .subtitle {
        color: var(--text-secondary);
        text-align: center;
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 2rem;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .sidebar .sidebar-content {
        background: var(--bg-secondary);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem;
        box-shadow: var(--shadow-lg);
    }
    
    /* Card styling */
    .custom-card {
        background: var(--bg-primary);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .custom-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    
    .custom-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-primary);
    }
    
    /* Chat message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 1.5rem 1.5rem 0.5rem 1.5rem;
        margin: 0.5rem 0 0.5rem 2rem;
        max-width: 70%;
        margin-left: auto;
        box-shadow: var(--shadow-md);
        animation: slideInRight 0.3s ease-out;
        font-weight: 500;
    }
    
    .assistant-message {
        background: var(--bg-primary);
        color: var(--text-primary);
        padding: 1rem 1.5rem;
        border-radius: 1.5rem 1.5rem 1.5rem 0.5rem;
        margin: 0.5rem 2rem 0.5rem 0;
        max-width: 70%;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-md);
        animation: slideInLeft 0.3s ease-out;
        position: relative;
    }
    
    .assistant-message::before {
        content: '🤖';
        position: absolute;
        top: -0.5rem;
        left: -0.5rem;
        background: var(--gradient-primary);
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        box-shadow: var(--shadow-md);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: var(--bg-primary);
        border: 2px solid var(--border-color);
        border-radius: 1rem;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        outline: none;
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 1rem;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Success/Error messages */
    .element-container .stAlert {
        border-radius: 1rem;
        border: none;
        box-shadow: var(--shadow-md);
    }
    
    .stAlert[data-baseweb="notification"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    /* Code blocks */
    .stCode {
        border-radius: 1rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
    }
    
    /* Spinner styling */
    .stSpinner {
        text-align: center;
    }
    
    /* File uploader */
    .uploadedFile {
        background: var(--bg-secondary);
        border-radius: 0.5rem;
        padding: 0.5rem;
        border: 1px solid var(--border-color);
    }
    
    /* Metrics styling */
    .metric-card {
        background: var(--bg-primary);
        border-radius: 1rem;
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.02);
        box-shadow: var(--shadow-lg);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Inter', sans-serif;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .user-message, .assistant-message {
            max-width: 85%;
            margin-left: 1rem;
            margin-right: 1rem;
        }
    }
    
    /* Loading animation */
    .loading-dots {
        display: inline-block;
        position: relative;
        width: 80px;
        height: 80px;
    }
    
    .loading-dots div {
        position: absolute;
        top: 33px;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background: var(--primary-color);
        animation-timing-function: cubic-bezier(0, 1, 1, 0);
    }
    
    .loading-dots div:nth-child(1) {
        left: 8px;
        animation: loading1 0.6s infinite;
    }
    
    .loading-dots div:nth-child(2) {
        left: 8px;
        animation: loading2 0.6s infinite;
    }
    
    .loading-dots div:nth-child(3) {
        left: 32px;
        animation: loading2 0.6s infinite;
    }
    
    .loading-dots div:nth-child(4) {
        left: 56px;
        animation: loading3 0.6s infinite;
    }
    
    @keyframes loading1 {
        0% { transform: scale(0); }
        100% { transform: scale(1); }
    }
    
    @keyframes loading3 {
        0% { transform: scale(1); }
        100% { transform: scale(0); }
    }
    
    @keyframes loading2 {
        0% { transform: translate(0, 0); }
        100% { transform: translate(24px, 0); }
    }
</style>
""", unsafe_allow_html=True)

# === Setup folders ===
os.makedirs("Datasets", exist_ok=True)
os.makedirs("JSONs", exist_ok=True)

# === Sidebar with beautiful styling ===
with st.sidebar:
    st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
    st.markdown("# 🚀 Control Panel")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Upload section
    st.markdown("---")
    st.markdown("### 📁 Dataset Upload")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", help="Upload your dataset for training")
    
    if uploaded_file:
        file_path = os.path.join("Datasets", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ Saved: `{uploaded_file.name}`")
    
    # Vectorstore section
    st.markdown("---")
    st.markdown("### 🔄 Vector Database")
    
    @st.cache_resource
    def init_vectorstore():
        with st.spinner("🔧 Building knowledge base..."):
            docs = load_text_docs()
            return build_vectorstore(docs)
    
    if st.button("🔁 Rebuild Vectorstore", help="Refresh the AI knowledge base"):
        init_vectorstore.clear()
        st.success("🎯 Vectorstore refreshed!")
        st.rerun()
    
    # Chat management
    st.markdown("---")
    st.markdown("### 💬 Chat Management")
    
    if st.button("🗑️ Clear History", help="Clear all chat history"):
        st.session_state.chat = []
        st.success("🧹 Chat cleared!")
        st.rerun()
    
    # Statistics
    if "chat" in st.session_state and st.session_state.chat:
        st.markdown("---")
        st.markdown("### 📊 Session Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Messages", len(st.session_state.chat))
        with col2:
            json_count = sum(1 for _, response in st.session_state.chat if response.strip().startswith("{"))
            st.metric("JSON Specs", json_count)

# Initialize vectorstore
vectorstore = init_vectorstore()

# === Main App Header ===
st.markdown('<h1 class="main-title">SMARTML Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🧠 Your AI-powered machine learning companion for intelligent model development</p>', unsafe_allow_html=True)

# === Quick Actions ===
st.markdown("### 🎯 Quick Actions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📈 Model Comparison"):
        st.session_state.quick_question = "Compare different machine learning algorithms for classification tasks"

with col2:
    if st.button("🔍 Data Analysis"):
        st.session_state.quick_question = "Help me analyze my dataset and suggest preprocessing steps"

with col3:
    if st.button("⚡ Quick Build"):
        st.session_state.quick_question = "Create a simple classification model JSON specification"

with col4:
    if st.button("📚 ML Concepts"):
        st.session_state.quick_question = "Explain key machine learning concepts and best practices"

# === Session Chat Memory ===
if "chat" not in st.session_state:
    st.session_state.chat = []

if "quick_question" not in st.session_state:
    st.session_state.quick_question = ""

# === Chat Interface ===
st.markdown("---")
st.markdown("### 💭 Ask SMARTML Anything")

# Use quick question if available
default_value = st.session_state.quick_question if st.session_state.quick_question else ""
if st.session_state.quick_question:
    st.session_state.quick_question = ""  # Clear after using

user_input = st.text_input(
    "Your question", 
    value=default_value,
    placeholder="Ask about ML concepts, request model builds, or get data insights...",
    help="Type your question or request. I can explain concepts, generate JSON specs, and run models!"
)

if user_input:
    history = st.session_state.chat
    
    # Beautiful thinking animation
    with st.container():
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown(
            '<div style="text-align: center; padding: 2rem;"><div class="loading-dots"><div></div><div></div><div></div><div></div></div><p style="margin-top: 1rem; color: #6b7280;">🧠 SMARTML is thinking...</p></div>',
            unsafe_allow_html=True
        )
        
        # Get response
        response = rag(history, user_input, vectorstore)
        thinking_placeholder.empty()
    
    # Validate response
    if not response or response.strip() == "undefined":
        response = "I couldn't generate a proper response. Please try again with a different question."
    
    # Save to chat history
    history.append((user_input, response))
    st.session_state.chat = history
    
    # === Response Handling ===
    response_clean = response.strip()
    
    # Check for execution signal
    execution_triggers = [
        response_clean == "-1",
        response_clean.lower() == "run_model",
        "run_model" in response_clean.lower(),
        "-1" in response_clean,
        ("json" in response_clean.lower() and ("-1" in response_clean or "run" in response_clean.lower())),
        (response_clean.startswith("{") and "command" in response_clean.lower())
    ]
    
    if any(execution_triggers):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.success("🚀 **Model Execution Initiated!**")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Simulate loading progress
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("🔧 Loading model configuration...")
                elif i < 60:
                    status_text.text("⚡ Training model...")
                elif i < 90:
                    status_text.text("📊 Evaluating performance...")
                else:
                    status_text.text("✨ Generating insights...")
                time.sleep(0.02)
            
            result = runner("sample.json", "model_parameters.json")
            progress_bar.empty()
            status_text.empty()
            
            if "error" in result:
                st.error(f"❌ **Model Execution Failed:** {result['error']}")
            else:
                # Display results with beautiful cards
                st.markdown("### 🎯 Model Performance Results")
                
                # Metrics in beautiful cards
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">{result['acc']:.1%}</div>
                        <div class="metric-label">Accuracy</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    # Extract precision from classification report if available
                    precision = "N/A"
                    if 'cr' in result and result['cr']:
                        lines = result['cr'].split('\n')
                        for line in lines:
                            if 'weighted avg' in line or 'macro avg' in line:
                                parts = line.split()
                                if len(parts) >= 2:
                                    try:
                                        precision = f"{float(parts[1]):.1%}"
                                        break
                                    except:
                                        pass
                    
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">{precision}</div>
                        <div class="metric-label">Precision</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">✅</div>
                        <div class="metric-label">Status</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Detailed results in expandable sections
                with st.expander("📊 **Detailed Classification Report**", expanded=False):
                    st.code(result['cr'], language="text")
                
                with st.expander("🔢 **Confusion Matrix**", expanded=False):
                    st.write(result['cm'])
                
                # Get AI explanation
                user_summary = (
                    f"Explain the following model training results:\n\n"
                    f"Accuracy: {result['acc']:.4f}\n"
                    f"Classification Report:\n{result['cr']}\n"
                    f"Confusion Matrix: {result['cm']}\n"
                    f"Used Parameters: {result['paramters']}"
                )
                
                with st.spinner("🤖 Generating AI insights..."):
                    explanation = rag(st.session_state.chat, user_summary, vectorstore)
                
                st.markdown("### 🧠 SMARTML Analysis")
                st.markdown(f'<div class="assistant-message" style="max-width: 100%; margin: 1rem 0;">{explanation}</div>', unsafe_allow_html=True)
                
                # Save explanation to chat history
                st.session_state.chat.append(("Explain the model training results", explanation))
        
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ **Execution Error:** {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif response_clean.startswith("{") and response_clean.endswith("}"):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 📋 **Generated JSON Specification**")
        st.code(response_clean, language="json")
        
        # Save JSON spec
        try:
            parsed = json.loads(response_clean)
            with open("JSONs/sample.json", "w") as f:
                json.dump(parsed, f, indent=2)
            st.success("✅ **Specification saved** to `JSONs/sample.json`")
        except Exception as e:
            st.error(f"⚠️ **JSON Save Error:** {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Regular response
        st.markdown(f'<div class="assistant-message" style="max-width: 100%; margin: 1rem 0; padding-left: 3rem;">{response_clean}</div>', unsafe_allow_html=True)

# === Beautiful Conversation History ===
if st.session_state.chat:
    st.markdown("---")
    st.markdown("### 💬 Conversation History")
    
    # Reverse order to show latest first
    for i, (q, a) in enumerate(reversed(st.session_state.chat)):
        with st.container():
            # User message
            st.markdown(f'<div class="user-message"><strong>You:</strong> {q}</div>', unsafe_allow_html=True)
            
            # Clean response
            cleaned_response = a.strip() if a else ""
            
            # Assistant response with appropriate formatting
            execution_check = [
                cleaned_response == "-1",
                "json-1" in cleaned_response.lower(),
                "-1" in cleaned_response,
                ("json" in cleaned_response.lower() and ("-1" in cleaned_response or "run" in cleaned_response.lower())),
                "run_model" in cleaned_response.lower(),
                (cleaned_response.startswith("{") and "command" in cleaned_response.lower())
            ]
            
            if any(execution_check):
                st.markdown('<div class="assistant-message" style="max-width: 100%; margin: 1rem 0; padding-left: 3rem;"><em>🚀 SMARTML executed model pipeline</em></div>', unsafe_allow_html=True)
            elif cleaned_response.startswith("{") and cleaned_response.endswith("}"):
                st.markdown('<div class="assistant-message" style="max-width: 100%; margin: 1rem 0; padding-left: 3rem;"><strong>🤖 SMARTML:</strong> Generated JSON specification</div>', unsafe_allow_html=True)
                with st.expander(f"View JSON Spec #{len(st.session_state.chat) - i}", expanded=False):
                    st.code(cleaned_response, language="json")
            elif cleaned_response and cleaned_response != "undefined":
                st.markdown(f'<div class="assistant-message" style="max-width: 100%; margin: 1rem 0; padding-left: 3rem;"><strong>🤖 SMARTML:</strong> {cleaned_response}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="assistant-message" style="max-width: 100%; margin: 1rem 0; padding-left: 3rem;"><em>⚠️ No response generated</em></div>', unsafe_allow_html=True)
            
            st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)

# === Footer ===
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #6b7280; padding: 2rem;"><p>🧠 Powered by SMARTML AI • Built with ❤️ using Streamlit</p></div>',
    unsafe_allow_html=True
)