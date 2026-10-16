"""Shared UI helper functions."""

import streamlit as st


def mi(name, size=20):
    """Render a Material Symbols Outlined icon as inline HTML.

    Args:
        name: Material icon identifier (e.g. 'home', 'people').
        size: Icon size in pixels.

    Returns:
        HTML string for the icon span element.
    """
    return (
        f'<span class="material-symbols-outlined" '
        f'style="font-size:{size}px;vertical-align:middle">'
        f"{name}</span>"
    )


def section_header(icon_name, title, subtitle=""):
    """Render a page section header with Material icon.

    Args:
        icon_name: Material icon identifier.
        title: Header title text.
        subtitle: Optional subtitle text.
    """
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f'<div class="section-header">'
        f"<h2>{mi(icon_name, 28)} {title}</h2>{sub}</div>",
        unsafe_allow_html=True,
    )


def status_banner(message, ok=True):
    """Display a styled status banner.

    Args:
        message: HTML message content.
        ok: If True, show success style. Otherwise, warning.
    """
    cls = "status-ok" if ok else "status-warn"
    icon = "check_circle" if ok else "warning"
    st.markdown(
        f'<div class="status {cls}">{mi(icon, 18)} {message}</div>',
        unsafe_allow_html=True,
    )
