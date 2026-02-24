import networkx as nx
from pyvis.network import Network
import os
import webbrowser


def create_college_graph(triples):

    G = nx.DiGraph()

    # 🎨 Node Type Colors
    color_map = {
        "Student": "#00E5FF",
        "Course": "#FFCA28",
        "Professor": "#FF5252",
        "Department": "#7C4DFF",
        "College": "#69F0AE"
    }

    # 🔗 Build Graph
    for subject, relation, obj, subject_type, object_type in triples:

        G.add_node(
            subject,
            label=subject,
            group=subject_type,
            color=color_map.get(subject_type, "#CCCCCC"),
            title=f"<b>{subject}</b><br>Type: {subject_type}",
            size=25
        )

        G.add_node(
            obj,
            label=obj,
            group=object_type,
            color=color_map.get(object_type, "#CCCCCC"),
            title=f"<b>{obj}</b><br>Type: {object_type}",
            size=25
        )

        G.add_edge(
            subject,
            obj,
            label=relation,
            title=relation,
            width=2
        )

    # 🌐 Create Network
    net = Network(
        height="900px",
        width="100%",
        bgcolor="#0f172a",
        font_color="white",
        directed=True
    )

    net.from_nx(G)

    # ⚙️ Graph Options (PURE JSON)
    net.set_options("""
    {
      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "keyboard": true,
        "zoomView": true,
        "dragView": true,
        "multiselect": true
      },
      "physics": {
        "enabled": true,
        "solver": "forceAtlas2Based",
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 150,
          "springConstant": 0.08
        }
      },
      "edges": {
        "arrows": { "to": { "enabled": true } },
        "smooth": { "type": "dynamic" },
        "font": { "size": 14, "color": "white" }
      },
      "nodes": {
        "shadow": true,
        "font": { "size": 16, "color": "white" }
      }
    }
    """)

    file_path = os.path.abspath("college_graph.html")
    net.write_html(file_path)

    # 🔥 Add Modern UI Controls
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("""
<style>
body {
    margin:0;
    font-family: 'Segoe UI', sans-serif;
    background: #0f172a;
}

.control-panel {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(30, 41, 59, 0.9);
    backdrop-filter: blur(12px);
    padding: 15px 25px;
    border-radius: 15px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.6);
    z-index: 999;
    display: flex;
    gap: 15px;
    align-items: center;
}

.control-panel input,
.control-panel select {
    padding: 8px 12px;
    border-radius: 8px;
    border: none;
    outline: none;
    background: #1e293b;
    color: white;
}

.control-panel button {
    padding: 8px 15px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-weight: 600;
    transition: 0.3s;
}

.search-btn { background: #00E5FF; }
.filter-btn { background: #FFCA28; }
.png-btn { background: #69F0AE; }

.control-panel button:hover {
    transform: scale(1.08);
}
</style>

<div class="control-panel">

<input type="text" id="searchInput" placeholder="🔍 Search node">
<button class="search-btn" onclick="searchNode()">Search</button>

<select id="filterType">
<option value="">All Types</option>
<option value="Student">Student</option>
<option value="Course">Course</option>
<option value="Professor">Professor</option>
<option value="Department">Department</option>
<option value="College">College</option>
</select>
<button class="filter-btn" onclick="filterNodes()">Filter</button>

<button class="png-btn" onclick="exportPNG()">Export PNG</button>

</div>

<script>

function searchNode() {
    var input = document.getElementById("searchInput").value.toLowerCase();
    var nodes = network.body.data.nodes;
    var found = null;

    nodes.forEach(function(node) {
        if(node.label.toLowerCase().includes(input)) {
            found = node.id;
        }
    });

    if(found){
        network.selectNodes([found]);
        network.focus(found, {scale:1.6});
    } else {
        alert("Node not found");
    }
}

function filterNodes() {
    var type = document.getElementById("filterType").value;
    var nodes = network.body.data.nodes;

    nodes.forEach(function(node) {
        if(type === "" || node.group === type){
            nodes.update({id: node.id, hidden:false});
        } else {
            nodes.update({id: node.id, hidden:true});
        }
    });
}

function exportPNG() {
    var canvas = document.querySelector("canvas");
    var link = document.createElement("a");
    link.download = "knowledge_graph.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
}

</script>
""")

    webbrowser.open("file://" + file_path)