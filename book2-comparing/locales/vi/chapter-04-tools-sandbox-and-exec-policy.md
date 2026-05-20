# Chương 4 Công cụ, Hộp cát và Ngôn ngữ Chính sách: Ai Ngăn chặn Mô hình Hành động Quá nhanh

![Tool Governance Comparison](diagrams/diag-03-tool-governance-comparison.png)

## 4.1 Khoảnh khắc thực sự nguy hiểm là lúc bắt đầu thực thi

Một mô hình nói sai chỉ gây lãng phí thời gian; nhưng chạy sai một câu lệnh có thể kéo theo sự sụp đổ của thư mục, kho lưu trữ, các tiến trình và toàn bộ quy trình làm việc. Điều phân biệt các hệ thống lập trình AI là ai sở hữu quyền giải thích cuối cùng trước khi một công cụ hành động. Cả Claude Code và Codex đều coi trọng điều này theo những cách khác nhau. Claude Code đưa các công cụ vào kỷ luật lập lịch runtime — `toolOrchestration.ts`, `toolExecution.ts`, `StreamingToolExecutor.ts`, `useCanUseTool.tsx`, các prompt đặc thù cho Bash, ngữ nghĩa `allow/deny/ask` rõ ràng — quyết định xem một cuộc gọi công cụ có thể chạy hay không, chạy thế nào, có đồng thời hay không, liệu người dùng có từ chối hay không, làm thế nào để ngắt và cách kết quả trả về ngữ cảnh. Codex trước tiên biến các công cụ thành các giao diện được định kiểu (typed interfaces) — `tools/src/lib.rs` xuất ra các hàm khởi tạo công cụ, `local_tool.rs` định nghĩa lược đồ (schemas) cho `exec_command`, `shell`, `shell_command`, `request_permissions`. Các công cụ trong Codex trước hết là một API chuẩn hóa, và chỉ đóng vai trò là một đơn vị thực thi ở khía cạnh thứ hai.

## 4.2 Claude Code: điều phối runtime và các ràng buộc hành động nguy hiểm

Hệ thống công cụ mang lại cảm giác điều phối hiện trường mạnh mẽ: tính đồng thời phụ thuộc vào lược đồ và `isConcurrencySafe()`, sửa đổi ngữ cảnh bảo toàn thứ tự phát lại, thực thi truyền phát phải xử lý các ngắt, kết quả tổng hợp và phản hồi giao diện người dùng (UI feedback). Việc gọi công cụ được đối xử như một quy trình có hệ quả, chứ không phải là một hành động đơn điểm đơn lẻ — khung kiểm soát giống như một giám sát viên công trường đi kèm với mô hình, theo dõi công cụ nào chạy trước, công cụ nào có thể chạy song song, công cụ nào phải tuần tự hóa, cách kết quả được ghi nhận và điều gì xảy ra khi công việc bị dừng lại giữa chừng. Bash được đối xử với sự rõ ràng gần như ám ảnh — các hệ thống trưởng thành thường rất kỹ tính xung quanh giao diện nguy hiểm nhất này.

## 4.3 Codex: lược đồ công cụ, các tham số phê duyệt và một công cụ chính sách (policy engine)

Codex thể hiện sự kiểm soát đối với các hành động rủi ro dưới dạng các ràng buộc giao diện chính thức. Trong `local_tool.rs`, `exec_command` sở hữu rõ ràng các trường dữ liệu — `cmd`, `workdir`, `shell`, `tty`, `yield_time_ms`, `max_output_tokens`, `login`, các tham số liên quan đến phê duyệt — thay vì chấp nhận một lệnh dạng chuỗi đơn lẻ. Các mô tả về `shell` / `shell_command` yêu cầu `workdir` và cảnh báo chống lại việc sử dụng `cd` cẩu thả. Cách sử dụng đúng được mã hóa ngay trong định nghĩa công cụ. Phê duyệt và leo thang (escalation) là các tham số rõ ràng, `request_permissions` là một công cụ riêng biệt và `execpolicy` là một crate riêng — `Policy`, `Rule`, `Evaluation`, `Decision`, trình phân tích cú pháp (parser) — các ranh giới thực thi đã trở thành một ngôn ngữ chính sách nhỏ thay vì một vài kiểm tra `if / else`. Và đó không phải là lý thuyết suông: các lược đồ đánh dấu các trường bắt buộc và vô hiệu hóa các thuộc tính đi lạc thông qua `additional_properties = false`; `execpolicy/src/lib.rs` xuất ra trình phân tích cú pháp, `PolicyParser`, cùng với các hàm bổ trợ như `blocking_append_allow_prefix_rule` and `blocking_append_network_rule`. Codex đánh giá chính sách và cũng sửa đổi nó theo những cách có cấu trúc.

## 4.4 Phê duyệt runtime so với ngôn ngữ chính sách

Claude Code nghiêng về chuỗi phê duyệt runtime; Codex nghiêng về ngôn ngữ chính sách rõ ràng và các phê duyệt được tham số hóa. Cơ chế `ask/allow/deny` của Claude Code được liên kết chặt chẽ với nơi gọi (call site), quyết định dựa trên ngữ cảnh, loại công cụ, hành động của người dùng và trạng thái phiên làm việc — nhạy bén, nhưng các quy tắc vẫn bị chôn vùi trong logic runtime. Chính sách thực thi (exec-policy) của Codex kéo các quy tắc ra ngoài thành các thực thể có thể phân tích cú pháp và đánh giá riêng biệt — dễ đọc và dễ di chuyển hơn, phù hợp tự nhiên với quản trị nhóm; cái giá phải trả là sức nặng và công việc thiết kế thực tế liên tục. Nói một cách thẳng thắn: giống như một quản lý ca trực đưa ra quyết định tại hiện trường so với một công ty viết chính sách trước rồi mới kiểm tra tính tuân thủ sau.

### Khung xương: hai chốt chặn rủi ro

```
// khung xương: phê duyệt runtime của Claude Code (nguồn: src/hooks/useCanUseTool.tsx, StreamingToolExecutor.ts)
decision = hasPermissionsToUseTool(tool, input, ctx)  // allow | deny | ask
match decision:
    allow: schedule_with_concurrency_check(tool)       // isConcurrencySafe()
    deny:  reject(reason)                              // sticky
    ask:   route_to(coordinator | swarm | interactive)
interrupt_semantics = tool.interruptBehavior ∈ {cancel, block}

// khung xương: đánh giá exec-policy của Codex (nguồn: execpolicy/src/lib.rs, local_tool.rs)
policy = PolicyParser.parse(source)
for rule in policy.rules:
    eval = rule.evaluate(exec_command { cmd, workdir, shell, tty,
                                         yield_time_ms, max_output_tokens, login })
    if eval.matches: return Decision::{Allow | Deny | RequestPermissions}
return Decision::default
```

### Cây quyết định phê duyệt

```
tool_call
  ├─ xác thực lược đồ thất bại   → deny (additional_properties=false ngăn chặn tham số đi lạc)
  ├─ khớp quy tắc từ chối (tiền tố) → deny
  ├─ khớp quy tắc yêu cầu (mạng/leo thang) → request_permissions (công cụ rõ ràng)
  ├─ không khớp + hộp cát nới lỏng → allow (bị giới hạn bởi workdir / chế độ hộp cát)
  └─ không khớp + hộp cát nghiêm ngặt → ask
```

### Ngưỡng thời gian chờ (Timeout) và các tham số

| Tên | Mục đích | Nguồn |
|---|---|---|
| `yield_time_ms` | số ms tối đa một lần thực thi có thể chặn | `local_tool.rs (exec_command)` |
| `max_output_tokens` | giới hạn đầu ra công cụ được đưa vào ngữ cảnh | `local_tool.rs` |
| `additional_properties=false` | ngăn chặn mô hình tiêm các tham số đi lạc | `local_tool.rs (schema)` |
| Giới hạn lệnh con Bash | số lệnh con gộp tối đa cho mỗi cuộc gọi Bash | `bashPermissions.ts` |

## 4.5 Hộp cát (Sandbox) và phê duyệt định hình sản phẩm

Hộp cát, phê duyệt và phân quyền không phải là những phụ kiện bảo mật — đối với một coding agent, chúng định nghĩa bản chất sản phẩm là gì. Một hệ thống cho phép mô hình chạy các lệnh tùy ý trong thư mục người dùng là một agent chuyển giao rủi ro cho người dùng, chứ không chỉ đơn thuần là một agent "mạnh mẽ hơn". Việc thể hiện rõ ràng chế độ hộp cát, quyền truy cập mạng, chính sách phê duyệt, các thư mục bổ sung, vị trí lưu trữ trạng thái và phê duyệt công cụ MCP là những gì mang lại năng lực đi kèm với các ranh giới hành vi. Codex phơi bày các điều kiện ở cấp độ lượt hội thoại này trong `thread.ts` như một phần của ngữ nghĩa luồng; Claude Code đẩy ranh giới vào runtime — xử lý công cụ, ngắt, các hook phân quyền, các hạn chế đối với Bash. Một bên là "thực thi trong khi bị giám sát," bên kia là "khai báo hợp đồng thực thi trước khi bắt đầu."

## 4.6 MCP, các công cụ bên ngoài và di trú ranh giới

Cả hai hệ thống đều có thể gắn thêm nhiều khả năng hơn, nhưng sự khác biệt vẫn tồn tại. Claude Code đan cài các kỹ năng, hook, quyền hạn và các prompt công cụ vào một chuỗi quản trị tình huống (situational governance chain) để các quy tắc cục bộ đi cùng vòng lặp chính. Codex kéo các khả năng bên ngoài vào một hệ thống công cụ thống nhất — các tài nguyên MCP, các công cụ động và việc khám phá công cụ trong `tools/src/lib.rs` kỳ vọng các phần mở rộng (extensions) trở thành các đối tượng công cụ được định nghĩa bằng lược đồ, được quản lý bằng quy tắc thay vì những ngầm hiểu runtime. Một khi hệ sinh thái phát triển, "cách các phần mở rộng tuân thủ các quy tắc chung" sẽ trở thành bánh lái: đội ngũ nghĩ thông suốt về việc di trú ranh giới từ sớm sẽ giữ cho hệ sinh thái phần mở rộng của mình không bị thoái hóa thành một nhà kho chứa đồ phế thải.

## 4.7 Kết luận chương

Chương này có thể được thu gọn lại thành một câu đanh thép:

> Quản trị công cụ của Claude Code phụ thuộc nhiều hơn vào việc điều phối runtime và các phê duyệt tình huống, trong khi quản trị công cụ của Codex phụ thuộc nhiều hơn vào các lược đồ, phân quyền được tham số hóa và một hệ thống chính sách độc lập.

Bên trước giống như một đốc công giàu kinh nghiệm.

Bên sau giống như một nhà thầu có văn phòng tuân thủ và phòng pháp lý.

Nếu bạn chỉ nhìn vào thực tế là cả hai đều có thể chạy các câu lệnh, bạn sẽ bỏ lỡ sự khác biệt có ý nghĩa. Câu hỏi thực sự là ai sở hữu trật tự trước khi công cụ bắt đầu chuyển động.

Chương tiếp theo xem xét một lớp thực tế hơn: kỹ năng, hook, các tệp quy tắc cục bộ và các thể chế của nhóm. Một khi một hệ thống kỹ thuật phải gia nhập một nhóm, cuối cùng nó phải học luật lệ của làng.
