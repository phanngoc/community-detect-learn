# Thuật toán Walktrap - Phát hiện cộng đồng dựa trên Random Walks

**Walktrap** là một thuật toán phát hiện cộng đồng (community detection) dựa trên ý tưởng: **Các bước đi ngẫu nhiên (random walks) có xu hướng bị "mắc kẹt" (trapped) bên trong các cộng đồng**.

---

## 1. Ý tưởng cơ bản

Thuật toán Walktrap dựa trên nguyên lý:

1. Khi thực hiện các bước đi ngẫu nhiên trên đồ thị, bước đi có xu hướng ở lâu hơn trong cùng một cộng đồng.
2. Các node thuộc cùng một cộng đồng sẽ có "xác suất tiếp cận" (proximity probability) cao hơn.
3. Ta sử dụng các bước đi ngẫu nhiên có độ dài ngắn để xác định khoảng cách giữa các node, sau đó gom cụm các node gần nhau.

---

## 2. Định nghĩa toán học

Cho một đồ thị không có hướng $G = (V, E)$:
- $V$ là tập các đỉnh (nodes)
- $E$ là tập các cạnh (edges)
- $n = |V|$ là số lượng nodes
- $A$ là ma trận kề (adjacency matrix) của đồ thị

### 2.1. Ma trận chuyển (Transition Matrix)

Ma trận chuyển $P$ được định nghĩa như sau:

$$P_{ij} = \frac{A_{ij}}{d(i)}$$

Trong đó:
- $A_{ij}$ là phần tử $(i,j)$ của ma trận kề (1 nếu có cạnh nối $i$ và $j$, 0 nếu không)
- $d(i)$ là bậc (degree) của node $i$

$P_{ij}$ đại diện cho xác suất từ node $i$ đi đến node $j$ trong 1 bước.

### 2.2. Ma trận xác suất bước đi ngẫu nhiên t bước

Gọi $P^t$ là ma trận xác suất cho bước đi ngẫu nhiên độ dài $t$:

$$P^t_{ij} = \text{Xác suất từ node $i$ đi đến node $j$ trong $t$ bước}$$

### 2.3. Khoảng cách giữa các node

Khoảng cách giữa hai node $i$ và $j$ được định nghĩa dựa trên bước đi ngẫu nhiên độ dài $t$:

$$r_{ij} = \sqrt{\sum_{k=1}^{n} \frac{(P^t_{ik} - P^t_{jk})^2}{d(k)}}$$

Trong đó:
- $P^t_{ik}$ là xác suất đi từ $i$ đến $k$ trong $t$ bước
- $d(k)$ là bậc của node $k$

### 2.4. Khoảng cách giữa các cộng đồng (clusters)

Gọi $C_1$ và $C_2$ là hai cộng đồng, khoảng cách giữa chúng được định nghĩa:

$$D(C_1, C_2) = \frac{|C_1||C_2|}{|C_1|+|C_2|} r^2(C_1, C_2)$$

Trong đó $r(C_1, C_2)$ là khoảng cách Ward giữa hai cộng đồng, được tính từ vector xác suất của chúng.

---

## 3. Thuật toán Walktrap

Thuật toán Walktrap là một thuật toán phân cụm phân cấp (hierarchical clustering) với các bước như sau:

### Bước 1: Khởi tạo
- Tính ma trận chuyển $P$ từ đồ thị.
- Tính $P^t$ với $t$ là một tham số (thường là 4 hoặc 5).
- Mỗi node ban đầu là một cộng đồng riêng biệt.

### Bước 2: Gộp cộng đồng theo phân cụm phân cấp
- Tại mỗi bước, gộp hai cộng đồng $C_1$ và $C_2$ có khoảng cách $D(C_1, C_2)$ nhỏ nhất.
- Cập nhật khoảng cách giữa cộng đồng mới và các cộng đồng còn lại.

### Bước 3: Lặp lại
- Lặp lại Bước 2 cho đến khi chỉ còn một cộng đồng duy nhất.

### Bước 4: Chọn phân vùng tốt nhất
- Sử dụng một chỉ số đánh giá (như modularity) để chọn phân vùng tốt nhất từ cây phân cụm phân cấp.

---

## 4. Lý do thuật toán hoạt động tốt

1. **Đặc tính của random walk**: Trong một cộng đồng, các node có nhiều kết nối với nhau hơn so với bên ngoài, nên bước đi ngẫu nhiên có xu hướng ở lại cộng đồng.

2. **Độ dài bước đi vừa phải**: 
   - Nếu $t$ quá nhỏ: chỉ phản ánh cấu trúc cục bộ.
   - Nếu $t$ quá lớn: hội tụ đến phân phối dừng (stationary distribution) và mất thông tin cấu trúc.
   - $t$ vừa phải (thường từ 3-7) nắm bắt được cấu trúc cộng đồng.

3. **Khoảng cách hiệu quả**: Công thức khoảng cách được thiết kế để phản ánh mức độ tương đồng về cấu trúc cộng đồng giữa các node.

---

## 5. Ví dụ minh họa

Xét đồ thị đơn giản như sau:

```
    A --- B
   /|     |\
  / |     | \
 C  |     |  D
  \ |     | /
   \|     |/
    E --- F
```

### Bước 1: Tính ma trận chuyển $P$

$$P = \begin{bmatrix}
0 & 1/3 & 1/3 & 0 & 1/3 & 0 \\
1/3 & 0 & 0 & 1/3 & 0 & 1/3 \\
1/2 & 0 & 0 & 0 & 1/2 & 0 \\
0 & 1/2 & 0 & 0 & 0 & 1/2 \\
1/3 & 0 & 1/3 & 0 & 0 & 1/3 \\
0 & 1/3 & 0 & 1/3 & 1/3 & 0
\end{bmatrix}$$

### Bước 2: Tính $P^t$ (giả sử $t=2$)

$$P^2 = P \times P$$

(Kết quả của phép nhân ma trận)

### Bước 3: Tính khoảng cách giữa các node

Sử dụng công thức:

$$r_{ij} = \sqrt{\sum_{k=1}^{n} \frac{(P^2_{ik} - P^2_{jk})^2}{d(k)}}$$

### Bước 4: Phân cụm phân cấp

Ban đầu, mỗi node là một cộng đồng:
- $C_1 = \{A\}$
- $C_2 = \{B\}$
- $C_3 = \{C\}$
- $C_4 = \{D\}$
- $C_5 = \{E\}$
- $C_6 = \{F\}$

Theo tính toán khoảng cách, giả sử:
1. Gộp $C_1$ và $C_3$ thành $C_{13} = \{A, C\}$
2. Gộp $C_2$ và $C_4$ thành $C_{24} = \{B, D\}$
3. Gộp $C_5$ và $C_6$ thành $C_{56} = \{E, F\}$
4. Gộp $C_{13}$ và $C_{56}$ thành $C_{1356} = \{A, C, E, F\}$
5. Gộp $C_{1356}$ và $C_{24}$ thành $C_{135624} = \{A, B, C, D, E, F\}$

### Bước 5: Chọn phân vùng tốt nhất dựa trên modularity

Tính modularity cho mỗi phân vùng, giả sử phân vùng tốt nhất là:
- Community 1: $\{A, C, E\}$
- Community 2: $\{B, D, F\}$

---

## 6. Phức tạp thuật toán

- **Thời gian**: $O(mn^2)$ trong trường hợp tệ nhất, với $m$ là số cạnh, $n$ là số node.
- **Không gian**: $O(n^2)$ để lưu trữ ma trận chuyển và khoảng cách.

Trong thực tế, với các đồ thị thưa (sparse graphs), phức tạp có thể giảm đáng kể.

---

## 7. Triển khai thực tế trong Python

```python
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster

def walktrap_community(G, t=4):
    # Tính ma trận chuyển P
    n = G.number_of_nodes()
    nodes = list(G.nodes())
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    
    # Khởi tạo ma trận chuyển
    P = np.zeros((n, n))
    for u in G.nodes():
        neighbors = list(G.neighbors(u))
        degree = len(neighbors)
        if degree > 0:  # Tránh chia cho 0
            for v in neighbors:
                P[node_to_idx[u], node_to_idx[v]] = 1.0 / degree
    
    # Tính P^t bằng cách lũy thừa ma trận
    P_t = np.linalg.matrix_power(P, t)
    
    # Tính ma trận khoảng cách
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            # Tính khoảng cách giữa node i và j
            d_ij = 0
            for k in range(n):
                degree_k = G.degree(nodes[k])
                if degree_k > 0:  # Tránh chia cho 0
                    d_ij += (P_t[i, k] - P_t[j, k])**2 / degree_k
            D[i, j] = np.sqrt(d_ij)
            D[j, i] = D[i, j]  # Ma trận đối xứng
    
    # Áp dụng phân cụm phân cấp
    condensed_D = []
    for i in range(n):
        for j in range(i+1, n):
            condensed_D.append(D[i, j])
    
    Z = linkage(condensed_D, method='ward')
    
    # Chọn số cộng đồng tối ưu (đơn giản là 2 trong ví dụ này)
    # Trong thực tế, ta sẽ tính modularity hoặc chỉ số đánh giá khác
    k = 2
    labels = fcluster(Z, k, criterion='maxclust')
    
    # Chuyển kết quả về định dạng cộng đồng
    communities = {}
    for i, label in enumerate(labels):
        if label not in communities:
            communities[label] = []
        communities[label].append(nodes[i])
    
    return list(communities.values())

# Ví dụ sử dụng
G = nx.Graph()
G.add_edges_from([('A', 'B'), ('A', 'C'), ('A', 'E'), ('B', 'D'), ('B', 'F'),
                   ('C', 'E'), ('D', 'F'), ('E', 'F')])

communities = walktrap_community(G)

# Hiển thị kết quả
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(10, 6))

# Vẽ đồ thị với màu sắc theo cộng đồng
for i, community in enumerate(communities):
    nx.draw_networkx_nodes(G, pos, nodelist=community, 
                          node_color=f'C{i}', 
                          label=f'Community {i+1}')

nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos)

plt.title("Walktrap Communities")
plt.legend()
plt.axis('off')
plt.show()
```

---

## 8. So sánh với các thuật toán khác

### Ưu điểm
- **Phát hiện cộng đồng tự động**: Không cần biết trước số lượng cộng đồng.
- **Hiểu được cấu trúc phân cấp**: Cho phép phân tích cộng đồng ở nhiều mức độ.
- **Phù hợp với đồ thị không định hướng và có trọng số**.
- **Có nền tảng toán học vững chắc** dựa trên lý thuyết bước đi ngẫu nhiên.

### Nhược điểm
- **Yêu cầu tính toán cao** cho đồ thị lớn (do cần tính ma trận $P^t$).
- **Cần chọn tham số $t$** phù hợp (số bước đi).
- **Không hoạt động tốt với đồ thị có hướng**.

---

## 9. Tóm tắt

Thuật toán Walktrap là một phương pháp phát hiện cộng đồng tinh vi dựa trên ý tưởng:

1. **Các bước đi ngẫu nhiên có xu hướng ở lâu hơn trong cộng đồng**
2. **Sử dụng khoảng cách giữa xác suất bước đi ngẫu nhiên để đo lường độ tương đồng giữa các node**
3. **Áp dụng phân cụm phân cấp để tìm ra các cộng đồng**

Tham số quan trọng nhất là **độ dài bước đi $t$**, thường được chọn từ 3-7 tùy thuộc vào kích thước và cấu trúc đồ thị.

Thuật toán phù hợp với các đồ thị kích thước trung bình và đặc biệt hiệu quả khi cần hiểu cấu trúc phân cấp của cộng đồng.