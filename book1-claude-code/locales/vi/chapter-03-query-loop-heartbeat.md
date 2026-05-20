# Chương 3 Vòng lặp Truy vấn (Query Loop): Nhịp đập của một Hệ thống Agent

## 3.1 Để đánh giá mức độ trưởng thành, trước tiên hãy hỏi xem hệ thống có vòng lặp hay không

Hình dung một mô hình viết mã nguồn như một API Hỏi & Đáp (Q&A API) được nâng cấp là sai lầm dễ mắc phải nhất: một khi hệ thống bắt đầu gọi công cụ (calling tools), kéo dài qua nhiều lượt (spanning turns), xử lý ngắt (handling interrupts), duy trì trạng thái (persisting state) và rút gọn ngữ cảnh (compacting context), mô hình Hỏi & Đáp một lần (one-shot Q&A) sẽ sụp đổ. Claude Code thừa nhận về mặt cấu trúc rằng các agent phụ thuộc vào việc thực thi liên tục và có trạng thái (stateful execution).

Hàm `query()` tại `src/query.ts:219` là lớp vỏ ngoài (shell); `queryLoop()` tại `src/query.ts:241` là cốt lõi. Nó duy trì trạng thái giữa các lần lặp (cross-iteration state), thực hiện quản trị trước (pre-governance), truyền phát (stream) kết quả đầu ra của mô hình, sau đó quyết định xem có thực thi các công cụ, khôi phục, rút gọn, tiếp tục hay chấm dứt.

![Claude Code Query Loop Core](diagrams/diag-ch03-01-query-loop-core.png)

Từ khóa quan trọng ở đây là vòng đời (lifecycle). Việc một hệ thống có xứng đáng được gọi là agent hay không phụ thuộc ít hơn vào cách nó nói chuyện, mà phụ thuộc nhiều hơn vào việc liệu nó có còn biết mình đang làm gì sau vài lượt hội thoại hay không.

## 3.2 Trạng thái (State) là hoạt động cốt lõi, không phải gánh nặng

Nhiều hệ thống ban đầu coi trạng thái như một gánh nặng và coi tính phi trạng thái (statelessness) là sự thanh lịch. Đối với các hệ thống agent, sở thích này có giá trị hạn chế. Một khi agent đi vào các quy trình làm việc thực tế, trạng thái sẽ xuất hiện một cách tự nhiên. Bỏ qua trạng thái không làm mất đi nó; nó chỉ khiến nó quay trở lại dưới một dạng khó quản lý hơn.

Claude Code thể hiện rất rõ ràng ở điểm này. Từ `src/query.ts:203` đến `:217`, trạng thái có thể thay đổi của vòng lặp truy vấn (mutable query-loop state) được định nghĩa một cách rõ ràng:

- messages
- toolUseContext
- autoCompactTracking
- maxOutputTokensRecoveryCount
- hasAttemptedReactiveCompact
- pendingToolUseSummary
- stopHookActive
- turnCount
- transition

Tại `src/query.ts:268`, các thuộc tính này được tập hợp thành một đối tượng `State` khi vòng lặp truy vấn bắt đầu, và được cập nhật toàn bộ thông qua các nhánh tiếp tục (continue branches).

Claude Code không phân tán việc khôi phục (recovery), rút gọn (compaction), ngân sách (budget), các hook và việc đếm lượt (turn counting) ra các biến boolean cục bộ tạm thời. Các tập lệnh (scripts) chỉ hỏi xem bước này đã kết thúc chưa. Các hệ thống agent còn phải hỏi xem liệu bước tiếp theo có thể tiếp tục từ trạng thái được để lại bởi một bước bị lỗi hay không.

### Khung xương (Skeleton): queryLoop()

```
// skeleton: queryLoop()  (src/query.ts:203–1305)
state = { messages, toolUseContext, autoCompactTracking,
          maxOutputTokensRecoveryCount, hasAttemptedReactiveCompact,
          pendingToolUseSummary, stopHookActive, turnCount, transition }

while not done(state):
    govern_input(state)                 // nạp trước / cắt bớt / vi rút gọn / thu gọn / tự động rút gọn
    events = stream_model(state)
    for e in events:
        if e.is(tool_use):  schedule(e, state.toolUseContext)
        if e.is(api_error): return surface(e)
    if interrupted:
        drain_tools_with_synthetic_results(state); break
    state = advance(state, recover_if_needed(state))

assert state.turnCount_{t+1} >= state.turnCount_t            # trạng thái là đơn điệu (monotonic)
assert every emitted tool_use has a matching tool_result     # sổ cái được đóng (ledger is closed)
assert hasAttemptedReactiveCompact ⇒ no further compact      # không lặp vô tận (no self-loop)
```

## 3.3 Nhiệm vụ đầu tiên của vòng lặp truy vấn là quản trị đầu vào

Từ bên ngoài nhìn vào, mọi người thường cho rằng hành động cốt lõi của một agent là "gọi mô hình". Trong kỹ thuật, điều quan trọng hơn thường là sự chuẩn bị lâu dài trước cuộc gọi đó. Claude Code thể hiện điều này một cách rõ ràng trong `queryLoop()`.

Trước khi bước vào giai đoạn mô hình, runtime thực hiện tất cả các việc sau:

- Bắt đầu nạp trước bộ nhớ (memory prefetch), xem `src/query.ts:297`
- Nạp trước phát hiện kỹ năng (skill discovery), xem `src/query.ts:323`
- Cắt các tin nhắn hợp lệ sau ranh giới rút gọn (compact boundary), xem `src/query.ts:365`
- Áp dụng ngân sách kết quả công cụ (tool result budget), xem `src/query.ts:369`
- Thực hiện cắt bớt lịch sử (history snip), xem `src/query.ts:396`
- Thực hiện vi rút gọn (microcompact), xem `src/query.ts:412`
- Thực hiện thu gọn ngữ cảnh (context collapse), xem `src/query.ts:428`
- Thử tự động rút gọn (autocompact) cuối cùng, xem `src/query.ts:453`

Trình tự này tự nó đã là một tuyên ngôn về kiến trúc. Nó cho bạn biết Claude Code đặt việc quản trị ngữ cảnh (context governance) lên trước lập luận của mô hình. Nói cách khác, nó không giao phó việc "biến hỗn loạn thành trật tự" cho mô hình. Runtime quản trị trước, sau đó chuyển đầu vào sạch hơn cho mô hình.

Điều này rất quan trọng vì nhiều hệ thống làm ngược lại: nhồi nhét ngữ cảnh khổng lồ vào, rồi hy vọng mô hình sẽ quyết định điều gì là quan trọng. Điều đó có vẻ tiện lợi nhưng lại chuyển trách nhiệm của runtime sang cho các phân phối xác suất.

Claude Code áp dụng một tư thế kỹ thuật truyền thống hơn: dọn sạch thực địa trước, sau đó mới thực thi. Cách này kém thanh lịch hơn, nhưng thường ổn định hơn.

## 3.4 Gọi mô hình (Model invocation) chỉ là một giai đoạn của vòng lặp, không phải bản thân vòng lặp

Chỉ sau các bước quản trị đó, Claude Code mới tiến hành gọi mô hình, vào khoảng `src/query.ts:652`. Có một chi tiết đáng lưu ý: kết quả đầu ra được tiêu thụ bằng luồng truyền phát `for await` (streaming), chứ không phải là một phản hồi hoàn chỉnh đồng bộ.

Điều đó có nghĩa là đầu ra của mô hình trong Claude Code là một luồng sự kiện (event stream), chứ không chỉ là văn bản phản hồi cuối cùng. Các sự kiện có thể bao gồm:

- văn bản của trợ lý (assistant text)
- các khối `tool_use` (sử dụng công cụ)
- cập nhật mức độ sử dụng (usage updates)
- lý do dừng (stop reasons)
- các lỗi API (API errors)

Điều này đặc biệt rõ ràng sau `src/query.ts:826`. Hệ thống lưu trữ các tin nhắn của trợ lý, trích xuất các khối `tool_use`, quyết định các nhu cầu tiếp theo và có thể gửi các tác vụ công cụ tới trình thực thi công cụ truyền phát `StreamingToolExecutor` trong khi quá trình truyền phát vẫn đang diễn ra.

Về mặt kỹ thuật, đây là một sự dịch chuyển cấu trúc. Một khi đầu ra trở thành luồng sự kiện, kiến trúc không còn là yêu cầu-phản hồi đơn thuần nữa, mà là một quy trình điều phối-lập lịch-phản hồi (drive-schedule-feedback process). Truyền phát không chỉ là để nhìn thấy các từ sớm hơn; nó cho phép runtime lập lịch cho các hành động tiếp theo trước khi đầu ra của mô hình kết thúc hoàn toàn.

Đó là lý do tại sao vòng lặp truy vấn, chứ không phải lệnh gọi mô hình, mới là nhịp đập. Lệnh gọi mô hình chỉ là một nhịp co bóp bên trong nhịp đập đó. Thứ giữ cho hệ thống sống sót là toàn bộ chu kỳ: tiếp nhận đầu vào, tiêu thụ luồng truyền phát, lập lịch công cụ, khôi phục khi thất bại và tiếp tục lượt hội thoại.

## 3.5 Một nhịp đập phải xử lý được các ngắt (interrupts), nếu không nó chỉ là quán tính

Một nhịp đập thực sự không chỉ tiếp tục đập, nó còn có thể dừng lại khi cần thiết. Nếu nó không thể dừng lại, những gì còn lại chỉ là quán tính.

Claude Code xử lý ngắt (interrupts) rất cụ thể. Sau `src/query.ts:1011`, việc hủy truyền phát (streaming abort) được xử lý trước tiên. Nếu `streamingToolExecutor` đang hoạt động, các kết quả còn lại phải được tiêu thụ và các kết quả công cụ tổng hợp (synthetic tool results) phải được tạo ra, để các khối `tool_use` đã phát ra không bị bỏ lại mà không có kết quả đi kèm tương ứng. Nếu không, `yieldMissingToolResultBlocks()` sẽ lấp đầy các bản ghi ngắt bị thiếu.

Điều này tuân theo một nguyên lý kỹ thuật cơ bản: một khi hệ thống đã cam kết thực thi ra bên ngoài, việc ngắt vẫn đòi hỏi phải đóng sổ cái (ledger closure). Bạn không thể giả vờ như các cuộc gọi `tool_use` trước đó chưa từng xảy ra chỉ vì người dùng đã thực hiện ngắt sau đó. Các hệ thống bên ngoài, giao diện người dùng (UI) và bản ghi hội thoại (transcripts) cần một chuỗi nhân quả (causal chain) nhất quán. Ngay cả trạng thái "bị ngắt" cũng phải là một sự ngắt hoàn chỉnh.

Điều này quan trọng bởi vì một khi agent đi vào chế độ đa công cụ (multi-tool), đa lượt (multi-turn), các kỳ vọng bên ngoài sẽ nhiều hơn là "nó có trả lời không". Hệ thống phải để lại các dấu vết có thể giải thích được. Các dấu vết không thể giải thích được cuối cùng sẽ trở thành các vấn đề về vận hành, vấn đề kiểm toán hoặc các trách nhiệm pháp lý tiềm ẩn của nhóm mà không ai có thể giải thích.

Do đó, xử lý ngắt là nhiệm vụ cốt lõi của runtime. Các hành động đã bắt đầu cần được đóng lại, ngay cả khi việc đóng đó có nghĩa là "chưa hoàn thành".

## 3.6 Một nhịp đập cũng phải có khả năng khôi phục, nếu không nó chỉ là sự lặp lại mỏng manh

Nếu ngắt là các cú sốc bên ngoài, thì khôi phục là dự phòng nội bộ (internal slack). Các vòng lặp không có khả năng khôi phục cuối cùng sẽ để lộ một khuyết điểm phổ biến: họ coi sự may mắn là thiết kế.

Cơ chế khôi phục của Claude Code được phân lớp, chứ không phải là thử lại (retry) một cách đơn giản. Prompt quá dài (prompt-too-long) và số lượng token đầu ra tối đa (max-output-tokens) là các trường hợp điển hình.

Sau `src/query.ts:1065`, hệ thống kiểm tra xem tin nhắn cuối cùng của trợ lý có phải là một lỗi `prompt quá dài` (prompt too long) bị giữ lại hay không. Nếu có, trước tiên nó cố gắng đẩy ra (flush) các thu gọn ngữ cảnh (context collapse) đã được chuẩn bị sẵn (từ `:1086` đến `:1116`); nếu vẫn không đủ, nó sẽ bước vào giai đoạn rút gọn phản ứng (reactive compact) (từ `:1119` đến `:1166`). Do đó, việc khôi phục tiến hành từ mức chi phí thấp hơn và ít tính phá hủy hơn lên cao.

Lỗi `max_output_tokens` được xử lý tương tự. Sau `src/query.ts:1185`, runtime trước tiên cố gắng tăng giới hạn token; nếu vẫn không đủ, nó sẽ nối thêm một tin nhắn meta yêu cầu mô hình tiếp tục chính xác từ điểm bị cắt ngắn, không xin lỗi, không tóm tắt lại hoặc viết các câu đệm lịch sự.

Điều này bộc lộ tư thế thiết kế của Claude Code. Khôi phục là một phần của lộ trình chính của runtime, chứ không phải là phép xã giao sau khi thất bại. Khôi phục tồn tại để bảo vệ khả năng tiếp tục công việc. Trong kỹ thuật thực tế, tính liên tục thường có giá trị hơn vẻ bóng bẩy bên ngoài.

## 3.7 Điều kiện dừng không thể chỉ có một, nếu không thất bại và hoàn thành sẽ bị nhầm lẫn

Trong các hệ thống trò chuyện thông thường, điều kiện dừng rất đơn giản: có câu trả lời, kết thúc. Các hệ thống agent không thể lười biếng như vậy. Trong một phiên làm việc, "lượt này kết thúc" không đồng nghĩa với "tác vụ đã hoàn thành", và không đồng nghĩa với "hệ thống đã thành công".

Vòng lặp truy vấn của Claude Code phân biệt ít nhất các trường hợp:

- Quá trình truyền phát hoàn thành với `tool_use`, yêu cầu theo dõi (follow-up)
- Không có `tool_use`, đi vào các hook dừng (stop hooks) và các kiểm tra tiếp theo
- Người dùng ngắt quãng (user interruption)
- Nhánh khôi phục do prompt quá dài (prompt-too-long)
- Nhánh khôi phục do đạt giới hạn token đầu ra tối đa (max-output-tokens)
- Bị chặn bởi hook dừng, yêu cầu vào lại vòng lặp
- Các lỗi API trả về trực tiếp

Bạn có thể thấy điều này từ `src/query.ts:1062` đến `:1305`. Phần hook dừng xung quanh `:1267` đến `:1305` đặc biệt quan trọng: nó ngăn chặn một cách rõ ràng các vòng lặp vô hạn (dead loops) như "vẫn quá dài sau khi rút gọn, bị chặn bởi hook, tiếp tục rút gọn mãi mãi".

Đây là điều đáng chú ý. Nhiều hệ thống chỉ có một quy tắc ngây thơ: thử lại nếu thất bại. Claude Code thừa nhận rằng chính việc thử lại cũng cần được quản trị. Runtime phải biết tại sao mình thử lại, những gì đã được thử, trạng thái bảo vệ nào không thể thiết lập lại và những khuôn mẫu nào sẽ dẫn đến vô hạn. Những quyết định này phân biệt các hệ thống chỉ biết "tiếp tục thử" với các hệ thống "biết khi nào không nên thử lại nữa".

### Ma trận lỗi của điều kiện dừng (Stop-condition failure matrix)

| Trật tự sự kiện | Trạng thái trước | Tác nhân kích hoạt | Bước tiếp theo |
|---|---|---|---|
| stream hoàn thành + `tool_use` | có sẵn tool_use đang chờ | lý do dừng | theo dõi, thực thi công cụ |
| stream hoàn thành, không `tool_use` | không có công cụ đang chờ | lý do dừng | đi vào các hook dừng |
| người dùng ngắt | bất kỳ | tín hiệu hủy | xả các kết quả còn lại, tạo `tool_result` tổng hợp |
| prompt_too_long | chưa thử rút gọn | lỗi có thể khôi phục | xả thu gọn / rút gọn phản ứng |
| max_output_tokens | giới hạn < MAX | lý do dừng | tăng `maxOutputTokensOverride`, chạy lại |
| max_output_tokens | giới hạn = MAX | lý do dừng | nối thêm tin nhắn meta người dùng, tiếp tục ghi |
| chặn bởi hook dừng + lặp lại PTL | `hasAttemptedReactiveCompact` | lỗi kép (double failure) | bỏ qua hook dừng, hiển thị lỗi |
| lỗi API | — | api_error | trả về trực tiếp, không thử lại |

## 3.8 QueryEngine chứng minh điều này thuộc về vòng đời cuộc hội thoại

Nếu `queryLoop()` chưa đủ làm bằng chứng, thì `QueryEngine` sẽ làm sáng tỏ điều đó.

Tại `src/QueryEngine.ts:176`, mã nguồn nêu rõ:

> QueryEngine sở hữu vòng đời truy vấn (query lifecycle) và trạng thái phiên (session state) cho một cuộc hội thoại.

![Claude Code QueryEngine Turn Flow](diagrams/diag-ch03-02-queryengine-turn-flow.png)

![Claude Code QueryEngine State Carry-Over](diagrams/diag-ch03-03-queryengine-state-carryover.png)

Dòng này khẳng định trực tiếp luận điểm của chương. `QueryEngine` sở hữu vòng đời cuộc hội thoại, chứ không phải chỉ sở hữu một lệnh gọi đơn lẻ. Tại `src/QueryEngine.ts:180`, mã nguồn cho biết thêm rằng một `QueryEngine` ánh xạ tới một cuộc hội thoại, và mỗi lần gọi `submitMessage()` sẽ mở ra một lượt mới bên trong cuộc hội thoại đó trong khi vẫn bảo toàn trạng thái.

Sau `src/QueryEngine.ts:675`, `QueryEngine` chuyển giao các thông tin đã chuẩn bị gồm `messages`, `systemPrompt`, `userContext`, `systemContext`, và `toolUseContext` cho hàm `query()`, sau đó ghi lại các tin nhắn của trợ lý (assistant), người dùng (user) và ranh giới rút gọn (compact-boundary) vào bản ghi hội thoại (transcript).

Điều này có nghĩa là vòng lặp truy vấn mới là trung tâm thực thi thực tế của runtime cuộc hội thoại. Giao diện người dùng (UI) bên ngoài, SDK và tính năng lưu trữ phiên (session persistence) đều quay quanh nó. Để hiểu Claude Code, bạn không thể dừng lại ở việc liệt kê các công cụ hoặc đọc văn bản prompt. Bạn phải kiểm tra cách vòng lặp này biến các ràng buộc đó thành hành vi liên tục.

## 3.9 Nguyên lý thứ ba có thể trích xuất từ mã nguồn

Chương này có thể được nén lại trong một dòng duy nhất:

> Năng lực cốt lõi của một hệ thống agent là duy trì một vòng lặp thực thi có thể khôi phục được.

Bộ khung xương (skeleton), các bất biến (invariants) và ma trận điều kiện dừng ở trên đã làm rõ bằng chứng. Một dòng là đủ để kết luận: nhịp đập của một agent trưởng thành phải đồng thời quản trị trạng thái giữa các lượt hội thoại (cross-turn state), quản trị đầu vào (input governance), tiêu thụ luồng truyền phát (streaming consumption), sổ cái ngắt (interrupt ledger) và sự phân biệt giữa {hoàn thành (completion), thất bại (failure), khôi phục (recovery), tiếp tục (continuation)}.

Nếu không có các cấu trúc này, các hệ thống vẫn có thể tạo ra các bản demo hấp dẫn, nhưng chúng giống như các buổi biểu diễn được dàn dựng hơn là các runtime thực tế. Các buổi biểu diễn có giá trị riêng, nhưng chúng không thay thế được trật tự.

Chương tiếp theo sẽ chuyển sang nơi nhịp đập tiếp xúc trực tiếp nhất với thế giới bên ngoài: các công cụ, quyền hạn và ngắt. Chương này đã giải thích tại sao các vòng lặp tồn tại. Tiếp theo, chúng tôi sẽ giải thích tại sao một khi các vòng lặp sở hữu công cụ, chúng cũng phải học cách kiềm chế.
