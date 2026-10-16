"""
Sistem Cerdas E-Commerce
Customer Segmentation & Market Basket Analysis
Main application entry point.
"""

import streamlit as st
from styles import get_css
from utils.helpers import mi
from utils.views_home import render_home_page, render_about_page
from utils.views_analysis import render_explorer_page, render_segmentation_page
from utils.views_mba import render_market_basket_page

# ─── Page Configuration ───
st.set_page_config(
    page_title="Sistem Cerdas E-Commerce",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Theme Management ───
if "is_dark_theme" not in st.session_state:
    st.session_state["is_dark_theme"] = True

# ─── Sidebar Header & Controls ───
with st.sidebar:
    st.markdown(
        f"""
        <div class="sidebar-logo">
            <div>{mi('hub', 36)}</div>
            <h3>Sistem Cerdas</h3>
            <p>E-COMMERCE ANALYTICS</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Theme toggle
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.markdown(
            f"<span style='font-size:0.85rem; font-weight:600; color:var(--text); vertical-align:middle;'>"
            f"{mi('dark_mode' if st.session_state['is_dark_theme'] else 'light_mode', 18)} Mode Gelap</span>",
            unsafe_allow_html=True
        )
    with col_t2:
        dark_toggle = st.toggle(
            "Mode",
            value=st.session_state["is_dark_theme"],
            label_visibility="collapsed"
        )
        if dark_toggle != st.session_state["is_dark_theme"]:
            st.session_state["is_dark_theme"] = dark_toggle
            st.rerun()

    st.markdown("<hr style='border:none; border-top:1px solid var(--border); margin:12px 0 16px 0;'>", unsafe_allow_html=True)

    # Navigation Menu
    menu_options = [
        "Beranda",
        "Data Explorer",
        "Customer Segmentation",
        "Market Basket Analysis",
        "Tentang Sistem"
    ]
    menu_icons = {
        "Beranda": "home",
        "Data Explorer": "table_chart",
        "Customer Segmentation": "groups",
        "Market Basket Analysis": "shopping_basket",
        "Tentang Sistem": "info"
    }

    selected_page = st.radio(
        "NAVIGASI",
        menu_options,
        index=0,
        format_func=lambda x: f"{x}",
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border:none; border-top:1px solid var(--border); margin:18px 0;'>", unsafe_allow_html=True)

    # Dataset Status Card in Sidebar
    if "df_clean" in st.session_state:
        n_rows = len(st.session_state["df_clean"])
        st.markdown(
            f"""
            <div class="sidebar-status" style="background:var(--success-bg); border:1px solid var(--success); color:var(--success);">
                <div style="font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.8px;">
                    {mi('check_circle', 16)} Dataset Aktif
                </div>
                <div style="font-size:1.35rem; font-weight:700; margin:4px 0 2px 0;">{n_rows:,}</div>
                <div style="font-size:0.75rem; opacity:0.85;">baris data bersih</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="sidebar-status" style="background:var(--warning-bg); border:1px solid var(--warning); color:var(--warning);">
                <div style="font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.8px;">
                    {mi('info', 16)} Status Data
                </div>
                <div style="font-size:0.85rem; font-weight:600; margin:4px 0 2px 0;">Belum Ada Dataset</div>
                <div style="font-size:0.72rem; opacity:0.85;">Muat via Data Explorer</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ─── Inject Clean Dynamic Styling ───
st.markdown(get_css(dark=st.session_state["is_dark_theme"]), unsafe_allow_html=True)

# ─── Main Content Router ───
is_dark = st.session_state["is_dark_theme"]

if selected_page == "Beranda":
    render_home_page()
elif selected_page == "Data Explorer":
    render_explorer_page()
elif selected_page == "Customer Segmentation":
    render_segmentation_page(is_dark)
elif selected_page == "Market Basket Analysis":
    render_market_basket_page(is_dark)
elif selected_page == "Tentang Sistem":
    render_about_page()

# ─── Footer ───
st.markdown(
    f"""
    <div style="text-align: center; padding: 36px 0 20px 0; margin-top: 48px; border-top: 1px solid var(--border);">
        <p style="color: var(--text-muted); font-size: 0.8rem; margin: 0;">
            Sistem Cerdas E-Commerce • Customer Segmentation & Market Basket Analysis<br>
            <span style="font-size: 0.75rem;">Desain Minimalis Modern • Modul Terstruktur • Analitik Komputasi Lokal</span>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
