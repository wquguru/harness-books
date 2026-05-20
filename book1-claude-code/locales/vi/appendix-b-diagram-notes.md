# Phụ lục B Sơ đồ: Vẽ khung xương Runtime

Các chương trước đã giải thích cấu trúc runtime bằng văn bản. Văn bản là cần thiết, nhưng một số cấu trúc sẽ trở nên rõ ràng hơn khi được thể hiện dưới dạng sơ đồ: Claude Code là một hệ thống máy trạng thái (state-machine) rõ ràng, chứ không phải "một đống prompt cộng với một vài công cụ".

## B.1 Sơ đồ 1: Mặt phẳng điều khiển toàn cục (global control plane) của Claude Code

![Claude Code global control plane](diagrams/diag-01-claude-code-control-plane.png)

Điều này không nên được vẽ dưới dạng lưu đồ đơn giản như sách thiếu nhi kiểu "user -> model -> tool -> output," bởi vì cách đó che giấu đi các cơ quan thực tế. Một góc nhìn chính xác hơn là phân chia thành năm lớp:

1. lớp tương tác người dùng (user interaction layer)
2. lớp mặt phẳng điều khiển (control plane layer)
3. lớp vòng lặp thực thi (execution loop layer)
4. lớp năng lực bên ngoài (external capability layer)
5. lớp bền vững và khả năng quan sát (persistence and observability layer)

Mục đích không phải là liệt kê mọi mô-đun. Điểm mấu chốt là:

- mô hình không nằm ở vị trí cao nhất cũng không phải thấp nhất
- mô hình là một giai đoạn bên trong vòng lặp truy vấn (query loop)
- các mặt phẳng điều khiển và khôi phục là thứ liên kết toàn bộ hệ thống lại với nhau

## B.2 Sơ đồ 2: Chu kỳ chính của vòng lặp truy vấn và các nhánh khôi phục

![Query loop main cycle](diagrams/diag-b02-01-query-loop-main.png)

![Query loop recovery branches](diagrams/diag-b02-02-query-loop-recovery-branches.png)

## B.3 Sơ đồ 3: Thứ tự phân nhóm công cụ (Tool batch ordering) và StreamingToolExecutor

![Tool batch ordering](diagrams/diag-b03-01-tool-batch-ordering.png)

![StreamingToolExecutor lifecycle](diagrams/diag-b03-02-streaming-tool-executor.png)

## B.4 Sơ đồ 4: Các nguồn ngữ cảnh và việc xây dựng lại rút gọn (compact rebuild)

![Context sources and budget](diagrams/diag-b04-01-context-sources-and-budget.png)

![Compact rebuild pipeline](diagrams/diag-b04-02-compact-rebuild-pipeline.png)

## B.5 Sơ đồ 5: Luồng Coordinator-worker và sự phân tách xác minh

![Coordinator and worker flow](diagrams/diag-b05-01-coordinator-worker-flow.png)

![Verification separation](diagrams/diag-b05-02-verification-separation.png)

## B.6 Sơ đồ 6: Bản đồ quản trị nhóm (Team governance map)

![Team governance map](diagrams/diag-06-team-governance-map.png)
