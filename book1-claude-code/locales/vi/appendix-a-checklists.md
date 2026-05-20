# Phụ lục A Bảng kiểm (Checklists): Biến các Nguyên lý thành Ràng buộc có thể Thực thi

Previous chapters discussed principles. If principles cannot be turned into checklists, they often decay into judgments that sound right but do not hold up in practice. This appendix turns easy-to-say, hard-to-sustain judgments into directly usable lists.

Các chương trước đã thảo luận về các nguyên lý. Nếu các nguyên lý không thể chuyển hóa thành các bảng kiểm (checklists), chúng thường suy giảm thành các nhận định nghe có vẻ đúng nhưng không đứng vững trong thực tế. Phụ lục này chuyển đổi các nhận định dễ nói nhưng khó duy trì thành các danh sách có thể sử dụng trực tiếp.

Những bảng kiểm này không đảm bảo sự cải tiến tự động. Chúng chủ yếu ngăn ngừa các lỗi phổ biến và lặp đi lặp lại tái diễn. Trong kỹ thuật, nhiều sự cải tiến đến từ việc ít lặp lại các lỗi có thể tránh được.

## A.1 Bảng kiểm thiết kế Agent runtime

Nếu một AI coding agent chuẩn bị được đưa vào quy trình kỹ thuật thực tế, nó nên trả lời được ít nhất các câu hỏi:

- Có vòng lặp truy vấn (query loop) rõ ràng thay vì coi mỗi lượt hội thoại là một phiên Hỏi & Đáp cô lập hay không?
- Có đối tượng trạng thái liên lượt (cross-turn state object) ghi lại các thông tin khôi phục, ngân sách, rút gọn, các hook và bộ đếm lượt hội thoại hay không?
- Kết quả đầu ra của mô hình được xử lý dưới dạng dòng sự kiện (event stream) thay vì một khối văn bản hoàn chỉnh hay không?
- Các cuộc gọi công cụ bị ngắt có thể được đóng lại bằng các kết quả tổng hợp để giữ cho sổ cái thực thi (execution ledger) hoàn chỉnh hay không?
- Sự hoàn thành, thất bại, khôi phục và tiếp tục có được mô hình hóa thành các ngữ nghĩa dừng khác nhau hay không?
- Có lập ngân sách ngữ cảnh cho các phiên làm việc dài, thay vì chỉ xử lý khẩn cấp tạm thời sau khi bị tràn hay không?

Nếu hai hoặc ba câu hỏi trong số này không thể được trả lời rõ ràng, hệ thống có khả năng vẫn đang ở giai đoạn "chỉ có thể demo" chứ chưa đạt đến giai đoạn "có thể vận hành quy trình".

## A.2 Bảng kiểm thiết kế Prompt

Prompt hệ thống không nên chỉ đơn thuần là dài. Nó nên được phân lớp với các nhiệm vụ rõ ràng.

Tối thiểu, hãy kiểm tra:

- Danh tính, quy tắc hành vi, ràng buộc công cụ và kỷ luật đầu ra có được tổ chức riêng biệt hay không?
- Thứ tự ưu tiên của nguồn prompt có rõ ràng không (mặc định, dự án, tùy chỉnh, nối thêm, đặc thù của agent)?
- Các thao tác nguy hiểm, hành vi trái phép và kỷ luật xác minh có được viết thành các quy tắc rõ ràng thay vì các gợi ý mơ hồ hay không?
- Prompt có được giải phóng khỏi các nhiệm vụ thuộc về sự thực thi của runtime (runtime enforcement) hay không?
- Nhóm có thể bảo trì nó một cách ổn định, thay vì nối thêm văn bản khẩn cấp sau mỗi lỗi phát sinh hay không?

Một bài kiểm tra thực tế: nếu việc loại bỏ một phần gây ra sự thay đổi cấu trúc hành vi, phần đó có khả năng là logic mặt phẳng điều khiển (control-plane) thực sự. Nếu hành vi hầu như không thay đổi, nó có thể chỉ là vật trang trí.

## A.3 Bảng kiểm thiết kế Công cụ và Phân quyền

Bất kỳ hệ thống nào cho phép mô hình chạm vào thế giới bên ngoài trước tiên nên tự hỏi:

- Các lệnh gọi công cụ có đi qua lớp điều phối thống nhất (unified orchestration) thay vì cuộc gọi mô hình trực tiếp hay không?
- Tính đồng thời có đòi hỏi bằng chứng an toàn rõ ràng thay vì mặc định cho phép hay không?
- Có sự rẽ nhánh ngữ nghĩa kiểu `allow / deny / ask` hay không?
- Các công cụ có rủi ro cao có được đối xử như các trường hợp đặc biệt thay vì giống hệt các công cụ thông thường hay không?
- Các ngắt, rút lui (fallbacks) và lỗi đồng cấp có thể tạo ra các ngữ nghĩa đóng rõ ràng hay không?
- Việc thực thi có thể bảo toàn chuỗi nhân quả và tránh các khối `tool_use` lửng lơ hay không?

Nếu `Bash` và `ReadTool` được quản trị gần như giống hệt nhau, thì hiểu biết về rủi ro thường là không đầy đủ.

## A.4 Bảng kiểm quản trị ngữ cảnh

Bất kỳ agent phiên làm việc dài nào cuối cùng cũng sẽ bị kỷ luật bởi các giới hạn ngữ cảnh. Quản trị sớm sẽ ít tốn kém hơn.

Tối thiểu, hãy kiểm tra:

- Các quy tắc lâu dài, bộ nhớ bền vững, tính liên tục của phiên và đối thoại tạm thời có được phân lớp hay không?
- Có sự phân tách rõ ràng giữa các tệp điểm bắt đầu (entrypoint) và các tệp phần thân (body) để ngăn ngừa phình to chỉ mục hay không?
- Có ngân sách token cho bộ nhớ, bộ nhớ phiên và tệp đính kèm kỹ năng hay không?
- Không gian đầu ra rút gọn có được dự phòng trước thay vì đợi cho đến khi cửa sổ đầy hay không?
- Sau khi rút gọn, các ngữ nghĩa công việc có được khôi phục (kế hoạch, kỹ năng, các tệp chính, trạng thái công cụ) hay không?
- Có chiến lược khôi phục khi bản thân quá trình rút gọn thất bại hay không?

Các hệ thống có sự quản trị ngữ cảnh tốt thường trông có vẻ hơi đạm bạc. Sự đạm bạc đó thường lại là một thế mạnh.

## A.5 Bảng kiểm khôi phục lỗi

Thiết kế khôi phục có hai kiểu thất bại phổ biến: không thiết kế gì, và thiết kế vòng lặp chết (dead-loop).

Tối thiểu, hãy kiểm tra:

- Các lỗi có thể khôi phục có được định tuyến đến các nhánh khôi phục trước khi bị đẩy ngay ra ngoài hay không?
- Các lộ trình khôi phục có được phân lớp từ mức độ tàn phá thấp đến cao hay không?
- Có các chốt bảo vệ ngăn chặn việc rút gọn phản ứng (reactive-compact), các vòng lặp stop-hook và thử lại cắn xé lẫn nhau hay không?
- Sau lỗi `max_output_tokens`, việc tiếp tục có được ưu tiên hơn tóm tắt lại hay không?
- Các hoạt động khôi phục tự động có bao gồm bộ đếm, giới hạn số lần thử lại và cầu dao ngắt mạch hay không?
- Các ngắt có được đối xử như các trạng thái lỗi yêu cầu đóng ngữ nghĩa hay không?

Một hệ thống khôi phục không bao giờ dừng lại cũng nguy hiểm như một hệ thống khôi phục không bao giờ bắt đầu.

## A.6 Bảng kiểm đa agent

Thiết kế đa agent nên tổ chức lại sự không chắc chắn, chứ không phải nhân lên sự bối rối. Hãy kiểm tra:

- Thiết kế phân nhánh (fork) có bảo toàn tính nhất quán của bộ đệm prompt (prompt-cache) thông qua các tham số an toàn cache hay không?
- Trạng thái có thể thay đổi có được cô lập theo mặc định cho các agent con hay không?
- Các vai trò nghiên cứu, triển khai, xác minh và tổng hợp có được phân tách rõ ràng hay không?
- Điều phối viên có thực sự tổng hợp thay vì chỉ chuyển tiếp kết quả của worker hay không?
- Xác minh có độc lập với triển khai hay không?
- Vòng đời của agent có thể quan sát, có thể ngắt và có thể thu hồi hay không?
- Lệnh hủy từ parent có lan truyền đến các child để ngăn chặn các tác vụ mồ côi hay không?

Nếu một hệ thống tự xưng là đa agent nhưng tất cả các agent đều làm công việc tương tự nhau và không có ai sở hữu khâu tổng hợp hoặc xác minh, thì đó thường là sự hỗn loạn được chạy song song.

## A.7 Bảng kiểm áp dụng trong nhóm

Sự hiểu sai phổ biến nhất khi triển khai là nhầm lẫn giữa sự thành thạo cá nhân với sự trưởng thành của thể chế.

Trước khi triển khai, hãy xác minh:

- Tệp `CLAUDE.md` phân lớp có hoạt động, với hướng dẫn rõ ràng về những gì thuộc về và không thuộc về nó hay không?
- Định nghĩa xác minh có được chuẩn hóa trước khi nhân rộng số lượng kỹ năng hay không?
- Ranh giới phê duyệt có được phân tầng theo hệ quả và tính nhạy cảm của môi trường hay không?
- Các thể chế chính có được gắn vào thời điểm hook thích hợp thay vì nhồi nhét vào các tài liệu tĩnh hay không?
- Bản ghi hội thoại, đầu ra tác vụ và các sự kiện hook có được giữ lại làm bằng chứng phát lại hay không?
- Có chính sách bảo trì cho bộ nhớ cũ, các quy tắc lỗi thời và các kỹ năng không còn giá trị hay không?

Các nhóm có thể sử dụng agent một cách bền vững thường là các nhóm nơi các thành viên bình thường có thể vận hành chính xác bên trong các thể chế, chứ không phải các nhóm phụ thuộc vào một vài chuyên gia.

## A.8 Bộ câu hỏi soát xét

Để soát xét một đề xuất AI coding-agent, hãy hỏi trực tiếp:

- Những hành vi nào được ràng buộc bởi prompt và những hành vi nào được thực thi bởi runtime?
- Ai chặn việc lạm dụng công cụ, và ở lớp nào?
- Khi nào ngữ cảnh được rút gọn, và các ngữ nghĩa công việc được xây dựng lại như thế nào sau đó?
- Làm thế nào lỗi `prompt-too-long` và `max-output-tokens` được khôi phục khác nhau?
- Sau khi bị ngắt, tính nhất quán của bản ghi hội thoại được duy trì thế nào với các kết quả công cụ?
- Trong các luồng đa agent, ai sở hữu khâu tổng hợp và ai sở hữu khâu xác minh?
- Quá trình khôi phục lỗi có bao gồm cầu dao ngắt mạch và chốt chặn chống vòng lặp vô hạn hay không?
- Làm thế nào nhóm có thể kiểm toán những gì agent đã làm và tại sao?

Nếu các câu trả lời thường xuyên thu hẹp lại thành "chúng ta có thể thêm vào sau", runtime đó nhiều khả năng là vẫn chưa thực sự được thiết kế.

## A.9 Bảng kiểm ngắn cuối cùng

Nếu tất cả những điều trên cảm thấy quá dài, hãy giữ lại sáu điều này: thiết kế quyền hạn trước năng lực; rollback trước quyền tự trị; xác minh trước khi giao sản phẩm; ngân sách ngữ cảnh trước đối thoại dài; vòng đời trước đa agent; thể chế trước khi mong đợi sự thành thạo của nhóm. Đáp ứng được chúng không đảm bảo sự xuất sắc; nhưng thiếu chúng thường có nghĩa là hệ thống chỉ đơn giản là chưa thất bại mà thôi.

## A.10 Các mầm triển khai (pseudocode stubs)

Các khung xương từ các chương trước được thu gọn lại thành các điểm khởi đầu có thể tái sử dụng. Các dạng đầy đủ nằm trong các chương tương ứng; phần này chỉ giữ lại bộ xương sống tối giản.

### A.10.1 queryLoop (khung xương, trích từ Chương 3)

```
state = { messages, toolUseContext, autoCompactTracking, turnCount, transition, ... }
while not done(state):
    govern_input(state)                 // memory / cắt xén / thu hẹp / tự động rút gọn
    events = stream_model(state)
    for e in events:
        if e.is(tool_use): schedule(e, state.toolUseContext)
        if e.is(api_error): return surface(e)
    if interrupted: drain_tools_with_synthetic_results(state); break
    state = advance(state, recover_if_needed(state))
assert state.turnCount monotonic ∧ every tool_use has tool_result
```

### A.10.2 Quyết định phân quyền (khung xương, trích từ Chương 4)

```
decision = hasPermissionsToUseTool(tool, input, ctx)
match decision:
    allow: exec(tool, input)
    deny:  reject(reason)
    ask:   route_to(coordinator | worker | classifier | interactive)
assert decision ∈ {allow, deny, ask}        # ba giá trị, không bao giờ co hẹp
assert ask never auto-escalates to allow    # không tự động leo thang trái phép
```

### A.10.3 forkAgent (khung xương, trích từ Chương 7)

```
params = CacheSafeParams { systemPrompt, userContext, systemContext, toolUseContext, forkContextMessages }
ctx    = createSubagentContext(parent)       // trạng thái có thể thay đổi được cô lập theo mặc định
hooks.fire(SubagentStart, { agent_id, agent_type })
defer hooks.fire(SubagentStop, { agent_transcript_path })
assert parent.abort ⇒ propagate(child.abort)
```

### A.10.4 recoverFromError (khung xương, trích từ Chương 6)

```
on recoverable_error(e):
    if e.is(prompt_too_long):
        if stagedCollapse > 0: recoverFromOverflow()
        elif not hasAttemptedReactiveCompact: tryReactiveCompact()
        else: surface(e); skip_stop_hooks()
    if e.is(max_output_tokens):
        if cap < MAX: raise(maxOutputTokensOverride); retry()
        else: append(meta_continue_msg); retry()
assert consecutiveFailures < MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES
```
