import os
import requests
import streamlit as st
from datetime import datetime, date
import html  # Додано для екранування HTML та уникнення XSS/злому верстки

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Taskflow",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=DM+Serif+Display:ital@0;1&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hide Streamlit branding but KEEP the header visible so the sidebar toggle works! */
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent !important; }
.stDeployButton { display: none; }

/* App background */
.stApp {
    background: #0f0f13;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #16161d !important;
    border-right: 1px solid #2a2a35;
}
section[data-testid="stSidebar"] > div {
    background: #16161d !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #c8c8d8 !important;
}

/* Main content area */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 860px;
}

/* Typography */
h1 { font-family: 'DM Serif Display', serif !important; color: #f0f0f8 !important; letter-spacing: -0.5px; }
h2, h3 { color: #e0e0ee !important; font-weight: 500 !important; }

/* Cards for tasks */
.task-card {
    background: #1e1e28;
    border: 1px solid #2a2a38;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.6rem;
    transition: border-color 0.2s;
}
.task-card:hover { border-color: #6c5ce7; }

/* Priority badges */
.badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.3px;
}
.badge-high { background: #3d1f2a; color: #f48fb1; border: 1px solid #5c2d3d; }
.badge-medium { background: #2a2a1a; color: #ffd54f; border: 1px solid #4a420e; }
.badge-low { background: #1a2a1a; color: #81c784; border: 1px solid #1e421e; }

/* Status chip colors */
.status-todo { color: #9e9ec0; }
.status-progress { color: #82b1ff; }
.status-done { color: #69f0ae; }

/* Metric cards */
.metric-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: #1e1e28;
    border: 1px solid #2a2a38;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.metric-number { font-size: 28px; font-weight: 600; color: #e0e0ff; }
.metric-label { font-size: 12px; color: #7a7a9a; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 2px; }

/* Progress bar */
.progress-wrap {
    background: #2a2a38;
    border-radius: 8px;
    height: 6px;
    overflow: hidden;
    margin: 4px 0;
}
.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #6c5ce7, #a29bfe);
    border-radius: 8px;
}

/* Divider */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2a38, transparent);
    margin: 1rem 0;
}

/* Inputs styling */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: #1e1e28 !important;
    border: 1px solid #2a2a38 !important;
    border-radius: 8px !important;
    color: #e0e0ee !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #6c5ce7 !important;
    box-shadow: 0 0 0 2px rgba(108, 92, 231, 0.2) !important;
}

/* Buttons */
.stButton > button {
    background: #6c5ce7 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #7c6cf7 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(108, 92, 231, 0.35) !important;
}

/* Secondary button */
.stButton.secondary > button {
    background: #2a2a38 !important;
    color: #c8c8d8 !important;
}
.stButton.secondary > button:hover {
    background: #32323f !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #1e1e28 !important;
    border-radius: 10px;
    padding: 4px;
    border: 1px solid #2a2a38;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #7a7a9a !important;
    border-radius: 7px !important;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #6c5ce7 !important;
    color: #fff !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* Pills / filter */
.stPills [data-baseweb="button-group"] button {
    background: #1e1e28 !important;
    color: #9090b0 !important;
    border: 1px solid #2a2a38 !important;
}
.stPills [data-baseweb="button-group"] button[data-active="true"],
.stPills [aria-pressed="true"] {
    background: #6c5ce7 !important;
    color: #fff !important;
    border-color: #6c5ce7 !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #1e1e28 !important;
    border-radius: 10px !important;
    color: #c8c8d8 !important;
    font-weight: 500;
}
.streamlit-expanderContent {
    background: #16161d !important;
    border: 1px solid #2a2a38;
    border-top: none;
    border-radius: 0 0 10px 10px;
}

/* Form submit button */
.stFormSubmitButton > button {
    background: #6c5ce7 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    width: 100%;
}

/* Sidebar nav items */
.nav-item {
    padding: 8px 12px;
    border-radius: 8px;
    cursor: pointer;
    color: #9090b0;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
    transition: all 0.15s;
}
.nav-item:hover, .nav-item.active {
    background: rgba(108, 92, 231, 0.15);
    color: #a29bfe;
}
.nav-dot {
    width: 8px; height: 8px; border-radius: 50%;
    display: inline-block; margin-right: 4px;
}

/* Toast-style success */
.stSuccess {
    background: #1a2e1a !important;
    border: 1px solid #2d4d2d !important;
    color: #81c784 !important;
    border-radius: 10px !important;
}
.stError {
    background: #2e1a1a !important;
    border: 1px solid #4d2d2d !important;
    color: #f48fb1 !important;
    border-radius: 10px !important;
}
.stWarning {
    background: #2e2a1a !important;
    border: 1px solid #4d421a !important;
    border-radius: 10px !important;
}
.stInfo {
    background: #1a1e2e !important;
    border: 1px solid #2d354d !important;
    border-radius: 10px !important;
}

/* Date input */
.stDateInput input {
    background: #1e1e28 !important;
    border: 1px solid #2a2a38 !important;
    color: #e0e0ee !important;
    border-radius: 8px !important;
}

/* Checkbox */
.stCheckbox > label > span:first-child {
    border: 2px solid #3a3a4a !important;
    background: #1e1e28 !important;
    border-radius: 4px !important;
}
.stCheckbox > label > span[data-checked="true"]:first-child,
.stCheckbox [aria-checked="true"] span {
    background: #6c5ce7 !important;
    border-color: #6c5ce7 !important;
}

/* Select box */
[data-baseweb="select"] > div:first-child {
    background: #1e1e28 !important;
    border: 1px solid #2a2a38 !important;
    border-radius: 8px !important;
    color: #e0e0ee !important;
}
[data-baseweb="popover"] { background: #1e1e28 !important; border: 1px solid #2a2a38 !important; }
[data-baseweb="menu"] { background: #1e1e28 !important; }
[data-baseweb="option"]:hover { background: rgba(108, 92, 231, 0.2) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #16161d; }
::-webkit-scrollbar-thumb { background: #2a2a38; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #6c5ce7; }
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ─────────────────────────────────────────────────────
DEFAULTS = {
    "token": None,
    "user_email": None,
    "view": "tasks",  # tasks | stats | settings
    "edit_task_id": None,
    "search_query": "",
    "sort_by": "created",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

STATUS_META = {
    "todo": {"label": "To do", "icon": "○", "color": "#9e9ec0"},
    "in_progress": {"label": "In progress", "icon": "◑", "color": "#82b1ff"},
    "done": {"label": "Done", "icon": "●", "color": "#69f0ae"},
}
PRIORITY_META = {
    "high": {"label": "High", "icon": "↑", "badge_class": "badge-high"},
    "medium": {"label": "Medium", "icon": "→", "badge_class": "badge-medium"},
    "low": {"label": "Low", "icon": "↓", "badge_class": "badge-low"},
}
STATUS_VALUES = list(STATUS_META.keys())
PRIORITY_VALUES = list(PRIORITY_META.keys())


# ── Helpers ────────────────────────────────────────────────────────────────────
def api_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}


def handle_error(resp):
    if not resp.ok:
        try:
            detail = resp.json().get("detail", resp.text)
        except Exception:
            detail = resp.text
        st.error(f"❌ {detail}")
        return True
    return False


def fetch_tasks():
    try:
        # Оптимізовано: додано timeout для запобігання зависанню при падінні бекенду
        resp = requests.get(f"{API_URL}/tasks/", headers=api_headers(), timeout=10)
        if handle_error(resp):
            return []
        return resp.json()
    except requests.exceptions.RequestException:
        st.error("❌ Не вдалося з'єднатися з API. Перевірте, чи працює бекенд.")
        return []


def task_stats(tasks):
    total = len(tasks)
    done = sum(1 for t in tasks if t["status"] == "done")
    in_prog = sum(1 for t in tasks if t["status"] == "in_progress")
    todo = sum(1 for t in tasks if t["status"] == "todo")
    pct = int(done / total * 100) if total else 0
    return total, done, in_prog, todo, pct


# ── Auth page ──────────────────────────────────────────────────────────────────
def auth_page():
    col_l, col_c, col_r = st.columns([1, 1.6, 1])
    with col_c:
        st.markdown("""
        <div style='text-align:center; padding: 2.5rem 0 1.5rem;'>
            <div style='font-size:40px; margin-bottom:8px;'>✦</div>
            <h1 style='font-family:"DM Serif Display",serif; font-size:2.2rem; color:#f0f0f8; margin:0;'>Taskflow</h1>
            <p style='color:#6a6a8a; margin-top:6px; font-size:15px;'>Your tasks. Organized.</p>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["Sign in", "Create account"])

        with tab_login:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            with st.form("login_form"):
                email = st.text_input("Email address", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                submitted = st.form_submit_button("Sign in →", use_container_width=True)
            if submitted:
                if not email or not password:
                    st.warning("Please fill in all fields.")
                    return
                try:
                    resp = requests.post(
                        f"{API_URL}/auth/login",
                        data={"username": email, "password": password},
                        timeout=10,
                    )
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to API. Is the backend running?")
                    return
                if handle_error(resp):
                    return
                st.session_state.token = resp.json()["access_token"]
                st.session_state.user_email = email
                st.rerun()

        with tab_register:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            with st.form("register_form"):
                reg_email = st.text_input("Email address", placeholder="you@example.com", key="reg_email")
                reg_pass = st.text_input("Password", type="password", placeholder="min. 8 characters", key="reg_pass")
                reg_pass2 = st.text_input("Confirm password", type="password", placeholder="••••••••", key="reg_pass2")
                submitted = st.form_submit_button("Create account →", use_container_width=True)
            if submitted:
                if not reg_email or not reg_pass:
                    st.warning("Please fill in all fields.")
                    return
                if reg_pass != reg_pass2:
                    st.error("Passwords do not match.")
                    return
                if len(reg_pass) < 8:
                    st.warning("Password must be at least 8 characters.")
                    return
                try:
                    resp = requests.post(
                        f"{API_URL}/auth/register",
                        json={"email": reg_email, "password": reg_pass},
                        timeout=10,
                    )
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to API.")
                    return
                if handle_error(resp):
                    return
                st.success("✓ Account created! Please sign in.")


# ── Sidebar ────────────────────────────────────────────────────────────────────
def render_sidebar(tasks):
    with st.sidebar:
        st.markdown(f"""
        <div style='padding: 0.5rem 0 1rem;'>
            <div style='font-size:22px; font-family:"DM Serif Display",serif; color:#e0e0ff; margin-bottom:2px;'>✦ Taskflow</div>
            <div style='font-size:13px; color:#5a5a7a; border-bottom:1px solid #2a2a38; padding-bottom:1rem;'>{html.escape(st.session_state.user_email or "")}</div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation
        nav_items = [
            ("tasks", "📋", "My Tasks"),
            ("stats", "📊", "Analytics"),
            ("settings", "⚙️", "Settings"),
        ]
        for view_id, icon, label in nav_items:
            active = "active" if st.session_state.view == view_id else ""
            if st.button(f"{icon}  {label}", key=f"nav_{view_id}", use_container_width=True):
                st.session_state.view = view_id
                st.rerun()

        st.markdown("<div style='margin:1rem 0; border-top:1px solid #2a2a38;'></div>", unsafe_allow_html=True)

        # Quick stats
        if tasks:
            total, done, in_prog, todo, pct = task_stats(tasks)
            st.markdown(f"""
            <div style='margin-bottom:0.8rem;'>
                <div style='display:flex; justify-content:space-between; font-size:12px; color:#6a6a8a; margin-bottom:4px;'>
                    <span>Overall progress</span><span style='color:#a29bfe;'>{pct}%</span>
                </div>
                <div class='progress-wrap'>
                    <div class='progress-fill' style='width:{pct}%'></div>
                </div>
            </div>
            <div style='font-size:12px; color:#5a5a7a; line-height:1.8;'>
                <span style='color:#69f0ae;'>●</span> {done} done &nbsp;
                <span style='color:#82b1ff;'>◑</span> {in_prog} in progress &nbsp;
                <span style='color:#9e9ec0;'>○</span> {todo} to do
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin:1rem 0; border-top:1px solid #2a2a38;'></div>", unsafe_allow_html=True)

        # Share (Виправлено: тепер це спливаюче віконечко/popover, як ти просив)
        with st.popover("✉️ Share via Email", use_container_width=True):
            st.markdown("<div style='font-size:14px; font-weight:500; color:#c8c8d8; margin-bottom:10px;'>Send task list</div>", unsafe_allow_html=True)
            with st.form("share_form", clear_on_submit=True):
                share_email = st.text_input("Recipient", placeholder="colleague@company.com", label_visibility="collapsed")
                share_submitted = st.form_submit_button("Send", use_container_width=True)
            if share_submitted and share_email:
                try:
                    resp = requests.post(
                        f"{API_URL}/tasks/share",
                        json={"email": share_email},
                        headers=api_headers(),
                        timeout=10
                    )
                    if not handle_error(resp):
                        st.success(f"✓ Sent to {share_email}")
                except Exception:
                    st.error("Failed to share.")

        st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
        st.markdown("<div style='margin:1rem 0 0.5rem; border-top:1px solid #2a2a38;'></div>", unsafe_allow_html=True)
        if st.button("↩ Sign out", use_container_width=True):
            for k in list(DEFAULTS.keys()):
                st.session_state[k] = DEFAULTS[k]
            st.rerun()


# ── Tasks page ─────────────────────────────────────────────────────────────────
def tasks_page(tasks):
    st.markdown("<h1 style='margin-bottom:0.2rem;'>My Tasks</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#5a5a7a; margin-top:0; font-size:14px;'>{date.today().strftime('%A, %B %d')}</p>",
                unsafe_allow_html=True)

    # ── Stats row ──
    if tasks:
        total, done, in_prog, todo, pct = task_stats(tasks)
        c1, c2, c3, c4 = st.columns(4)
        for col, num, label, clr in [
            (c1, total, "Total", "#a29bfe"),
            (c2, todo, "To do", "#9e9ec0"),
            (c3, in_prog, "In progress", "#82b1ff"),
            (c4, done, "Done", "#69f0ae"),
        ]:
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-number' style='color:{clr};'>{num}</div>
                    <div class='metric-label'>{label}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Add task form ──
    with st.expander("＋  Add new task", expanded=False):
        with st.form("add_task_form", clear_on_submit=True):
            title = st.text_input("Task title *", placeholder="What needs to be done?")
            description = st.text_area("Description", placeholder="Optional details, context, links…", height=80)
            col_s, col_p, col_d = st.columns(3)
            with col_s:
                status = st.selectbox("Status", STATUS_VALUES,
                                      format_func=lambda s: f"{STATUS_META[s]['icon']} {STATUS_META[s]['label']}")
            with col_p:
                priority = st.selectbox("Priority", PRIORITY_VALUES,
                                        format_func=lambda p: f"{PRIORITY_META[p]['icon']} {PRIORITY_META[p]['label']}")
            with col_d:
                due_date = st.date_input("Due date", value=None)
            tags_raw = st.text_input("Tags", placeholder="design, frontend, bug  (comma-separated)")
            add_submitted = st.form_submit_button("Add Task →", use_container_width=True)

        if add_submitted:
            if not title.strip():
                st.warning("Task title is required.")
            else:
                tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []
                payload = {
                    "title": title.strip(),
                    "description": description or None,
                    "status": status,
                    "priority": priority,
                    "due_date": str(due_date) if due_date else None,
                    "tags": tags,
                }
                try:
                    resp = requests.post(f"{API_URL}/tasks/", json=payload, headers=api_headers(), timeout=10)
                    if not handle_error(resp):
                        st.success("✓ Task added!")
                        st.rerun()
                except Exception:
                    st.error("Cannot connect to API.")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if not tasks:
        st.markdown("""
        <div style='text-align:center; padding:3rem; color:#4a4a6a;'>
            <div style='font-size:48px; margin-bottom:1rem;'>✦</div>
            <div style='font-size:18px; color:#5a5a8a; font-weight:500;'>No tasks yet</div>
            <div style='font-size:14px; margin-top:6px;'>Add your first task above to get started.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Toolbar ──
    col_search, col_sort = st.columns([3, 1])
    with col_search:
        search = st.text_input("🔍", placeholder="Search tasks…", label_visibility="collapsed",
                               value=st.session_state.search_query)
        st.session_state.search_query = search
    with col_sort:
        sort_by = st.selectbox("Sort", ["created", "priority", "due_date", "title"], label_visibility="collapsed",
                               format_func=lambda s: {"created": "Newest", "priority": "Priority",
                                                      "due_date": "Due date", "title": "Title"}[s])
        st.session_state.sort_by = sort_by

    # ── Status filter ──
    filter_status = st.pills(
        "Filter",
        options=["all"] + STATUS_VALUES,
        format_func=lambda s: "All" if s == "all" else f"{STATUS_META[s]['icon']} {STATUS_META[s]['label']}",
        default="all",
        label_visibility="collapsed",
    )

    # ── Filter + sort ──
    filtered = tasks
    if filter_status != "all":
        filtered = [t for t in filtered if t["status"] == filter_status]
    if search:
        q = search.lower()
        filtered = [t for t in filtered if q in t["title"].lower() or q in (t.get("description") or "").lower()]

    priority_order = {"high": 0, "medium": 1, "low": 2, None: 3}
    if sort_by == "priority":
        filtered = sorted(filtered, key=lambda t: priority_order.get(t.get("priority"), 3))
    elif sort_by == "title":
        filtered = sorted(filtered, key=lambda t: t["title"].lower())
    elif sort_by == "due_date":
        filtered = sorted(filtered, key=lambda t: t.get("due_date") or "9999")

    st.markdown(
        f"<p style='color:#4a4a6a; font-size:13px; margin:0.5rem 0;'>{len(filtered)} task{'s' if len(filtered) != 1 else ''}</p>",
        unsafe_allow_html=True)

    # ── Task list ──
    for task in filtered:
        s = task.get("status", "todo")
        p = task.get("priority", "medium")
        s_meta = STATUS_META.get(s, STATUS_META["todo"])
        p_meta = PRIORITY_META.get(p, PRIORITY_META["medium"])
        due = task.get("due_date")
        tags = task.get("tags", [])

        is_done = s == "done"
        title_style = "text-decoration:line-through; color:#5a5a7a;" if is_done else "color:#e0e0ee;"

        # Оптимізація безпеки та верстки (екранування та формування рядків без порожніх абзаців)
        safe_title = html.escape(task.get("title", ""))
        safe_desc = html.escape(task.get("description", "")) if task.get("description") else ""

        # Due date formatting
        due_html = ""
        if due:
            try:
                due_dt = datetime.strptime(due[:10], "%Y-%m-%d").date()
                today = date.today()
                diff = (due_dt - today).days
                if diff < 0:
                    due_html = f"<span style='color:#f48fb1; font-size:12px;'>⚠ Overdue {abs(diff)}d</span>"
                elif diff == 0:
                    due_html = "<span style='color:#ffd54f; font-size:12px;'>⚡ Due today</span>"
                elif diff <= 3:
                    due_html = f"<span style='color:#ffb74d; font-size:12px;'>⏰ {diff}d left</span>"
                else:
                    due_html = f"<span style='color:#5a5a7a; font-size:12px;'>📅 {due_dt.strftime('%b %d')}</span>"
            except Exception:
                due_html = ""

        tags_html = " ".join(
            f"<span style='background:#1e1e38; color:#7a7aba; font-size:11px; padding:1px 7px; border-radius:12px; border:1px solid #2a2a4a;'>{html.escape(tag)}</span>"
            for tag in tags
        ) if tags else ""

        # Виправлення: збираємо HTML-блок без відкритого f-string форматування з переносами
        card_html = (
            f'<div class="task-card">'
            f'<div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">'
            f'<div style="flex:1;">'
            f'<div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:2px;">'
            f'<span style="{title_style} font-size:15px; font-weight:500;">{safe_title}</span>'
            f'<span class="badge {p_meta["badge_class"]}">{p_meta["icon"]} {p_meta["label"]}</span>'
            f'{due_html}'
            f'</div>'
        )

        if safe_desc:
            card_html += f"<div style='color:#6a6a8a; font-size:13px; margin-top:4px;'>{safe_desc}</div>"

        if tags_html:
            card_html += f"<div style='margin-top:8px; display:flex; gap:4px; flex-wrap:wrap;'>{tags_html}</div>"

        card_html += (
            f'</div>'
            f'<div style="display:flex; align-items:center; gap:6px;">'
            f'<span style="color:{s_meta["color"]}; font-size:13px; white-space:nowrap;">{s_meta["icon"]} {s_meta["label"]}</span>'
            f'</div>'
            f'</div>'
            f'</div>'
        )

        st.markdown(card_html, unsafe_allow_html=True)

        # Controls row
        col_s, col_p2, col_e, col_d = st.columns([3, 2, 1, 1])
        with col_s:
            new_status = st.selectbox("Status", STATUS_VALUES,
                                      format_func=lambda x: f"{STATUS_META[x]['icon']} {STATUS_META[x]['label']}",
                                      index=STATUS_VALUES.index(s),
                                      key=f"status_{task['id']}",
                                      label_visibility="collapsed")
            if new_status != s:
                requests.patch(f"{API_URL}/tasks/{task['id']}",
                               json={"status": new_status}, headers=api_headers(), timeout=10)
                st.rerun()
        with col_p2:
            new_prio = st.selectbox("Priority", PRIORITY_VALUES,
                                    format_func=lambda x: f"{PRIORITY_META[x]['icon']} {PRIORITY_META[x]['label']}",
                                    index=PRIORITY_VALUES.index(p) if p in PRIORITY_VALUES else 1,
                                    key=f"prio_{task['id']}",
                                    label_visibility="collapsed")
            if new_prio != p:
                requests.patch(f"{API_URL}/tasks/{task['id']}",
                               json={"priority": new_prio}, headers=api_headers(), timeout=10)
                st.rerun()
        with col_e:
            if st.button("✎", key=f"edit_{task['id']}", help="Edit task"):
                st.session_state.edit_task_id = task["id"]
                st.rerun()
        with col_d:
            if st.button("🗑", key=f"del_{task['id']}", help="Delete task"):
                requests.delete(f"{API_URL}/tasks/{task['id']}", headers=api_headers(), timeout=10)
                st.rerun()

        # Inline edit form
        if st.session_state.edit_task_id == task["id"]:
            with st.form(f"edit_form_{task['id']}"):
                st.markdown("<p style='color:#a29bfe; font-size:13px; margin-bottom:8px;'>✎ Editing task</p>",
                            unsafe_allow_html=True)
                new_title = st.text_input("Title", value=task["title"])
                new_desc = st.text_area("Description", value=task.get("description") or "", height=80)
                new_due = st.date_input("Due date",
                                        value=datetime.strptime(task["due_date"][:10], "%Y-%m-%d").date() if task.get(
                                            "due_date") else None)
                new_tags = st.text_input("Tags (comma-separated)", value=", ".join(task.get("tags", [])))
                col_save, col_cancel = st.columns(2)
                with col_save:
                    save = st.form_submit_button("Save", use_container_width=True)
                with col_cancel:
                    cancel = st.form_submit_button("Cancel", use_container_width=True)
            if save:
                tags_list = [t.strip() for t in new_tags.split(",") if t.strip()]
                try:
                    requests.patch(f"{API_URL}/tasks/{task['id']}", json={
                        "title": new_title,
                        "description": new_desc or None,
                        "due_date": str(new_due) if new_due else None,
                        "tags": tags_list,
                    }, headers=api_headers(), timeout=10)
                except Exception:
                    pass
                st.session_state.edit_task_id = None
                st.rerun()
            if cancel:
                st.session_state.edit_task_id = None
                st.rerun()


# ── Analytics page ─────────────────────────────────────────────────────────────
def stats_page(tasks):
    st.markdown("<h1>Analytics</h1>", unsafe_allow_html=True)

    if not tasks:
        st.info("No tasks yet. Add some tasks to see analytics.")
        return

    total, done, in_prog, todo, pct = task_stats(tasks)

    # Completion rate
    st.markdown(f"""
    <div class='metric-card' style='margin-bottom:1rem;'>
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <div class='metric-label'>Completion rate</div>
                <div class='metric-number' style='color:#a29bfe;'>{pct}%</div>
            </div>
            <div style='width:120px;'>
                <div class='progress-wrap'><div class='progress-fill' style='width:{pct}%'></div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, val, lbl, clr in [
        (c1, todo, "To do", "#9e9ec0"),
        (c2, in_prog, "In progress", "#82b1ff"),
        (c3, done, "Done", "#69f0ae"),
    ]:
        with col:
            bar_pct = int(val / total * 100) if total else 0
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-number' style='color:{clr};'>{val}</div>
                <div class='metric-label'>{lbl}</div>
                <div class='progress-wrap' style='margin-top:8px;'>
                    <div style='height:100%; width:{bar_pct}%; background:{clr}; border-radius:8px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Priority breakdown
    st.markdown("<h3>By priority</h3>", unsafe_allow_html=True)
    prio_counts = {p: sum(1 for t in tasks if t.get("priority") == p) for p in PRIORITY_VALUES}
    p_colors = {"high": "#f48fb1", "medium": "#ffd54f", "low": "#81c784"}
    col1, col2, col3 = st.columns(3)
    for col, (p, cnt) in zip([col1, col2, col3], prio_counts.items()):
        pct_p = int(cnt / total * 100) if total else 0
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-number' style='color:{p_colors[p]};'>{cnt}</div>
                <div class='metric-label'>{PRIORITY_META[p]['label']} priority</div>
                <div style='font-size:11px; color:#4a4a6a; margin-top:4px;'>{pct_p}% of tasks</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Overdue tasks
    overdue = []
    for t in tasks:
        if t.get("due_date") and t["status"] != "done":
            try:
                due_dt = datetime.strptime(t["due_date"][:10], "%Y-%m-%d").date()
                if due_dt < date.today():
                    overdue.append(t)
            except Exception:
                pass
    if overdue:
        st.markdown(f"<h3 style='color:#f48fb1;'>⚠ Overdue ({len(overdue)})</h3>", unsafe_allow_html=True)
        for t in overdue:
            safe_overdue_title = html.escape(t['title'])
            st.markdown(f"""
            <div class='task-card' style='border-color:#5c2d3d;'>
                <span style='color:#f48fb1; font-size:14px; font-weight:500;'>{safe_overdue_title}</span>
                <span style='color:#6a4a55; font-size:12px; margin-left:8px;'>due {t['due_date'][:10]}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✓ No overdue tasks!")


# ── Settings page ──────────────────────────────────────────────────────────────
def settings_page():
    st.markdown("<h1>Settings</h1>", unsafe_allow_html=True)

    st.markdown("<h3>Account</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='task-card'>
        <div style='color:#7a7a9a; font-size:12px; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:4px;'>Logged in as</div>
        <div style='color:#e0e0ee; font-size:15px; font-weight:500;'>{html.escape(st.session_state.user_email or "")}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3>Change Password</h3>", unsafe_allow_html=True)
    with st.form("change_pass_form"):
        old_pass = st.text_input("Current password", type="password")
        new_pass = st.text_input("New password", type="password")
        new_pass2 = st.text_input("Confirm new password", type="password")
        submitted = st.form_submit_button("Update password", use_container_width=True)
    if submitted:
        if new_pass != new_pass2:
            st.error("Passwords do not match.")
        elif len(new_pass) < 8:
            st.warning("Password must be at least 8 characters.")
        else:
            try:
                resp = requests.post(
                    f"{API_URL}/auth/change-password",
                    json={"old_password": old_pass, "new_password": new_pass},
                    headers=api_headers(),
                    timeout=10
                )
                if not handle_error(resp):
                    st.success("✓ Password updated.")
            except Exception:
                st.error("Cannot connect to API.")

    st.markdown("<h3>Danger Zone</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='task-card' style='border-color:#5c2d3d;'>
        <div style='color:#f48fb1; font-size:14px; font-weight:500; margin-bottom:4px;'>Delete all tasks</div>
        <div style='color:#6a4a55; font-size:13px;'>This action is irreversible.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🗑 Delete all tasks", use_container_width=True):
        try:
            resp = requests.delete(f"{API_URL}/tasks/", headers=api_headers(), timeout=10)
            if not handle_error(resp):
                st.success("All tasks deleted.")
                st.rerun()
        except Exception:
            st.error("Cannot connect to API.")


# ── Main app ───────────────────────────────────────────────────────────────────
def main_page():
    tasks = fetch_tasks()
    render_sidebar(tasks)

    view = st.session_state.view
    if view == "tasks":
        tasks_page(tasks)
    elif view == "stats":
        stats_page(tasks)
    elif view == "settings":
        settings_page()


# ── Entry point ────────────────────────────────────────────────────────────────
if st.session_state.token:
    main_page()
else:
    auth_page()