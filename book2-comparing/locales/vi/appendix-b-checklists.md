# Phụ lục B Bảng kiểm: Cách nhận biết Khung kiểm soát của bạn giống Claude Code, Codex hay một Bản dựng thử nghiệm chưa hoàn thiện

Nếu bài so sánh không thể đúc kết thành các bảng kiểm, những gì còn lại thường chỉ là một tập hợp các kết luận nghe thì hay nhưng khó áp dụng. Phụ lục này nén các chương trước thành các câu hỏi mà một đội ngũ thực sự có thể cùng nhau thảo luận.

## B.1 Bảng kiểm mặt phẳng điều khiển (bất biến)

```
assert every instruction has {source, type, precedence}        # các phân đoạn có thể nhận diện được
assert prompt separates control plane from output style        # giọng điệu ≠ mệnh lệnh
assert local-rule scope (CLAUDE.md / AGENTS.md) explicitly labeled
assert team-rule changes land via diff                         # không phải thỏa thuận miệng
```

Nếu không thể trả lời được những điều này, mặt phẳng điều khiển vẫn đang ở mức "đủ tốt để sử dụng" chứ chưa đạt đến "đủ tốt để quản trị".

## B.2 Bảng kiểm tính liên tục (bất biến)

```
assert continuity sovereignty ∈ {main loop, thread+rollout+state}  # chọn một cái một cách rõ ràng
assert interrupt ⇒ tool_result closed (synthetic fallback counts)
assert long session has compact / truncation / recovery trio
assert thread.id / session indexing / persisted state = first-class concepts
```

Nếu các phiên làm việc dài vẫn dựa vào việc mô hình "tự nhớ", bạn không cần thực hiện phần còn lại của bài đánh giá này nữa.

## B.3 Bảng kiểm công cụ và phê duyệt (bất biến)

```
assert tool = schema-typed interface, additional_properties=false
assert approval policy independently evaluable (not buried in code if/else)
assert high-risk tools (Bash etc) get dedicated governance       # không đối xử cào bằng
assert {workdir, network, sandbox, approval} explicitly expressible
```

Nếu câu trả lời duy nhất chỉ là "chúng tôi cũng có kiểm soát phân quyền", thì hệ thống phân quyền đó thực chất vẫn chưa được thiết kế.

## B.4 Bảng kiểm quản trị cục bộ (bất biến)

```
assert local rules layerable by {directory, team, task type}
assert skill = reusable institutional slice, not long prompt    # có phiên bản / nguồn
assert hooks attach to explicit lifecycle events (pre/post/session_start/stop)
assert {skill, rule, hook} carry {version, source, trigger boundary}
```

## B.5 Bảng kiểm đa agent và xác minh (bất biến)

```
assert multi-agent's first purpose is responsibility split; parallelism is a bonus  # nếu không thì đó là sự hỗn loạn chạy song song
assert independent verifier exists (verifier ≠ implementer)
assert delegation = explicit tool or explicit state event, not runtime magic
assert child-agent {failure, timeout, cancel} ⇒ named cleanup owner
```

## B.6 Bạn ở gần loại hệ thống nào hơn?

Các dấu hiệu cho thấy bạn ở gần Claude Code hơn:

- bạn quan tâm nhất đến vòng lặp truy vấn (query loop), điều phối công cụ, các lệnh ngắt, rút gọn và khôi phục
- bạn giỏi trong việc nhanh chóng đưa các quy tắc vào phiên làm việc trực tiếp
- bạn chủ yếu quan tâm đến cách một agent tiếp tục chạy bên trong các tác vụ phức tạp

Các dấu hiệu cho thấy bạn ở gần Codex hơn:

- bạn quan tâm nhất đến các phân đoạn hướng dẫn (instruction fragments), lược đồ công cụ, chính sách phê duyệt, luồng / triển khai / trạng thái
- bạn giỏi trong việc biến các quy tắc cục bộ thành các tài sản có cấu trúc
- bạn chủ yếu quan tâm đến cách một agent được quản trị lâu dài bên trong một tổ chức

Các dấu hiệu cho thấy bạn ở gần một bản dựng thử nghiệm chưa hoàn thiện:

- bạn có thể đọc thuộc lòng thuật ngữ từ cả hai bên, nhưng không thể giải thích ai là người nắm giữ trật tự
- bạn có nhiều điểm bắt đầu cho các năng lực (capability entry points), nhưng không có lộ trình khôi phục rõ ràng
- bạn có nhiều văn bản quy tắc, nhưng không có phạm vi hoạt động hay thứ tự ưu tiên
- bạn có sự thực thi đa agent, nhưng không có sự phân chia trách nhiệm và không có cơ chế đóng

## B.7 Sáu câu hỏi cuối cùng

Nếu thời gian có hạn, chỉ cần hỏi sáu câu hỏi này:

- Ai nắm giữ quyền kiểm soát cuối cùng, mô hình hay khung kiểm soát?
- Tính liên tục tồn tại chủ yếu ở trong vòng lặp, hay trong luồng và trạng thái?
- Trước khi công cụ hành động, ai ngăn chặn bước đi nguy hiểm cuối cùng?
- Các quy tắc cục bộ đi vào hệ thống như thế nào, và chúng được phân lớp ra sao?
- Ai sở hữu khâu xác minh, và nó được giữ độc lập như thế nào?
- Sau khi có lỗi xảy ra, bằng chứng nào cho phép đội ngũ truy vết ngược lại lộ trình?

Một khi sáu câu hỏi này được đặt ra, "gia phả kiến trúc" của hệ thống thường sẽ tự bộc lộ.

## B.8 Tham chiếu nhanh về các Ngưỡng & Thứ tự

| Tên | Giá trị | Mục đích | Nguồn |
|---|---|---|---|
| `MAX_ENTRYPOINT_LINES` | 200 | giới hạn số dòng tệp điểm vào | Tập 1 ch5 / `memdir/memdir.ts` |
| `MAX_SECTION_LENGTH` | 2_000 | giới hạn mỗi phần của bộ nhớ phiên | `SessionMemory/prompts.ts` |
| `MAX_TOTAL_SESSION_MEMORY_TOKENS` | 12_000 | tổng ngân sách bộ nhớ phiên | `SessionMemory/prompts.ts` |
| `AUTOCOMPACT_BUFFER_TOKENS` | 13_000 | bộ đệm cảnh báo tự động rút gọn | `compact/autoCompact.ts` |
| `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES` | 3 | ngưỡng cầu dao | `compact/autoCompact.ts` |
| `yield_time_ms` | theo từng công cụ | số ms tối đa một lần thực thi có thể chặn | `local_tool.rs` |
| `wait_agent.timeout` | tối thiểu/mặc định/tối đa | cửa sổ chờ của agent con | `agent_tool.rs` |
| Giới hạn lệnh con Bash | ngầm định | số lệnh con gộp tối đa mỗi cuộc gọi | `bashPermissions.ts` |

Thứ tự sự kiện:

- session_start → user_prompt_submit → pre_tool_use → tool exec → post_tool_use → stop
- spawn_agent → send_input* → wait_agent → close_agent (cascades to descendants)
- PTL → collapse → reactive compact → if still PTL, surface error (no further loop)
