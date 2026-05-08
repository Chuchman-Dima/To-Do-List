import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="📋 Todo App", page_icon="📋", layout="centered")

# ── Session state defaults ─────────────────────────────────────────────────────
if "token" not in st.session_state:
    st.session_state.token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None


# ── Helpers ────────────────────────────────────────────────────────────────────
def api_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}


def handle_error(resp):
    if not resp.ok:
        detail = resp.json().get("detail", resp.text)
        st.error(f"Error: {detail}")
        return True
    return False


# ── Auth page ──────────────────────────────────────────────────────────────────
def auth_page():
    st.title("📋 Todo App")
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
        if submitted:
            resp = requests.post(
                f"{API_URL}/auth/login",
                data={"username": email, "password": password},
            )
            if handle_error(resp):
                return
            st.session_state.token = resp.json()["access_token"]
            st.session_state.user_email = email
            st.rerun()

    with tab_register:
        with st.form("register_form"):
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_pass")
            submitted = st.form_submit_button("Register", use_container_width=True)
        if submitted:
            resp = requests.post(
                f"{API_URL}/auth/register",
                json={"email": email, "password": password},
            )
            if handle_error(resp):
                return
            st.success("Registered! Please log in.")


# ── Main app ───────────────────────────────────────────────────────────────────
def main_page():
    STATUS_LABELS = {
        "todo": "⬜ Todo",
        "in_progress": "🔄 In Progress",
        "done": "✅ Done",
    }
    STATUS_VALUES = list(STATUS_LABELS.keys())

    # Sidebar
    with st.sidebar:
        st.markdown(f"👤 **{st.session_state.user_email}**")
        st.divider()

        st.subheader("📨 Share via Email")
        with st.form("share_form"):
            share_email = st.text_input("Recipient email")
            share_submitted = st.form_submit_button("Send", use_container_width=True)
        if share_submitted:
            resp = requests.post(
                f"{API_URL}/tasks/share",
                json={"email": share_email},
                headers=api_headers(),
            )
            if not handle_error(resp):
                st.success("List sent!")

        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.user_email = None
            st.rerun()

    # Main area
    st.title("📋 My Tasks")

    # Add task form
    with st.expander("➕ Add new task", expanded=False):
        with st.form("add_task_form"):
            title = st.text_input("Title")
            description = st.text_area("Description (optional)")
            status = st.selectbox(
                "Status",
                options=STATUS_VALUES,
                format_func=lambda s: STATUS_LABELS[s],
            )
            add_submitted = st.form_submit_button("Add Task", use_container_width=True)
        if add_submitted:
            if not title.strip():
                st.warning("Title is required.")
            else:
                resp = requests.post(
                    f"{API_URL}/tasks/",
                    json={"title": title, "description": description or None, "status": status},
                    headers=api_headers(),
                )
                if not handle_error(resp):
                    st.rerun()

    # Fetch and display tasks
    resp = requests.get(f"{API_URL}/tasks/", headers=api_headers())
    if handle_error(resp):
        return
    tasks = resp.json()

    if not tasks:
        st.info("No tasks yet. Add your first task above!")
        return

    # Filter
    filter_status = st.pills(
        "Filter by status",
        options=["all"] + STATUS_VALUES,
        format_func=lambda s: "🔍 All" if s == "all" else STATUS_LABELS[s],
        default="all",
    )

    filtered = tasks if filter_status == "all" else [t for t in tasks if t["status"] == filter_status]

    st.markdown(f"**{len(filtered)} task(s)**")
    st.divider()

    for task in filtered:
        col_main, col_status, col_del = st.columns([5, 3, 1])

        with col_main:
            st.markdown(f"**{task['title']}**")
            if task.get("description"):
                st.caption(task["description"])

        with col_status:
            new_status = st.selectbox(
                "Status",
                options=STATUS_VALUES,
                format_func=lambda s: STATUS_LABELS[s],
                index=STATUS_VALUES.index(task["status"]),
                key=f"status_{task['id']}",
                label_visibility="collapsed",
            )
            if new_status != task["status"]:
                requests.patch(
                    f"{API_URL}/tasks/{task['id']}",
                    json={"status": new_status},
                    headers=api_headers(),
                )
                st.rerun()

        with col_del:
            if st.button("🗑️", key=f"del_{task['id']}", help="Delete task"):
                requests.delete(f"{API_URL}/tasks/{task['id']}", headers=api_headers())
                st.rerun()

        st.divider()


# ── Entry point ────────────────────────────────────────────────────────────────
if st.session_state.token:
    main_page()
else:
    auth_page()
