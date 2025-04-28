# Đường Đi và Kết Nối trong Đồ Thị

## 1. Khái Niệm Về Đường Đi (Paths)

**Đường đi** là một khái niệm cơ bản và quan trọng trong lý thuyết đồ thị. Hiểu về đường đi là tiền đề để phát hiện cộng đồng, tìm đường đi ngắn nhất và phân tích kết nối.

### 1.1. Định nghĩa toán học

Cho đồ thị $G = (V, E)$:

- **Đường đi** (path) từ đỉnh $u$ đến đỉnh $v$ là một dãy các đỉnh $v_0, v_1, v_2, \ldots, v_k$ trong đó:
  - $v_0 = u$ (đỉnh bắt đầu)
  - $v_k = v$ (đỉnh kết thúc)
  - $(v_i, v_{i+1}) \in E$ với mọi $0 \leq i < k$ (có cạnh nối giữa các đỉnh liên tiếp)

- **Độ dài của đường đi** là số cạnh trong đường đi, trong trường hợp trên là $k$.

### 1.2. Các loại đường đi đặc biệt

- **Đường đi đơn** (Simple Path): không có đỉnh nào xuất hiện quá một lần.
- **Chu trình** (Cycle): đường đi đóng, với $v_0 = v_k$ và $k \geq 3$.
- **Chu trình đơn** (Simple Cycle): chu trình không đi qua đỉnh nào quá một lần (trừ đỉnh đầu/cuối).

### 1.3. Ví dụ minh họa

Cho đồ thị:

```
A --- B --- C
|     |     |
D --- E --- F
```

- Đường đi từ A đến F: A → B → C → F
- Độ dài của đường đi này là 3.
- Một đường đi khác: A → D → E → F, cũng có độ dài 3.

## 2. Đường Đi Ngắn Nhất (Shortest Paths)

### 2.1. Định nghĩa

**Đường đi ngắn nhất** từ đỉnh $u$ đến đỉnh $v$ là đường đi có độ dài nhỏ nhất trong số tất cả các đường đi có thể từ $u$ đến $v$.

### 2.2. Thuật toán Dijkstra

Thuật toán Dijkstra tìm đường đi ngắn nhất từ một đỉnh nguồn đến tất cả các đỉnh khác trong đồ thị có trọng số không âm.

#### Ý tưởng chính:
1. Duy trì một tập đỉnh $S$ mà khoảng cách ngắn nhất từ nguồn đã được xác định.
2. Lặp lại việc chọn đỉnh $u \notin S$ có khoảng cách nhỏ nhất từ nguồn.
3. Thêm $u$ vào $S$ và cập nhật khoảng cách đến các đỉnh lân cận của $u$.

#### Thuật toán:
```
function Dijkstra(Graph, source):
    // Khởi tạo
    for each vertex v in Graph:
        dist[v] = INFINITY
        prev[v] = UNDEFINED
        visited[v] = false
    
    dist[source] = 0
    priority_queue Q = all vertices in Graph
    
    // Thuật toán chính
    while Q is not empty:
        u = vertex in Q with min dist[u]
        remove u from Q
        visited[u] = true
        
        for each neighbor v of u:
            if visited[v] == false:
                alt = dist[u] + weight(u, v)
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
    
    return dist[], prev[]
```

#### Phức tạp thuật toán:
- Với hàng đợi ưu tiên thông thường: O(V²)
- Với hàng đợi ưu tiên Fibonacci heap: O(E + V log V)

### 2.3. Thuật toán Floyd-Warshall

Thuật toán Floyd-Warshall tìm đường đi ngắn nhất giữa mọi cặp đỉnh trong đồ thị.

#### Ý tưởng chính:
- Sử dụng quy hoạch động để tính khoảng cách ngắn nhất.
- Cho phép cạnh có trọng số âm, nhưng không cho phép chu trình âm.

#### Thuật toán:
```
function FloydWarshall(Graph):
    // Khởi tạo ma trận khoảng cách
    let dist[1...V][1...V] = adjacency matrix of Graph
    
    for each vertex v:
        dist[v][v] = 0
    
    // Thuật toán chính
    for k = 1 to V:
        for i = 1 to V:
            for j = 1 to V:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist[][]
```

#### Phức tạp thuật toán:
- Thời gian: O(V³)
- Không gian: O(V²)

### 2.4. Triển khai thuật toán Dijkstra trong Python

```python
import heapq

def dijkstra(graph, source):
    # Khởi tạo
    dist = {node: float('infinity') for node in graph}
    dist[source] = 0
    prev = {node: None for node in graph}
    visited = {node: False for node in graph}
    
    # Hàng đợi ưu tiên
    pq = [(0, source)]
    
    while pq:
        # Lấy node có khoảng cách nhỏ nhất
        current_dist, current_node = heapq.heappop(pq)
        
        # Nếu node đã xử lý, bỏ qua
        if visited[current_node]:
            continue
        
        visited[current_node] = True
        
        # Cập nhật khoảng cách cho các node lân cận
        for neighbor, weight in graph[current_node].items():
            if visited[neighbor]:
                continue
            
            distance = current_dist + weight
            
            # Nếu tìm thấy đường đi ngắn hơn, cập nhật
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                prev[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    return dist, prev

# Ví dụ sử dụng
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

distances, predecessors = dijkstra(graph, 'A')
print("Khoảng cách từ A:", distances)
print("Đỉnh tiền nhiệm:", predecessors)
```

## 3. Kết Nối (Connectivity) trong Đồ Thị

Kết nối là một thuộc tính quan trọng của đồ thị, phản ánh mức độ liên kết giữa các đỉnh. Kết nối là nền tảng cho việc phân tích cộng đồng trên đồ thị.

### 3.1. Các khái niệm kết nối

#### Trong đồ thị vô hướng:

- **Đồ thị liên thông** (Connected Graph): tồn tại đường đi giữa mọi cặp đỉnh.
- **Thành phần liên thông** (Connected Component): tập con lớn nhất các đỉnh mà giữa hai đỉnh bất kỳ luôn tồn tại đường đi.
- **Cầu** (Bridge): cạnh mà khi loại bỏ sẽ tăng số lượng thành phần liên thông.
- **Khớp** (Articulation Point): đỉnh mà khi loại bỏ sẽ tăng số lượng thành phần liên thông.

#### Trong đồ thị có hướng:

- **Đồ thị liên thông mạnh** (Strongly Connected): tồn tại đường đi có hướng giữa mọi cặp đỉnh.
- **Thành phần liên thông mạnh** (Strongly Connected Component): tập con lớn nhất các đỉnh mà giữa hai đỉnh bất kỳ luôn tồn tại đường đi có hướng.
- **Đồ thị liên thông yếu** (Weakly Connected): trở nên liên thông nếu bỏ qua hướng của các cạnh.

### 3.2. Tính liên thông trong đồ thị

#### Kiểm tra liên thông bằng BFS/DFS:

```python
from collections import deque

def is_connected(graph):
    if not graph:
        return True
    
    # Chọn một đỉnh bất kỳ
    start_node = next(iter(graph))
    
    # BFS từ đỉnh đó
    visited = set()
    queue = deque([start_node])
    visited.add(start_node)
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    # Kiểm tra xem đã thăm tất cả các đỉnh chưa
    return len(visited) == len(graph)
```

#### Tìm các thành phần liên thông:

```python
def find_connected_components(graph):
    visited = set()
    components = []
    
    def dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)
    
    for node in graph:
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(component)
    
    return components
```

### 3.3. Thuật toán Tarjan tìm thành phần liên thông mạnh

Thuật toán Tarjan sử dụng DFS để tìm thành phần liên thông mạnh trong đồ thị có hướng.

#### Ý tưởng chính:
- Thuật toán dựa trên việc tìm các thành phần liên thông mạnh dưới dạng đồ thị con mà một đỉnh bất kỳ có thể đến được đỉnh khác thông qua một đường đi có hướng.
- Sử dụng thuật toán DFS với stack bổ sung để theo dõi các đỉnh trong thành phần hiện tại.

```python
def tarjan_scc(graph):
    index_counter = [0]
    index = {}  # node -> index
    lowlink = {}  # node -> lowlink
    onstack = set()  # đỉnh trên stack
    stack = []
    connected_components = []
    
    def strongconnect(node):
        # Gán chỉ số và lowlink cho node
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        onstack.add(node)
        
        # Xét các đỉnh kề
        for successor in graph.get(node, []):
            if successor not in index:
                # Successor chưa được thăm
                strongconnect(successor)
                lowlink[node] = min(lowlink[node], lowlink[successor])
            elif successor in onstack:
                # Successor đang trên stack (edge trở lại)
                lowlink[node] = min(lowlink[node], index[successor])
        
        # Nếu node là gốc của SCC, lấy tất cả các đỉnh trên stack cho đến node
        if lowlink[node] == index[node]:
            connected_component = []
            while True:
                successor = stack.pop()
                onstack.remove(successor)
                connected_component.append(successor)
                if successor == node:
                    break
            connected_components.append(connected_component)
    
    for node in graph:
        if node not in index:
            strongconnect(node)
    
    return connected_components
```

## 4. Độ Đo Kết Nối và Trung Tâm (Centrality Measures)

Các độ đo trung tâm giúp xác định tầm quan trọng của các đỉnh trong đồ thị. Đây là cơ sở quan trọng cho việc phân tích cộng đồng và mạng xã hội.

### 4.1. Degree Centrality

**Degree Centrality** đo lường mức độ kết nối trực tiếp của một đỉnh - số lượng cạnh kết nối với đỉnh đó.

- Trong đồ thị **vô hướng**: $C_D(v) = \frac{deg(v)}{n-1}$
- Trong đồ thị **có hướng**:
  - **In-degree**: $C_{D,in}(v) = \frac{deg^-(v)}{n-1}$
  - **Out-degree**: $C_{D,out}(v) = \frac{deg^+(v)}{n-1}$

Trong đó:
- $deg(v)$ là bậc của đỉnh $v$
- $n$ là tổng số đỉnh trong đồ thị
- $deg^-(v)$ là bậc vào của $v$
- $deg^+(v)$ là bậc ra của $v$

### 4.2. Closeness Centrality

**Closeness Centrality** đo lường mức độ gần của một đỉnh với các đỉnh khác. Nó dựa trên khoảng cách trung bình từ một đỉnh đến tất cả các đỉnh khác.

$$C_C(v) = \frac{n-1}{\sum_{u \neq v} d(v, u)}$$

Trong đó:
- $d(v, u)$ là khoảng cách ngắn nhất từ $v$ đến $u$
- $n$ là tổng số đỉnh trong đồ thị

### 4.3. Betweenness Centrality

**Betweenness Centrality** đo lường khả năng một đỉnh nằm trên đường đi ngắn nhất giữa các cặp đỉnh khác.

$$C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$

Trong đó:
- $\sigma_{st}$ là tổng số đường đi ngắn nhất từ đỉnh $s$ đến đỉnh $t$
- $\sigma_{st}(v)$ là số đường đi ngắn nhất từ $s$ đến $t$ đi qua đỉnh $v$

### 4.4. Eigenvector Centrality

**Eigenvector Centrality** đo lường ảnh hưởng của một đỉnh trong mạng dựa trên nguyên lý: kết nối với các đỉnh quan trọng sẽ làm tăng tầm quan trọng của đỉnh đó.

$$C_E(v) = \frac{1}{\lambda} \sum_{u \in N(v)} C_E(u)$$

Trong đó:
- $\lambda$ là một hằng số (giá trị riêng lớn nhất của ma trận kề)
- $N(v)$ là tập các đỉnh kề với $v$

PageRank là một biến thể của Eigenvector Centrality.

### 4.5. Ví dụ tính toán Centrality

Xét đồ thị đơn giản sau:

```
    A --- B
   /|     |\
  / |     | \
 C  |     |  D
  \ |     | /
   \|     |/
    E --- F
```

#### Degree Centrality:
- $C_D(A) = \frac{3}{5} = 0.6$ (A kết nối với B, C, E)
- $C_D(B) = \frac{3}{5} = 0.6$ (B kết nối với A, D, F)
- $C_D(C) = \frac{2}{5} = 0.4$ (C kết nối với A, E)
- $C_D(D) = \frac{2}{5} = 0.4$ (D kết nối với B, F)
- $C_D(E) = \frac{3}{5} = 0.6$ (E kết nối với A, C, F)
- $C_D(F) = \frac{3}{5} = 0.6$ (F kết nối với B, D, E)

#### Closeness Centrality:
(Tính toán khoảng cách ngắn nhất từ mỗi đỉnh đến các đỉnh khác, rồi áp dụng công thức)

## 5. Ứng Dụng Trong Phát Hiện Cộng Đồng

### 5.1. Phát hiện cộng đồng dựa trên kết nối

Các thuật toán phát hiện cộng đồng thường dựa trên các khái niệm về đường đi và kết nối:

1. **Connected Components**: Mỗi thành phần liên thông là một cộng đồng.
2. **Đường đi ngắn nhất**: Các đỉnh thuộc cùng một cộng đồng có xu hướng có đường đi ngắn giữa chúng.
3. **Random Walks** (như thuật toán Walktrap): Các bước đi ngẫu nhiên thường bị "mắc kẹt" trong cộng đồng.

### 5.2. Edge Betweenness

**Edge Betweenness** là một khái niệm tương tự như Betweenness Centrality nhưng áp dụng cho cạnh. Đây là cơ sở cho thuật toán phát hiện cộng đồng Girvan-Newman.

$$EB(e) = \sum_{s \neq t} \frac{\sigma_{st}(e)}{\sigma_{st}}$$

Trong đó:
- $\sigma_{st}$ là tổng số đường đi ngắn nhất từ đỉnh $s$ đến đỉnh $t$
- $\sigma_{st}(e)$ là số đường đi ngắn nhất từ $s$ đến $t$ đi qua cạnh $e$

### 5.3. Thuật toán Girvan-Newman

Thuật toán Girvan-Newman phát hiện cộng đồng bằng cách loại bỏ dần các cạnh có Edge Betweenness cao nhất:

1. Tính Edge Betweenness cho tất cả các cạnh trong đồ thị.
2. Loại bỏ cạnh có Edge Betweenness cao nhất.
3. Tính lại Edge Betweenness cho tất cả các cạnh còn lại.
4. Lặp lại bước 2 và 3 cho đến khi đồ thị bị chia thành các thành phần liên thông.

## 6. Kết Luận

Hiểu về đường đi và kết nối là nền tảng quan trọng cho việc phát hiện cộng đồng và phân tích mạng xã hội:

- **Đường đi ngắn nhất** giúp xác định cấu trúc hiệu quả của mạng lưới.
- **Kết nối** giúp xác định các thành phần và cộng đồng trong đồ thị.
- **Độ đo trung tâm** giúp xác định các đỉnh và cạnh quan trọng.

Các thuật toán như Dijkstra, Floyd-Warshall, Tarjan, và Girvan-Newman là những công cụ mạnh mẽ để phân tích đường đi và kết nối trong đồ thị, từ đó hỗ trợ việc phát hiện cộng đồng.

---

## Bài Tiếp Theo

Trong bài tiếp theo, chúng ta sẽ tìm hiểu về [Phân tích mạng xã hội](social_network_analysis.md), áp dụng các khái niệm về đường đi và kết nối vào việc phân tích các mạng xã hội thực tế.