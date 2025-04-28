# Lý Thuyết Đồ Thị: Các Khái Niệm Cơ Bản

## 1. Đồ Thị Là Gì?

**Đồ thị** (Graph) là một cấu trúc dữ liệu gồm hai thành phần chính:
- Tập hợp các **đỉnh** (vertices/nodes)
- Tập hợp các **cạnh** (edges) nối giữa các đỉnh

Về mặt toán học, đồ thị được ký hiệu là $G = (V, E)$ trong đó:
- $V$ là tập hợp các đỉnh
- $E$ là tập hợp các cạnh, mỗi cạnh là một cặp đỉnh $(u, v)$ với $u, v \in V$

## 2. Biểu Diễn Trực Quan

Đồ thị thường được vẽ như một sơ đồ với các điểm (đỉnh) được kết nối bởi các đường thẳng hoặc đường cong (cạnh).

Ví dụ đơn giản:
```
    A --- B
   /|     |\
  / |     | \
 C  |     |  D
  \ |     | /
   \|     |/
    E --- F
```

## 3. Các Loại Đồ Thị

### 3.1. Phân loại theo hướng cạnh

#### Đồ thị vô hướng (Undirected Graph)
- Các cạnh không có hướng
- Nếu $(u, v) \in E$ thì $(v, u)$ cũng $\in E$
- Ví dụ: mạng lưới bạn bè trên Facebook (nếu A là bạn của B thì B cũng là bạn của A)

#### Đồ thị có hướng (Directed Graph)
- Các cạnh có hướng, từ đỉnh này đến đỉnh khác
- Cạnh $(u, v)$ khác với cạnh $(v, u)$
- Ví dụ: mạng lưới người theo dõi trên Twitter (A có thể theo dõi B mà B không theo dõi lại A)

### 3.2. Phân loại theo trọng số

#### Đồ thị không trọng số (Unweighted Graph)
- Tất cả các cạnh có giá trị bằng nhau (thường là 1)

#### Đồ thị có trọng số (Weighted Graph)
- Mỗi cạnh có một giá trị (trọng số) riêng
- Ví dụ: mạng lưới đường giao thông với khoảng cách giữa các thành phố

### 3.3. Các loại đồ thị đặc biệt

#### Đồ thị đầy đủ (Complete Graph)
- Mọi cặp đỉnh đều được nối với nhau
- Với $n$ đỉnh, số cạnh là $\frac{n(n-1)}{2}$

#### Đồ thị hai phía (Bipartite Graph)
- Tập đỉnh có thể chia thành hai tập con không giao nhau
- Các cạnh chỉ nối giữa các đỉnh thuộc hai tập con khác nhau
- Ví dụ: đồ thị biểu diễn mối quan hệ giữa sinh viên và môn học

#### Đồ thị chu trình (Cycle Graph)
- Tất cả các đỉnh đều kết nối với chính xác 2 đỉnh khác
- Tạo thành một vòng kín

#### Đồ thị cây (Tree)
- Đồ thị liên thông không có chu trình
- Với $n$ đỉnh, có đúng $n-1$ cạnh

## 4. Các Khái Niệm Cơ Bản

### 4.1. Bậc của đỉnh (Degree)

- **Bậc vào** (in-degree): số cạnh đi vào một đỉnh (trong đồ thị có hướng)
- **Bậc ra** (out-degree): số cạnh đi ra từ một đỉnh (trong đồ thị có hướng)
- **Bậc** (degree): tổng số cạnh nối với một đỉnh (trong đồ thị vô hướng)

Ví dụ: Trong đồ thị vô hướng, nếu đỉnh A kết nối với 3 đỉnh khác, bậc của A là 3.

### 4.2. Đường đi (Path)

- Một **đường đi** từ đỉnh $u$ đến đỉnh $v$ là một dãy các đỉnh và cạnh bắt đầu từ $u$ và kết thúc tại $v$.
- **Độ dài của đường đi** là số cạnh trong đường đi.
- **Đường đi đơn** (simple path): không đi qua đỉnh nào quá một lần.

### 4.3. Chu trình (Cycle)

- **Chu trình** là đường đi bắt đầu và kết thúc tại cùng một đỉnh.
- **Chu trình đơn** (simple cycle): không đi qua đỉnh nào quá một lần (trừ đỉnh đầu/cuối).

### 4.4. Kết nối (Connectivity)

- Đồ thị **liên thông** (connected): tồn tại đường đi giữa mọi cặp đỉnh.
- **Thành phần liên thông** (connected component): tập con lớn nhất các đỉnh mà giữa hai đỉnh bất kỳ luôn tồn tại đường đi.
- Đồ thị **liên thông mạnh** (strongly connected): trong đồ thị có hướng, tồn tại đường đi có hướng giữa mọi cặp đỉnh.

## 5. Biểu Diễn Đồ Thị Trong Máy Tính

### 5.1. Ma trận kề (Adjacency Matrix)

Ma trận kề $A$ của đồ thị $G$ với $n$ đỉnh là ma trận $n \times n$ được định nghĩa như sau:

$$A[i][j] = \begin{cases}
1 & \text{nếu có cạnh từ đỉnh } i \text{ đến đỉnh } j \\
0 & \text{nếu không có cạnh}
\end{cases}$$

Với đồ thị có trọng số:

$$A[i][j] = \begin{cases}
w(i,j) & \text{nếu có cạnh từ đỉnh } i \text{ đến đỉnh } j \text{ với trọng số } w(i,j) \\
0 \text{ hoặc } \infty & \text{nếu không có cạnh}
\end{cases}$$

**Ưu điểm**:
- Truy vấn nhanh (O(1)) để kiểm tra cạnh giữa hai đỉnh
- Dễ hiểu và triển khai

**Nhược điểm**:
- Tốn bộ nhớ O(V²) ngay cả với đồ thị thưa (sparse graph)

### 5.2. Danh sách kề (Adjacency List)

Mỗi đỉnh được liên kết với một danh sách các đỉnh kề với nó.

**Ưu điểm**:
- Tiết kiệm bộ nhớ cho đồ thị thưa: O(V + E)
- Hiệu quả khi duyệt qua tất cả các đỉnh kề

**Nhược điểm**:
- Kiểm tra sự tồn tại của cạnh chậm hơn (O(degree(v)))

### 5.3. Ma trận incidence

Với đồ thị có $n$ đỉnh và $m$ cạnh, ma trận incidence $M$ là ma trận $n \times m$:

$$M[i][j] = \begin{cases}
1 & \text{nếu đỉnh } i \text{ là một trong hai đầu mút của cạnh } j \\
0 & \text{nếu không}
\end{cases}$$

## 6. Ví Dụ Biểu Diễn Đồ Thị

Xét đồ thị vô hướng sau:

```
   A --- B
  /|     |\
 / |     | \
C  |     |  D
 \ |     | /
  \|     |/
   E --- F
```

### Ma trận kề

```
    A  B  C  D  E  F
A  [0, 1, 1, 0, 1, 0]
B  [1, 0, 0, 1, 0, 1]
C  [1, 0, 0, 0, 1, 0]
D  [0, 1, 0, 0, 0, 1]
E  [1, 0, 1, 0, 0, 1]
F  [0, 1, 0, 1, 1, 0]
```

### Danh sách kề

```
A: [B, C, E]
B: [A, D, F]
C: [A, E]
D: [B, F]
E: [A, C, F]
F: [B, D, E]
```

## 7. Triển Khai Cấu Trúc Đồ Thị trong Python

```python
# Biểu diễn đồ thị bằng ma trận kề
def create_adjacency_matrix(n, edges):
    """
    Tạo ma trận kề cho đồ thị có n đỉnh và tập edges
    """
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for u, v in edges:
        matrix[u][v] = 1
        matrix[v][u] = 1  # Đối với đồ thị vô hướng
    return matrix

# Biểu diễn đồ thị bằng danh sách kề
def create_adjacency_list(n, edges):
    """
    Tạo danh sách kề cho đồ thị có n đỉnh và tập edges
    """
    adj_list = [[] for _ in range(n)]
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)  # Đối với đồ thị vô hướng
    return adj_list

# Sử dụng thư viện NetworkX
import networkx as nx
import matplotlib.pyplot as plt

def create_and_visualize_graph(edges):
    """
    Tạo và hiển thị đồ thị sử dụng NetworkX
    """
    G = nx.Graph()
    G.add_edges_from(edges)
    
    plt.figure(figsize=(10, 6))
    nx.draw(G, with_labels=True, node_color='skyblue', 
            node_size=1500, edge_color='black', linewidths=1, 
            font_size=15)
    plt.title("Đồ thị đơn giản")
    plt.show()

# Ví dụ sử dụng
edges = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 4), (3, 5), (4, 5)]
create_and_visualize_graph(edges)
```

## 8. Kết Luận

Đồ thị là cấu trúc dữ liệu linh hoạt có thể biểu diễn nhiều mối quan hệ và hiện tượng trong thế giới thực. Hiểu về các khái niệm cơ bản của lý thuyết đồ thị là nền tảng quan trọng để tiếp cận các thuật toán nâng cao như thuật toán đường đi ngắn nhất, phát hiện chu trình, phát hiện cộng đồng, v.v.

---

## Bài Tiếp Theo

Trong bài tiếp theo, chúng ta sẽ tìm hiểu về [Các thuật toán duyệt đồ thị](graph_traversal.md) như BFS (Breadth-First Search) và DFS (Depth-First Search), là nền tảng cho nhiều thuật toán đồ thị phức tạp hơn.