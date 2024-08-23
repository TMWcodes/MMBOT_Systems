import ast
import os
import networkx as nx
import matplotlib.pyplot as plt

# Function to extract dependencies from a file
def extract_dependencies(filename, root_dir):
    dependencies = set()

    if not os.path.isfile(filename):
        return dependencies
    
    with open(filename, 'r') as file:
        tree = ast.parse(file.read(), filename=filename)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                dependencies.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            dependencies.add(node.module)
    
    # Resolve relative imports (e.g., from . import something)
    absolute_deps = set()
    for dep in dependencies:
        if dep is not None:
            dep_path = os.path.join(root_dir, dep.replace('.', os.sep) + '.py')
            if os.path.isfile(dep_path):
                absolute_deps.add(dep_path)
            else:
                absolute_deps.add(dep)
    
    return absolute_deps

# Function to recursively collect all dependencies
def collect_all_dependencies(filename, root_dir, graph, visited, exclude_dirs=None):
    if filename in visited:
        return
    visited.add(filename)
    
    dependencies = extract_dependencies(filename, root_dir)
    for dep in dependencies:
        dep_relative = os.path.relpath(dep, root_dir)

        # Check if the dependency should be excluded
        if exclude_dirs and any(ex_dir in dep_relative for ex_dir in exclude_dirs):
            continue

        graph.add_edge(os.path.relpath(filename, root_dir), dep_relative)
        if dep.endswith('.py'):
            collect_all_dependencies(dep, root_dir, graph, visited, exclude_dirs)

# Function to create and draw a dependency graph
def create_and_draw_graph(filename, output_file='dependency_graph.png', exclude_dirs=None):
    root_dir = os.path.dirname(filename)
    G = nx.DiGraph()

    # Collect all dependencies
    visited = set()
    collect_all_dependencies(filename, root_dir, G, visited, exclude_dirs)

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
    plt.savefig(output_file)
    plt.show()

# Specify the filename and generate the dependency graph
filename = r''  # Adjust path
exclude_dirs = ['dev_tools', 'tests']  # Add any directories you want to exclude
create_and_draw_graph(filename, exclude_dirs=exclude_dirs)
