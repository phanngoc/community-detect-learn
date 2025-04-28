# Thuật toán Louvain - Phát hiện cộng đồng trên đồ thị

Thuật toán Louvain là một thuật toán phát hiện cộng đồng dựa trên việc **tối đa hóa modularity** - một chỉ số đo lường mức độ tốt của việc chia đồ thị thành các cộng đồng.

---

## 1. Bài toán đặt ra (Định nghĩa toán học)

Cho một **đồ thị** $G = (V, E)$ gồm:
- $V$: tập các đỉnh (nodes)
- $E$: tập các cạnh (edges)

Mục tiêu:
- Chia $V$ thành nhiều nhóm $C_1, C_2, ..., C_k$ (**communities**)
- Sao cho các đỉnh trong cùng 1 nhóm **kết nối nhiều** với nhau hơn so với các đỉnh ngoài nhóm đó.

### Để đo "tốt" hay "xấu" của việc phân nhóm, ta dùng một đại lượng gọi là **Modularity** $Q$.

---

## 2. Công thức Modularity $Q$

Công thức tổng quát:

$$
Q = \frac{1}{2m} \sum_{i,j} \left( A_{ij} - \frac{k_i k_j}{2m} \right) \delta(c_i, c_j)
$$

Giải thích từng phần:
- $A_{ij} = 1$ nếu có cạnh giữa đỉnh $i$ và đỉnh $j$, 0 nếu không.
- $k_i$ = tổng số cạnh nối đến node $i$ (degree của node $i$).
- $m$ = tổng số cạnh trong đồ thị: $m = \frac{1}{2} \sum_{i} k_i$.
- $c_i$ = community mà node $i$ thuộc về.
- $\delta(c_i, c_j) = 1$ nếu $i$ và $j$ cùng 1 cộng đồng, 0 nếu khác.

👉 Cốt lõi:
- $A_{ij}$ là thực tế: có kết nối hay không.
- $\frac{k_i k_j}{2m}$ là kỳ vọng: xác suất có kết nối nếu các cạnh được nối ngẫu nhiên.
- Nếu thực tế nhiều hơn kỳ vọng → node cùng community có kết nối chặt hơn random → **Tốt!**

---

## 3. Ý nghĩa trực quan

- Nếu $Q$ **lớn** (gần 1): chia nhóm rất tốt (nội bộ rất chặt, giữa nhóm rất lỏng).
- Nếu $Q$ gần 0 hoặc âm: chia nhóm không ý nghĩa (giống random).

Thông thường:
- $Q \in [0.3, 0.7]$ là tốt.
- $Q > 0.7$ cực kỳ chặt chẽ.

---

## 4. Thuật toán Louvain

Thuật toán Louvain hoạt động theo hai pha lặp đi lặp lại:

### Pha 1: Local Move
- Mỗi node bắt đầu là một community riêng.
- Với mỗi node $i$:
  - Xét di chuyển node $i$ sang community của một node lân cận $j$.
  - Nếu chuyển như vậy mà modularity $Q$ tăng, thì thực hiện chuyển.
  - Cứ tiếp tục cho đến khi không chuyển được nữa.

### Pha 2: Aggregation
- Gom các node cùng community thành **siêu-node** mới.
- Tạo một đồ thị mới nhỏ hơn.
- Quay lại Pha 1.

👉 Tiếp tục cho đến khi modularity **không thể tăng thêm**.

---

## 5. Công thức tính thay đổi modularity khi di chuyển 1 node

Khi xét node $i$ di chuyển vào một community $C$, thay đổi modularity $\Delta Q$ được tính nhanh như sau:

$$
\Delta Q = \left[ \frac{\sum_{in} + k_{i, in}}{2m} - \left( \frac{\sum_{tot} + k_i}{2m} \right)^2 \right] - \left[ \frac{\sum_{in}}{2m} - \left( \frac{\sum_{tot}}{2m} \right)^2 - \left( \frac{k_i}{2m} \right)^2 \right]
$$

Trong đó:
- $\sum_{in}$ = tổng trọng số các cạnh **nội bộ** trong community $C$ trước khi thêm $i$.
- $\sum_{tot}$ = tổng degree của các node trong community $C$ trước khi thêm $i$.
- $k_i$ = degree của node $i$.
- $k_{i, in}$ = tổng trọng số cạnh từ $i$ đến các node trong $C$.

👉 Nếu $\Delta Q > 0$, thì việc thêm node $i$ vào community $C$ sẽ tăng modularity.

---

## 6. Tóm lại bằng toán học

- **Input**: $G = (V, E)$
- **Mục tiêu**: Maximize $Q$
- **Lặp**:
  - Cố gắng di chuyển node để tăng $Q$ lớn nhất.
  - Gom cộng đồng lại → tạo đồ thị mới → lặp lại.
- **Kết thúc**: khi không thể tăng $Q$ thêm nữa.

---

## 7. Ví dụ minh họa thuật toán Louvain

Xét đồ thị 6 node như sau:

```
    A --- B
   /|     |\
  / |     | \
 C  |     |  D
  \ |     | /
   \|     |/
    E --- F
```

### Ban đầu: Mỗi node là một community

- Node A: community 1
- Node B: community 2
- Node C: community 3
- Node D: community 4
- Node E: community 5
- Node F: community 6

### Bước 1: Tính modularity ban đầu

Với mỗi node trong community riêng, modularity $Q = 0$ (không có cạnh nội bộ community)

### Bước 2: Pha 1 - Local Move

#### Xét node A:
- A kết nối với B, C, E
- Thử di chuyển A vào community của B:
  - $\Delta Q = \frac{1}{2m} > 0$ (tăng modularity)
  - A → community 2

#### Xét node C:
- C kết nối với A, E
- A đã thuộc community 2, E thuộc community 5
- Thử di chuyển C vào community 2 (của A):
  - $\Delta Q > 0$ (tăng modularity)
  - C → community 2

#### Tiếp tục với các node khác...

Sau Pha 1, giả sử ta có:
- Community 2: {A, B, C}
- Community 6: {D, E, F}

### Bước 3: Pha 2 - Aggregation

- Gom các node trong cùng community thành 2 siêu-node:
  - Siêu-node 1 = {A, B, C}
  - Siêu-node 2 = {D, E, F}

- Đồ thị mới sẽ có 2 siêu-node với cạnh giữa chúng.

### Bước 4: Lặp lại Pha 1 và Pha 2

- Xét di chuyển các siêu-node giữa các community
- Nếu modularity không tăng, kết thúc thuật toán

### Kết quả cuối cùng:

- Community 1: {A, B, C}
- Community 2: {D, E, F}

Modularity cuối cùng = 0.35 (giá trị ví dụ)

---

## 8. Triển khai thực tế

Để triển khai thuật toán Louvain trong Python:

```python
import networkx as nx
import community as community_louvain

# Tạo đồ thị
G = nx.Graph()
G.add_edges_from([(0, 1), (0, 2), (0, 4), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 5)])

# Áp dụng thuật toán Louvain
partition = community_louvain.best_partition(G)

# In kết quả
print("Các community phát hiện được:")
for node, community_id in partition.items():
    print(f"Node {node} thuộc community {community_id}")

# Tính modularity
modularity = community_louvain.modularity(partition, G)
print(f"Modularity: {modularity}")
```

Thuật toán Louvain cũng được triển khai trong nhiều thư viện phân tích đồ thị như NetworkX, igraph và các hệ thống cơ sở dữ liệu đồ thị như Neo4j.