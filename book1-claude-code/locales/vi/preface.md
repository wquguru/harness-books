# Lời nói đầu: Khung kiểm soát (Harness), Terminal và các Ràng buộc Kỹ thuật

Trong những năm gần đây, mọi người thích gọi các mô hình viết mã nguồn là "agent" (agent). Thuật ngữ này mang theo sự lạc quan rõ rệt, như thể việc đọc một kho lưu trữ (repo), gọi các công cụ (tools) và tạo ra một bản vá (patch) tàm tạm là đủ để làm việc độc lập trong các môi trường kỹ thuật. Nhưng các môi trường kỹ thuật luôn đi kèm với các hệ quả. Terminal (terminal), hệ thống tệp (filesystem) và lịch sử Git không phải là không gian trừu tượng; mỗi thay đổi đều để lại dấu vết.

Một mô hình chỉ xuất ra văn bản hầu như chỉ tạo ra chi phí diễn giải khi nó thất bại. Một mô hình có thể chạy các lệnh, ghi tệp, truy cập mạng và sửa đổi kho lưu trữ (repositories) sẽ để lại các sản phẩm thực thi (execution artifacts) khi nó thất bại. Thư mục thay đổi, tiến trình bị lỗi, cấu hình bị hỏng và lịch sử trở nên khó kiểm toán. Tại thời điểm đó, câu hỏi then chốt không còn là liệu mô hình có đủ thông minh hay không, mà là liệu hệ thống có áp đặt đủ ràng buộc hay không.

Đó là những gì cuốn sách này thảo luận.

Tôi gọi nó là Kỹ thuật Khung kiểm soát (Harness Engineering). Ở đây, khung kiểm soát (harness) nghĩa là các cấu trúc điều khiển hoạt động liên tục nhằm giới hạn hành vi của mô hình trong các môi trường kỹ thuật. Đối với các agent lập trình AI, năng lực không bị ràng buộc chỉ làm mở rộng bán kính thiệt hại (blast radius).

Đây không phải là một tài liệu đi qua từng dòng mã nguồn của Claude Code. Mã nguồn rất quan trọng, nhưng nếu chúng ta chỉ đi theo các thư mục và giải thích từng hàm một, chúng ta sẽ kết thúc với một tập hợp các chú thích được biên soạn lại. Điều đó có thể cho chúng ta biết các hàm làm gì, nhưng không giải thích được tại sao hệ thống phải phát triển theo hình dạng này. Để hiểu các hệ thống như Claude Code, việc biết sự tồn tại của `queryLoop()`, `compactConversation()` và `runTools()` là chưa đủ. Câu hỏi khó hơn là: tại sao một hệ thống "viết mã nguồn" cuối cùng lại yêu cầu phân lớp prompt (prompt layering), kiểm tra quyền hạn (permission checks), máy trạng thái (state machines), logic rút gọn (compact logic), các nhánh khôi phục (recovery branches), kiểm soát vòng đời subagent (subagent lifecycle control), các giai đoạn xác minh (verification stages) và quy trình của nhóm (team process)?

Câu trả lời không phức tạp: các mô hình vốn không ổn định.

Nhận định đó không phải lúc nào cũng dễ chịu, nhưng các hệ thống kỹ thuật không thể vận hành dựa trên những câu chuyện kể đầy lạc quan. Nếu một thành phần cốt lõi có bản chất không ổn định, hệ thống phải được thiết kế xoay quanh thực tế đó. Nếu không, vấn đề sẽ tích tụ lại trong các buổi họp rút kinh nghiệm sự cố (incident retrospectives).

Claude Code rất đáng để nghiên cứu vì việc triển khai của nó được giữ ở mức tiết chế một cách có chủ ý:

- Nó không giả định rằng tính chính xác của mô hình được duy trì liên tục, vì vậy nó sử dụng một vòng lặp truy vấn (query loop) để quản lý trạng thái
- Nó không giả định rằng các lượt gọi công cụ (tool calls) tự bản chất là an toàn, vì vậy nó ràng buộc các công cụ thông qua quyền hạn và lập lịch
- Nó không giả định rằng việc có nhiều ngữ cảnh hơn lúc nào cũng tốt hơn, vì vậy nó đưa vào bộ nhớ (memory), `CLAUDE.md`, rút gọn (compact) và bộ nhớ phiên (session memory)
- Nó không xem lỗi là các sự kiện hiếm hoi, vì vậy nó thiết kế các lộ trình khôi phục (recovery paths) cho các trường hợp prompt quá dài, số lượng token đầu ra tối đa (max output tokens), ngắt (interrupts) và vòng lặp hook (hook loops)
- Nó không đồng nhất đa agent (multi-agent) với năng lực mạnh mẽ hơn, vì vậy nó tách biệt phần tổng hợp (synthesis) và xác minh (verification) để tránh hiện tượng tự xác nhận (self-endorsement)

Kết hợp lại, đây chính là agent. Mô hình chỉ là thành phần hùng biện nhất và kém ổn định nhất bên trong nó.

Vì vậy, cuốn sách này giữ vững một quan điểm nhất quán:

> Prompt quyết định cách nó nói. Khung kiểm soát (Harness) quyết định cách nó hành động.

Khung kiểm soát (Harness) ở đây không phải là một lớp phụ kiện và không phải là sự phòng thủ cảm tính trước năng lực của mô hình. Nó là điều kiện tiên quyết để đưa một mô hình vào các môi trường kỹ thuật. Nếu không có lớp đó, rủi ro sẽ bị chuyển sang cho người dùng, các nhóm và những người duy trì hệ thống trong tương lai.

Một ranh giới rõ ràng ngay từ đầu: cuốn sách này không bao gồm mã nguồn của Claude Code, và không sao chép lại các đoạn mã nguồn lớn. Lý do rất đơn giản: giới hạn bản quyền. Những gì chúng ta có thể làm là trích xuất các nguyên lý thiết kế, cơ chế runtime và các nhận định mang tính phương pháp luận thông qua phân tích kỹ thuật hợp lý và các trích dẫn có giới hạn, chứ không xuất bản lại văn bản triển khai đã được bảo hộ.

Cuốn sách này cố gắng thực hiện hai việc.

Thứ nhất, sử dụng cấu trúc nguồn của Claude Code, nó giải thích các cấu trúc thực sự quyết định độ tin cậy. Trọng tâm là tại sao quản trị ngữ cảnh (context governance) phải là một lộ trình chính yếu, tại sao đa agent (multi-agent) giải quyết việc phân chia vai trò, và tại sao quy trình nhóm phải gắn liền với các điểm kiểm tra vòng đời (lifecycle checkpoints), thay vì chỉ liệt kê đơn thuần "có rút gọn (compact)", "có subagent", "có hook".

Thứ hai, nó trích xuất các nguyên lý kỹ thuật rộng hơn đằng sau những lựa chọn triển khai đó. Các phiên bản mã cụ thể thay đổi, tên hàm thay đổi, giao diện sản phẩm thay đổi. Nhưng chừng nào con người còn tiếp tục tích hợp các mô hình không ổn định vào quy trình làm việc thực tế, một số nguyên lý nhất định vẫn sẽ giữ nguyên giá trị. Ví dụ:

- Các lộ trình xử lý lỗi (error paths) phải được thiết kế như các lộ trình cốt lõi (first-class paths)
- Xác minh phải là một phần của định nghĩa về sự hoàn thành (definition of done)
- Quyền hạn (permission) là một cơ quan của hệ thống, không phải là một tính năng phụ trợ
- Ngữ cảnh (context) là một tài nguyên, không phải là một ngăn kéo chứa rác
- Đa agent (multi-agent) phụ thuộc vào sự phân chia vai trò, chứ không phải là chiến thuật gia tăng nhân số
- Các thể chế nhóm (team institutions) quan trọng hơn các mẹo cá nhân

Nếu những nhận định đó đúng, tốt nhất nên coi Claude Code như một mẫu vật tham chiếu. Giá trị của nó không phải là dạy mọi người sao chép chính xác một giao diện dòng lệnh (CLI), mà là chỉ ra cách một AI agent khi đối mặt với các điều kiện kỹ thuật thực tế sẽ phát triển hướng tới cấu trúc ràng buộc chặt chẽ hơn.

Nói một cách trực tiếp hơn, cuốn sách này không phải là về việc đóng gói một mô hình thành một ảo tưởng "giống như kỹ sư". Đó là về việc xây dựng một hệ thống kỹ thuật có thể vận hành được mặc dù mô hình thiếu đi sự ổn định ở cấp độ kỹ sư.

Công việc này hiếm khi hào nhoáng. Khôi phục trạng thái (rollback), phê duyệt (approval), quyền hạn (permission), xác minh (verification), rút gọn (compact) và dọn dẹp tiến trình mồ côi (orphan-process cleanup) không phải là những thứ hào nhoáng. Tuy nhiên, sự ổn định lâu dài của hệ thống thường phụ thuộc chính xác vào những mảnh ghép này. Nếu bạn quá ưu tiên "sự tự nhiên giống con người", kết quả phổ biến là một hệ thống thừa hưởng các kiểu lỗi giống con người mà không có trách nhiệm giải trình của con người.

Vì lẽ đó, chúng ta bắt đầu với các ràng buộc.

Trong chín chương tiếp theo, chúng ta thảo luận về cách cấu trúc khung kiểm soát (harness) này phát triển, tại sao nó phải phát triển theo hướng này và cách một nhóm biến kinh nghiệm cá nhân thành các thể chế kỹ thuật có thể tái sử dụng.

@wquguru  
2026-04-01  
Vào ngày rò rỉ mã nguồn Claude Code, Ngày Cá tháng Tư  

Bạn cũng có thể đọc bản trực tuyến tại [harness-books.agentway.dev/book1-claude-code](https://harness-books.agentway.dev/book1-claude-code/) để có trải nghiệm đọc tốt hơn.
