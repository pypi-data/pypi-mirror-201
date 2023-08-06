from sseclient import SSEClient
from rich.live import Live
from rich.table import Table
import json
from rich.layout import Layout

def get_workspace_usage(metrics, node_filter=None) -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("User")
    table.add_column("Workspace")
    table.add_column("%CPU")
    table.add_column("Memory(GB)")
    table.add_column("Limits(CPU/Memory)")
    table.add_column("Node")

    data = []
    for k, m in metrics.items():
        if node_filter and m["node"] != node_filter:
            continue

        name = k.split("-")[1]
        cpu = round(m["cpu"]/10**7,1)
        cpu_limit = m["limits"]["cpu"]
        memory = round(m["memory"]/10**6,3)
        memory_limit = m["limits"]["memory"]

        node_name =  m["node"].split(".")[0]
        data.append([f"{m['user']}", name, cpu, memory,f"{cpu_limit}/{memory_limit}",f"{node_name}"])
    
    data.sort(key=lambda x: x[2], reverse=True)
    for row in data:
        table.add_row(row[0],row[1],str(row[2]), str(row[3]), row[4], row[5])

    return table

def get_nodes_usage(metrics, node_filter=None) -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("Node")
    table.add_column("Type")
    table.add_column("%CPU")
    table.add_column("Memory(GB)")

    data = []
    for k, m in metrics.items():
        if node_filter and k != node_filter:
            continue
        cpu = round(m["cpu"]/10**7,1)
        memory = round(m["memory"]/10**6,3)
        data.append([k, m["type"], cpu, memory])
    
    data.sort(key=lambda x: x[2], reverse=True)
    for row in data:
        table.add_row(row[0],row[1],str(row[2]), str(row[3]))
    return table

if __name__ == "__main__":
    layout = Layout()
    layout.split_column(Layout(name="Workspaces", ratio=3), Layout(name="Nodes", ratio=1))
    layout["Workspaces"].update(get_workspace_usage({}))
    layout["Nodes"].update(get_nodes_usage({}))
    with Live(layout, refresh_per_second=1) as live:
        messages = SSEClient('http://localhost:8000/api/ds/metrics')
        for msg in messages:
            if msg.data.startswith("{"):
                metrics = json.loads(msg.data)
                layout["Workspaces"].update(get_workspace_usage(metrics["workspaces"]))
                layout["Nodes"].update(get_nodes_usage(metrics["nodes"]))
                live.update(layout)