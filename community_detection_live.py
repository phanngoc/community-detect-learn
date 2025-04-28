#!/usr/bin/env python3
"""
Real-world Graph Example with Community Detection
================================================
This script creates a realistic social network graph and detects communities using the Louvain algorithm.
"""

import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
try:
    # First try community package
    import community as community_louvain
except ImportError:
    # If that fails, try python-louvain package
    try:
        import community.community_louvain as community_louvain
    except ImportError:
        # If that fails too, inform the user
        print("Please install the python-louvain package:")
        print("pip install python-louvain networkx matplotlib")
        exit(1)

def create_realistic_social_network(num_communities=3, 
                                   nodes_per_community=10, 
                                   p_within=0.7, 
                                   p_between=0.01):
    """
    Create a realistic social network with community structure.
    
    Parameters:
    - num_communities: Number of communities to create
    - nodes_per_community: Number of nodes in each community
    - p_within: Probability of connection within a community
    - p_between: Probability of connection between communities
    
    Returns:
    - G: networkx graph with realistic community structure
    - true_communities: Dictionary mapping node to its true community
    """
    G = nx.Graph()
    true_communities = {}
    
    # Create communities with dense internal connections
    for community_id in range(num_communities):
        # Create a dense subgraph for this community
        community_nodes = list(range(
            community_id * nodes_per_community, 
            (community_id + 1) * nodes_per_community
        ))
        
        # Add nodes with attributes
        for node in community_nodes:
            G.add_node(node)
            true_communities[node] = community_id
            
        # Add edges within community (high probability)
        for i in range(len(community_nodes)):
            for j in range(i + 1, len(community_nodes)):
                if random.random() < p_within:
                    G.add_edge(community_nodes[i], community_nodes[j])
    
    # Add some random edges between communities (low probability)
    nodes = list(G.nodes())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            # If nodes are from different communities
            if true_communities[nodes[i]] != true_communities[nodes[j]]:
                # Add edge with low probability
                if random.random() < p_between:
                    G.add_edge(nodes[i], nodes[j])
    
    return G, true_communities

def plot_communities(G, partition, title="Community Detection Results"):
    """
    Plot the graph with nodes colored by community.
    
    Parameters:
    - G: networkx graph
    - partition: Dictionary mapping each node to its community ID
    - title: Title for the plot
    """
    plt.figure(figsize=(10, 8))
    
    # Set position using force-directed layout
    pos = nx.spring_layout(G, seed=42)
    
    # Color nodes according to their community
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    
    # Draw nodes
    for community in set(partition.values()):
        # List of nodes in this community
        list_nodes = [nodes for nodes, com in partition.items() if com == community]
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, 
                              nodelist=list_nodes,
                              node_size=300,
                              node_color=[cmap(community)],
                              label=f"Community {community}")
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10)
    
    plt.title(title)
    plt.legend(scatterpoints=1)
    plt.axis('off')
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(f"{title.replace(' ', '_').lower()}.png")
    print(f"Saved plot to {title.replace(' ', '_').lower()}.png")
    
    # Show the plot
    plt.show()

def analyze_communities(G, partition):
    """
    Analyze the discovered communities.
    
    Parameters:
    - G: networkx graph
    - partition: Dictionary mapping each node to its community ID
    
    Returns:
    - stats: Dictionary with community statistics
    """
    stats = {}
    
    # Number of communities
    num_communities = len(set(partition.values()))
    stats["num_communities"] = num_communities
    
    # Size of communities
    community_sizes = {}
    for community in set(partition.values()):
        community_sizes[community] = len([n for n, com in partition.items() if com == community])
    stats["community_sizes"] = community_sizes
    
    # Modularity score
    modularity = community_louvain.modularity(partition, G)
    stats["modularity"] = modularity
    
    # Density within communities
    communities_density = {}
    for community in set(partition.values()):
        nodes = [n for n, com in partition.items() if com == community]
        subgraph = G.subgraph(nodes)
        density = nx.density(subgraph)
        communities_density[community] = density
    stats["communities_density"] = communities_density
    
    return stats

def print_stats(stats):
    """Print community statistics in a nice format."""
    print("\n===== Community Detection Statistics =====")
    print(f"Number of communities: {stats['num_communities']}")
    print(f"Modularity score: {stats['modularity']:.4f} (higher is better)")
    
    print("\nCommunity sizes:")
    for comm, size in stats["community_sizes"].items():
        print(f"  Community {comm}: {size} nodes")
    
    print("\nDensity within communities:")
    for comm, density in stats["communities_density"].items():
        print(f"  Community {comm}: {density:.4f} (higher means more connected)")
    
    print("==========================================\n")

def main():
    """Main function to demonstrate community detection."""
    print("\n==== Real-world Graph Community Detection Example ====\n")
    
    # Create a realistic social network
    print("Creating a realistic social network with community structure...")
    G, true_communities = create_realistic_social_network(
        num_communities=4,
        nodes_per_community=12,
        p_within=0.7,
        p_between=0.02
    )
    
    print(f"Created graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    print(f"True number of communities: 4")
    
    # Plot the original graph (no community labels)
    print("\nPlotting the original graph...")
    all_same_community = {node: 0 for node in G.nodes()}
    plot_communities(G, all_same_community, "Original Graph (No Community Labels)")
    
    # Apply Louvain community detection
    print("\nApplying Louvain community detection algorithm...")
    partition = community_louvain.best_partition(G)
    
    # Plot the discovered communities
    print("\nPlotting communities discovered by Louvain algorithm...")
    plot_communities(G, partition, "Louvain Community Detection")
    
    # Analyze the communities
    stats = analyze_communities(G, partition)
    print_stats(stats)
    
    # Compare with ground truth
    print("\n== Comparing detected communities with ground truth ==")
    
    # Build a reverse mapping from community ID to nodes
    detected_communities = {}
    for node, comm_id in partition.items():
        if comm_id not in detected_communities:
            detected_communities[comm_id] = []
        detected_communities[comm_id].append(node)
    
    # Build a reverse mapping from true community ID to nodes
    ground_truth = {}
    for node, comm_id in true_communities.items():
        if comm_id not in ground_truth:
            ground_truth[comm_id] = []
        ground_truth[comm_id].append(node)
    
    # Compare detected communities with ground truth
    print("\nDetected communities:")
    for comm_id, nodes in detected_communities.items():
        print(f"  Community {comm_id}: {sorted(nodes)}")
    
    print("\nGround truth communities:")
    for comm_id, nodes in ground_truth.items():
        print(f"  Community {comm_id}: {sorted(nodes)}")
    
    print("\nNote: The community IDs might not match between detected and ground truth,")
    print("but the node groupings should be similar if detection worked well.")
    print("\n====================================================")

if __name__ == "__main__":
    # Check if required packages are installed
    try:
        import networkx
        import matplotlib
        # Continue with main function
        main()
    except ImportError as e:
        print(f"Error: {e}")
        print("\nPlease install the required packages:")
        print("pip install networkx matplotlib python-louvain")