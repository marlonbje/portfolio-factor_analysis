import dash
from analysis import PFA
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

BG_PAGE   = "#0d0f14"
BG_CARD   = "#13161e"
BORDER    = "#1f2535"
ACCENT    = "#5b8dee"
ACCENT2   = "#e05b8d"
TEXT_PRI  = "#e8eaf0"
TEXT_SEC  = "#7a8299"
FONT      = "IBM Plex Mono, monospace"

PLOT_TEMPLATE = dict(
    template="plotly_dark",
    paper_bgcolor=BG_CARD,
    plot_bgcolor=BG_CARD,
    font_family=FONT,
    font_color=TEXT_PRI,
    height=800,
    margin=dict(l=48, r=32, t=56, b=48),
)


def build_pc_figure(pc):
    expl_var_cs = pc[0]
    try:
        comps = pc[1].iloc[:3].T
    except (ValueError, KeyError):
        comps = pc[1].

    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=["Cumulative Explained Variance", "Top-3 Principal Components"],
        vertical_spacing=0.12,
    )

    fig.add_trace(
        go.Bar(
            x=expl_var_cs.index,
            y=expl_var_cs,
            name="Expl. Variance",
            marker_color=ACCENT,
            marker_line_width=0,
        ),
        row=1, col=1,
    )

    palette = [ACCENT, ACCENT2, "#5be0b3"]
    for i, comp in enumerate(comps.columns):
        fig.add_trace(
            go.Scatter(
                x=comps.index,
                y=comps[comp],
                mode="lines+markers",
                name=str(comp),
                line=dict(color=palette[i % len(palette)], width=2),
                marker=dict(size=5),
            ),
            row=2, col=1,
        )

    fig.update_layout(**PLOT_TEMPLATE)
    fig.update_xaxes(gridcolor=BORDER, zeroline=False)
    fig.update_yaxes(gridcolor=BORDER, zeroline=False)
    return fig


def build_risk_figure(risk):
    std = risk[0].sort_values()
    cov = risk[1]

    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=["Covariance Matrix", "Standard Deviations"],
        vertical_spacing=0.12,
    )

    fig.add_trace(
        go.Heatmap(
            z=cov,
            x=cov.columns,
            y=cov.columns,
            colorscale="Blues",
            showscale=True,
        ),
        row=1, col=1,
    )

    fig.add_trace(
        go.Bar(
            x=std.index,
            y=std,
            name="Std Dev",
            marker_color=ACCENT2,
            marker_line_width=0,
        ),
        row=2, col=1,
    )

    fig.update_layout(**PLOT_TEMPLATE)
    fig.update_xaxes(gridcolor=BORDER, zeroline=False)
    fig.update_yaxes(gridcolor=BORDER, zeroline=False)
    return fig

app = dash.Dash(__name__)
app.title = "PFA Dashboard"

DROPDOWN_STYLE = dict(
    backgroundColor=BG_CARD,
    color=TEXT_PRI,
    border=f"1px solid {BORDER}",
    fontFamily=FONT,
    fontSize="13px",
    borderRadius="6px",
    width="320px",
)

app.layout = html.Div(
    style={
        "backgroundColor": BG_PAGE,
        "minHeight": "100vh",
        "fontFamily": FONT,
        "color": TEXT_PRI,
        "padding": "32px 40px",
    },
    children=[
        html.Div(
            style={"marginBottom": "28px"},
            children=[
                html.Span(
                    "PFA",
                    style={
                        "fontSize": "11px",
                        "letterSpacing": "4px",
                        "color": ACCENT,
                        "textTransform": "uppercase",
                        "display": "block",
                        "marginBottom": "6px",
                    },
                ),
                html.H1(
                    "Portfolio Factor Analysis",
                    style={
                        "margin": "0",
                        "fontSize": "26px",
                        "fontWeight": "600",
                        "color": TEXT_PRI,
                        "letterSpacing": "-0.5px",
                    },
                ),
                html.Hr(style={"borderColor": BORDER, "marginTop": "18px"}),
            ],
        ),

        html.Div(
            style={"display": "flex", "alignItems": "center", "gap": "16px", "marginBottom": "28px"},
            children=[
                html.Label(
                    "View",
                    style={"color": TEXT_SEC, "fontSize": "12px", "letterSpacing": "1px"},
                ),
                dcc.Dropdown(
                    id="view-dropdown",
                    options=[
                        {"label": "Principal Component Analysis", "value": "pc"},
                        {"label": "Risk Analysis",                "value": "risk"},
                    ],
                    value="pc",
                    clearable=False,
                    style=DROPDOWN_STYLE,
                ),
            ],
        ),

        html.Div(
            style={
                "backgroundColor": BG_CARD,
                "border": f"1px solid {BORDER}",
                "borderRadius": "10px",
                "padding": "8px",
            },
            children=[
                dcc.Graph(id="main-graph", config={"displayModeBar": False}),
            ],
        ),
    ],
)

@app.callback(
    Output("main-graph", "figure"),
    Input("view-dropdown", "value"),
)

def update_graph(selected_view):
    pc = pfa.pc_analysis()
    risk = pfa.risk_analysis()

    if selected_view == "pc":
        return build_pc_figure(pc)
    else:
        return build_risk_figure(risk)
    
if __name__ == "__main__":
    file_path = "data/watchlist.txt"
    pfa = PFA(file_path)
    app.run()