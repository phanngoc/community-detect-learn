# Thuật toán Label Propagation - Phát hiện cộng đồng trên đồ thị

**Label Propagation** là một thuật toán đơn giản và hiệu quả để phát hiện cộng đồng (community) trong đồ thị. Cơ chế hoạt động của nó là: **Các node nhận nhãn (label) từ các node lân cận của mình** — và cứ tiếp tục lan truyền cho đến khi nhãn ổn định.

---

## 1. Ý tưởng cơ bản

Thuật toán Label Propagation có ý tưởng đơn giản:

1. **Mỗi node ban đầu có một nhãn duy nhất**. (Có thể là chỉ số riêng biệt, ví dụ: 1, 2, 3, …)
2. **Mỗi node lan truyền nhãn** cho các node láng giềng của nó. Mỗi node sẽ **nhận nhãn phổ biến nhất** từ các node lân cận của nó.
3. **Lặp lại quá trình này** cho đến khi nhãn của các node không thay đổi nữa — tức là, các node đã ổn định.

---

## 2. Định nghĩa toán học

Cho một đồ thị $G = (V, E)$:
- $V$ là tập các đỉnh
- $E$ là tập các cạnh

Mỗi node $i \in V$ được gán một nhãn $L_i$.
Quá trình lan truyền được mô tả như sau:

$$
L_i^{(t+1)} = \arg \max_{l} \sum_{j \in N(i)} [L_j^{(t)} = l]
$$

Trong đó:
- $L_i^{(t)}$ là nhãn của node $i$ ở bước $t$
- $N(i)$ là tập các node láng giềng của node $i$
- $[L_j^{(t)} = l]$ là hàm chỉ báo, nhận giá trị 1 nếu $L_j^{(t)} = l$ và 0 nếu ngược lại
- $\arg \max_{l}$ lấy nhãn $l$ xuất hiện nhiều nhất

---

## 3. Thuật toán Label Propagation

Thuật toán được thực hiện qua các bước sau:

### Bước 1: Khởi tạo nhãn
- Mỗi node $i$ trong đồ thị $G = (V, E)$ được gán một nhãn ban đầu $L_i$, có thể là một giá trị duy nhất.
- Ví dụ: ban đầu, $L = [1, 2, 3, 4]$ cho các node $A, B, C, D$.

### Bước 2: Lan truyền nhãn
- Mỗi node sẽ chọn nhãn phổ biến nhất từ các node láng giềng của nó.
- Cụ thể: node $i$ sẽ nhận nhãn $L_i'$ sao cho $L_i'$ là nhãn xuất hiện **nhiều nhất** trong số các nhãn của các node láng giềng của $i$.
   
$$
L_i' = \arg \max \{ \text{Count}(L_j) \text{ for } j \in N(i) \}
$$

Trong đó:
- $N(i)$ là tập các node láng giềng của $i$.
- $L_j$ là nhãn của node $j$.
- **Count** là số lần xuất hiện của nhãn $L_j$ trong các láng giềng của node $i$.

### Bước 3: Lặp lại
- Thuật toán sẽ lặp lại Bước 2 cho đến khi nhãn của các node không thay đổi nữa, tức là thuật toán **ổn định**.

---

## 4. Đặc điểm của thuật toán

1. **Đơn giản và hiệu quả**: Thuật toán dễ hiểu, dễ triển khai và cho kết quả nhanh.
2. **Không đòi hỏi tham số trước**: Không cần biết trước số lượng cộng đồng.
3. **Không ổn định**: Kết quả có thể thay đổi giữa các lần chạy khác nhau do yếu tố ngẫu nhiên.
4. **Không tối ưu theo một metric cụ thể**: Khác với Louvain tối ưu modularity, Label Propagation không tối ưu theo một metric rõ ràng.

---

## 5. Ví dụ minh họa chi tiết

Xét đồ thị đơn giản gồm 4 node như sau:

```
A --- B
|     |
C --- D
```

### Khởi tạo nhãn ban đầu
- $L_A = 1$
- $L_B = 2$
- $L_C = 3$
- $L_D = 4$

### Vòng lặp 1: Lan truyền nhãn

#### Node A:
- Láng giềng: B và C, có nhãn 2 và 3
- Không có nhãn nào phổ biến hơn, chọn ngẫu nhiên, giả sử chọn 2
- $L_A' = 2$

#### Node B:
- Láng giềng: A và D, có nhãn 1 và 4
- Không có nhãn nào phổ biến hơn, chọn ngẫu nhiên, giả sử chọn 1
- $L_B' = 1$

#### Node C:
- Láng giềng: A và D, có nhãn 1 và 4
- Không có nhãn nào phổ biến hơn, chọn ngẫu nhiên, giả sử chọn 1
- $L_C' = 1$

#### Node D:
- Láng giềng: B và C, có nhãn 2 và 3
- Không có nhãn nào phổ biến hơn, chọn ngẫu nhiên, giả sử chọn 2
- $L_D' = 2$

Sau vòng lặp 1:
- $L_A' = 2$, $L_B' = 1$, $L_C' = 1$, $L_D' = 2$

### Vòng lặp 2: Lan truyền nhãn

#### Node A:
- Láng giềng: B và C, có nhãn 1 và 1
- Nhãn phổ biến nhất là 1
- $L_A' = 1$

#### Node B:
- Láng giềng: A và D, có nhãn 2 và 2
- Nhãn phổ biến nhất là 2
- $L_B' = 2$

#### Node C:
- Láng giềng: A và D, có nhãn 2 và 2
- Nhãn phổ biến nhất là 2
- $L_C' = 2$

#### Node D:
- Láng giềng: B và C, có nhãn 1 và 1
- Nhãn phổ biến nhất là 1
- $L_D' = 1$

Sau vòng lặp 2:
- $L_A' = 1$, $L_B' = 2$, $L_C' = 2$, $L_D' = 1$

### Vòng lặp 3: Lan truyền nhãn

#### Node A:
- Láng giềng: B và C, có nhãn 2 và 2
- Nhãn phổ biến nhất là 2
- $L_A' = 2$

#### Node B:
- Láng giềng: A và D, có nhãn 1 và 1
- Nhãn phổ biến nhất là 1
- $L_B' = 1$

(Tiếp tục với các node khác...)

Quá trình có thể tiếp tục qua vài vòng lặp nữa trước khi hội tụ hoặc bắt đầu dao động giữa các trạng thái.

### Xử lý dao động:
Để tránh dao động, một số triển khai sẽ:
1. Giới hạn số vòng lặp tối đa
2. Cập nhật không đồng bộ (các node được cập nhật theo thứ tự ngẫu nhiên)
3. Sử dụng các kỹ thuật phá vỡ đối xứng

### Kết quả cuối cùng

Sau khi thuật toán hội tụ (hoặc đạt số vòng lặp tối đa), các node có cùng nhãn được xem là thuộc cùng một cộng đồng.

---

## 6. Triển khai thực tế trong Python

```python
import networkx as nx
import random
import matplotlib.pyplot as plt

def label_propagation(G, max_iter=10):
    # Khởi tạo nhãn
    labels = {node: i for i, node in enumerate(G.nodes())}
    
    # Lặp qua các vòng lan truyền
    for _ in range(max_iter):
        # Tạo một bản sao của nhãn hiện tại
        old_labels = labels.copy()
        
        # Xáo trộn thứ tự các node để cập nhật ngẫu nhiên
        nodes = list(G.nodes())
        random.shuffle(nodes)
        
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
            max_count = max(label_counts.values())
            most_common_labels = [label for label, count in label_counts.items() if count == max_count]
            
            # Nếu có nhiều nhãn cùng phổ biến nhất, chọn ngẫu nhiên
            labels[node] = random.choice(most_common_labels)
            
        # Kiểm tra hội tụ
        if labels == old_labels:
            break
            
    # Chuyển đổi các nhãn thành id cộng đồng liên tục
    unique_labels = set(labels.values())
    label_to_community = {label: i for i, label in enumerate(unique_labels)}
    community_labels = {node: label_to_community[label] for node, label in labels.items()}
    
    return community_labels

# Ví dụ sử dụng
G = nx.karate_club_graph()
communities = label_propagation(G)

# Hiển thị kết quả
pos = nx.spring_layout(G)
plt.figure(figsize=(10, 8))
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_nodes(G, pos, node_color=list(communities.values()), 
                      cmap=plt.cm.rainbow, node_size=500)
nx.draw_networkx_labels(G, pos)
plt.title("Label Propagation Communities")
plt.axis('off')
plt.show()
```

---

## 7. Tóm tắt

Thuật toán Label Propagation là một thuật toán phát hiện cộng đồng đơn giản dựa trên quá trình lan truyền nhãn:

1. **Mỗi node bắt đầu với một nhãn duy nhất**
2. **Lặp lại**: mỗi node nhận nhãn phổ biến nhất từ các láng giềng
3. **Kết thúc**: khi nhãn ổn định hoặc đạt số vòng lặp tối đa
4. **Kết quả**: các node có cùng nhãn thuộc cùng một cộng đồng

Ưu điểm:
- Đơn giản, dễ hiểu
- Nhanh, có thể mở rộng với đồ thị lớn
- Không cần biết trước số lượng cộng đồng

Nhược điểm:
- Có thể không ổn định giữa các lần chạy
- Không đảm bảo tối ưu theo một metric cụ thể
- Có thể gặp vấn đề dao động và không hội tụ trong một số trường hợp