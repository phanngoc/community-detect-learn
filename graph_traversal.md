# Các Thuật Toán Duyệt Đồ Thị

## 1. Giới Thiệu

Duyệt đồ thị là quá trình thăm tất cả các đỉnh trong đồ thị theo một thứ tự nhất định. Đây là nền tảng cho nhiều thuật toán đồ thị khác nhau, bao gồm cả các thuật toán phát hiện cộng đồng. Có hai phương pháp duyệt đồ thị phổ biến:

- **Duyệt theo chiều rộng** (Breadth-First Search - BFS)
- **Duyệt theo chiều sâu** (Depth-First Search - DFS)

## 2. Duyệt Theo Chiều Rộng (BFS)

### 2.1. Nguyên lý hoạt động

BFS duyệt đồ thị theo nguyên tắc **"duyệt theo tầng"**, nghĩa là:
1. Bắt đầu từ một đỉnh nguồn
2. Thăm tất cả các đỉnh kề với đỉnh nguồn 
3. Tiếp tục thăm các đỉnh kề với các đỉnh vừa thăm
4. Lặp lại quá trình cho đến khi thăm hết tất cả các đỉnh có thể đến được

### 2.2. Ý tưởng toán học

Có thể hình dung BFS tạo ra một "cây BFS" từ đỉnh nguồn với các tính chất:
- Khoảng cách từ gốc đến bất kỳ đỉnh nào trong cây là khoảng cách ngắn nhất từ đỉnh nguồn đến đỉnh đó trong đồ thị ban đầu
- Mỗi tầng của cây bao gồm các đỉnh có cùng khoảng cách từ đỉnh nguồn

### 2.3. Thuật toán BFS

```
BFS(graph, source):
    // Khởi tạo
    for each vertex u in graph except source:
        distance[u] = INFINITY
        visited[u] = false
        parent[u] = NULL
    
    distance[source] = 0
    visited[source] = true
    queue = empty queue
    queue.enqueue(source)
    
    // Duyệt BFS
    while queue is not empty:
        u = queue.dequeue()
        for each neighbor v of u:
            if visited[v] == false:
                visited[v] = true
                distance[v] = distance[u] + 1
                parent[v] = u
                queue.enqueue(v)
```

### 2.4. Triển khai trong Python

```python
from collections import deque

def bfs(graph, source):
    # Khởi tạo
    n = len(graph)
    distance = [float('inf')] * n
    visited = [False] * n
    parent = [None] * n
    
    distance[source] = 0
    visited[source] = True
    queue = deque([source])
    
    # Duyệt BFS
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if not visited[v]:
                visited[v] = True
                distance[v] = distance[u] + 1
                parent[v] = u
                queue.append(v)
    
    return distance, parent

# Ví dụ sử dụng
graph = [
    [1, 2],  # Đỉnh 0 kề với đỉnh 1, 2
    [0, 3],  # Đỉnh 1 kề với đỉnh 0, 3
    [0, 3, 4],  # Đỉnh 2 kề với đỉnh 0, 3, 4
    [1, 2, 5],  # Đỉnh 3 kề với đỉnh 1, 2, 5
    [2, 5],  # Đỉnh 4 kề với đỉnh 2, 5
    [3, 4]   # Đỉnh 5 kề với đỉnh 3, 4
]

distance, parent = bfs(graph, 0)
print("Khoảng cách từ đỉnh nguồn:", distance)
print("Đỉnh cha trong cây BFS:", parent)
```

### 2.5. Phân tích thuật toán BFS

- **Thời gian**: O(V + E) với V là số đỉnh và E là số cạnh
- **Không gian**: O(V) cho hàng đợi và các mảng phụ trợ

### 2.6. Ứng dụng của BFS

1. **Tìm đường đi ngắn nhất** trong đồ thị không trọng số
2. **Phát hiện chu trình** trong đồ thị
3. **Phát hiện thành phần liên thông** (Connected Components)
4. **Kiểm tra tính hai phía** (Bipartite) của đồ thị
5. **Tìm tất cả các đỉnh trong khoảng cách k** từ đỉnh nguồn

## 3. Duyệt Theo Chiều Sâu (DFS)

### 3.1. Nguyên lý hoạt động

DFS duyệt đồ thị theo nguyên tắc **"đi sâu nhất có thể trước"**:
1. Bắt đầu từ một đỉnh nguồn
2. Đi đến một đỉnh kề chưa thăm
3. Tiếp tục đi sâu từ đỉnh mới cho đến khi không thể đi tiếp
4. Quay lui và tìm đường đi khác
5. Lặp lại cho đến khi thăm hết các đỉnh có thể đến được

### 3.2. Ý tưởng toán học

DFS tạo ra một "cây DFS" hoặc "rừng DFS" (nhiều cây) với các tính chất:
- Các cạnh trong đồ thị được phân loại thành:
  - **Cạnh cây** (Tree edges): nằm trong cây DFS
  - **Cạnh ngược** (Back edges): nối đến tổ tiên trong cây DFS
  - **Cạnh chéo** (Cross edges): nối giữa các nhánh cây khác nhau
  - **Cạnh xuôi** (Forward edges): nối đến hậu duệ không trực tiếp trong cây

### 3.3. Thuật toán DFS đệ quy

```
DFS(graph, u):
    visited[u] = true
    time = time + 1
    discovery_time[u] = time
    
    for each neighbor v of u:
        if visited[v] == false:
            parent[v] = u
            DFS(graph, v)
    
    time = time + 1
    finish_time[u] = time
```

### 3.4. Thuật toán DFS sử dụng ngăn xếp (không đệ quy)

```
DFS_Iterative(graph, source):
    for each vertex u in graph:
        visited[u] = false
        parent[u] = NULL
    
    stack = empty stack
    stack.push(source)
    
    while stack is not empty:
        u = stack.top()  // Không lấy ra khỏi stack ngay
        
        if visited[u] == false:
            visited[u] = true
            // Xử lý đỉnh u
        
        // Tìm đỉnh kề chưa thăm
        has_unvisited_neighbor = false
        for each neighbor v of u:
            if visited[v] == false:
                parent[v] = u
                stack.push(v)
                has_unvisited_neighbor = true
                break
        
        // Nếu không có đỉnh kề chưa thăm, lấy ra khỏi ngăn xếp
        if not has_unvisited_neighbor:
            stack.pop()
```

### 3.5. Triển khai trong Python

```python
def dfs_recursive(graph, source):
    n = len(graph)
    visited = [False] * n
    discovery_time = [0] * n
    finish_time = [0] * n
    parent = [None] * n
    time = [0]  # Sử dụng list để time có thể thay đổi trong hàm đệ quy
    
    def dfs_visit(u):
        visited[u] = True
        time[0] += 1
        discovery_time[u] = time[0]
        
        for v in graph[u]:
            if not visited[v]:
                parent[v] = u
                dfs_visit(v)
        
        time[0] += 1
        finish_time[u] = time[0]
    
    # Gọi DFS cho đỉnh nguồn
    dfs_visit(source)
    
    # Nếu đồ thị không liên thông, gọi DFS cho các đỉnh chưa thăm
    for u in range(n):
        if not visited[u]:
            dfs_visit(u)
    
    return visited, discovery_time, finish_time, parent

# Triển khai không đệ quy
def dfs_iterative(graph, source):
    n = len(graph)
    visited = [False] * n
    parent = [None] * n
    
    stack = [source]
    while stack:
        u = stack[-1]  # Xem đỉnh trên cùng của ngăn xếp
        
        if not visited[u]:
            visited[u] = True
            print(f"Thăm đỉnh {u}")
        
        # Tìm đỉnh kề chưa thăm
        has_unvisited = False
        for v in graph[u]:
            if not visited[v]:
                parent[v] = u
                stack.append(v)
                has_unvisited = True
                break
        
        # Nếu không có đỉnh kề chưa thăm, lấy ra khỏi ngăn xếp
        if not has_unvisited:
            stack.pop()
    
    return visited, parent
```

### 3.6. Phân tích thuật toán DFS

- **Thời gian**: O(V + E) với V là số đỉnh và E là số cạnh
- **Không gian**: 
  - O(V) cho ngăn xếp và các mảng phụ trợ (triển khai không đệ quy)
  - O(V) cho không gian ngăn xếp hàm gọi (triển khai đệ quy)

### 3.7. Ứng dụng của DFS

1. **Phát hiện chu trình** trong đồ thị
2. **Sắp xếp tô-pô** (Topological Sort) cho đồ thị có hướng không có chu trình (DAG)
3. **Phát hiện thành phần liên thông mạnh** (Strongly Connected Components)
4. **Giải quyết mê cung** và các bài toán tìm đường
5. **Tìm cầu và khớp** trong đồ thị
6. **Tạo cây khung** (Spanning Tree)

## 4. So Sánh BFS và DFS

| Tiêu chí | BFS | DFS |
|---------|-----|-----|
| Chiến lược | Duyệt theo chiều rộng | Duyệt theo chiều sâu |
| Cấu trúc dữ liệu | Hàng đợi (Queue) | Ngăn xếp (Stack) |
| Tìm đường đi ngắn nhất | Tốt với đồ thị không trọng số | Không đảm bảo |
| Không gian bộ nhớ | Lớn hơn (lưu nhiều đỉnh) | Nhỏ hơn (chỉ lưu một đường đi) |
| Ứng dụng phổ biến | Tìm đường đi ngắn nhất, kiểm tra tính kết nối | Phát hiện chu trình, sắp xếp tô-pô |
| Vô hạn | Có thể không kết thúc với đồ thị vô hạn | Có thể không kết thúc với đồ thị vô hạn |

## 5. Ứng Dụng Trong Phát Hiện Cộng Đồng

### 5.1. BFS và Connected Components

```python
def find_connected_components_bfs(graph):
    n = len(graph)
    visited = [False] * n
    components = []
    
    for u in range(n):
        if not visited[u]:
            # Tìm thành phần liên thông chứa u
            component = []
            queue = deque([u])
            visited[u] = True
            
            while queue:
                v = queue.popleft()
                component.append(v)
                
                for w in graph[v]:
                    if not visited[w]:
                        visited[w] = True
                        queue.append(w)
            
            components.append(component)
    
    return components
```

### 5.2. DFS và Connected Components

```python
def find_connected_components_dfs(graph):
    n = len(graph)
    visited = [False] * n
    components = []
    
    def dfs(u, component):
        visited[u] = True
        component.append(u)
        
        for v in graph[u]:
            if not visited[v]:
                dfs(v, component)
    
    for u in range(n):
        if not visited[u]:
            component = []
            dfs(u, component)
            components.append(component)
    
    return components
```

## 6. Ví Dụ Minh Họa Chi Tiết

Xét đồ thị sau:

```
    0 --- 1
    |     |
    |     |
    2 --- 3 --- 5
    |           |
    |           |
    4 ----------+
```

### 6.1. Duyệt BFS từ đỉnh 0

1. Khởi tạo:
   - Queue = [0]
   - visited = [True, False, False, False, False, False]
   - distance = [0, ∞, ∞, ∞, ∞, ∞]
   - parent = [None, None, None, None, None, None]

2. Lấy đỉnh 0 từ queue, thêm các đỉnh kề (1, 2):
   - Queue = [1, 2]
   - visited = [True, True, True, False, False, False]
   - distance = [0, 1, 1, ∞, ∞, ∞]
   - parent = [None, 0, 0, None, None, None]

3. Lấy đỉnh 1 từ queue, thêm đỉnh kề (3):
   - Queue = [2, 3]
   - visited = [True, True, True, True, False, False]
   - distance = [0, 1, 1, 2, ∞, ∞]
   - parent = [None, 0, 0, 1, None, None]

4. Lấy đỉnh 2 từ queue, thêm đỉnh kề (4):
   - Queue = [3, 4]
   - visited = [True, True, True, True, True, False]
   - distance = [0, 1, 1, 2, 2, ∞]
   - parent = [None, 0, 0, 1, 2, None]

5. Lấy đỉnh 3 từ queue, thêm đỉnh kề (5):
   - Queue = [4, 5]
   - visited = [True, True, True, True, True, True]
   - distance = [0, 1, 1, 2, 2, 3]
   - parent = [None, 0, 0, 1, 2, 3]

6. Lấy đỉnh 4 từ queue, không có đỉnh kề mới:
   - Queue = [5]

7. Lấy đỉnh 5 từ queue, không có đỉnh kề mới:
   - Queue = []

Kết quả:
- distance = [0, 1, 1, 2, 2, 3]
- Cây BFS: 0 -> 1 -> 3 -> 5 và 0 -> 2 -> 4

### 6.2. Duyệt DFS từ đỉnh 0

1. Thăm đỉnh 0, đánh dấu visited[0] = True
2. Từ đỉnh 0, đến đỉnh kề 1, đánh dấu visited[1] = True
3. Từ đỉnh 1, đến đỉnh kề 3, đánh dấu visited[3] = True
4. Từ đỉnh 3, đến đỉnh kề 5, đánh dấu visited[5] = True
5. Đỉnh 5 không có đỉnh kề chưa thăm, quay lui về đỉnh 3
6. Đỉnh 3 không còn đỉnh kề chưa thăm, quay lui về đỉnh 1
7. Đỉnh 1 không còn đỉnh kề chưa thăm, quay lui về đỉnh 0
8. Từ đỉnh 0, đến đỉnh kề 2, đánh dấu visited[2] = True
9. Từ đỉnh 2, đến đỉnh kề 4, đánh dấu visited[4] = True
10. Đỉnh 4 không có đỉnh kề chưa thăm, quay lui về đỉnh 2
11. Đỉnh 2 không còn đỉnh kề chưa thăm, quay lui về đỉnh 0
12. Đỉnh 0 không còn đỉnh kề chưa thăm, kết thúc DFS

Thứ tự thăm: 0, 1, 3, 5, 2, 4
Cây DFS: 0 -> 1 -> 3 -> 5 và 0 -> 2 -> 4

## 7. Kết Luận

BFS và DFS là hai thuật toán duyệt đồ thị cơ bản nhưng rất mạnh mẽ. Chúng là nền tảng cho nhiều thuật toán đồ thị phức tạp hơn, đặc biệt là trong lĩnh vực phát hiện cộng đồng (community detection):

- **BFS** giúp tìm thành phần liên thông và phân tích cấu trúc cộng đồng dựa trên khoảng cách ngắn nhất.
- **DFS** hữu ích trong việc phát hiện chu trình, xác định thành phần liên thông mạnh và phân tích cấu trúc phân cấp của cộng đồng.

---

## Bài Tiếp Theo

Trong bài tiếp theo, chúng ta sẽ tìm hiểu về [Đường đi và kết nối](paths_and_connectivity.md) trong đồ thị, bao gồm các thuật toán tìm đường đi ngắn nhất và phân tích kết nối.