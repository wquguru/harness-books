# Chapter 8 Nếu Bạn Cần Tự Xây Dựng Khung Kiểm Soát (Harness): Nên Học Hỏi Từ Ai, và Nên Học Gì Trước

## 8.1 Công dụng thực sự của việc so sánh là để tránh các đường vòng không cần thiết

Kết cục ít thú vị nhất là kết cục mang tính tiêu dùng — chọn A hoặc B. Các hệ thống kỹ thuật không phải là tai nghe và không được phân phối qua các bảng xếp hạng. Câu hỏi hữu ích là: nếu bạn chuẩn bị xây dựng khung kiểm soát (harness) của riêng mình hoặc tái cấu trúc một Agent hiện có, bạn nên học hỏi các bài học của ai trước, và phần nào trước. Claude Code và Codex cung cấp hai nước đi mở đầu, chứ không phải hai câu trả lời cuối cùng. Claude Code cảnh báo bạn không nên làm cho các vấn đề runtime nghe có vẻ quá thanh lịch — những thứ kéo hệ thống đi xuống là các công việc tẻ nhạt, vất vả (dirty jobs) bên trong vòng lặp truy vấn (query loop) (đóng sổ cái kết quả công cụ, quản lý sự phình to của ngữ cảnh, phục hồi sau khi bị ngắt, dọn dẹp các Agent phụ, giữ cho việc xác minh độc lập, ngăn chặn việc xử lý lỗi lặp đi lặp lại vô hạn trên chính nó); việc xem nhẹ những vấn đề đó sẽ tạo ra một hệ thống trông có vẻ thông minh nhưng lại cực kỳ rủi ro khi vận hành. Codex cảnh báo bạn không được để lớp điều khiển tan biến vào sự ngầm hiểu (tacit understanding) — các nguồn chỉ dẫn (instruction sources), schema công cụ, chính sách phê duyệt, trạng thái luồng (thread state), sự kiện hook và tài sản kỹ năng trở nên dễ quản lý hơn nếu chúng được làm rõ ràng càng sớm càng tốt; những đội ngũ liên tục yêu cầu sự ứng biến runtime thay thế cho thể chế cuối cùng sẽ nhận thấy hệ thống của họ giống như một chiếc lán được dựng lên từ những thỏa thuận bằng lời nói.

## 8.2 Ba hình thái đội ngũ phổ biến, ba hướng đi mở đầu

### Tuyến một: đội ngũ đã có một nguyên mẫu (prototype) Agent, nhưng các phiên dài thường xuyên mất kiểm soát

Loại đội ngũ này thường cần đến Claude Code trước tiên.

Vấn đề của họ hiếm khi là "mặt phẳng điều khiển chưa được định nghĩa rõ ràng." Vấn đề của họ là hệ thống không thể duy trì hoạt động đủ lâu. Các triệu chứng điển hình bao gồm:

- ngữ cảnh ngày càng nhiễu loạn theo thời gian
- các chuỗi gọi công cụ (tool-call chains) bị đứt gãy
- trạng thái trở nên không rõ ràng sau khi bị ngắt
- không ai dọn dẹp công việc của Agent phụ một cách sạch sẽ
- xác minh thoái hóa thành thứ mà mọi người chỉ nói suông

Khi đó là những triệu chứng của bạn, điều đầu tiên cần sửa chữa là nhịp đập runtime (runtime heartbeat), chứ không phải thêm cấu hình. Hãy ổn định vòng lặp trước. Tính thẩm mỹ của thể chế có thể đợi sau.

### Tuyến hai: đội ngũ đã có nhiều quy tắc, nhưng các nguồn quy tắc bị phân tán và ranh giới quyền hạn không rõ ràng

Loại đội ngũ này thường cần đến Codex trước tiên.

Vấn đề của họ không phải là bối cảnh thực địa không thể tồn tại được. Vấn đề của họ là hệ thống ngày càng trở nên khó quản trị hơn. Các triệu chứng phổ biến bao gồm:

- quy tắc địa phương rải rác ở khắp mọi nơi
- không ai có thể nói ràng buộc nào nằm ở prompt và ràng buộc nào nằm ở công cụ
- logic phê duyệt được trộn lẫn vào mã nguồn và khó giải thích
- một khi nhiều phần mở rộng (extensions) được đưa vào, các ranh giới càng bị mờ nhạt hơn

Những gì các đội ngũ này cần là một lớp điều khiển rõ ràng. Hãy biến chỉ dẫn (instruction), công cụ (tool), chính sách (policy) và luồng (thread) thành các khái niệm rõ ràng trước khi yêu cầu runtime hoạt động bên trong chúng.

### Tuyến ba: chưa có hệ thống trưởng thành nào và đội ngũ đang bắt đầu từ con số không

Đây là trường hợp nguy hiểm nhất, bởi vì dễ dàng thèm muốn thế mạnh của cả hai bên cùng một lúc và xây dựng nên một sự thỏa hiệp thất bại.

Một lộ trình ổn định hơn thường là:

- chọn một mâu thuẫn chính
- thiết kế khung xương chính xung quanh mâu thuẫn đó
- hiện tại chỉ thêm phía đối diện ở mức độ tối thiểu

Nếu rủi ro ở giai đoạn đầu của bạn chủ yếu là "mô hình sẽ hành xử liều lĩnh," hãy bắt đầu với kỷ luật runtime theo nghĩa của Claude Code.

Nếu rủi ro ở giai đoạn đầu của bạn chủ yếu là "đội ngũ sẽ mất đi trật tự thể chế," hãy bắt đầu với một lớp điều khiển rõ ràng theo nghĩa của Codex.

Nước đi tồi tệ nhất là cố gắng học hỏi đầy đủ cả hai bên cùng một lúc và kết quả là không có cả vòng lặp chính ổn định lẫn mặt phẳng điều khiển rõ ràng.

### Danh sách kiểm tra dành cho nhà xây dựng theo giai đoạn (Staged builder checklists) cho ba hình thái đội ngũ

```
# Loại một: nguyên mẫu đã tồn tại, các phiên dài mất kiểm soát (học Claude Code trước)
- [ ] Tuần 1: định nghĩa tập hợp trạng thái vòng lặp {messages, toolUseContext, compactTracking, turnCount}
- [ ] Tuần 1: mọi tool_use đều được đóng hoặc điền giả lập (synthetic-filled); đường dẫn hủy bỏ (abort path) được kết nối
- [ ] Tuần 2: bộ ba quản trị ngữ cảnh — các ngưỡng memory / collapse / autocompact được cố định trong bảng
- [ ] Tuần 2: xác minh độc lập với triển khai (verifier ≠ implementer)
- [ ] Tuần 3: vòng đời Agent phụ SubagentStart/Stop có thể quan sát được
Cửa kiểm soát (Gate): phiên làm việc liên tục 24 giờ không bị ngắt token, không có Agent phụ mồ côi (orphan subagents), hoặc rò rỉ tool_result

# Loại hai: quy tắc nhân lên, nguồn phân tán, ranh giới không rõ ràng (học Codex trước)
- [ ] Tuần 1: tất cả các chỉ dẫn trở thành các đoạn cắt (fragments) — khai báo cả ba: nhãn đánh dấu (marker), nguồn (source), độ ưu tiên (precedence)
- [ ] Tuần 1: công cụ được định kiểu schema với additional_properties=false
- [ ] Tuần 2: chính sách phê duyệt được đưa lên thành các quy tắc — deny/ask/allow có thể đánh giá độc lập
- [ ] Tuần 2: thiết lập thread.id / rollout; làm rõ {approvalPolicy, sandboxMode} ở cấp độ lượt chạy
- [ ] Tuần 3: các hook được chia thành pre/post/session_start/stop; các tài sản kỹ năng được cài đặt bằng fingerprint
Cửa kiểm soát (Gate): bất kỳ thay đổi quy tắc nào đều được thực hiện chỉ qua PR diff, không yêu cầu chỉnh sửa mã nguồn lúc chạy

# Loại ba: bắt đầu từ con số không (chọn một mâu thuẫn chính trước)
- [ ] Tuần 1: tuyên bố mâu thuẫn chính — "mô hình chạy hoang dã" hoặc "đội ngũ mất trật tự"
- [ ] Tuần 1: định nghĩa mô hình quyền tối thiểu (danh sách deny/ask cho các hành động rủi ro cao)
- [ ] Tuần 2: dựng khung xương ở phía mâu thuẫn chính (loop HOẶC fragment+thread, chọn một)
- [ ] Tuần 3: đưa phía còn lại lên mức khả thi tối thiểu (đường dẫn phục hồi HOẶC các hook cơ bản)
- [ ] Tuần 4: đưa vào 1–2 kỹ năng/công cụ; chứng minh vòng lặp đóng đầu-cuối (end to end)
Cửa kiểm soát (Gate): thành viên mới có thể thực hiện danh sách kiểm tra mà không cần sự hướng dẫn bằng lời nói từ tác giả ban đầu
```

## 8.3 Nên học gì từ Claude Code, và nên học gì từ Codex

Ưu tiên học Claude Code về: tư duy trạng thái (state mind-set) của vòng lặp truy vấn (query loop), nén bộ nhớ và quản trị ngữ cảnh, điều phối công cụ và xử lý ngắt, vòng đời của Agent phụ và tính độc lập của việc xác minh, coi các đường dẫn thất bại là đường dẫn chính. Ưu tiên học Codex về: phân mảnh chỉ dẫn (instruction fragmentation), schema công cụ, biểu thức rõ ràng của phê duyệt và chính sách, cơ sở hạ tầng cho luồng (thread) / rollout / trạng thái (state), các sự kiện hook và quản lý tài sản kỹ năng. Đây không phải là sự thỏa hiệp — nó giả định rằng bạn biết mình đang học cái gì. Lý do đúng đắn để vay mượn điều gì đó là vì nó khắc phục điểm yếu của bạn, chứ không phải vì người khác đã xây dựng nó.

<p>Mang các đánh giá quản trị ngữ cảnh từ tập đầu tiên vào các khung kiểm soát (harness) của bên thứ ba, chúng ta sẽ dễ dàng nhận diện ra một lộ trình phổ biến nhưng tốn kém. Lộ trình đó không phân chia ngữ cảnh thành các đơn vị có thời gian tồn tại, nhiệm vụ và chi phí đầu vào khác nhau. Thay vào đó, nó đóng gói tối đa các tệp khởi động (bootstrap files), mô tả kỹ năng, thiết lập danh tính và văn bản không gian làm việc vào prompt, sau đó dựa vào các chuỗi cắt ngắn (truncation), nén bộ nhớ (compaction) và phục hồi khi cửa sổ ngữ cảnh bị thu hẹp. Các hệ thống này có thể vẫn có bộ nhớ, kỹ năng, nén bộ nhớ, thậm chí là các giới hạn trên — nhưng trục quản trị vẫn là "tiêm trước, giải cứu sau" (inject first, rescue later). Một khi ngữ cảnh được tổ chức chủ yếu bằng cách xếp chồng văn bản, lãng phí token chỉ là chi phí đầu tiên; sự loãng tín hiệu (signal dilution) mới là chi phí sâu sắc hơn: mô hình nhìn thấy nhiều hơn, nhưng không nhất thiết phải rõ ràng hơn về ngữ nghĩa hoạt động nào quan trọng tiếp theo.</p>

<p>Ba lộ trình trong một dòng: Claude Code coi ngữ cảnh là bộ nhớ làm việc (những gì phải tồn tại, những gì cần được nén); Codex coi ngữ cảnh là các đơn vị có cấu trúc (loại nguồn, phạm vi, bàn giao trạng thái); họ OpenClaw (OpenClaw family) coi ngữ cảnh là một thùng chứa prompt (những gì khác có thể được đóng gói thêm vào trước khi đạt giới hạn). Đó là lý do tại sao các đội ngũ đi theo lộ trình thứ ba lúc đầu cảm thấy "đầy đủ thông tin hơn," sau đó phàn nàn về hai điều cùng một lúc — token tiêu tốn nhanh và chất lượng không tăng lên khi ngữ cảnh phình to. Nó đang giải quyết việc có thể chèn vào bao nhiêu, chứ không phải những gì phải được giữ lại để tiếp tục công việc.</p>

<p><img src="diagrams/diag-05-context-governance-three-paths.png" alt="Three-path comparison of context governance" /></p>

## 8.4 Một quan niệm sai lầm nguy hiểm: tính rõ ràng và tính linh hoạt không phải là kẻ thù tự nhiên của nhau

Các nhà xây dựng hệ thống thường dựa vào một sự đối lập sai lầm lười biếng. Nhắc đến "lớp điều khiển rõ ràng" (explicit control layer) và họ tưởng tượng ra một hệ thống nặng nề, chậm chạp, cứng nhắc; nhắc đến "tính linh hoạt của runtime" (runtime flexibility) và họ tưởng tượng rằng kinh nghiệm có thể chèo lái hệ thống ở hiện tại trong khi cấu trúc được trì hoãn. Cả hai bản năng đều không thông minh. Tính rõ ràng vốn dĩ không cứng nhắc, và tính linh hoạt vốn dĩ không hỗn loạn. Câu hỏi thực sự là bạn đã định nghĩa rõ ràng những gì bắt buộc phải rõ ràng và những gì có thể để lại cho phán đoán thực địa hay chưa. Thế mạnh của Claude Code không phải là bác bỏ cấu trúc mà là biết những rắc rối nào phải đối mặt bên trong runtime; thế mạnh của Codex không phải là từ chối tính linh hoạt mà là biết những ranh giới nào sẽ biến thành những cuộc tranh chấp vô tận nếu không được khai báo sớm. Một khung kiểm soát thứ ba tốt không cào bằng cả hai — nó phân biệt quy tắc nào phải được viết ra trước, phán đoán nào có thể giữ lại trong runtime, trạng thái nào phải bền vững và kinh nghiệm nào chỉ cần tồn tại bên trong bộ nhớ phiên (session memory).

## 8.5 Thứ tự hoạt động thực tế cho các nhà xây dựng sau này

Từ con số không, trình tự được khuyến nghị là: (1) các hành động có rủi ro cao và mô hình quyền tối thiểu; (2) vòng lặp chính (main loop) hoặc vòng đời luồng (thread lifecycle); (3) quản trị ngữ cảnh và đường dẫn phục hồi; (4) kỹ năng, quy tắc địa phương và hook; (5) đa Agent, khả năng nền tảng và hệ sinh thái phức tạp. Không hào nhoáng, nhưng gần như là thứ tự xuất hiện của các sự cố. Trong kỹ thuật, nhiều thứ tự thiết kế nên tuân theo thứ tự của thất bại, chứ không phải thứ tự của tính thẩm mỹ demo.

## 8.6 Kết luận chương

Chương này chỉ muốn để lại một câu nói giản dị:

> Học hỏi từ Claude Code chủ yếu để hiểu cách một hệ thống duy trì sự ổn định tại thực địa; học hỏi từ Codex chủ yếu để hiểu cách một hệ thống duy trì trật tự theo thời gian bên trong một tổ chức.

Những đội ngũ chỉ học theo cách thứ nhất có xu hướng trở nên giàu kinh nghiệm và nghèo thể chế.

Những đội ngũ chỉ học theo cách thứ hai có xu hướng tạo ra những thể chế thanh lịch và hành vi thực địa mong manh.

Nước đi tốt hơn không phải là chọn phe. Đó là quyết định khung xương nào mà hệ thống của bạn phải phát triển trước tiên dựa trên mâu thuẫn chính của nó.
