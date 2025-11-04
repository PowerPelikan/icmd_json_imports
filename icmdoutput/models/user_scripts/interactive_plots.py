from scipy.spatial import KDTree
import ipywidgets as widgets
from IPython.display import display
import numpy as np
import plotly.graph_objects as go

def prepare_lookup(grouped_df, comp_cols):
    comps = []
    groups = []
    for comp, g in grouped_df:
        comps.append(comp)
        groups.append(g)
    comp_array = np.array(comps)
    tree = KDTree(comp_array)
    return tree, comp_array, groups


def get_nearest_group(target, comp_cols, tree, comp_array, groups):
    # Ziel in Array-Reihenfolge bringen
    target_arr = np.array([target[c] for c in comp_cols])
    dist, idx = tree.query(target_arr)
    return comp_array[idx], groups[idx]

def make_interactive_liquidphase(comp_cols, tree, comp_array, groups, 
                                  t_col="Temperature in C", liquid_col="LIQUID"):
    # Wertebereiche für Slider (außer Al)
    ranges = {c: (comp_array[:, i].min(), comp_array[:, i].max())
              for i, c in enumerate(comp_cols) if c != "Al"}

    '''sliders = {c: widgets.FloatSlider(
        value=(ranges[c][0] + ranges[c][1]) / 2,
        min=ranges[c][0],
        max=ranges[c][1],
        step=0.1,
        description=c,
        continuous_update=Falsei
    ) for c in ranges}'''

    # Slider für alle Elemente außer Al
    sliders = {}
    for i, c in enumerate(comp_cols):
        if c == "Al":
            continue
        values = sorted(set(comp_array[:, i]))
        sliders[c] = widgets.SelectionSlider(
            options=values,
            value=values[len(values)//2],  # mittlerer Wert als Start
            description=c,
            continuous_update=True
        )

    out = widgets.Output()

    def plot_update(**kwargs):
        out.clear_output(wait=True)
        target = {**kwargs}
        target["Al"] = 100 - sum(target.values())  # anpassen, falls normiert auf 1

        comp, g = get_nearest_group(target, comp_cols, tree, comp_array, groups)
        g = g.sort_values(t_col, ascending=False)

        fig = go.Figure()

        # Temperatur & Liquidus
        T = g[t_col].values
        fL = np.nan_to_num(g[liquid_col].values, nan=0.0)
        fig.add_trace(go.Scatter(
            x=T, y=fL, mode="lines", name="LIQUID", line=dict(color="black", width=2)
        ))

        # Nur Marker für das erste Auftreten jeder Phase
        phases = [c for c in g.columns if c not in {t_col, liquid_col, *comp_cols}]
        for p in phases:
            f = np.nan_to_num(g[p].values, nan=0.0)

            # Erstes Auftreten (>0)
            onset_idx = np.argmax(f > 0)
            if f[onset_idx] > 0:
                fig.add_trace(go.Scatter(
                    x=[T[onset_idx]], 
                    y=[fL[onset_idx]],  # Punkt auf Liquidus-Linie
                    mode="markers+text",
                    marker=dict(size=10, symbol="circle"),
                    text=[p],
                    textposition="top center",
                    name=p
                ))

        fig.update_layout(
            xaxis=dict(title="Temperatur [°C]"),
            yaxis=dict(title="Fraktion", range=[0, 1]),
            template="plotly_white",
            height=600,
            width=900,
            title=f"Komposition gewählt:\n" +
                  ", ".join(f"{k}={target[k]:.2f}" for k in comp_cols),
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
        )

        with out:
            display(fig)

    # Widgets verknüpfen und Layout darstellen
    interactive = widgets.interactive_output(plot_update, sliders)
    ui = widgets.VBox([*sliders.values(), out])
    display(ui, interactive)

def make_interactive_step(comp_cols, tree, comp_array, groups, 
                                  t_col="Temperature in C", liquid_col="LIQUID"):
    ranges = {c: (comp_array[:, i].min(), comp_array[:, i].max())
              for i, c in enumerate(comp_cols) if c != "Al"}

    # Slider für alle Elemente außer Al
    sliders = {}
    for i, c in enumerate(comp_cols):
        if c == "Al":
            continue
        values = sorted(set(comp_array[:, i]))
        sliders[c] = widgets.SelectionSlider(
            options=values,
            value=values[len(values)//2],  # mittlerer Wert als Start
            description=c,
            continuous_update=True
        )

    out = widgets.Output()

    def plot_update(**kwargs):
        out.clear_output(wait=True)
        target = {**kwargs}
        target["Al"] = 100 - sum(target.values())  # anpassen falls normiert auf 1

        # nächste Gruppe suchen
        comp, g = get_nearest_group(target, comp_cols, tree, comp_array, groups)
        g = g.sort_values(t_col, ascending=False)

        # Plot erstellen
        fig = go.Figure()
        T = g[t_col].values
        fL = np.nan_to_num(g[liquid_col].values, nan=0.0)

        fig.add_trace(go.Scatter(x=T, y=fL, mode="lines", name="LIQUID", line=dict(color="black", width=2)))

        phases = [c for c in g.columns if c not in {t_col, liquid_col, *comp_cols}]
        for p in phases:
            f = np.nan_to_num(g[p].values, nan=0.0)
            if f.max() > 0.0001:
                fig.add_trace(go.Scatter(x=T, y=f, mode="lines", name=p))

        fig.update_layout(
            xaxis=dict(title="Temperatur [°C]"),
            yaxis=dict(title="Fraktion", type="log", range=[-4, 0]),
            template="plotly_white",
            height=600,
            width=900,
            title=f"Komposition gewählt:\n" +
                  ", ".join(f"{k}={target[k]:.2f}" for k in comp_cols)
        )

        with out:
            display(fig)

    # interactive_output erzeugen
    interactive = widgets.interactive_output(plot_update, sliders)

    # Layout mit Slidern und Plot nebeneinander oder untereinander
    ui = widgets.VBox([*sliders.values(), out])
    display(ui, interactive)