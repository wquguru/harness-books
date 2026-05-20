# Chương 3 Nơi Nhịp đập Tồn tại: Vòng lặp Truy vấn so với Luồng, Triển khai và Trạng thái

![Continuity Comparison](diagrams/diag-02-continuity-comparison.png)

## 3.1 Cốt lõi của một hệ thống agent là tính liên tục

Coi một hệ thống agent như một cuộc "trò chuyện nhiều lượt (multi-turn chat)" cũng giống như coi một cơ sở dữ liệu là một "sổ tay bệnh nhân" — điều đó che giấu đi vấn đề kiến trúc thực sự. Tính liên tục (continuity) mới là điều khó khăn: cách lượt này tiếp nối lượt trước, cách các kết quả công cụ được hợp nhất, cách sự ngắt quãng được đóng lại, cách ngữ cảnh phình to được sắp xếp lại, liệu lỗi có kích hoạt thử lại, rút gọn (compaction) hay báo cáo trung thực hay không. Những câu trả lời này quyết định liệu một hệ thống có thực sự là một agent hay chỉ là một giao diện trả lời câu hỏi tình cờ hỗ trợ các cuộc gọi công cụ. Claude Code và Codex phân kỳ ở điểm này rõ ràng hơn bất kỳ bảng so sánh tính năng nào.

## 3.2 Claude Code: tính liên tục được nén vào vòng lặp chính

Trục xoay quanh `query()` và `queryLoop()`, các hàm này đẩy nhiều vấn đề quan trọng vào trạng thái vòng lặp: chuỗi thông điệp hiện tại, ngữ cảnh sử dụng công cụ (tool-use context), theo dõi rút gọn, bộ đếm phục hồi token đầu ra, các tóm tắt đang chờ xử lý, số lượt hội thoại, các bước chuyển trạng thái. Câu trả lời cho câu hỏi "làm thế nào một agent tiếp tục sống sót" mang hương vị runtime — tính liên tục được duy trì chủ yếu bởi vòng lặp, và cấu trúc cốt lõi mang lại cảm giác giống như một công cụ hội thoại tự sửa lỗi hơn là một hệ thống được điều khiển trước hết bởi một mô hình trạng thái bên ngoài. Điểm mạnh rất cụ thể: thứ tự trả về của công cụ, việc cắt ngắn đầu ra, các sự kiện prompt quá dài (prompt-too-long), cắt xén lịch sử (history snips), rút gọn vi mô (microcompact) và các sự xen ngang của người dùng đều diễn ra bên trong vòng lặp, và Claude Code đối xử với chúng như các trạng thái vòng lặp hợp lệ thay vì né tránh chúng. Thiết kế này có bề mặt kỹ thuật thô ráp — không phải lúc nào cũng thanh lịch, nhưng thường mạnh mẽ hơn.

## 3.3 Codex: tính liên tục được chia nhỏ trên các cấu trúc luồng, triển khai và cầu nối trạng thái

Codex trông giống một sổ cái hơn. Từ `core/src/lib.rs` trở đi, tính liên tục được phân bổ trên `codex_thread`, `thread_manager`, `rollout`, `state_db_bridge`, `state` và `message_history`.

![Codex thread-turn-state detail](diagrams/diag-06-codex-thread-state-detail.png)

Trong `sdk/typescript/src/thread.ts`, `Thread` đã là một khái niệm hạng nhất (first-class concept) đối với các nhà phát triển bên ngoài: nó sở hữu `id`, chạy thông qua `runStreamed()` hoặc `run()`, và `thread.started` báo cáo lại ID của luồng. Các điều kiện thực thi ở cấp độ lượt hội thoại — chính sách phê duyệt, thư mục làm việc, chế độ hộp cát (sandbox mode), quyền truy cập mạng, các thư mục bổ sung — đều là các tham số rõ ràng được liên kết chặt chẽ với việc thực thi luồng. Chủ quyền của luồng là theo nghĩa đen: `runStreamedInternal()` gọi `normalizeInput()` để tách văn bản khỏi hình ảnh, gọi `createOutputSchemaFile()` để chuẩn bị tệp lược đồ, sau đó truyền `threadId`, `approvalPolicy`, `sandboxMode`, `workingDirectory`, `networkAccessEnabled` và `additionalDirectories` vào `_exec.run()`. Khi luồng dữ liệu (stream) phát ra sự kiện `thread.started`, đối tượng sẽ cập nhật thuộc tính `_id` của nó. Luồng không phải là lớp vỏ bọc bên ngoài — nó là lớp mà ngữ nghĩa của lượt hội thoại thực sự đi qua. Tính liên tục không còn là "vòng lặp vẫn đang tiếp diễn" mà là "một luồng đang được ghi lại và ràng buộc bởi một cấu trúc trạng thái rõ ràng." Khái niệm triển khai (rollout), đặc biệt, báo hiệu rằng Codex quan tâm đến khả năng phát lại (replayability), lập chỉ mục, tính bền vững và khả năng hiển thị ngoài phiên làm việc — hệ thống mang lại cảm giác giống như một công cụ ghi lại quá trình thực thi hơn là một trình quản lý hội thoại trực tiếp.

## 3.4 Sự khác biệt là nơi chủ quyền trạng thái (state sovereignty) tồn tại

Claude Code có trạng thái, Codex có các vòng lặp — sự khác biệt không phải là có hay không có mà là chủ quyền. Claude Code trao nhiều chủ quyền hơn cho vòng lặp truy vấn: "làm thế nào để phiên làm việc tiếp tục" là một vấn đề cốt lõi của runtime, và many vấn đề được giải quyết trực tiếp bên trong vòng lặp. Codex trao chủ quyền cho các cấu trúc luồng (thread) và triển khai (rollout): tính liên tục không nên chỉ là sản phẩm phụ của luồng kiểm soát nội bộ; nó phải trở thành một thực tế rõ ràng được mang theo bởi cơ sở hạ tầng luồng và trạng thái. Đó là lý do tại sao `Thread` trong TypeScript SDK mang lại cảm giác giống như một khái niệm sản phẩm, và các nhà phát triển suy nghĩ về các lượt hội thoại của agent trực tiếp thông qua nó. Vòng lặp truy vấn của Claude Code giống như phòng động cơ hơn — quan trọng, nhưng không phải mọi người dùng đều phải sắp xếp mô hình tư duy của họ xung quanh nó.

### Bất biến: chủ quyền của tính liên tục (continuity sovereignty)

```
// Claude Code (nguồn: src/query.ts)
assert loop owns {messages, toolUseContext, compactTracking, turnCount}
assert each loop iteration recomputes "what matters now"
assert pending tool_use closed or synthetic-filled before iteration ends

// Codex (nguồn: core/src/lib.rs, sdk/typescript/src/thread.ts)
assert thread.id stable across runs; rollout records every turn
assert turn-level {approvalPolicy, sandboxMode, workingDirectory} explicit in exec.run() args
assert thread.started event emitted before any tool call
assert state_db_bridge persists before the main loop exits
```

### Ma trận lỗi: ngắt khi có tool_use chưa xử lý xong

| Thứ tự sự kiện | Trạng thái trước | Tác nhân kích hoạt | Bước tiếp theo của Claude Code | Bước tiếp theo của Codex |
|---|---|---|---|---|
| người dùng ngắt + công cụ đang chạy | tool_use chưa đóng | người dùng hủy | tổng hợp tool_result trong vòng lặp, đóng sổ cái | hủy ở cấp luồng, ghi sự kiện "interrupted" vào rollout |
| đầu ra mô hình bị cắt ngắn | max_output_tokens | chạm giới hạn | nâng giới hạn hoặc nối thêm tin nhắn người dùng giả lập để tiếp tục | luồng ghi lại việc cắt ngắn, bên gọi khởi động lại lượt |
| prompt quá dài | phiên làm việc bị phình to | prompt_too_long | thu hẹp / rút gọn phản ứng / đẩy ra ngoài bên trong vòng lặp | thread_manager cắt bớt lịch sử, chuyển sang lượt tiếp theo |
| khởi động lại tiến trình | sập giữa phiên | sập / bị buộc dừng | dựa vào PR / Git bên ngoài để xây dựng lại; trạng thái vòng lặp dễ vỡ | phát lại rollout + state_db_bridge theo thread.id |
| khôi phục cạn kiệt | lỗi rút gọn liên tiếp | ngưỡng cầu dao | bỏ qua stop hook, báo lỗi trung thực | trả về lỗi state-bridge, giữ lại bản ghi luồng |

## 3.5 Các hệ quả khác nhau đối với việc phục hồi và khả năng kiểm toán

Vị trí đặt trạng thái ảnh hưởng trực tiếp đến khả năng phục hồi và khả năng kiểm toán. Sức mạnh khôi phục của Claude Code đến từ sự gần gũi với hiện trường — nhiều vấn đề được phát hiện và xử lý ngay bên trong chính vòng lặp (rút gọn phản ứng, phục hồi token đầu ra, dọn dẹp khi ngắt công cụ), mà không cần đưa chúng lên một mô hình trạng thái cấp cao hơn trước. Sức mạnh khôi phục của Codex nằm ở khả năng truy vết: luồng có ID, triển khai (rollouts) có hồ sơ, các cầu nối trạng thái cộng với lịch sử thông điệp cung cấp cấu trúc bên ngoài rõ ràng hơn, giúp câu hỏi "chính xác điều gì đã xảy ra ở lượt trước" có thể trả lời được từ các tài liệu lưu trữ thay vì hồi tưởng runtime. Khi đọc `core/src/lib.rs` cùng với lớp SDK, thiết kế thiên về lưu trữ hiển thị rất rõ ràng — việc xuất (export) không chỉ `CodexThread` mà cả `ThreadManager`, `RolloutRecorder`, `state_db_bridge` và `message_history` ngay gần mô-đun gốc thực chất đã tuyên bố tính liên tục là cơ sở hạ tầng, chứ không phải là tác dụng phụ của việc lặp. Nói một cách bình dân: Claude Code gần giống như một đội cứu hộ tại hiện trường, Codex gần giống như một trung tâm điều phối có lưu trữ lưu tệp — bên trước giỏi hơn trong việc duy trì thực thi tiếp tục, bên sau giỏi hơn trong việc giải thích cách tính liên tục được duy trì.

## 3.6 Các tác động khác nhau đối với giao diện sản phẩm và giao diện nhóm

Chủ quyền trong vòng lặp hướng các đội ngũ đến các câu hỏi về runtime: những thất bại nào cần phục hồi, những hành động nào nên có khả năng bị ngắt, khi nào kích hoạt rút gọn, làm thế nào kết quả công cụ trả về cuộc hội thoại chính. Chủ quyền trong các cấu trúc luồng và trạng thái hướng các đội ngũ đến các câu hỏi về giao diện và quản trị: vòng đời của luồng, sự kiện nào rollout nên giữ lại, kho lưu trữ trạng thái nằm ở đâu, làm thế nào chính sách phê duyệt trở thành một tùy chọn ở cấp lượt hội thoại. Claude Code gần với việc làm cho agent vận hành trước tiên rồi mới nhúng các thể chế vào sau; Codex gần với việc định nghĩa các giao diện thể chế trước tiên rồi mới để agent vận hành bên trong chúng.

## 3.7 Kết luận chương

Kết luận có thể được phát biểu một cách đơn giản:

> Claude Code đặt nhiều tính liên tục hơn bên trong vòng lặp truy vấn (query loop), trong khi Codex đặt nhiều tính liên tục hơn bên trong cơ sở hạ tầng luồng, triển khai (rollout) và trạng thái.

Bên trước nhấn mạnh vào nhịp đập runtime.

Bên sau nhấn mạnh vào nền tảng phiên làm việc bền vững (persisted session substrate).

Đây không phải là một sự khác biệt về mặt thẩm mỹ. Đó là sự phân bổ quyền lực của hệ thống. Bất cứ ai sở hữu tính liên tục sẽ định nghĩa trung tâm của khung kiểm soát.

Chương tiếp theo sẽ đi vào lớp khó khăn nhất: công cụ, hộp cát, phê duyệt và chính sách thực thi. Một khi shell bước vào bức tranh, những câu chuyện lãng mạn thường tự khắc rời đi.
