# Thực Hành Với NetworkX: Phân Tích Đồ Thị và Phát Hiện Cộng Đồng

NetworkX là một thư viện Python mạnh mẽ và phổ biến để tạo, phân tích và biểu diễn đồ thị. Trong bài hướng dẫn này, chúng ta sẽ áp dụng các khái niệm đã học trong chuỗi bài về lý thuyết đồ thị để thực hiện các phân tích thực tế.

## 1. Cài Đặt và Chuẩn Bị

### 1.1. Cài đặt các thư viện cần thiết

```python
# Cài đặt NetworkX và các thư viện hỗ trợ
!pip install networkx matplotlib scipy numpy python-louvain
```

### 1.2. Import các thư viện

```python
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import community as community_louvain
from collections import defaultdict, deque
import warnings
warnings.filterwarnings('ignore')  # Tắt cảnh báo không cần thiết

# Cấu hình hiển thị
plt.figure(figsize=(12, 8))
```

## 2. Tạo và Biểu Diễn Đồ Thị

### 2.1. Tạo đồ thị từ đầu

```python
# Tạo đồ thị vô hướng
G = nx.Graph()

# Thêm các đỉnh
G.add_node(1, name="A")
G.add_node(2, name="B")
G.add_node(3, name="C")

# Thêm một danh sách các đỉnh
G.add_nodes_from([4, 5, 6], color="red")

# Thêm các cạnh
G.add_edge(1, 2, weight=0.5)
G.add_edge(2, 3, weight=1.0)
G.add_edge(1, 3, weight=0.8)

# Thêm danh sách các cạnh
G.add_edges_from([(1, 4), (2, 5), (3, 6)])

# Kiểm tra thông tin đồ thị
print("Số lượng đỉnh:", G.number_of_nodes())
print("Số lượng cạnh:", G.number_of_edges())
print("Danh sách các đỉnh:", list(G.nodes()))
print("Danh sách các cạnh:", list(G.edges(data=True)))
```

### 2.2. Tạo đồ thị đặc biệt

NetworkX cung cấp nhiều hàm để tạo các loại đồ thị thông dụng:

```python
# Đồ thị đầy đủ (mỗi đỉnh kết nối với tất cả các đỉnh còn lại)
K5 = nx.complete_graph(5)

# Đồ thị đường (path)
P10 = nx.path_graph(10)

# Đồ thị vòng (cycle)
C7 = nx.cycle_graph(7)

# Đồ thị ngẫu nhiên Erdos-Renyi
# n: số đỉnh, p: xác suất có cạnh giữa hai đỉnh bất kỳ
G_random = nx.erdos_renyi_graph(n=100, p=0.05)

# Đồ thị phi tỷ lệ Barabasi-Albert
# n: số đỉnh, m: số cạnh mỗi đỉnh mới tạo
G_scale_free = nx.barabasi_albert_graph(n=100, m=2)

# Đồ thị thế giới nhỏ Watts-Strogatz
# n: số đỉnh, k: số láng giềng ban đầu, p: xác suất nối lại
G_small_world = nx.watts_strogatz_graph(n=100, k=4, p=0.1)
```

### 2.3. Biểu diễn đồ thị

```python
def visualize_graph(G, title="Đồ thị", node_color='skyblue', node_size=300, with_labels=True):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)  # Vị trí của các đỉnh
    
    # Vẽ các đỉnh
    nx.draw_networkx_nodes(G, pos, node_color=node_color, node_size=node_size)
    
    # Vẽ các cạnh
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    
    # Thêm nhãn nếu cần
    if with_labels:
        nx.draw_networkx_labels(G, pos)
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Ví dụ: Biểu diễn đồ thị ngẫu nhiên
visualize_graph(G_random, title="Đồ thị Ngẫu nhiên Erdos-Renyi")

# Biểu diễn đồ thị phi tỷ lệ
visualize_graph(G_scale_free, title="Đồ thị Phi tỷ lệ Barabasi-Albert")

# Biểu diễn đồ thị thế giới nhỏ
visualize_graph(G_small_world, title="Đồ thị Thế giới nhỏ Watts-Strogatz")
```

## 3. Phân Tích Cơ Bản Đồ Thị

### 3.1. Thuộc tính đồ thị

```python
def analyze_graph_properties(G):
    print(f"Thông tin đồ thị:")
    print(f"- Số lượng đỉnh: {G.number_of_nodes()}")
    print(f"- Số lượng cạnh: {G.number_of_edges()}")
    print(f"- Mật độ đồ thị: {nx.density(G):.4f}")
    
    if nx.is_connected(G):
        print("- Đồ thị liên thông!")
        print(f"- Đường kính: {nx.diameter(G)}")
        print(f"- Độ dài đường đi trung bình: {nx.average_shortest_path_length(G):.4f}")
    else:
        print("- Đồ thị không liên thông!")
        components = list(nx.connected_components(G))
        print(f"- Số thành phần liên thông: {len(components)}")
    
    print(f"- Hệ số phân cụm trung bình: {nx.average_clustering(G):.4f}")
    
    # Phân tích độ đo trung tâm
    print("\nTop 5 đỉnh theo Degree Centrality:")
    degree_centrality = nx.degree_centrality(G)
    sorted_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    for node, score in sorted_degree:
        print(f"  Đỉnh {node}: {score:.4f}")
    
    print("\nTop 5 đỉnh theo Betweenness Centrality:")
    betweenness_centrality = nx.betweenness_centrality(G)
    sorted_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    for node, score in sorted_betweenness:
        print(f"  Đỉnh {node}: {score:.4f}")

# Phân tích đồ thị phi tỷ lệ
analyze_graph_properties(G_scale_free)
```

### 3.2. Phân phối bậc

```python
def plot_degree_distribution(G, title="Phân phối bậc"):
    degrees = [d for n, d in G.degree()]
    plt.figure(figsize=(10, 6))
    
    # Histogram
    plt.hist(degrees, bins=20, alpha=0.7)
    plt.xlabel("Bậc")
    plt.ylabel("Số lượng đỉnh")
    plt.title(title)
    
    # Hiển thị thống kê
    plt.axvline(np.mean(degrees), color='r', linestyle='--', label=f'Trung bình: {np.mean(degrees):.2f}')
    plt.axvline(np.median(degrees), color='g', linestyle='--', label=f'Trung vị: {np.median(degrees):.2f}')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Log-log plot cho mạng phi tỷ lệ
    plt.figure(figsize=(10, 6))
    degree_count = defaultdict(int)
    for d in degrees:
        degree_count[d] += 1
    
    x = sorted(degree_count.keys())
    y = [degree_count[d] for d in x]
    
    plt.loglog(x, y, 'o-')
    plt.xlabel("Bậc (log scale)")
    plt.ylabel("Số lượng đỉnh (log scale)")
    plt.title(f"Phân phối bậc - Log-log scale: {title}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Phân tích phân phối bậc của đồ thị phi tỷ lệ
plot_degree_distribution(G_scale_free, title="Đồ thị Phi tỷ lệ")

# Phân tích phân phối bậc của đồ thị ngẫu nhiên
plot_degree_distribution(G_random, title="Đồ thị Ngẫu nhiên")
```

### 3.3. Đường đi ngắn nhất

```python
def analyze_shortest_paths(G):
    # Chọn một đỉnh nguồn
    source = list(G.nodes())[0]
    
    # Tính đường đi ngắn nhất từ source đến tất cả các đỉnh khác
    shortest_paths = nx.single_source_shortest_path(G, source)
    
    # Hiển thị một số ví dụ
    print(f"Đường đi ngắn nhất từ đỉnh {source}:")
    count = 0
    for target, path in shortest_paths.items():
        if target != source and count < 5:  # Chỉ hiển thị 5 ví dụ
            print(f"  Đến đỉnh {target}: {path} (độ dài: {len(path)-1})")
            count += 1
    
    # Tính và hiển thị phân phối độ dài đường đi
    path_lengths = [len(path)-1 for path in shortest_paths.values()]
    
    plt.figure(figsize=(10, 6))
    plt.hist(path_lengths, bins=max(path_lengths)-min(path_lengths)+1, alpha=0.7)
    plt.xlabel("Độ dài đường đi")
    plt.ylabel("Số lượng đỉnh")
    plt.title(f"Phân phối độ dài đường đi từ đỉnh {source}")
    plt.axvline(np.mean(path_lengths), color='r', linestyle='--', 
                label=f'Trung bình: {np.mean(path_lengths):.2f}')
    plt.legend()
    plt.tight_layout()
    plt.show()

analyze_shortest_paths(G_small_world)
```

## 4. Thuật Toán Duyệt Đồ Thị

### 4.1. Breadth-First Search (BFS)

```python
def bfs_with_visualization(G, source):
    print(f"BFS từ đỉnh {source}:")
    
    # Khởi tạo
    visited = {node: False for node in G.nodes()}
    distance = {node: float('inf') for node in G.nodes()}
    parent = {node: None for node in G.nodes()}
    
    visited[source] = True
    distance[source] = 0
    queue = deque([source])
    
    # Tính khoảng cách và lưu trữ thứ tự duyệt
    bfs_order = []
    
    while queue:
        u = queue.popleft()
        bfs_order.append(u)
        
        for v in G.neighbors(u):
            if not visited[v]:
                visited[v] = True
                distance[v] = distance[u] + 1
                parent[v] = u
                queue.append(v)
    
    # In kết quả
    print("Thứ tự duyệt BFS:", bfs_order)
    
    # Biểu diễn bằng màu sắc theo khoảng cách từ đỉnh nguồn
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    
    # Tạo danh sách màu dựa trên khoảng cách
    max_distance = max(distance.values())
    node_colors = [distance[node] for node in G.nodes()]
    
    # Vẽ đồ thị
    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                                  node_size=300, cmap=plt.cm.rainbow)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_labels(G, pos)
    
    # Biểu diễn cây BFS
    bfs_edges = [(parent[node], node) for node in G.nodes() if parent[node] is not None]
    nx.draw_networkx_edges(G, pos, edgelist=bfs_edges, width=2, edge_color='r')
    
    plt.colorbar(nodes, label="Khoảng cách từ nguồn")
    plt.title(f"BFS từ đỉnh {source}")
    plt.axis('off')
    plt.show()
    
    return distance, parent, bfs_order

# Tạo một đồ thị nhỏ cho dễ minh họa
demo_graph = nx.grid_2d_graph(4, 4)
# Chuyển đổi các tọa độ thành số nguyên
mapping = {node: i for i, node in enumerate(demo_graph.nodes())}
demo_graph = nx.relabel_nodes(demo_graph, mapping)

# Thực hiện BFS từ đỉnh 0
distance, parent, bfs_order = bfs_with_visualization(demo_graph, 0)
```

### 4.2. Depth-First Search (DFS)

```python
def dfs_with_visualization(G, source):
    print(f"DFS từ đỉnh {source}:")
    
    # Khởi tạo
    visited = {node: False for node in G.nodes()}
    discovery_time = {node: 0 for node in G.nodes()}
    finish_time = {node: 0 for node in G.nodes()}
    parent = {node: None for node in G.nodes()}
    time = [0]
    
    # Tính thời gian khám phá và hoàn thành, lưu trữ thứ tự duyệt
    dfs_order = []
    
    def dfs_visit(u):
        visited[u] = True
        time[0] += 1
        discovery_time[u] = time[0]
        dfs_order.append(u)
        
        for v in G.neighbors(u):
            if not visited[v]:
                parent[v] = u
                dfs_visit(v)
        
        time[0] += 1
        finish_time[u] = time[0]
    
    # Bắt đầu DFS từ đỉnh nguồn
    dfs_visit(source)
    
    # Nếu đồ thị không liên thông, duyệt các đỉnh chưa thăm
    for u in G.nodes():
        if not visited[u]:
            dfs_visit(u)
    
    # In kết quả
    print("Thứ tự duyệt DFS:", dfs_order)
    
    # Biểu diễn bằng màu sắc theo thời gian khám phá
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    
    # Tạo danh sách màu dựa trên thời gian khám phá
    node_colors = [discovery_time[node] for node in G.nodes()]
    
    # Vẽ đồ thị
    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                                  node_size=300, cmap=plt.cm.rainbow)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    
    # Biểu diễn cây DFS
    dfs_edges = [(parent[node], node) for node in G.nodes() if parent[node] is not None]
    nx.draw_networkx_edges(G, pos, edgelist=dfs_edges, width=2, edge_color='r')
    
    # Thêm nhãn
    nx.draw_networkx_labels(G, pos)
    
    plt.colorbar(nodes, label="Thời gian khám phá")
    plt.title(f"DFS từ đỉnh {source}")
    plt.axis('off')
    plt.show()
    
    return discovery_time, finish_time, parent, dfs_order

# Thực hiện DFS từ đỉnh 0
discovery_time, finish_time, parent, dfs_order = dfs_with_visualization(demo_graph, 0)
```

## 5. Thuật Toán Đường Đi Ngắn Nhất

### 5.1. Thuật toán Dijkstra

```python
def dijkstra_with_visualization(G, source, target=None):
    # Thêm trọng số cho cạnh nếu chưa có
    for u, v in G.edges():
        if 'weight' not in G[u][v]:
            G[u][v]['weight'] = 1
    
    # Thực hiện thuật toán Dijkstra
    distances = nx.single_source_dijkstra_path_length(G, source)
    paths = nx.single_source_dijkstra_path(G, source)
    
    # Hiển thị kết quả
    print(f"Khoảng cách ngắn nhất từ đỉnh {source}:")
    for node, dist in sorted(distances.items())[:5]:  # Chỉ hiển thị 5 kết quả đầu
        print(f"  Đến đỉnh {node}: {dist}")
    
    # Biểu diễn dựa trên khoảng cách
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    
    # Tạo danh sách màu dựa trên khoảng cách
    node_colors = [distances[node] if node in distances else -1 for node in G.nodes()]
    
    # Vẽ đồ thị
    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                                  node_size=300, cmap=plt.cm.rainbow)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    
    # Thêm nhãn
    nx.draw_networkx_labels(G, pos)
    
    # Nếu có đỉnh đích, biểu diễn đường đi ngắn nhất
    if target is not None and target in paths:
        path = paths[target]
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, 
                               width=2, edge_color='r')
        print(f"\nĐường đi ngắn nhất từ {source} đến {target}:")
        print(f"  Đường đi: {path}")
        print(f"  Khoảng cách: {distances[target]}")
    
    plt.colorbar(nodes, label="Khoảng cách từ nguồn")
    plt.title(f"Thuật toán Dijkstra từ đỉnh {source}")
    plt.axis('off')
    plt.show()
    
    return distances, paths

# Tạo đồ thị có trọng số
weighted_graph = nx.Graph()
weighted_graph.add_weighted_edges_from([
    (0, 1, 4), (0, 7, 8), 
    (1, 2, 8), (1, 7, 11), 
    (2, 3, 7), (2, 8, 2), (2, 5, 4), 
    (3, 4, 9), (3, 5, 14), 
    (4, 5, 10), 
    (5, 6, 2), 
    (6, 7, 1), (6, 8, 6), 
    (7, 8, 7)
])

# Thực hiện Dijkstra và hiển thị đường đi từ đỉnh 0 đến đỉnh 4
distances, paths = dijkstra_with_visualization(weighted_graph, 0, target=4)
```

### 5.2. Thuật toán Floyd-Warshall

```python
def floyd_warshall_with_visualization(G):
    # Tính ma trận khoảng cách giữa mọi cặp đỉnh
    dist = dict(nx.floyd_warshall(G))
    
    # Hiển thị ma trận khoảng cách
    print("Ma trận khoảng cách (một phần):")
    nodes = list(G.nodes())[:5]  # Chỉ hiển thị 5 đỉnh đầu tiên
    
    # In tiêu đề cột
    print("   ", end="")
    for j in nodes:
        print(f"{j:4}", end="")
    print()
    
    # In ma trận
    for i in nodes:
        print(f"{i:2} ", end="")
        for j in nodes:
            print(f"{dist[i][j]:4.1f}", end="")
        print()
    
    # Tính và hiển thị phân phối khoảng cách
    all_distances = []
    for i in dist:
        for j in dist[i]:
            if i != j:  # Bỏ qua khoảng cách từ một đỉnh đến chính nó
                all_distances.append(dist[i][j])
    
    plt.figure(figsize=(10, 6))
    plt.hist(all_distances, bins=20, alpha=0.7)
    plt.xlabel("Khoảng cách")
    plt.ylabel("Số lượng cặp đỉnh")
    plt.title("Phân phối khoảng cách giữa các cặp đỉnh")
    plt.axvline(np.mean(all_distances), color='r', linestyle='--', 
                label=f'Trung bình: {np.mean(all_distances):.2f}')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return dist

# Thực hiện Floyd-Warshall trên đồ thị có trọng số
distance_matrix = floyd_warshall_with_visualization(weighted_graph)
```

## 6. Phát Hiện Cộng Đồng

### 6.1. Liên thông thành phần (Connected Components)

```python
def analyze_connected_components(G):
    # Tìm tất cả các thành phần liên thông
    components = list(nx.connected_components(G))
    
    print(f"Số lượng thành phần liên thông: {len(components)}")
    print("Kích thước các thành phần liên thông:")
    for i, component in enumerate(components):
        print(f"  Thành phần {i+1}: {len(component)} đỉnh")
    
    # Biểu diễn thành phần liên thông bằng màu sắc
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    
    # Gán màu cho mỗi thành phần
    color_map = {}
    for i, component in enumerate(components):
        for node in component:
            color_map[node] = i
    
    # Tạo danh sách màu
    node_colors = [color_map[node] for node in G.nodes()]
    
    # Vẽ đồ thị
    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                                  node_size=300, cmap=plt.cm.rainbow)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_labels(G, pos)
    
    plt.colorbar(nodes, label="Thành phần liên thông")
    plt.title("Các thành phần liên thông")
    plt.axis('off')
    plt.show()
    
    return components

# Tạo đồ thị không liên thông
disconnected_graph = nx.Graph()
# Thành phần 1
disconnected_graph.add_edges_from([(0, 1), (1, 2), (2, 0)])
# Thành phần 2
disconnected_graph.add_edges_from([(3, 4), (4, 5), (5, 3)])
# Thành phần 3
disconnected_graph.add_edges_from([(6, 7)])

components = analyze_connected_components(disconnected_graph)
```

### 6.2. Label Propagation

```python
def label_propagation_with_visualization(G, max_iter=5):
    # Khởi tạo: gán mỗi đỉnh một nhãn duy nhất
    labels = {node: i for i, node in enumerate(G.nodes())}
    
    print("Nhãn ban đầu:", labels)
    
    # Lặp qua các vòng lan truyền
    for iteration in range(max_iter):
        # Tạo một bản sao của nhãn hiện tại
        old_labels = labels.copy()
        
        # Xáo trộn thứ tự các node để cập nhật ngẫu nhiên
        nodes = list(G.nodes())
        np.random.shuffle(nodes)
        
        # Cập nhật nhãn cho mỗi node
        for node in nodes:
            # Lấy các nhãn của láng giềng
            neighbor_labels = [labels[neighbor] for neighbor in G.neighbors(node)]
            if not neighbor_labels:
                continue
                
            # Đếm tần suất của mỗi nhãn
            label_counts = {}
            for label in neighbor_labels:
                label_counts[label] = label_counts.get(label, 0) + 1
                
            # Tìm nhãn phổ biến nhất
            max_count = max(label_counts.values()) if label_counts else 0
            most_common_labels = [label for label, count in label_counts.items() if count == max_count]
            
            # Nếu có nhiều nhãn cùng phổ biến nhất, chọn ngẫu nhiên
            labels[node] = np.random.choice(most_common_labels) if most_common_labels else labels[node]
        
        # Kiểm tra hội tụ
        if labels == old_labels:
            print(f"Hội tụ sau {iteration+1} vòng lặp!")
            break
            
        print(f"Vòng lặp {iteration+1}:", {k: labels[k] for k in list(labels)[:5]}, "...")
    
    # Chuyển đổi các nhãn thành id cộng đồng liên tục
    unique_labels = set(labels.values())
    label_to_community = {label: i for i, label in enumerate(unique_labels)}
    community_labels = {node: label_to_community[label] for node, label in labels.items()}
    
    # Biểu diễn cộng đồng
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    
    # Tạo danh sách màu dựa trên cộng đồng
    node_colors = [community_labels[node] for node in G.nodes()]
    
    # Vẽ đồ thị
    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                                  node_size=300, cmap=plt.cm.rainbow)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_labels(G, pos)
    
    plt.colorbar(nodes, label="Cộng đồng")
    plt.title("Label Propagation Communities")
    plt.axis('off')
    plt.show()
    
    return community_labels

# Thực hiện Label Propagation trên đồ thị nhỏ
label_communities = label_propagation_with_visualization(demo_graph)
```

### 6.3. Thuật toán Louvain

```python
def louvain_with_visualization(G):
    # Áp dụng thuật toán Louvain
    partition = community_louvain.best_partition(G)
    
    # Hiển thị kết quả
    print("Kết quả phân cộng đồng Louvain:")
    community_sizes = {}
    for community_id in set(partition.values()):
        size = list(partition.values()).count(community_id)
        community_sizes[community_id] = size
        print(f"  Cộng đồng {community_id}: {size} đỉnh")
    
    # Tính modularity
    modularity = community_louvain.modularity(partition, G)
    print(f"Modularity: {modularity:.4f}")
    
    # Biểu diễn cộng đồng
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    
    # Tạo danh sách màu dựa trên cộng đồng
    node_colors = [partition[node] for node in G.nodes()]
    
    # Vẽ đồ thị
    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                                  node_size=300, cmap=plt.cm.rainbow)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_labels(G, pos)
    
    plt.colorbar(nodes, label="Cộng đồng")
    plt.title(f"Louvain Communities (Modularity: {modularity:.4f})")
    plt.axis('off')
    plt.show()
    
    return partition, modularity

# Tạo đồ thị với cấu trúc cộng đồng rõ ràng
community_graph = nx.Graph()
# Cộng đồng 1
for i in range(10):
    for j in range(i+1, 10):
        if np.random.rand() < 0.7:
            community_graph.add_edge(i, j)

# Cộng đồng 2
for i in range(10, 20):
    for j in range(i+1, 20):
        if np.random.rand() < 0.7:
            community_graph.add_edge(i, j)

# Cộng đồng 3
for i in range(20, 30):
    for j in range(i+1, 30):
        if np.random.rand() < 0.7:
            community_graph.add_edge(i, j)

# Kết nối giữa các cộng đồng
for _ in range(5):
    i = np.random.randint(0, 10)
    j = np.random.randint(10, 20)
    community_graph.add_edge(i, j)

for _ in range(5):
    i = np.random.randint(10, 20)
    j = np.random.randint(20, 30)
    community_graph.add_edge(i, j)

for _ in range(2):
    i = np.random.randint(0, 10)
    j = np.random.randint(20, 30)
    community_graph.add_edge(i, j)

# Thực hiện thuật toán Louvain
partition, modularity = louvain_with_visualization(community_graph)
```

## 7. Ứng dụng: Phân tích mạng xã hội Zachary's Karate Club

Zachary's Karate Club là một bộ dữ liệu nổi tiếng trong phân tích mạng xã hội, mô tả mạng lưới tình bạn giữa 34 thành viên của câu lạc bộ karate đại học trong những năm 1970.

```python
def analyze_karate_club():
    # Tạo đồ thị Zachary's Karate Club
    karate = nx.karate_club_graph()
    
    print("Thông tin đồ thị Zachary's Karate Club:")
    print(f"- Số lượng đỉnh: {karate.number_of_nodes()}")
    print(f"- Số lượng cạnh: {karate.number_of_edges()}")
    print(f"- Mật độ đồ thị: {nx.density(karate):.4f}")
    
    # Phân tích độ đo trung tâm
    degree_centrality = nx.degree_centrality(karate)
    betweenness_centrality = nx.betweenness_centrality(karate)
    eigenvector_centrality = nx.eigenvector_centrality(karate)
    
    # Top 5 đỉnh có độ trung tâm cao nhất
    print("\nTop 5 đỉnh theo Degree Centrality:")
    for node, score in sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  Node {node}: {score:.4f}")
    
    print("\nTop 5 đỉnh theo Betweenness Centrality:")
    for node, score in sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  Node {node}: {score:.4f}")
    
    print("\nTop 5 đỉnh theo Eigenvector Centrality:")
    for node, score in sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  Node {node}: {score:.4f}")
    
    # Phát hiện cộng đồng bằng thuật toán Louvain
    partition = community_louvain.best_partition(karate)
    modularity = community_louvain.modularity(partition, karate)
    
    print(f"\nSố lượng cộng đồng phát hiện được: {len(set(partition.values()))}")
    print(f"Modularity: {modularity:.4f}")
    
    # Biểu diễn đồ thị với cộng đồng
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(karate, seed=42)
    
    # Tạo danh sách màu dựa trên cộng đồng
    node_colors = [partition[node] for node in karate.nodes()]
    
    # Thông tin thực tế về nhóm (từ dữ liệu gốc)
    # Node 0: giảng viên (Mr. Hi), Node 33: quản trị viên (John A)
    # Node với club = 'Mr. Hi' theo giảng viên sau khi câu lạc bộ chia tách
    # Node với club = 'Officer' theo quản trị viên
    node_shapes = []
    for node in karate.nodes():
        club = karate.nodes[node]['club']
        if club == 'Mr. Hi':
            node_shapes.append('o')  # Hình tròn cho nhóm Mr. Hi
        else:
            node_shapes.append('s')  # Hình vuông cho nhóm Officer
    
    # Vẽ đồ thị với các hình dạng khác nhau cho hai nhóm thực tế
    for shape in set(node_shapes):
        nodes_with_shape = [node for node, s in zip(karate.nodes(), node_shapes) if s == shape]
        colors = [partition[node] for node in nodes_with_shape]
        if shape == 'o':
            nx.draw_networkx_nodes(karate, pos, nodelist=nodes_with_shape, 
                                  node_color=colors, node_shape=shape, 
                                  node_size=300, cmap=plt.cm.rainbow, label='Nhóm Mr. Hi')
        else:
            nx.draw_networkx_nodes(karate, pos, nodelist=nodes_with_shape, 
                                  node_color=colors, node_shape=shape, 
                                  node_size=300, cmap=plt.cm.rainbow, label='Nhóm Officer')
    
    nx.draw_networkx_edges(karate, pos, alpha=0.5)
    nx.draw_networkx_labels(karate, pos)
    
    plt.title(f"Zachary's Karate Club - Louvain Communities (Modularity: {modularity:.4f})")
    plt.legend()
    plt.axis('off')
    plt.show()
    
    return karate, partition

karate, karate_partition = analyze_karate_club()
```

## 8. Tóm tắt

Chúng ta đã tìm hiểu và thực hành nhiều khía cạnh của phân tích đồ thị sử dụng NetworkX:

1. **Tạo và biểu diễn đồ thị**: NetworkX cho phép tạo nhiều loại đồ thị khác nhau và biểu diễn chúng một cách trực quan.

2. **Phân tích cơ bản**: Tính toán các đặc tính đồ thị như mật độ, đường kính, hệ số phân cụm và phân phối bậc.

3. **Thuật toán duyệt đồ thị**: Triển khai BFS và DFS để hiểu cách thuật toán này hoạt động và cách biểu diễn kết quả.

4. **Đường đi ngắn nhất**: Sử dụng thuật toán Dijkstra và Floyd-Warshall để tìm đường đi ngắn nhất trong đồ thị.

5. **Phát hiện cộng đồng**: Áp dụng các thuật toán phát hiện cộng đồng như Connected Components, Label Propagation và Louvain.

6. **Ứng dụng thực tế**: Phân tích mạng xã hội Zachary's Karate Club, một ví dụ kinh điển trong phân tích mạng xã hội.

Các kỹ năng và kiến thức này là nền tảng vững chắc cho việc phát triển các ứng dụng phân tích mạng xã hội, tối ưu hóa mạng lưới, và nhiều ứng dụng khác của lý thuyết đồ thị trong thế giới thực.

## 9. Nguồn tham khảo và học thêm

1. [Tài liệu chính thức của NetworkX](https://networkx.org/documentation/stable/)
2. [Đồ thị và thuật toán trên đồ thị trong Python](https://www.python.org/doc/essays/graphs/)
3. [Sách "Networks, Crowds, and Markets" của Easley và Kleinberg](https://www.cs.cornell.edu/home/kleinber/networks-book/)
4. [Khóa học Social Network Analysis của Coursera](https://www.coursera.org/specializations/social-network-analysis)
5. [Visualizing Networks in Python](https://www.datacamp.com/community/tutorials/social-network-analysis-python)

---

Đây là bài cuối cùng trong chuỗi bài tutorial về lý thuyết đồ thị và phát hiện cộng đồng. Hy vọng bạn đã học được nhiều điều hữu ích và có thể áp dụng chúng vào các bài toán thực tế.