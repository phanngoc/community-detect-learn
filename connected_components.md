# Thuật toán Connected Components - Phát hiện cộng đồng trên đồ thị

**Connected Components** là thuật toán đơn giản nhất trong phát hiện cộng đồng trên đồ thị, dựa trên nguyên tắc cơ bản: **Các node có thể đi đến nhau thì thuộc cùng một cộng đồng**.

---

## 1. Ý tưởng cơ bản

Thuật toán Connected Components có ý tưởng cực kỳ đơn giản:

- Mỗi **thành phần liên thông** (connected component) của đồ thị được xem là một **cộng đồng** riêng.
- Hai node thuộc cùng một thành phần liên thông nếu tồn tại đường đi giữa chúng.

---

## 2. Định nghĩa toán học

Cho một đồ thị không có hướng $G = (V, E)$:
- $V$ là tập các đỉnh (nodes)
- $E$ là tập các cạnh (edges)

Định nghĩa **thành phần liên thông** (connected component):
- Một tập con $C \subseteq V$ là một thành phần liên thông nếu:
  1. Với mọi cặp node $u, v \in C$, tồn tại một đường đi từ $u$ đến $v$.
  2. Không tồn tại node $w \in V \setminus C$ sao cho $w$ có thể đi đến bất kỳ node nào trong $C$.

Hay nói cách khác:
- Một thành phần liên thông là tập lớn nhất các node mà giữa hai node bất kỳ trong tập đều tồn tại đường đi.

---

## 3. Thuật toán Connected Components

Thuật toán được thực hiện qua các bước sau:

### Thuật toán với BFS (Breadth-First Search)

1. **Khởi tạo**:
   - Đánh dấu tất cả các node là "chưa thăm".
   - Khởi tạo một tập rỗng các thành phần liên thông.

2. **Tìm kiếm**:
   - Với mỗi node $u$ chưa thăm:
     - Sử dụng BFS để tìm tất cả các node có thể đi đến từ $u$.
     - Các node này tạo thành một thành phần liên thông.
     - Đánh dấu tất cả các node trong thành phần này là "đã thăm".
     - Thêm thành phần liên thông mới này vào tập kết quả.

3. **Kết thúc**:
   - Khi đã thăm tất cả các node, mỗi thành phần liên thông là một cộng đồng riêng biệt.

### Thuật toán với DFS (Depth-First Search)

Tương tự, ta có thể sử dụng DFS thay cho BFS:

1. **Khởi tạo**:
   - Đánh dấu tất cả các node là "chưa thăm".
   - Khởi tạo một tập rỗng các thành phần liên thông.

2. **Tìm kiếm**:
   - Với mỗi node $u$ chưa thăm:
     - Sử dụng DFS để tìm tất cả các node có thể đi đến từ $u$.
     - Đánh dấu tất cả các node này là "đã thăm" và đưa vào một thành phần liên thông.
     - Thêm thành phần liên thông này vào tập kết quả.

3. **Kết thúc**:
   - Khi đã thăm tất cả các node, ta có tập các thành phần liên thông.

---

## 4. Phức tạp thuật toán

- **Thời gian**: $O(|V| + |E|)$ - cần duyệt qua tất cả các node và cạnh một lần.
- **Không gian**: $O(|V|)$ - cần lưu trữ trạng thái thăm của mỗi node và hàng đợi/ngăn xếp cho BFS/DFS.

---

## 5. Mô tả toán học

Giả sử $G = (V, E)$ là một đồ thị vô hướng.

Định nghĩa quan hệ tương đương $R$ trên $V$:
- $u R v$ nếu tồn tại đường đi từ $u$ đến $v$.

Các lớp tương đương của $R$ chính là các thành phần liên thông của $G$.

Thuật toán Connected Components trả về tập các lớp tương đương này:

$$CC(G) = V / R = \{[v]_R : v \in V\}$$

Trong đó $[v]_R = \{u \in V : u R v\}$ là tập tất cả các node có thể đến được từ $v$.

---

## 6. Ví dụ minh họa

Xét đồ thị không có hướng sau:

```
A --- B   C --- D
|     |   |
E --- F   G
```

### Bước 1: Khởi tạo
- Đánh dấu tất cả các node (A, B, C, D, E, F, G) là "chưa thăm".
- Tập thành phần liên thông = ∅.

### Bước 2: Tìm kiếm

#### BFS từ node A:
- Queue = [A]
- Đánh dấu A là "đã thăm"
- Lấy A từ queue, thêm các node kề chưa thăm (B, E) vào queue
- Queue = [B, E]
- Lấy B từ queue, thêm F vào queue
- Queue = [E, F]
- Lấy E từ queue, F đã nằm trong queue
- Queue = [F]
- Lấy F từ queue, không có node kề chưa thăm
- Queue = []
- BFS kết thúc, thành phần liên thông 1 = {A, B, E, F}

#### BFS từ node C (chưa thăm):
- Queue = [C]
- Đánh dấu C là "đã thăm"
- Lấy C từ queue, thêm D, G vào queue
- Queue = [D, G]
- Lấy D từ queue, không có node kề chưa thăm
- Queue = [G]
- Lấy G từ queue, không có node kề chưa thăm
- Queue = []
- BFS kết thúc, thành phần liên thông 2 = {C, D, G}

### Bước 3: Kết quả
- Thành phần liên thông 1: {A, B, E, F} → Community 1
- Thành phần liên thông 2: {C, D, G} → Community 2

---

## 7. Ứng dụng và mở rộng

### Ứng dụng
- **Phát hiện mạng con**: Xác định các mạng con bị ngắt kết nối trong hệ thống mạng.
- **Phân tích mạng xã hội**: Xác định các nhóm người hoàn toàn tách biệt không có liên kết.
- **Phân tích hình ảnh**: Tách các đối tượng riêng biệt trong xử lý ảnh.

### Mở rộng cho đồ thị có hướng: Strongly Connected Components (SCC)
- Trong đồ thị có hướng, ta phân biệt **Strongly Connected Components** (các node có thể đi đến nhau theo chiều mũi tên) và **Weakly Connected Components** (bỏ qua chiều mũi tên).
- Thuật toán Kosaraju và Tarjan thường được sử dụng để tìm SCC.

---

## 8. Triển khai thực tế trong Python

```python
import networkx as nx
import matplotlib.pyplot as plt

def find_connected_components(graph):
    # Khởi tạo danh sách chứa các thành phần liên thông
    connected_components = []
    # Đánh dấu các node đã thăm
    visited = set()
    
    # Hàm BFS để tìm tất cả node có thể đến được từ start_node
    def bfs(start_node):
        component = []  # Thành phần liên thông hiện tại
        queue = [start_node]  # Hàng đợi BFS
        visited.add(start_node)  # Đánh dấu node bắt đầu là đã thăm
        
        while queue:
            node = queue.pop(0)  # Lấy node từ đầu hàng đợi
            component.append(node)  # Thêm node vào thành phần liên thông
            
            # Thêm các node kề chưa thăm vào hàng đợi
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return component
    
    # Duyệt qua tất cả các node chưa thăm
    for node in graph:
        if node not in visited:
            # Tìm thành phần liên thông chứa node
            component = bfs(node)
            connected_components.append(component)
    
    return connected_components

# Ví dụ
graph = {
    'A': ['B', 'E'],
    'B': ['A', 'F'],
    'C': ['D', 'G'],
    'D': ['C'],
    'E': ['A', 'F'],
    'F': ['B', 'E'],
    'G': ['C']
}

components = find_connected_components(graph)
print("Các thành phần liên thông:")
for i, component in enumerate(components, 1):
    print(f"Community {i}: {component}")

# Sử dụng NetworkX để hiển thị
G = nx.Graph()
for node, neighbors in graph.items():
    for neighbor in neighbors:
        G.add_edge(node, neighbor)

# Tạo color map dựa vào các thành phần liên thông
color_map = {}
for i, component in enumerate(components):
    for node in component:
        color_map[node] = i

node_colors = [color_map[node] for node in G.nodes()]

plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.rainbow, node_size=500)
plt.title("Connected Components")
plt.show()
```

---

## 9. Tóm tắt

Thuật toán Connected Components là thuật toán đơn giản nhất để phát hiện cộng đồng, dựa trên cơ sở kết nối giữa các node:

1. **Đơn giản**: Chỉ dựa vào khả năng đi đến giữa các node.
2. **Hiệu quả**: Thời gian chạy tuyến tính theo số node và cạnh.
3. **Giới hạn**: Chỉ hoạt động tốt khi các cộng đồng thực sự ngắt kết nối hoàn toàn.

Ưu điểm:
- Đơn giản, dễ hiểu và triển khai
- Thời gian chạy nhanh
- Kết quả xác định và ổn định

Nhược điểm:
- Không phát hiện được cộng đồng trong đồ thị liên thông
- Không linh hoạt với cấu trúc cộng đồng phức tạp
- Không phân tích được mức độ kết nối mạnh/yếu giữa các node