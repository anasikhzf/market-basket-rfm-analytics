"""Interactive Plotly charts styled for minimal aesthetics and theme-reactivity."""

import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import pandas as pd
from utils.charts import chart_layout, PALETTE


def plot_elbow(k_range, inertias, is_dark):
    """Render elbow curve for optimal K."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=k_range,
        y=inertias,
        mode="lines+markers",
        line=dict(color="#6366F1", width=2.5),
        marker=dict(size=8, color="#818CF8", line=dict(width=2, color="#4F46E5")),
        name="Inertia"
    ))
    fig.update_layout(
        **chart_layout(
            is_dark,
            height=340,
            xaxis_title="Jumlah Cluster (K)",
            yaxis_title="Inertia (Within-Cluster Sum of Squares)",
            showlegend=False
        )
    )
    return fig


def plot_3d_clusters(rfm_df, is_dark):
    """Render 3D Scatter Plot for Recency vs Frequency vs Monetary."""
    fig = px.scatter_3d(
        rfm_df,
        x="Recency",
        y="Frequency",
        z="Monetary",
        color="Segment",
        opacity=0.75,
        hover_data=["CustomerID", "Recency", "Frequency", "Monetary"],
        color_discrete_sequence=PALETTE
    )
    bg_grid = "rgba(255,255,255,0.06)" if is_dark else "rgba(0,0,0,0.06)"
    text_color = "#EAEAF0" if is_dark else "#0F172A"

    fig.update_layout(
        template="plotly_dark" if is_dark else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        height=580,
        margin=dict(l=0, r=0, t=10, b=0),
        font=dict(family="Inter, sans-serif", color=text_color),
        legend=dict(
            bgcolor="rgba(22, 27, 46, 0.85)" if is_dark else "rgba(255, 255, 255, 0.85)",
            bordercolor="rgba(129, 140, 248, 0.3)",
            borderwidth=1,
            font=dict(size=11)
        ),
        scene=dict(
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor=bg_grid),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor=bg_grid),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor=bg_grid),
        )
    )
    return fig


def plot_segment_distribution(segment_counts, is_dark):
    """Render bar chart of customer segments."""
    fig = px.bar(
        segment_counts,
        x="Segment",
        y="Count",
        text=segment_counts.apply(lambda r: f"{r['Count']:,} ({r['Percentage']}%)", axis=1),
        color="Segment",
        color_discrete_sequence=PALETTE
    )
    fig.update_layout(
        **chart_layout(
            is_dark,
            height=400,
            showlegend=False,
            yaxis_title="Jumlah Pelanggan",
            xaxis_title=""
        )
    )
    fig.update_traces(textposition="outside")
    return fig


def plot_segment_pie(segment_counts, is_dark):
    """Render donut chart of customer segment distribution."""
    fig = px.pie(
        segment_counts,
        values="Count",
        names="Segment",
        color_discrete_sequence=PALETTE,
        hole=0.5
    )
    text_color = "#EAEAF0" if is_dark else "#0F172A"
    fig.update_layout(
        template="plotly_dark" if is_dark else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        height=380,
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(family="Inter, sans-serif", color=text_color),
        legend=dict(font=dict(size=11))
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def plot_rfm_comparison(cluster_means, is_dark):
    """Render grouped bar chart for mean RFM values."""
    fig = go.Figure()
    metrics = ["Recency", "Frequency", "Monetary"]
    units = ["(hari)", "(transaksi)", "(£)"]
    colors = ["#818CF8", "#34D399", "#FB923C"]

    for i, (m, u) in enumerate(zip(metrics, units)):
        fig.add_trace(go.Bar(
            x=cluster_means["Segment"],
            y=cluster_means[m],
            name=f"{m} {u}",
            marker_color=colors[i],
            opacity=0.88
        ))

    fig.update_layout(
        **chart_layout(
            is_dark,
            height=420,
            barmode="group",
            yaxis_title="Nilai Rata-rata",
            xaxis_title=""
        )
    )
    return fig


def plot_top_rules(rules_df, is_dark):
    """Render horizontal bar chart for top association rules."""
    top = rules_df.head(15).copy()
    fig = px.bar(
        top,
        x="lift",
        y=top.apply(lambda r: f"{r['antecedents'][:28]} → {r['consequents'][:28]}", axis=1),
        orientation="h",
        color="confidence",
        color_continuous_scale="Viridis",
        labels={"lift": "Lift", "y": "Aturan Produk", "confidence": "Confidence"}
    )
    fig.update_layout(
        **chart_layout(
            is_dark,
            height=480,
            yaxis=dict(autorange="reversed"),
            xaxis_title="Nilai Lift"
        )
    )
    return fig


def plot_rules_network(rules_df, is_dark, top_n=20):
    """Render interactive network graph for product associations."""
    net_rules = rules_df.head(top_n)
    graph = nx.DiGraph()

    for _, row in net_rules.iterrows():
        graph.add_edge(row["antecedents"][:30], row["consequents"][:30], weight=row["lift"])

    pos = nx.spring_layout(graph, k=1.8, seed=42)

    edge_x, edge_y = [], []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color="rgba(129, 140, 248, 0.45)"),
        hoverinfo="none",
        mode="lines"
    )

    node_x = [pos[n][0] for n in graph.nodes()]
    node_y = [pos[n][1] for n in graph.nodes()]
    degrees = [graph.degree(n) for n in graph.nodes()]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        hoverinfo="text",
        text=[n[:18] for n in graph.nodes()],
        textposition="top center",
        textfont=dict(size=9, color="#94A3B8" if not is_dark else "#CBD5E1"),
        marker=dict(
            size=[12 + d * 3 for d in degrees],
            color=degrees,
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Hubungan", thickness=12),
            line=dict(width=1, color="rgba(99, 102, 241, 0.5)")
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        **chart_layout(
            is_dark,
            height=520,
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )
    )
    return fig


def plot_rules_heatmap(rules_df, is_dark, max_items=12):
    """Render association heatmap matrix."""
    top_subset = rules_df.head(30)
    items = set()
    for _, r in top_subset.iterrows():
        items.add(r["antecedents"][:26])
        items.add(r["consequents"][:26])
    items = sorted(list(items))[:max_items]

    matrix = pd.DataFrame(0.0, index=items, columns=items)
    for _, r in top_subset.iterrows():
        ant = r["antecedents"][:26]
        con = r["consequents"][:26]
        if ant in items and con in items:
            matrix.loc[ant, con] = r["lift"]

    fig = px.imshow(
        matrix.values,
        x=matrix.columns,
        y=matrix.index,
        color_continuous_scale="Viridis",
        labels=dict(color="Lift"),
        aspect="auto"
    )
    fig.update_layout(
        **chart_layout(
            is_dark,
            height=480,
            xaxis=dict(tickangle=45, tickfont=dict(size=9)),
            yaxis=dict(tickfont=dict(size=9))
        )
    )
    return fig
