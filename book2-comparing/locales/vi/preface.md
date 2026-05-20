# Lời tựa: Hai khung kiểm soát, không phải một bộ phụ kiện

Việc so sánh hai khung kiểm soát (harnesses) lập trình AI rất dễ bị sai lệch nếu bạn chỉ xếp chúng cạnh nhau bằng các bảng kiểm tính năng. Cả Claude Code và Codex đều có các kỹ năng, hộp cát và sub-agent. Nhưng việc thấy chúng chia sẻ cùng một thuật ngữ không có nghĩa là khung xương của chúng giống nhau. Điều này giống như việc lưu ý rằng cả hai thành phố đều có cầu — câu hỏi thực sự là chúng đang muốn bắc qua dòng sông nào.

Cuốn sách này nhằm mục đích so sánh các phần cốt lõi bên trong (the bones), chứ không phải các nhãn tên.

Cả hai hệ thống đều thừa nhận một điều mà hoạt động tiếp thị thường che giấu: một mô hình không thể được tin cậy để thực thi mà không có các ràng buộc. Shell, hệ thống tệp, quyền hạn, các cuộc gọi công cụ, các nhóm làm việc, các phiên làm việc dài và các lộ trình khôi phục là những thực tế hỗn độn. Khung kiểm soát chính là thực tế hỗn độn đó; nó là bộ máy ngăn một mô hình không đáng tin cậy thiêu rụi môi trường xung quanh. Khi khung kiểm soát đó tồn tại, bạn không còn đo lường thành công bằng việc mô hình nói năng lưu loát ra sao — bạn đo lường nó bằng việc hệ thống đặt các rào chắn (guardrails) ở đâu và như thế nào.

Trong tập đầu tiên, tôi đã coi Claude Code như một mẫu vật và trích xuất các nguyên lý chung của Kỹ thuật Khung kiểm soát (Harness Engineering). Đó là giải phẫu một hệ thống đơn lẻ. Ở đây, mục tiêu là đặt Claude Code bên cạnh một khung kiểm soát nghiêm túc khác có nguồn gốc khác biệt. Chỉ khi so sánh, nhiều lựa chọn thiết kế mới tự bộc lộ là một con đường kỹ thuật trong số nhiều con đường.

Codex rất đáng để so sánh chính xác bởi vì nó không phải là một bản sao. Một cái nhìn thoáng qua vào `core/src/lib.rs` của nó cho thấy một chương trình được thiết kế có chủ ý: luồng (threads), triển khai (rollouts), cầu nối trạng thái (state bridges), hướng dẫn (instructions), kỹ năng (skills), hook, hộp cát (sandboxing), chính sách thực thi (exec policy), công cụ (tools) — mỗi thứ được cấu thành trong một mô-đun rõ ràng. Tham vọng ở đây là làm cho lớp kiểm soát có thể cấu thành (composable), tuần tự hóa (serializable) và nhận biết chính sách (policy-aware) thay vì giấu nó bên trong một mớ trực giác runtime.

Ngược lại, Claude Code mang lại cảm giác giống như một thứ gì đó lớn lên dưới áp lực của vòng lặp runtime của nó. Hãy nhìn vào `src/query.ts` và logic rút gọn, điều phối công cụ, xử lý phân quyền, ngắt và phục hồi xung quanh. Hầu hết sự kỳ diệu của nó trả lời cho câu hỏi “làm thế nào để lượt hội thoại này chuyển giao an toàn cho lượt tiếp theo?” Khung kiểm soát trước tiên phải tiếp tục chạy liên tục; một khi tính liên tục ổn định, người ta mới có thể tinh chỉnh các quy tắc giữa các giai đoạn.

Cả hai hệ thống đều thống nhất rằng các mô hình là không đáng tin cậy. Niềm tin chung đó rất quan trọng. Một khi bạn thừa nhận mô hình không thể tự sinh tồn trong shell, tệp tin, phân quyền và các cuộc hội thoại dài một mình, một khung kiểm soát bắt buộc phải phát triển — xếp chồng prompt (prompt stacking), tính bền vững của trạng thái (state persistence), phê duyệt, quản trị ngữ cảnh (context governance), luồng khôi phục (recovery flows), xác minh (verification) và các quy ước cục bộ (local conventions). Chỉ có vị trí sắp xếp của các cơ quan đó là khác nhau.

Cuốn sách này không sao chép lại mã nguồn của Claude Code hay Codex, và nó không chép lại các đoạn trích dẫn triển khai dài dòng. Ranh giới đó không có gì bí ẩn: đó là sự tôn trọng đối với mã nguồn độc quyền, cũng như mong muốn giữ cho lập luận nằm trong phạm vi phân tích kỹ thuật. Những gì tiếp theo là sự so sánh về cách các hệ thống này tự nhìn nhận về bản thân, chứ không phải là việc sao chép-dán các triển khai của chúng.

Nếu tôi phải tóm tắt trong một câu:

> Claude Code và Codex đồng điệu với nhau không phải vì cả hai đều gọi công cụ, mà vì không hệ thống nào sẵn sàng đối xử với mô hình như một thực thể thực thi tự do.

Còn về sự khác biệt của chúng, chúng thú vị hơn nhiều.

Claude Code tiếp cận việc thiết kế khung kiểm soát thông qua kỷ luật runtime. Nó lo lắng về đứt gãy phiên (session rupture), chuỗi công cụ (tool chaining), hành vi rút gọn (compact behavior), sự xen ngang của người dùng (user interjections) và điều gì xảy ra nếu một agent phân nhánh (forked agent) bị chết giữa cuộc hội thoại. Nó mang lại cảm giác của một người đã từng dọn dẹp sau những ca làm việc hỗn độn trong một trung tâm vận hành thực tế — thích giải quyết các vấn đề "thông minh" thông qua sự khéo léo trong các luồng kiểm soát và khôi phục.

Codex tiếp cận nó thông qua kiểm soát có cấu trúc. Các phân đoạn hướng dẫn (instruction fragments), luồng (threads), chính sách phê duyệt, lược đồ công cụ, sự kiện hook và chính sách thực thi (exec policies) đều được viết rõ ràng. Nó coi trọng việc đặt tên, ranh giới rõ ràng và cấu hình. Codex không dựa vào sự ngầm hiểu; nó thích khai báo các kiểu đánh dấu (marker types) và tiêm chúng một cách xác định.

Cả hai lộ trình đều hợp lệ. Chúng chỉ hợp lệ theo những cách khác nhau.

Đây không phải là một bài viết về kẻ thắng người thua. So sánh kỹ thuật có giá trị giúp xác định các phụ thuộc vào lộ trình (path dependencies), chứ không phải xếp hạng tốc độ thực thi. Cách bạn chọn để ràng buộc một mô hình không đáng tin cậy sẽ quyết định khung kiểm soát của bạn trở thành gì. Nơi nhóm của bạn đặt sự kiểm soát là nơi hệ thống sẽ đắp da đắp thịt. Thay vì hỏi “thực tiễn tốt nhất (best practice) là gì?”, hãy hỏi “tôi đang chống lại sự không chắc chắn nào, và tôi sẵn sàng neo giữ trật tự ở đâu?”

Bảy chương tiếp theo bắt đầu từ câu hỏi đó.

@wquguru  
2026.04.01  
Claude Code fools-day source leak

P.S. Đọc phiên bản trực tuyến tại [harness-books.agentway.dev/book2-comparing](https://harness-books.agentway.dev/book2-comparing/) để có trải nghiệm phong phú hơn.
