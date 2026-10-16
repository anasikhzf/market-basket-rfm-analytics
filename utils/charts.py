"""Shared Plotly chart configuration for consistent theming."""

# Curated color palette for chart series
PALETTE = [
    "#818CF8", "#34D399", "#FB923C", "#F472B6",
    "#38BDF8", "#A78BFA", "#FBBF24", "#6EE7B7",
]


def chart_layout(is_dark, height=450, **overrides):
    """Return a base Plotly layout dict matching the app theme.

    Args:
        is_dark: Whether dark mode is active.
        height: Chart height in pixels.
        **overrides: Additional layout properties.

    Returns:
        Dict suitable for fig.update_layout(**result).
    """
    grid = "rgba(255,255,255,0.06)" if is_dark else "rgba(0,0,0,0.06)"
    text_color = "#EAEAF0" if is_dark else "#0F172A"
    layout = dict(
        template="plotly_dark" if is_dark else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(family="Inter, sans-serif", color=text_color),
        xaxis=dict(gridcolor=grid),
        yaxis=dict(gridcolor=grid),
    )
    layout.update(overrides)
    return layout
