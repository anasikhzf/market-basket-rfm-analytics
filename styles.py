"""Application CSS with theme support and responsive design."""


def get_css(dark=True):
    """Generate complete CSS based on theme mode.

    Args:
        dark: If True, use dark color scheme. Otherwise, light.

    Returns:
        HTML string with font/icon imports and CSS styles.
    """
    if dark:
        c = {
            "bg": "#0F1117", "surface": "#161B2E", "surface-alt": "#1E2338",
            "text": "#EAEAF0", "text-sec": "#9CA3AF", "text-muted": "#6B7280",
            "accent": "#818CF8", "accent-hover": "#6366F1",
            "border": "#2A2F45",
            "success": "#34D399", "success-bg": "rgba(52,211,153,0.08)",
            "warning": "#FBBF24", "warning-bg": "rgba(251,191,36,0.08)",
        }
    else:
        c = {
            "bg": "#F8FAFC", "surface": "#FFFFFF", "surface-alt": "#F1F5F9",
            "text": "#0F172A", "text-sec": "#64748B", "text-muted": "#94A3B8",
            "accent": "#6366F1", "accent-hover": "#4F46E5",
            "border": "#E2E8F0",
            "success": "#10B981", "success-bg": "rgba(16,185,129,0.06)",
            "warning": "#F59E0B", "warning-bg": "rgba(245,158,11,0.06)",
        }

    return f"""<!-- Font & Icon Imports -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
      rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:\
opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet">

<style>
/* ── Base ── */
:root {{
    --bg:{c['bg']}; --surface:{c['surface']}; --surface-alt:{c['surface-alt']};
    --text:{c['text']}; --text-sec:{c['text-sec']}; --text-muted:{c['text-muted']};
    --accent:{c['accent']}; --accent-hover:{c['accent-hover']};
    --border:{c['border']};
    --success:{c['success']}; --success-bg:{c['success-bg']};
    --warning:{c['warning']}; --warning-bg:{c['warning-bg']};
}}
* {{ font-family: 'Inter', sans-serif !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.stApp {{ background: var(--bg); }}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: var(--surface);
    border-right: 1px solid var(--border);
}}

/* ── Section Header ── */
.section-header {{
    margin-bottom: 24px; padding-bottom: 14px;
    border-bottom: 1px solid var(--border);
}}
.section-header h2 {{
    color: var(--text); font-size: 1.5rem; font-weight: 700;
    margin: 0 0 4px; display: flex; align-items: center; gap: 10px;
}}
.section-header h2 .material-symbols-outlined {{ color: var(--accent); }}
.section-header p {{ color: var(--text-sec); margin: 0; font-size: 0.92rem; }}

/* ── Card ── */
.card {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 18px 22px; margin-bottom: 14px;
    transition: border-color 0.2s ease;
}}
.card:hover {{ border-color: var(--accent); }}
.card h4 {{
    color: var(--text); margin: 0 0 8px; font-size: 0.95rem; font-weight: 600;
    display: flex; align-items: center; gap: 8px;
}}
.card h4 .material-symbols-outlined {{ color: var(--accent); font-size: 20px; }}
.card p {{ color: var(--text-sec); margin: 0; font-size: 0.88rem; line-height: 1.6; }}

/* ── Metric ── */
[data-testid="stMetric"] {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 14px 18px;
}}
[data-testid="stMetric"] label {{
    color: var(--text-sec) !important; font-size: 0.75rem !important;
    font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.5px;
}}
[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: var(--accent) !important; font-weight: 700 !important;
}}

/* ── Button ── */
.stButton > button {{
    background: var(--accent); color: #fff; border: none;
    border-radius: 8px; font-weight: 600; transition: background 0.2s;
}}
.stButton > button:hover {{ background: var(--accent-hover); color: #fff; border: none; }}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {{
    border: 2px dashed var(--border); border-radius: 10px; padding: 14px;
}}
[data-testid="stFileUploader"]:hover {{ border-color: var(--accent); }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
.stTabs [data-baseweb="tab"] {{ border-radius: 8px; font-weight: 500; color: var(--text-sec); }}
.stTabs [aria-selected="true"] {{ color: var(--accent) !important; }}

/* ── Status ── */
.status {{
    border-radius: 0 8px 8px 0; padding: 12px 16px;
    font-size: 0.88rem; font-weight: 500; margin-bottom: 16px;
}}
.status-ok {{
    background: var(--success-bg); border-left: 3px solid var(--success);
    color: var(--success);
}}
.status-warn {{
    background: var(--warning-bg); border-left: 3px solid var(--warning);
    color: var(--warning);
}}

/* ── Process Step (About page) ── */
.process-step {{
    background: var(--surface); border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0; padding: 14px 18px; margin-bottom: 10px;
}}
.process-step h4 {{
    color: var(--text); margin: 0 0 6px; font-size: 0.92rem; font-weight: 600;
    display: flex; align-items: center; gap: 8px;
}}
.process-step h4 .material-symbols-outlined {{ color: var(--accent); font-size: 20px; }}
.process-step p {{
    color: var(--text-sec); margin: 0; font-size: 0.85rem; line-height: 1.65;
}}

/* ── Sidebar Custom ── */
.sidebar-logo {{
    text-align: center; padding: 16px 0 20px;
    border-bottom: 1px solid var(--border); margin-bottom: 12px;
}}
.sidebar-logo .material-symbols-outlined {{ color: var(--accent); }}
.sidebar-logo h3 {{
    color: var(--text); margin: 6px 0 2px; font-size: 1.05rem; font-weight: 700;
}}
.sidebar-logo p {{
    color: var(--text-muted); font-size: 0.68rem; letter-spacing: 1.5px; margin: 0;
}}
.sidebar-status {{
    border-radius: 8px; padding: 12px; text-align: center;
}}
.sidebar-status .material-symbols-outlined {{
    font-size: 16px; vertical-align: middle;
}}

/* ── Responsive ── */
@media (max-width: 768px) {{
    .section-header h2 {{ font-size: 1.2rem; }}
    .section-header p {{ font-size: 0.82rem; }}
    .card h4 {{ font-size: 0.88rem; }}
    .card p, .process-step p {{ font-size: 0.8rem; }}
    .process-step h4 {{ font-size: 0.85rem; }}
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        font-size: 1.1rem !important;
    }}
}}
@media (max-width: 480px) {{
    .section-header h2 {{ font-size: 1rem; }}
    .card {{ padding: 12px 14px; }}
    .process-step {{ padding: 10px 14px; }}
}}
</style>
"""
