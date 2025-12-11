import streamlit as st

from services.get_models_list import get_ollama_models_list
from services.get_title import get_chat_title
from services.chat_utilities import get_answer
from db.conversations import(
    create_new_conversation,
    add_message,
    get_conversation,
    get_all_conversations,
    delete_conversation
)

st.set_page_config(page_title="ConvoPro", page_icon="💬", layout="centered")
st.title("💬 ConvoPro - Chat with LLMs/Local ChatGpt Clone")

if "OLLAMA_MODELS" not in st.session_state:
    st.session_state.OLLAMA_MODELS = get_ollama_models_list()

# Model selection
selected_model = st.selectbox("Select LLM Model", st.session_state.OLLAMA_MODELS)

# Session state initialization
st.session_state.setdefault("conversation_id", None)
st.session_state.setdefault("conversation_title", None)
st.session_state.setdefault("chat_history", [])

# Sidebar conversations
with st.sidebar:
    st.header("💬 Chat History")
    conversations = get_all_conversations()

    if st.button("➕ New Chat"):
        st.session_state.conversation_id = None
        st.session_state.conversation_title = None
        st.session_state.chat_history = []
    
    for cid, title in conversations.items():
        cols = st.columns([4, 1])  # main button + delete button

        with cols[0]:
            is_current = cid == st.session_state.conversation_id
            label = f"📌 {title}" if is_current else title
            if st.button(label, key=f"conv_{cid}"):
                doc = get_conversation(cid) or {}
                st.session_state.conversation_id = cid
                st.session_state.conversation_title = doc.get("title", "Untitled Conversation")
                st.session_state.chat_history = [
                    {"role": m["role"], "content": m["content"]} for m in doc.get("messages", [])
                ]

        with cols[1]:
            if st.button("🗑", key=f"delete_{cid}"):
                delete_conversation(cid)

                # If user deletes the active one — wipe UI state
                if st.session_state.get("conversation_id") == cid:
                    st.session_state.conversation_id = None
                    st.session_state.chat_history = []
                    st.rerun()

                # Refresh sidebar immediately
                st.rerun()

# Show chat so far 
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_query = st.chat_input("Type your message here...")
if user_query:
    # 1. Show and store message in UI state
    st.chat_message("user").markdown(user_query)
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    # 2. Persist to DB. Create new conversation on first message else append
    if st.session_state.conversation_id is None:
        try:
            title = get_chat_title(selected_model, user_query) or "New Chat"
        except Exception:
            title = "New Chat"
        
        conv_id = create_new_conversation(title=title, role="user", content=user_query)
        st.session_state.conversation_id = conv_id
        st.session_state.conversation_title = title
    else:
        add_message(st.session_state.conversation_id, role="user", content=user_query)

    # 3. Get assistant response (direct service)
    try:
        assistant_response = get_answer(selected_model, st.session_state.chat_history)
    except Exception as e:
        assistant_response = f"Error {e}: Unable to get response from the model."

    # 4. Show and store assistant response in UI state
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # 5. Persist assistant response to DB
    if st.session_state.conversation_id:
        add_message(st.session_state.conversation_id, role="assistant", content=assistant_response)