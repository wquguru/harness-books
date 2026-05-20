# Chương 1 Tại sao Kỹ nghệ Khung quản lý lại quan trọng

## 1.1 Vấn đề cốt lõi là giữ cho mô hình không đi lệch kịch bản

Một khi phân phối xác suất biết nói có thể chạm vào shell, Git, mạng và các tệp cục bộ, vấn đề sẽ chuyển dịch từ "câu trả lời không đủ tốt" sang "việc thực thi gây ra thiệt hại thực sự". Kỹ nghệ Khung quản lý (Harness Engineering) là việc giới hạn thành phần cốt lõi không ổn định đó vào một hệ thống có thể quản lý được. Nó giải quyết một thực tế thực tiễn: các mô hình mặc định không đáng tin cậy.

Nhận định đó không phải lúc nào cũng dễ nghe, nhưng nó thường rất hữu ích. Bỏ qua nó, và vấn đề thường sẽ tái xuất hiện trong nhật ký (log) và các báo cáo sự cố (incident report).

## 1.2 Lớp khung quản lý đầu tiên của Claude Code: hệ thống hội thoại có ràng buộc

Ở bề nổi, Claude Code trông giống như một CLI trò chuyện với người dùng và có thể vá mã nguồn. Xét về mặt triển khai, nó chưa bao giờ được thiết kế như một lớp vỏ bọc mô hình đơn thuần (bare model wrapper). Nó được thiết kế như một hệ thống hội thoại có ranh giới ngữ cảnh (context boundary), trạng thái runtime (runtime state) và các quy tắc hành vi (behavior rule).

Bạn có thể thấy điều này ngay lập tức trong cách tổ chức system prompt.

- Bắt đầu từ `src/constants/prompts.ts:175`, hệ thống định nghĩa danh tính và nhiệm vụ cấp cao nhất
- Bắt đầu từ `src/constants/prompts.ts:186`, nó bổ sung các quy tắc cấp hệ thống cho các công cụ (tool), quyền hạn (permission), lời nhắc (reminder) và nén ngữ cảnh (context compression)
- Bắt đầu từ `src/constants/prompts.ts:199`, nó bổ sung các ràng buộc kỹ thuật cho việc thực thi tác vụ, chẳng hạn như tránh các chỉnh sửa trái phép, không tự ý tuyên bố việc xác nhận (validation) đã hoàn thành khi thực tế chưa hoàn thành, và không tự bịa ra các lớp trừu tượng (abstraction) để cho thuận tiện

Hãy dừng lại ở điểm này. Nhiều cuộc thảo luận về prompt vẫn chỉ dừng lại ở mức độ tu từ của câu hỏi "bạn là loại trợ lý nào". Claude Code đặt prompt bên trong cấu trúc kiểm soát runtime (runtime control structure). Những đoạn văn bản này định nghĩa các ranh giới thực thi (execution boundary), hành vi thất bại (failure behavior) và trách nhiệm báo cáo (reporting responsibility).

Quan trọng hơn, prompt này được lắp ráp theo từng phân đoạn. Trong `getSystemPrompt()` tại `src/constants/prompts.ts:444`, các phần tĩnh và động được phân tách rõ ràng, với bộ nhớ (memory), ngôn ngữ, kiểu đầu ra (output style), các hướng dẫn MCP (MCP instructions) và scratchpad được chèn vào theo từng phần. Trong `src/utils/systemPrompt.ts:28`, prompt mặc định (default prompt), prompt tùy chỉnh (custom prompt), prompt tác nhân (agent prompt) và prompt nối thêm (appended prompt) sau đó được cấu thành thông qua các quy tắc ưu tiên rõ ràng.

Điều này phản ánh một thực tế kỹ thuật rõ ràng: một hệ thống tác nhân thực sự hữu dụng không thể dựa vào một "prompt vạn năng (universal prompt)" duy nhất để giải quyết mọi thứ. Nó phải chia việc kiểm soát thành các lớp, sau đó chia các lớp thành các trách nhiệm. Nếu không, mỗi lời nhắc và lệnh cấm mới sẽ nhanh chóng xung đột với những cái khác, và hành vi sẽ trở nên không thể dự đoán trước.

### Invariants: ba ràng buộc cứng trên mặt phẳng kiểm soát

```
assert prompt.layers ⊇ {default, project, custom, agent, append}    # danh tính ≠ runtime
assert ∀ tool_call t: scheduler.decides_concurrency(t) before exec(t) # các công cụ được lập lịch
assert on recoverable_error: route ∈ {recover, terminate_clean}      # lỗi thuộc đường dẫn chính
```

Khoảnh khắc mà bất kỳ điều nào trong số này bị bỏ qua, vòng lặp truy vấn (query loop), các công cụ (tool), ngữ cảnh (context) và các cơ chế phục hồi (recovery mechanisms) trong các chương sau đều bắt đầu trở nên đáng nghi ngờ.

## 1.3 Lớp khung quản lý thứ hai: tác nhân phụ thuộc vào một vòng lặp liên tục

Nếu prompt định nghĩa những gì nó nên là, vòng lặp truy vấn (query loop) định nghĩa cách nó thực sự chạy.

Cốt lõi của Claude Code không phải là một lượt gọi API riêng lẻ. Đó là `query()` bắt đầu từ `src/query.ts:219` và đặc biệt là `queryLoop()` bắt đầu từ `src/query.ts:241`. Điểm mấu chốt trong việc triển khai này là sự thừa nhận rõ ràng rằng các hệ thống tác nhân phụ thuộc vào việc thực thi nhiều lượt có lưu trạng thái (stateful multi-turn execution).

Tại `src/query.ts:268`, hệ thống đưa `messages`, `toolUseContext`, `autoCompactTracking`, `maxOutputTokensRecoveryCount`, `hasAttemptedReactiveCompact`, `pendingToolUseSummary`, `turnCount`, `transition`, và nhiều thông tin khác vào một đối tượng trạng thái xuyên qua các vòng lặp (cross-iteration state object). Khi một hệ thống hội thoại được thiết kế theo cách này, nó chính thức thừa nhận rằng các vấn đề chưa được giải quyết từ lượt trước sẽ đi vào lượt tiếp theo, và hệ thống phải tiếp tục từ đó.

Đó chính là tư duy cốt lõi của khung quản lý (harness mindset). Câu hỏi thực sự là liệu hành vi có duy trì tính nhất quán qua các lượt liên tục hay không:

- Có khái niệm ngân sách (budget) không?
- Có khái niệm phục hồi (recovery) không?
- Có cơ chế tự cứu (self-rescue mechanism) sau khi ngữ cảnh mở rộng không?
- Tác vụ có thể tiếp tục sau khi công cụ bị lỗi không?

Nếu không có các cấu trúc này, một tác nhân chỉ đơn thuần là một trình thực thi không ổn định.

Sau `src/query.ts:365`, vòng lặp cũng xử lý việc cắt lát tin nhắn (message slicing), ngân sách kết quả công cụ (tool result budget), cắt bớt lịch sử (history snip), nén vi mô (microcompact), thu gọn ngữ cảnh (context collapse) và tự động nén (autocompact) trước mỗi lượt gọi mô hình. Có rất nhiều chi tiết, nhưng chúng đều chỉ ra một điều: Claude Code cố gắng kéo quyền kiểm soát trở lại runtime trước khi gọi mô hình.

Đây là lý do tại sao Kỹ nghệ Khung quản lý (Harness Engineering) không thể bị giản lược thành kỹ nghệ prompt (prompt engineering). Kỹ nghệ Khung quản lý quản trị các máy trạng thái (state machine); kỹ nghệ prompt quản trị cách dùng từ. Cách dùng từ rất quan trọng, nhưng máy trạng thái mới quyết định ai chịu trách nhiệm về hành vi.

## 1.4 Lớp khung quản lý thứ ba: các lượt gọi công cụ phải tuân thủ kỷ luật lập lịch

Khi một mô hình chỉ có thể xuất ra văn bản, trường hợp xấu nhất là nó nghe có vẻ quá tự tin. Một khi nó có thể gọi các công cụ, rủi ro sẽ chuyển dịch từ rủi ro tu từ sang rủi ro thực thi. Khi đó, câu hỏi then chốt là: ai quyết định cách thức chạy của các công cụ?

Câu trả lời của Claude Code rất trực diện. Runtime chọn thực thi song song (parallel execution) hoặc tuần tự (serial execution) tùy thuộc vào các thuộc tính của công cụ.

Trong `runTools()` tại `src/services/tools/toolOrchestration.ts:19`, các lượt gọi công cụ trước tiên được nhóm lại bởi `partitionToolCalls()`. Tại `src/services/tools/toolOrchestration.ts:91`, hệ thống đọc schema của công cụ và gọi `isConcurrencySafe()` để quyết định xem một công cụ có an toàn khi thực thi song song hay không. Các lượt gọi an toàn đồng thời (concurrency-safe) sẽ chạy theo lô (batch); các lượt gọi không an toàn sẽ chạy từng cái một. Trong các đường dẫn song song, các bộ sửa đổi ngữ cảnh (context modifier) trước tiên được đưa vào bộ đệm (buffer) và sau đó được phát lại (replay) theo đúng thứ tự khối ban đầu, xem từ `src/services/tools/toolOrchestration.ts:31` đến `:63`.

Đây là một ví dụ mang tính đại diện. Nó cho thấy Claude Code không coi các công cụ là sự mở rộng tự nhiên của năng lực mô hình, mà là các đơn vị thực thi được quản lý đòi hỏi kỷ luật lập lịch. Một hệ thống công cụ không có kỷ luật lập lịch chỉ làm khuếch đại tính không ổn định của mô hình ra thế giới bên ngoài.

Tính song song không bị ràng buộc làm tăng bán kính ảnh hưởng của thiệt hại (blast radius). Claude Code áp dụng một chiến lược thận trọng ở đây. Trong các môi trường chạm vào tệp, terminal và các ranh giới quyền hạn, sự thận trọng đó thường đáng tin cậy hơn.

## 1.5 Lớp khung quản lý thứ tư: công cụ nguy hiểm nhất cần những quy tắc nghiêm ngặt nhất

Trong tất cả các công cụ, Bash là công cụ đáng ngờ vực nhất. Nó hầu như không có ranh giới miền: nó có thể chạm trực tiếp vào các tệp, tiến trình, mạng và kho lưu trữ Git, chưa kể đến ngữ nghĩa chuyển hướng shell (shell redirection) và đường ống (pipeline). Bất kỳ hệ thống nào quá tin tưởng vào Bash thường sẽ nhận lại những hậu quả cụ thể.

Lập trường của Claude Code rất rõ ràng trong `src/tools/BashTool/prompt.ts:42` và các dòng dưới. Nó chứa các quy tắc vận hành mở rộng, đặc biệt là xung quanh Git và PR: không tùy ý sửa đổi cấu hình git, không bỏ qua các hook, không sử dụng `git add .` một cách tùy tiện, không sử dụng `--amend` để gộp các commit trước đó sau khi gặp lỗi pre-commit, không commit trừ khi được yêu cầu rõ ràng, và không mặc định đẩy mã nguồn (push).

Một số người gọi điều này là quá chi tiết. Nhưng các giao diện rủi ro cao thường đòi hỏi các ràng buộc mật độ cao. Một khi Bash đi vào luồng công việc thực tế, nhiều quy tắc bắt buộc phải được nêu rõ ràng.

Một nguyên lý cốt lõi của Kỹ nghệ Khung quản lý (Harness Engineering) là đóng gói năng lực rủi ro cao dưới dạng năng lực có ràng buộc cao. Năng lực càng mạnh thì sự kiểm soát càng phải tinh tế. Các hệ thống bên ngoài không tha thứ cho một lần thực thi tồi chỉ vì giọng điệu của mô hình nghe có vẻ tự tin.

## 1.6 Lớp khung quản lý thứ năm: lỗi là một phần của đường dẫn chính

Nhiều hệ thống phần mềm coi các đường dẫn thất bại là các ngoại lệ và đường dẫn thành công là nội dung chính. Các hệ thống tác nhân không thể làm như vậy. Các thất bại ở đây không phải là thỉnh thoảng mới xảy ra; chúng hiện diện một cách có cấu trúc. Các mô hình chạm giới hạn token, kích hoạt `prompt too long` (prompt quá dài), chạm `max_output_tokens` (mã báo hiệu đầu ra tối đa), đối mặt với việc bị từ chối công cụ, người dùng ngắt quãng, hook bị chặn, các lượt thử lại API, và nhiều vấn đề khác. Nếu tất cả các vấn đề này chỉ được xử lý như các khối `catch` được thêm vào sau, hệ thống trông có vẻ như đang hoạt động nhưng thực chất đang liên tục đẩy rắc rối về phía trước.

Claude Code không làm điều này trong vòng lặp truy vấn (query loop). Hãy xem cách xử lý tự động nén (autocompact) sau `src/query.ts:453`, và các chú thích xung quanh giới hạn ngữ cảnh cũng như logic chặn sau `src/query.ts:592`: các thất bại được xử lý như các điều kiện cấu trúc thường trực.

Đây là một sự khác biệt lớn giữa khung quản lý (harness) và các trợ lý thông thường. Các trợ lý thông thường thường làm theo kiểu "trả lời trước, xin lỗi nếu sai". Khung quản lý nhấn mạnh ràng buộc trước, thực thi sau; và nếu xảy ra lỗi, hãy điều hướng qua các đường dẫn phục hồi chứ không ứng biến tùy tiện.

Một hệ thống biết xin lỗi chưa chắc đã trưởng thành. Một hệ thống biết khi nào không nên bắt đầu, khi nào nên thử lại, khi nào nên chấm dứt và cách báo cáo lỗi chính xác mới là hệ thống gần hơn với sự trưởng thành.

## 1.7 Nguyên lý đầu tiên có thể trích xuất từ nguồn

Cho đến lúc này, Chương 1 thực sự chỉ nói lên một điều:

> Năng lực then chốt của một hệ thống tác nhân là việc thực thi có ràng buộc.

Mã nguồn Claude Code cũng chỉ ra cùng một kết luận ở các vị trí quan trọng:

- `constants/prompts.ts` cho thấy prompt là một phần của mặt phẳng kiểm soát (control plane), chứ không phải là đồ trang trí tính cách
- `utils/systemPrompt.ts` cho thấy hành vi phải tuân theo sự ưu tiên phân lớp rõ ràng
- `query.ts` cho thấy runtime của tác nhân phụ thuộc vào trạng thái vòng lặp liên tục, chứ không phải Q&A một lần duy nhất
- `services/tools/toolOrchestration.ts` cho thấy các lượt gọi công cụ phải tuân thủ kỷ luật lập lịch
- `tools/BashTool/prompt.ts` cho thấy các công cụ rủi ro cao đòi hỏi các ràng buộc mật độ cao

Nhìn chung, Kỹ nghệ Khung quản lý không hề bí ẩn. Nó chỉ nhấn mạnh vào những lẽ thường tình trong kỹ nghệ vốn thường bị bỏ qua:

- Các mô hình luôn mắc sai lầm
- Các công cụ khuếch đại hậu quả
- Ngữ cảnh luôn mở rộng
- Trạng thái làm ô nhiễm các lượt tiếp theo
- Người dùng ngắt quãng
- Các thất bại tái diễn

Vì thế, các hệ thống không thể duy trì trật tự thông qua "sự thông minh". Chúng duy trì trật tự thông qua cấu trúc. Cấu trúc ít hào nhoáng hơn sự thông minh, nhưng thường đáng tin cậy hơn.

Chương tiếp theo sẽ chuyển sang lớp dễ bị hiểu lầm nhất trong cấu trúc này: system prompt. Nhiều người coi nó như văn bản tính cách (persona text). Chúng tôi sẽ chỉ ra rằng nó gần giống với chính sách quy chế (institutional policy) trong một hệ điều hành hơn. Tính cách cải thiện cảm giác; chính sách ràng buộc máy móc.
