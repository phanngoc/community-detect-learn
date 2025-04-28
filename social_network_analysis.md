# Phân Tích Mạng Xã Hội (Social Network Analysis)

Phân tích mạng xã hội (Social Network Analysis - SNA) là ứng dụng của lý thuyết đồ thị vào việc nghiên cứu và phân tích các mối quan hệ xã hội. Trong phần này, chúng ta sẽ tìm hiểu cách áp dụng các khái niệm đồ thị để hiểu và phân tích các mạng xã hội.

## 1. Mạng Xã Hội Dưới Góc Nhìn Đồ Thị

### 1.1. Mô hình hóa mạng xã hội bằng đồ thị

Trong mạng xã hội:
- **Đỉnh** (Nodes): đại diện cho các thực thể (người dùng, tổ chức, trang web, v.v.)
- **Cạnh** (Edges): đại diện cho các mối quan hệ giữa các thực thể (bạn bè, theo dõi, tương tác, v.v.)
- **Trọng số cạnh**: có thể đại diện cho độ mạnh của mối quan hệ (số lần tương tác, mức độ thân thiết, v.v.)

### 1.2. Các loại mạng xã hội

#### Mạng không có hướng
- Các mối quan hệ có tính đối xứng
- Ví dụ: mạng lưới bạn bè Facebook (nếu A là bạn của B thì B cũng là bạn của A)

#### Mạng có hướng
- Các mối quan hệ không nhất thiết phải đối xứng
- Ví dụ: mạng lưới theo dõi Twitter (A có thể theo dõi B mà B không theo dõi lại A)

#### Mạng hai phía (Bipartite)
- Mạng có hai loại đỉnh khác nhau, các cạnh chỉ kết nối giữa các đỉnh thuộc hai loại khác nhau
- Ví dụ: mạng người dùng - sản phẩm (đỉnh đại diện cho người dùng hoặc sản phẩm, cạnh là mối quan hệ mua/đánh giá)

## 2. Các Đặc Trưng của Mạng Xã Hội

### 2.1. Hiện tượng thế giới nhỏ (Small-World Phenomenon)

Hiện tượng "sáu độ tách biệt" (six degrees of separation) cho rằng bất kỳ hai người nào trên thế giới cũng có thể kết nối với nhau thông qua không quá 6 mối quan hệ trung gian.

**Đặc điểm của mạng thế giới nhỏ**:
- **Đường kính mạng** (network diameter) nhỏ: khoảng cách trung bình giữa hai đỉnh bất kỳ tương đối nhỏ
- **Hệ số phân cụm** (clustering coefficient) cao: thể hiện xu hướng các đỉnh tạo thành các nhóm có kết nối mật thiết

### 2.2. Phân phối bậc luật lũy thừa (Power Law Degree Distribution)

Trong nhiều mạng xã hội thực tế, phân phối bậc của các đỉnh tuân theo luật lũy thừa:

$$P(k) \propto k^{-\gamma}$$

Trong đó:
- $P(k)$ là xác suất một đỉnh có bậc $k$
- $\gamma$ là hằng số (thường nằm trong khoảng từ 2 đến 3)

Mạng có phân phối bậc theo luật lũy thừa được gọi là **mạng phi tỷ lệ** (scale-free network) với đặc điểm:
- Một số ít đỉnh có rất nhiều kết nối (**hub**)
- Phần lớn đỉnh có ít kết nối

### 2.3. Hiệu ứng ưu tiên gắn kết (Preferential Attachment)

Hiệu ứng "giàu càng giàu" (rich-get-richer): các đỉnh mới có xu hướng kết nối với các đỉnh đã có nhiều kết nối.

Mô hình Barabási-Albert mô tả quá trình phát triển mạng phi tỷ lệ:
1. Bắt đầu với một mạng nhỏ ban đầu
2. Thêm các đỉnh mới, mỗi đỉnh kết nối với $m$ đỉnh hiện có
3. Xác suất một đỉnh mới kết nối với đỉnh $i$ tỷ lệ thuận với bậc của đỉnh $i$:
   $$P(i) = \frac{k_i}{\sum_j k_j}$$

## 3. Phát Hiện Cộng Đồng trong Mạng Xã Hội

### 3.1. Cộng đồng trong mạng xã hội

**Cộng đồng** trong mạng xã hội là một nhóm các đỉnh có kết nối nội bộ mật thiết hơn so với kết nối với các đỉnh bên ngoài.

Đặc điểm của cộng đồng trong mạng xã hội:
- Mật độ cạnh cao trong cùng cộng đồng
- Mật độ cạnh thấp giữa các cộng đồng
- Thường có các đặc điểm chung (sở thích, vị trí địa lý, nghề nghiệp, v.v.)

### 3.2. Modularity trong mạng xã hội

**Modularity** đo lường chất lượng của việc phân chia mạng thành các cộng đồng. Trong mạng xã hội, modularity cao thể hiện cấu trúc cộng đồng rõ ràng.

Modularity của một phân vùng cộng đồng trong mạng xã hội:

$$Q = \frac{1}{2m} \sum_{i,j} \left[ A_{ij} - \frac{k_i k_j}{2m} \right] \delta(c_i, c_j)$$

Ý nghĩa trong mạng xã hội:
- $A_{ij}$ thể hiện sự tồn tại của mối quan hệ giữa hai người dùng
- $\frac{k_i k_j}{2m}$ là xác suất hai người dùng có mối quan hệ nếu các mối quan hệ được phân bố ngẫu nhiên
- Giá trị Q cao chỉ ra rằng các mối quan hệ trong cộng đồng nhiều hơn so với kỳ vọng trong một mạng ngẫu nhiên

### 3.3. Các thuật toán phát hiện cộng đồng trong mạng xã hội

#### 3.3.1. Thuật toán Girvan-Newman

Thích hợp cho các mạng xã hội khi:
- Các cộng đồng được kết nối bởi một số ít người "cầu nối"
- Cần hiểu cấu trúc phân cấp của cộng đồng

#### 3.3.2. Thuật toán Louvain

Thích hợp cho các mạng xã hội khi:
- Mạng có quy mô lớn (hàng triệu người dùng)
- Cần phương pháp hiệu quả và nhanh chóng

#### 3.3.3. Label Propagation

Thích hợp cho các mạng xã hội khi:
- Mạng có quy mô cực lớn
- Tốc độ quan trọng hơn độ chính xác
- Cần giải pháp đơn giản, dễ hiểu

## 4. Các Độ Đo Trung Tâm trong Phân Tích Mạng Xã Hội

Trong phân tích mạng xã hội, các độ đo trung tâm giúp xác định các "người dùng có ảnh hưởng" và các vị trí chiến lược.

### 4.1. Degree Centrality - Người có nhiều kết nối

Trong mạng xã hội, người dùng có Degree Centrality cao là:
- **Người nổi tiếng** (nhiều người kết nối)
- **Người kết nối** (có nhiều mối quan hệ xã hội)
- Thường là người tiếp cận thông tin nhanh nhất

**Hạn chế**: chỉ xem xét kết nối trực tiếp, không đánh giá được vị trí chiến lược

### 4.2. Betweenness Centrality - Người cầu nối

Trong mạng xã hội, người dùng có Betweenness Centrality cao:
- **Người môi giới thông tin** giữa các nhóm khác nhau
- **Cầu nối** giữa các cộng đồng
- Có vai trò quan trọng trong việc lan truyền thông tin và ảnh hưởng

Ví dụ thực tế: người kết nối các nhóm nghề nghiệp, văn hóa khác nhau trong mạng xã hội LinkedIn

### 4.3. Closeness Centrality - Người tiếp cận nhanh

Trong mạng xã hội, người dùng có Closeness Centrality cao:
- Có thể tiếp cận nhanh đến nhiều người dùng khác
- Có thể lan truyền thông tin nhanh chóng
- Thường nằm ở vị trí trung tâm về mặt cấu trúc

Ứng dụng: xác định người dùng hữu ích để lan truyền thông tin nhanh chóng

### 4.4. Eigenvector Centrality & PageRank - Người có ảnh hưởng

Trong mạng xã hội, người dùng có Eigenvector Centrality/PageRank cao:
- Kết nối với những người có ảnh hưởng khác
- Có sức ảnh hưởng lớn nhờ vị thế trong mạng lưới
- Quan trọng trong chiến lược marketing ảnh hưởng (influencer marketing)

**PageRank**: biến thể của Eigenvector Centrality, được Google sử dụng để đánh giá tầm quan trọng của các trang web, nay được áp dụng rộng rãi trong SNA

## 5. Ví dụ Phân Tích Facebook Network

### 5.1. Thu thập dữ liệu

```python
import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
import numpy as np

# Giả lập dữ liệu Facebook (trong thực tế, dữ liệu này sẽ được thu thập từ Facebook Graph API)
def create_facebook_network_sample():
    G = nx.Graph()
    
    # Thêm các đỉnh đại diện cho người dùng
    for i in range(1, 31):
        G.add_node(i, name=f"User {i}")
    
    # Tạo một số cộng đồng
    # Cộng đồng 1: User 1-10
    for i in range(1, 10):
        for j in range(i+1, 11):
            if np.random.rand() < 0.7:  # 70% xác suất tạo kết nối trong cộng đồng
                G.add_edge(i, j)
    
    # Cộng đồng 2: User 11-20
    for i in range(11, 20):
        for j in range(i+1, 21):
            if np.random.rand() < 0.7:
                G.add_edge(i, j)
    
    # Cộng đồng 3: User 21-30
    for i in range(21, 30):
        for j in range(i+1, 31):
            if np.random.rand() < 0.7:
                G.add_edge(i, j)
    
    # Thêm một số kết nối giữa các cộng đồng
    for _ in range(15):
        community1 = np.random.randint(1, 11)
        community2 = np.random.randint(11, 21)
        G.add_edge(community1, community2)
    
    for _ in range(15):
        community2 = np.random.randint(11, 21)
        community3 = np.random.randint(21, 31)
        G.add_edge(community2, community3)
    
    for _ in range(5):
        community1 = np.random.randint(1, 11)
        community3 = np.random.randint(21, 31)
        G.add_edge(community1, community3)
    
    return G

# Tạo mạng xã hội mẫu
facebook_network = create_facebook_network_sample()
```

### 5.2. Phân tích cơ bản

```python
# Thống kê cơ bản
def analyze_basic_metrics(G):
    print(f"Số lượng người dùng: {G.number_of_nodes()}")
    print(f"Số lượng kết nối bạn bè: {G.number_of_edges()}")
    print(f"Mật độ mạng: {nx.density(G):.4f}")
    
    degrees = [d for n, d in G.degree()]
    print(f"Số bạn bè trung bình: {np.mean(degrees):.2f}")
    print(f"Số bạn bè trung vị: {np.median(degrees)}")
    print(f"Số bạn bè lớn nhất: {max(degrees)}")
    print(f"Số bạn bè nhỏ nhất: {min(degrees)}")
    
    if nx.is_connected(G):
        print("Mạng liên thông!")
        print(f"Đường kính mạng: {nx.diameter(G)}")
        print(f"Độ dài đường đi trung bình: {nx.average_shortest_path_length(G):.2f}")
    else:
        print("Mạng không liên thông!")
        components = list(nx.connected_components(G))
        print(f"Số lượng thành phần liên thông: {len(components)}")
        largest_cc = max(components, key=len)
        print(f"Kích thước thành phần liên thông lớn nhất: {len(largest_cc)}")

    print(f"Hệ số phân cụm trung bình: {nx.average_clustering(G):.4f}")

analyze_basic_metrics(facebook_network)
```

### 5.3. Phát hiện cộng đồng

```python
def analyze_communities(G):
    # Sử dụng thuật toán Louvain
    partition = community_louvain.best_partition(G)
    
    # Số lượng cộng đồng
    num_communities = len(set(partition.values()))
    print(f"Số lượng cộng đồng phát hiện được: {num_communities}")
    
    # Kích thước các cộng đồng
    community_sizes = {}
    for community_id in set(partition.values()):
        size = list(partition.values()).count(community_id)
        community_sizes[community_id] = size
    
    print("Kích thước các cộng đồng:")
    for community_id, size in community_sizes.items():
        print(f"Cộng đồng {community_id}: {size} người dùng")
    
    # Modularity
    modularity = community_louvain.modularity(partition, G)
    print(f"Modularity: {modularity:.4f}")
    
    return partition

partition = analyze_communities(facebook_network)
```

### 5.4. Tìm người dùng có ảnh hưởng

```python
def find_influential_users(G):
    print("Top 5 người dùng theo Degree Centrality:")
    degree_centrality = nx.degree_centrality(G)
    sorted_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    for user, score in sorted_degree:
        print(f"User {user}: {score:.4f}")
    
    print("\nTop 5 người dùng theo Betweenness Centrality:")
    betweenness_centrality = nx.betweenness_centrality(G)
    sorted_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    for user, score in sorted_betweenness:
        print(f"User {user}: {score:.4f}")
    
    print("\nTop 5 người dùng theo Eigenvector Centrality:")
    eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)
    sorted_eigenvector = sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    for user, score in sorted_eigenvector:
        print(f"User {user}: {score:.4f}")

find_influential_users(facebook_network)
```

### 5.5. Biểu diễn trực quan

```python
def visualize_network(G, partition=None):
    plt.figure(figsize=(12, 12))
    
    # Vẽ đồ thị với các cộng đồng được tô màu
    if partition is not None:
        # Màu sắc dựa trên cộng đồng
        cmap = plt.cm.rainbow
        colors = [partition[node] for node in G.nodes()]
        
        # Vẽ đồ thị
        pos = nx.spring_layout(G, seed=42)  # Sử dụng thuật toán spring layout
        nx.draw_networkx_nodes(G, pos, node_size=100, node_color=colors, cmap=cmap)
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        
        plt.title("Facebook Network - Communities")
    else:
        # Vẽ đồ thị không tô màu cộng đồng
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_size=100, node_color='skyblue', 
                font_size=8, width=0.5, alpha=0.8)
        
        plt.title("Facebook Network")
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Biểu diễn mạng với cộng đồng
visualize_network(facebook_network, partition)
```

## 6. Các Ứng Dụng Thực Tế của SNA

### 6.1. Marketing và quảng cáo

- **Tiếp thị viral**: Xác định "người có ảnh hưởng" để tối đa hóa phạm vi tiếp cận
- **Tiếp thị theo phân khúc**: Nhắm mục tiêu đến các cộng đồng cụ thể
- **Marketing truyền miệng**: Tận dụng các mối quan hệ xã hội để lan truyền thông điệp

### 6.2. Phát hiện gian lận và an ninh mạng

- Phát hiện các mạng lưới gian lận dựa trên các mẫu kết nối bất thường
- Xác định các tài khoản bot trong mạng xã hội
- Phân tích mạng lưới tấn công và phát tán phần mềm độc hại

### 6.3. Dịch tễ học và sức khỏe cộng đồng

- Mô hình hóa sự lây lan của dịch bệnh thông qua mạng lưới xã hội
- Xác định "siêu lan truyền" (super-spreaders) trong đại dịch
- Thiết kế chiến lược tiêm chủng hiệu quả

### 6.4. Phân tích tổ chức và doanh nghiệp

- Tối ưu hóa cấu trúc tổ chức
- Phân tích mạng lưới giao tiếp nội bộ
- Xác định các "cầu nối" quan trọng trong tổ chức

## 7. Thách Thức và Hướng Phát Triển

### 7.1. Thách thức trong SNA

- **Quy mô**: Phân tích mạng xã hội với hàng tỷ người dùng và kết nối
- **Tính động**: Mạng xã hội liên tục thay đổi theo thời gian
- **Riêng tư**: Cân bằng giữa phân tích sâu và bảo vệ dữ liệu cá nhân

### 7.2. Xu hướng phát triển

- **SNA kết hợp với học máy**: Sử dụng neural networks để phân tích mạng xã hội
- **Phân tích mạng đa chiều**: Xem xét nhiều loại quan hệ đồng thời
- **Phân tích mạng động**: Theo dõi và dự đoán sự phát triển của mạng theo thời gian

## 8. Kết Luận

Phân tích mạng xã hội là ứng dụng mạnh mẽ của lý thuyết đồ thị, giúp chúng ta hiểu sâu hơn về cấu trúc và động lực của các mối quan hệ xã hội. Thông qua việc áp dụng các thuật toán phát hiện cộng đồng và phân tích độ đo trung tâm, SNA cung cấp những hiểu biết giá trị về hành vi con người, các xu hướng xã hội, và cách thức lan truyền thông tin.

Trong kỷ nguyên dữ liệu lớn và mạng xã hội trực tuyến, SNA trở nên ngày càng quan trọng cho các lĩnh vực từ marketing đến sức khỏe cộng đồng, an ninh mạng và nhiều lĩnh vực khác.

---

## Bài Tiếp Theo

Trong bài tiếp theo, chúng ta sẽ tìm hiểu về [Thực hành với NetworkX](networkx_tutorial.md), công cụ Python phổ biến để phân tích và biểu diễn đồ thị, giúp triển khai các phương pháp phân tích mạng xã hội một cách thực tế.