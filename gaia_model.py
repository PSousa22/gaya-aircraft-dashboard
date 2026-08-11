import networkx as nx
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. CONSTRUÇÃO DA REDE UNIFICADA (GAIA)
# ==========================================
# Coordenadas conceituais em uma esfera virtual (Planeta) para representação visual
# Nós estruturados pelo papel termodinâmico/metabólico
compartimentos = {
    "Atmosfera (Gases)": {"pos": (0.0, 0.0, 1.2), "color": "#00d2ff", "size": 35, "desc": "Troca rápida de gases e regulação térmica global."},
    "Oceanos (Nutrientes)": {"pos": (0.8, 0.5, 0.5), "color": "#1e90ff", "size": 40, "desc": "Maior sumidouro térmico e reservatório de nutrientes."},
    "Solo e Litosfera": {"pos": (-0.8, -0.5, -0.5), "color": "#8b4513", "size": 35, "desc": "Estrutura de suporte físico e ciclagem mineral lenta."},
    "Fitoplâncton": {"pos": (0.6, 0.7, 0.2), "color": "#00ff7f", "size": 25, "desc": "Produção primária marinha, base da bomba biológica de carbono."},
    "Florestas e Plantas": {"pos": (-0.5, -0.7, 0.4), "color": "#228b22", "size": 35, "desc": "Sequestro de carbono terrestre e transpiração (rios voadores)."},
    "Consumidores (Animais)": {"pos": (0.3, -0.4, -0.6), "color": "#ff4500", "size": 20, "desc": "Aceleradores metabólicos e vetores de transporte de nutrientes."},
    "Microbioma & Decompositores": {"pos": (0.0, 0.0, -1.0), "color": "#9400d3", "size": 40, "desc": "O gargalo de persistência topológica: fecha todos os loops reciclando matéria."},
    "Antropoceno (Tecnosfera)": {"pos": (-0.2, 0.8, 0.6), "color": "#ff0055", "size": 30, "desc": "Perturbação externa de alta energia que sobrecarrega os loops estáveis."}
}

G = nx.DiGraph()  # Grafo direcionado para representar o vetor de fluxo de energia

for nome, dados in compartimentos.items():
    G.add_node(nome, pos=dados["pos"], color=dados["color"], size=dados["size"], desc=dados["desc"])

# Fluxos que formam os ciclos homológicos estáveis e as pressões modernas
fluxos = [
    ("Atmosfera (Gases)", "Florestas e Plantas", "Fixação de CO2"),
    ("Atmosfera (Gases)", "Fitoplâncton", "Absorção de CO2"),
    ("Florestas e Plantas", "Consumidores (Animais)", "Fluxo Energético Trófico"),
    ("Fitoplâncton", "Oceanos (Nutrientes)", "Deposição Orgânica"),
    ("Consumidores (Animais)", "Microbioma & Decompositores", "Resíduos Orgânicos"),
    ("Florestas e Plantas", "Microbioma & Decompositores", "Ninhada/Matéria Morta"),
    ("Microbioma & Decompositores", "Solo e Litosfera", "Mineralização do Solo"),
    ("Microbioma & Decompositores", "Atmosfera (Gases)", "Liberação Quimiotrófica (CO2/CH4)"),
    ("Solo e Litosfera", "Florestas e Plantas", "Absorção de Nutrientes"),
    ("Oceanos (Nutrientes)", "Atmosfera (Gases)", "Evaporação e Vapor D'água"),
    
    # Impactos do Antropoceno (Sobrecarga de Loops)
    ("Antropoceno (Tecnosfera)", "Atmosfera (Gases)", "Emissões Industriais Críticas"),
    ("Antropoceno (Tecnosfera)", "Florestas e Plantas", "Desmatamento / Quebra de Feedback"),
    ("Solo e Litosfera", "Antropoceno (Tecnosfera)", "Extração de Recursos Fóssil/Mineral")
]
G.add_edges_from([(f[0], f[1], {"fluxo": f[2]}) for f in fluxos])

# ==========================================
# 2. PREPARAÇÃO DOS ELEMENTOS GRÁFICOS INTERATIVOS
# ==========================================
# Nós (Compartimentos do Planeta)
node_x, node_y, node_z = [], [], []
node_colors, node_sizes, node_text = [], [], []

for node in G.nodes():
    x, y, z = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)
    node_z.append(z)
    node_colors.append(G.nodes[node]['color'])
    node_sizes.append(G.nodes[node]['size'])
    # Texto interativo ao passar o mouse (Hover)
    node_text.append(f"<b>{node}</b><br>{G.nodes[node]['desc']}")

node_trace = go.Scatter3d(
    x=node_x, y=node_y, z=node_z,
    mode='markers+text',
    marker=dict(size=node_sizes, color=node_colors, opacity=0.9, line=dict(color='#ffffff', width=2)),
    text=[n for n in G.nodes()],
    textposition="top center",
    hoverinfo='text',
    hovertext=node_text,
    name="Compartimentos Biogeoquímicos"
)

# Arestas (Linhas de Conexão Vetorial)
edge_traces = []
for edge in G.edges(data=True):
    x0, y0, z0 = G.nodes[edge[0]]['pos']
    x1, y1, z1 = G.nodes[edge[1]]['pos']
    nome_fluxo = edge[2]['fluxo']
    
    # Determinar estilo da linha (Vermelho tracejado para o Antropoceno)
    is_anthropocene = "Antropoceno" in edge[0] or "Antropoceno" in edge[1]
    line_color = '#ff0055' if is_anthropocene else '#55c2da'
    line_dash = 'dash' if is_anthropocene else 'solid'
    
    trace = go.Scatter3d(
        x=[x0, x1, None], y=[y0, y1, None], z=[z0, z1, None],
        mode='lines',
        line=dict(color=line_color, width=3, dash=line_dash),
        hoverinfo='text',
        hovertext=f"Fluxo: {nome_fluxo}<br>De: {edge[0]} -> Para: {edge[1]}",
        name=nome_fluxo,
        showlegend=False
    )
    edge_traces.append(trace)

# Esfera Transparente de Fundo (Representando o Planeta Terra)
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
sphere_x = np.cos(u)*np.sin(v)
sphere_y = np.sin(u)*np.sin(v)
sphere_z = np.cos(v)

sphere_trace = go.Surface(
    x=sphere_x, y=sphere_y, z=sphere_z,
    opacity=0.08,
    colorscale=[[0, '#0044ff'], [1, '#00aaff']],
    showscale=False,
    hoverinfo='skip',
    name="Biosfera Terrestre"
)

# ==========================================
# 3. COMPOSIÇÃO E EXIBIÇÃO DO DASHBOARD
# ==========================================
layout = go.Layout(
    title=dict(
        text="<b>Modelo Interativo Gaia: O Esqueleto Topológico dos Sistemas Vivos</b><br><sup>Passe o mouse nos nós e conexões para analisar os feedbacks dinâmicos</sup>",
        x=0.5, y=0.95, font=dict(family="Arial", size=16, color="#ffffff")
    ),
    paper_bgcolor='#0e1017',
    plot_bgcolor='#0e1017',
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.0))
    ),
    margin=dict(l=0, r=0, b=0, t=80),
    showlegend=False
)

fig = go.Figure(data=[sphere_trace, node_trace] + edge_traces, layout=layout)

# Executa e abre automaticamente uma aba interativa no seu navegador padrâo
fig.show()
