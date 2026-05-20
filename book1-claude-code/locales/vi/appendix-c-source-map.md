# Phụ lục C Bản đồ Mã nguồn: Các tệp cơ sở cho mỗi Chương

Cuốn sách này không phải là tài liệu hướng dẫn chi tiết mã nguồn, nhưng nó dựa trên cơ sở mã nguồn thực tế. Phụ lục này ánh xạ mỗi chương tới các tệp hỗ trợ chính của nó.

Đây không phải là một chỉ mục đầy đủ. Nó chỉ liệt kê các tệp liên quan trực tiếp đến các lập luận trong cuốn sách.

Một lưu ý về giới hạn bản quyền: bản đồ này dùng để trích dẫn cơ sở phân tích, chứ không phải để cam kết tái hiện văn bản mã nguồn. Nó lưu giữ các tham chiếu kỹ thuật cần thiết, định vị mô-đun và phân tích cấu trúc, mà không đi kèm với bản sao mã nguồn hoặc các đoạn trích dẫn triển khai dài dòng.

## C.1 Chương 1 Tại sao Kỹ thuật Khung kiểm soát là quan trọng

Các tệp cốt lõi:

- `src/constants/prompts.ts`
- `src/utils/systemPrompt.ts`
- `src/query.ts`
- `src/services/tools/toolOrchestration.ts`
- `src/tools/BashTool/prompt.ts`

Cơ sở lập luận chính:

- prompt là thành phần mặt phẳng điều khiển (control-plane) chứ không phải lớp vỏ bọc tính cách
- vòng lặp truy vấn (query loop) là khung xương của hệ thống agent
- hồ sơ rủi ro của công cụ và Bash là bằng chứng cho thấy khung kiểm soát là cần thiết

## C.2 Chương 2 Prompt là Mặt phẳng Điều khiển, không phải Trang trí Tính cách

Các tệp cốt lõi:

- `src/constants/prompts.ts`
- `src/utils/systemPrompt.ts`
- `src/utils/claudemd.ts`
- `src/memdir/memdir.ts`
- `src/constants/systemPromptSections.ts`
- `src/main.tsx`

Cơ sở lập luận chính:

- lắp ráp prompt hệ thống theo phân lớp
- `CLAUDE.md` và bộ nhớ đóng vai trò đầu vào của mặt phẳng điều khiển
- nhắc nhở động và tiêm ngữ cảnh (context injection)

## C.3 Chương 3 Vòng lặp Truy vấn: Nhịp đập của một Hệ thống Agent

Các tệp cốt lõi:

- `src/query.ts`
- `src/QueryEngine.ts`

Cơ sở lập luận chính:

- các đặc tính máy trạng thái (state-machine) của vòng lặp truy vấn
- quản trị đầu vào trước khi gọi mô hình
- tiêu thụ luồng sự kiện và các nhánh khôi phục
- `QueryEngine` sở hữu vòng đời cuộc hội thoại

## C.4 Chương 4 Công cụ, Quyền hạn và Ngắt

Các tệp cốt lõi:

- `src/services/tools/toolOrchestration.ts`
- `src/services/tools/toolExecution.ts`
- `src/services/tools/StreamingToolExecutor.ts`
- `src/hooks/useCanUseTool.tsx`
- `src/utils/permissions/PermissionResult.ts`
- `src/tools/BashTool/prompt.ts`
- `src/tools/BashTool/bashPermissions.ts`

Cơ sở lập luận chính:

- an toàn đồng thời (concurrency safety) và phát lại ngữ cảnh theo thứ tự
- ngăn xếp thực thi công cụ được bao bọc (wrapped tool execution stack)
- ngữ nghĩa ủy quyền `allow / deny / ask`
- ngắt công cụ dạng truyền phát và đóng tổng hợp (synthetic closure)
- quản trị đặc biệt áp lực cao cho Bash

## C.5 Chương 5 Quản trị Ngữ cảnh: Bộ nhớ, CLAUDE.md và Rút gọn

Các tệp cốt lõi:

- `src/utils/claudemd.ts`
- `src/memdir/memdir.ts`
- `src/services/SessionMemory/prompts.ts`
- `src/services/compact/autoCompact.ts`
- `src/services/compact/compact.ts`
- `src/query.ts`

Cơ sở lập luận chính:

- phát hiện và tải `CLAUDE.md` phân lớp
- `MEMORY.md` đóng vai trò làm chỉ mục lối vào, không phải kho chứa nội dung
- tính liên tục có cấu trúc trong bộ nhớ phiên (session memory)
- các ngưỡng tự động rút gọn, bộ đệm và cầu dao ngắt mạch (circuit breaker)
- tái dựng các ngữ nghĩa làm việc sau rút gọn

## C.6 Chương 6 Lỗi và Khôi phục

Các tệp cốt lõi:

- `src/query.ts`
- `src/services/compact/autoCompact.ts`
- `src/services/compact/compact.ts`
- `src/services/api/withRetry.ts`

Cơ sở lập luận chính:

- giữ lại các lỗi có thể khôi phục
- xử lý lỗi prompt quá dài (prompt-too-long) thông qua thu hẹp và rút gọn phản ứng (reactive compact)
- leo thang `max_output_tokens` và chiến lược tiếp tục
- ngắt mạch khi tự động rút gọn thất bại
- tự khôi phục rút gọn trong lỗi prompt quá dài (PTL)

## C.7 Chương 7 Đa Agent và Xác minh

Các tệp cốt lõi:

- `src/utils/forkedAgent.ts`
- `src/coordinator/coordinatorMode.ts`
- `src/tasks/LocalAgentTask/LocalAgentTask.tsx`
- `src/utils/hooks/hooksConfigManager.ts`
- `src/skills/bundled/verify.ts`
- `src/memdir/memoryTypes.ts`

Cơ sở lập luận chính:

- các tham số phân nhánh an toàn cho cache và cô lập trạng thái
- trách nhiệm tổng hợp của điều phối viên (coordinator)
- giai đoạn xác minh độc lập
- các hook vòng đời subagent
- dọn dẹp tác vụ và lan truyền hủy bỏ giữa parent-child
- kỷ luật xác minh bộ nhớ cũ

## C.8 Chương 8 Áp dụng trong Nhóm

Các tệp cốt lõi:

- `src/utils/claudemd.ts`
- `src/tools/SkillTool/prompt.ts`
- `src/tools/SkillTool/SkillTool.ts`
- `src/utils/forkedAgent.ts`
- `src/utils/hooks/hooksConfigManager.ts`
- `src/main.tsx`

Cơ sở lập luận chính:

- tính ổn định phân lớp trong `CLAUDE.md` của nhóm
- kỹ năng đóng vai trò là các lát cắt thể chế thay vì các bộ sưu tập prompt
- ranh giới phê duyệt và phạm vi quy tắc cho phép (allow-rule scoping)
- quản trị vòng đời thông qua các hook
- hành vi khởi động phiên xung quanh việc tải hướng dẫn và kỹ năng

## C.9 Chương 9 Mười Nguyên lý

Chương 9 không bắt nguồn từ một tệp duy nhất. Nó cô đọng cấu trúc xuyên suốt các chương, được phản ánh đồng thời trong:

- lắp ráp prompt
- vòng lặp truy vấn (query loop)
- điều phối công cụ (tool orchestration)
- mô hình phân quyền
- quản trị ngữ cảnh
- hệ thống khôi phục
- điều phối đa agent (multi-agent orchestration)
- các hook quản trị nhóm
