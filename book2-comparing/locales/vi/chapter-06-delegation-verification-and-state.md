# Chapter 6 Ủy thác (Delegation), Xác minh (Verification) và Trạng thái Bền vững (Persistent State): Ai Ngăn Hệ thống Tự Đánh giá Mình

## 6.1 Vấn đề thực sự trong các hệ thống đa Agent (multi-agent systems) là trách nhiệm

Khi nghe nói đến "đa Agent" (multi-agent) và vội vàng nghĩ đến hiệu quả thì cũng giống như nghe nói về một kế hoạch nhân sự — phần thực sự khó khăn chưa bao giờ là việc có nhiều Agent hơn, mà là cách phân chia trách nhiệm. Nếu một hệ thống tự thực thi, tóm tắt, xác minh và thản nhiên viết bài đánh giá của riêng mình, kết quả sẽ rất dễ chịu nhưng không đáng tin cậy: "làm tốt lắm." Claude Code tách biệt các khâu khám phá (explore), thực thi (execute), tổng hợp (synthesis) và xác minh (verification), đồng thời coi việc xác minh là một kỷ luật độc lập chứ không phải là một nét vẽ lịch thiệp ở phần kết — trạng thái "hoàn thành" không chỉ do duy nhất Agent thực thi tuyên bố. Codex cũng đi trên cùng một con đường: `tools/src/lib.rs` để lộ `create_spawn_agent_tool_v*`, `create_wait_agent_tool_v*`, `create_send_message_tool`, `create_close_agent_tool_v*` — ủy thác (delegation) là khả năng công cụ chính thức, không phải là phép thuật đen lúc chạy (runtime black magic).

## 6.2 Claude Code: Đa Agent phục vụ cho việc tách biệt trách nhiệm lúc chạy (runtime separation of responsibility)

Cơ chế này vẫn tập trung vào vòng lặp chính (main loop) và tiến trình nhiệm vụ: Agent chính không nên tự mình làm mọi thứ, và không được phép vừa triển khai vừa chứng nhận. Đa Agent xử lý việc khám phá được thuê ngoài (outsourced exploration), phân chia triển khai, tổng hợp và xác minh độc lập. Điều đó phù hợp với thế mạnh trong điều phối lúc chạy (runtime orchestration) — đa Agent đi vào khuôn khổ quản trị của việc "nhiệm vụ hiện tại tiến triển như thế nào," thay vì một nền tảng Agent vĩ đại để đưa các nhiệm vụ vào.

## 6.3 Codex: Đa Agent phục vụ cho sự cộng tác rõ ràng thông qua công cụ (tool-mediated collaboration)

Ủy thác được định nghĩa là giao diện công cụ (tool interface), đẩy đa Agent hướng tới một phân hệ chính thức (formal subsystem). Hai hiệu ứng: ủy thác trở nên dễ ghi lại, kiểm toán và kết hợp hơn vì đó là một lượt gọi công cụ rõ ràng, không phải là sự điều động ẩn lúc chạy; sự cộng tác liên kết với các luồng (threads), trạng thái và hệ thống phê duyệt, kế thừa cơ sở hạ tầng hạng nhất (first-class infrastructure) mà Codex đã xây dựng. Trong `agent_tool.rs`, `spawn_agent`, `send_input`, `wait_agent` và `close_agent` đều có cấu trúc (schemas) riêng: `send_input` phân biệt giữa `interrupt=true` với phân phối xếp hàng (queued delivery) mặc định; `wait_agent` được tham số hóa với thời gian chờ mặc định/tối thiểu/tối đa (default/min/max timeouts); `close_agent` đóng rõ ràng các con cháu (descendants) đang mở. Codex biến quyền ưu tiên (preemption), chờ đợi và dọn dẹp thành các trường giao thức — một nền tảng vững chắc cho khả năng của nền tảng, không phải lúc nào cũng nhanh nhẹn nhưng bền vững.

## 6.4 Trạng thái bền vững (Persistent state) ngăn xác minh trở thành thủ tục nghi lễ

Việc xác minh trở thành nghi lễ chủ yếu là do việc bàn giao trạng thái (state handoff) bị yếu. Những gì đã được thực hiện, tại sao, công cụ nào, tệp nào — nếu điều đó chỉ nằm trong đầu của Agent thực thi, thì việc xác minh sẽ trở thành một màn kịch trông có vẻ nghiêm túc nhưng không có chất liệu thực tế. Claude Code giữ cho trạng thái phiên (session state), kết quả công cụ và các nhánh phục hồi liên tục hiển thị bên trong runtime, sau đó kết hợp tính liên tục đó với một kỷ luật xác minh độc lập. Codex cung cấp chất liệu rõ ràng thông qua luồng (thread), đợt triển khai (rollout), lịch sử tin nhắn và cầu nối cơ sở dữ liệu trạng thái (state DB bridge) — một hệ thống có nhận thức về lưu trữ phiên (session-archive awareness) đơn giản là trả lời tốt hơn cho câu hỏi "chính xác thì điều gì đã xảy ra vừa rồi." Cả hai không mâu thuẫn với nhau: Claude Code sửa chữa cho những Agent thực thi quá đắm chìm vào bối cảnh; Codex sửa chữa cho sự cộng tác bắt buộc phải để lại bằng chứng có cấu trúc.

## 6.5 Thái độ khác nhau đối với sự phục hồi (recovery) và đóng lại (closure)

Claude Code quan tâm sâu sắc đến việc dọn dẹp nhiệm vụ, sự lan truyền hủy bỏ giữa cha-con (parent-child abort propagation) và các hook vòng đời của Agent phụ (subagent lifecycle hooks) — trong thế giới của nó, công việc đa Agent trước hết là một hiện tượng runtime trực tiếp phải đóng lại nhanh chóng khi bối cảnh xảy ra sự cố. Codex nghiêng theo hướng ngược lại, đưa vòng đời Agent vào sự quản lý trạng thái và giao thức gọi (invocation protocol) rõ ràng: nó không chỉ quan tâm đến việc Agent phụ có chết hay không, mà còn quan tâm đến việc hành động ủy thác đó sẽ tồn tại như thế nào dưới dạng sự kiện hệ thống. Một bên giống như một người quản đốc công trường lo lắng về các lỗ hổng bị bỏ lại phía sau; bên kia giống như một nhà tổ chức có cơ sở hạ tầng dự án lo lắng về việc liệu mọi hành động cộng tác có được ghi nhận hay không.

### Skeleton: Giao thức ủy thác của Codex

```
// bộ khung (skeleton): agent_tool.rs spawn/wait/send/close
handle = spawn_agent { role, prompt, timeout, inherit_approval }
for msg in updates:
    send_input(handle, msg, interrupt ∈ {true, false})  // true=chiếm trước (preempt), false=xếp hàng (queue)
result = wait_agent(handle, timeout ∈ [min, default, max])
close_agent(handle, cascade=true)                        // cũng đóng cả các con cháu (descendants) đang mở
```

### Ma trận lỗi mồ côi (orphan) và thời gian chờ (timeout)

| Thứ tự sự kiện | Trạng thái trước | Tác nhân kích hoạt | Bước tiếp theo | Ngưỡng |
|---|---|---|---|---|
| hủy bỏ từ cha (parent abort) | con đang chạy (child in flight) | parent.abort | lan truyền hủy bỏ (cascade abort) tới handle; ghi lại sự kiện rollout | — |
| `wait_agent` timeout | con chưa phản hồi (child unreturned) | timeout ≥ max | đóng handle, trả về kết quả thời gian chờ | `wait_agent.max` |
| `send_input(interrupt=true)` | con đang xếp hàng (child queued) | chiếm trước (preemption) | bỏ hàng đợi, tiêm đầu vào mới | — |
| `close_agent` | các con cháu đang mở (open descendants) | đóng rõ ràng | đóng lan truyền (cascade-close) tất cả con cháu | `cascade=true` |
| crash ở con (child crash) | — | thoát bất thường | trả về lỗi, giữ bản ghi luồng | — |
| rò rỉ handle (handle leak) | nhiệm vụ kết thúc không đóng | hoàn tất (finalize) | bắt buộc đóng + trục xuất (evict) | không còn handle treo (no dangling handles) |

## 6.6 Kết luận chương

Kết luận không khó để nêu ra:

> Thiết kế đa Agent (multi-agent) của Claude Code nhấn mạnh vào sự tách biệt trách nhiệm lúc chạy và đóng lại tại thực địa, trong khi thiết kế đa Agent của Codex nhấn mạnh vào ủy thác thông qua công cụ, bàn giao trạng thái và cộng tác có thể kiểm toán.

Cả hai đều đang cố gắng ngăn hệ thống tự chấm điểm cao cho chính mình.

Claude Code dựa nhiều hơn vào sự tách biệt vai trò và kỷ luật xác minh.

Codex dựa nhiều hơn vào các giao diện rõ ràng, trạng thái luồng và hồ sơ cộng tác.

Chương cuối cùng nén sáu chương trước đó thành một đánh giá tổng thể duy nhất và trả lời trực tiếp câu hỏi ở tiêu đề của cuốn sách: hội tụ qua những con đường khác nhau, hay thực sự là những loài khác biệt?
