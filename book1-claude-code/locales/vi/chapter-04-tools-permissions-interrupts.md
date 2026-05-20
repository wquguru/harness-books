# Chương 4 Công cụ, Quyền hạn và Ngắt: Tại sao Agent không thể chạm trực tiếp vào thế giới

## 4.1 Một khi mô hình gọi công cụ, bản chất của rủi ro sẽ thay đổi

Một mô hình chỉ xuất văn bản hầu như chỉ làm tiêu tốn thời gian giao tiếp khi nó sai sót. Một khi nó bắt đầu gọi các công cụ (calling tools), bản chất rủi ro sẽ thay đổi: các công cụ không phải là ý kiến mà là hành động, và các hành động chạm trực tiếp vào thế giới thực. Một lời giải thích sai chỉ dừng lại ở cấp độ hiểu biết; một câu lệnh sai có thể xóa tệp, tắt các tiến trình (kill processes), làm hỏng lịch sử Git. Sự phát triển về năng lực sẽ đi kèm với sự gia tăng về hệ quả.

Vì vậy, câu hỏi trung tâm rất đơn giản: ai là người ràng buộc các công cụ này? Câu trả lời của Claude Code là biến các công cụ thành các giao diện thực thi được quản lý (managed execution interfaces), chứ không để các mô hình tiếp cận trực tiếp.

## 4.2 Điều phối công cụ (Tool orchestration) là một phần của quy tắc hành vi

Hàm `runTools()` tại `src/services/tools/toolOrchestration.ts:19` thực hiện một tác vụ mang tính đại diện: nó không trực tiếp thực thi danh sách `tool_use` — nó phân nhóm theo tính an toàn đồng thời (concurrency safety). Hàm `partitionToolCalls()` tại `:91` đọc `inputSchema` của từng công cụ và gọi `isConcurrencySafe()`; các lệnh gọi an toàn sẽ đi vào các nhóm chạy song song, các lệnh gọi không an toàn được chia thành các đơn vị chạy tuần tự.

Điều này có vẻ giống như tinh chỉnh hiệu năng nhưng thực chất là thiết kế tính nhất quán (consistency design). Một khi tính đồng thời (concurrency) được cho phép, một câu hỏi cũ sẽ quay trở lại: ai quyết định sự tiến hóa của ngữ cảnh (context evolution), và theo thứ tự nào? Trong các lộ trình song song (từ `:31` đến `:63`), Claude Code không để công cụ nhanh nhất thay đổi ngữ cảnh trước; nó đệm các callback `contextModifier` và phát lại (replay) chúng theo thứ tự khối ban đầu. Việc thực thi là song song trong khi sự tiến hóa ngữ cảnh về mặt ngữ nghĩa vẫn mang tính xác định (deterministic).

Sự thận trọng mang tính kỹ thuật kinh điển: tính đồng thời có thể cải thiện băng thông xử lý (throughput) nhưng tuyệt đối không được phá vỡ tính nhân quả (causality). Các hệ thống agent trưởng thành không thần tượng hóa tính song song — họ coi đó là một ngoại lệ cần phải chứng minh được tính an toàn, chứ không phải là một quyền tự do mặc định.

## 4.3 Rất nhiều việc xảy ra trước khi một công cụ thực sự chạy

Nhiều người cho rằng một khi `tool_use` xuất hiện, việc thực thi sẽ tự động diễn ra. Các hệ thống mạnh mẽ không hoạt động theo cách đó. Sau `src/services/tools/toolExecution.ts:30`, `runToolUse()` đã được bao bọc bởi logic phân quyền (permission logic), các hook, phép đo từ xa (telemetry) và việc cụ thể hóa lỗi tổng hợp (synthetic error materialization) — bao gồm kiểm tra trước (pre-checks), sự kiện đang diễn ra (in-flight events), sửa lỗi sau khi thực thi (post-execution correction) và bù đắp thất bại (failure compensation).

Các công cụ ở đây không phải là các hàm thư viện nội bộ thông thường. Các hàm nội bộ giả định người gọi ổn định và chịu trách nhiệm về hệ quả; các giao diện công cụ nằm giữa mô hình và thế giới bên ngoài, vì vậy runtime không thể giả định phán đoán của người gọi là ổn định. Đó là lý do tại sao có rất nhiều lớp bao bọc (wrappers) tồn tại: người gọi là biến số không ổn định nhất. Không nên mô hình hóa các công cụ như "các phần mở rộng năng lực của mô hình" mà là các năng lực bên ngoài mà rủi ro của chúng phải được quản lý bởi runtime. Một khi bạn chấp nhận điều đó, quyền hạn, các hook, các ngắt và kết quả tổng hợp sẽ trở thành những điều cơ bản, chứ không phải gánh nặng.

## 4.4 Quyền hạn (Permission) có trước năng lực

Điểm ghi nhận quyền hạn của Claude Code là sau `src/hooks/useCanUseTool.tsx:27`. Chính sự tồn tại của `CanUseToolFn` đã nói lên một điều quan trọng: việc cho phép công cụ không chỉ được quyết định bởi ý định của mô hình; nó phải đi qua một chuỗi ủy quyền (authorization chain).

Bên trong `useCanUseTool()`, runtime không tự động chạy chỉ vì mô hình yêu cầu một công cụ. Trước tiên, nó gọi `hasPermissionsToUseTool(...)`, xem `useCanUseTool.tsx:37`. Kết quả được chia thành `allow` (cho phép), `deny` (từ chối), hoặc `ask` (hỏi ý kiến). Điều này có vẻ bình thường, nhưng lại vô cùng cơ bản. Các hệ thống ủy quyền trưởng thành cần nhiều hơn việc chỉ trả lời có/không (yes/no); chúng cần một trạng thái thứ ba nơi bản thân hệ thống không nên tự quyết định thay cho người dùng.

Sau `useCanUseTool.tsx:64`, các nhánh tiếp tục hành trình:

- `deny`: từ chối trực tiếp
- `ask`: định tuyến tới điều phối viên (coordinator), swarm worker, bộ phân loại (classifier) hoặc phê duyệt tương tác (interactive approval)
- `allow`: thực thi

Điều này từ chối về mặt cấu trúc một ý tưởng nguy hiểm phổ biến: nếu mô hình hiểu được ý định của người dùng, nó có thẩm quyền thực thi. Thực tế không phải vậy. Hiểu ý định không phải là ủy quyền, và chắc chắn không phải là ủy quyền vĩnh viễn. Các hệ thống phải tách biệt giữa "có thể làm" (can do) và "được phép làm" (may do).

Từ góc độ này, quyền hạn làm rõ vai trò của agent: mô hình có thể đề xuất các hành động, nhưng runtime, các quy tắc và người dùng mới quyết định việc phê duyệt thực thi. Năng lực (capability) và thẩm quyền (authority) được tách biệt một cách có chủ ý.

### Khung xương (Skeleton): chuỗi phân quyền (permission chain)

```
// skeleton: useCanUseTool()  (src/hooks/useCanUseTool.tsx:27)
decision = hasPermissionsToUseTool(tool, input, ctx)
match decision:
    case allow:  return exec(tool, input)
    case deny:   return reject(reason)
    case ask:    return route_to(coordinator | swarm_worker | classifier | interactive_prompt)

assert decision ∈ {allow, deny, ask}                    # giá trị ba trạng thái, không đi tắt bằng boolean
assert ask never auto-escalates to allow                # không tự động leo thang quyền hạn trái phép
assert deny is sticky for this tool_use_id              # không tự động thử lại trong âm thầm để được allow
```

![Claude Code Permission Decision Layers](diagrams/diag-ch04-01-permission-decision-layers.png)

## 4.5 Kết quả phân quyền là ngữ nghĩa runtime, không phải các biến boolean

Sau `src/utils/permissions/PermissionResult.ts:23`, Claude Code thậm chí còn định nghĩa các mô tả rõ ràng cho ngữ nghĩa phân quyền: `allow`, `deny` và `ask`. Chi tiết này rất quan trọng. Phân quyền không phải là một biến boolean nội bộ; nó là một đối tượng runtime có ý nghĩa độc lập.

Tại sao điều này quan trọng: một hệ thống phân quyền phải cho phép runtime thể hiện rõ ràng lý do tại sao một bước không tiếp tục. Khi một agent nói "Tôi cần xác nhận", nó đang tuyên bố các ranh giới trách nhiệm. Một khi các ranh giới được làm rõ, thì sự từ chối, phê duyệt, quy tắc bộ nhớ đệm (cache rules), cấp quyền tạm thời và cấp quyền vĩnh viễn đều có chỗ đứng.

Nói một cách đơn giản, nếu một agent không thể phân biệt giữa "Tôi có thể làm việc này", "Tôi không thể làm việc này" và "Tôi phải hỏi ý kiến", thì nó không nên chạm vào terminal. Các terminal không tự bù đắp ngữ nghĩa còn thiếu. Các terminal chỉ thực thi.

## 4.6 StreamingToolExecutor chứng minh ngắt (interrupt) là ngữ nghĩa cốt lõi

Một khi các công cụ chạy song song và truyền phát (streaming), việc xử lý ngắt ngay lập tức trở nên phức tạp. Runtime lúc này phải đối mặt với một hàng đợi có các trạng thái như `queued` (đang xếp hàng), `executing` (đang thực thi), `completed` (đã hoàn thành), `yielded` (đã sinh kết quả), chứ không chỉ là một hành động đơn lẻ.

Sau `src/services/tools/StreamingToolExecutor.ts:34`, Claude Code thực hiện điều này thông qua một trình thực thi truyền phát chuyên dụng một cách rõ ràng. Quan trọng nhất là cách nó xử lý ngắt và loại bỏ.

Tại `StreamingToolExecutor.ts:64` đến `:70`, runtime có thể loại bỏ tập hợp công cụ hiện tại trong quá trình rút lui truyền phát (streaming fallback). Tại `:153` đến `:205`, nó tạo ra các thông báo lỗi tổng hợp cho các nguyên nhân khác nhau:

- lỗi từ tiến trình đồng cấp (sibling error)
- người dùng ngắt quãng (user interrupted)
- rút lui truyền phát (streaming fallback)

Sau `:210`, it further distinguishes interruption causes:

- bị hủy do lỗi của công cụ đồng cấp (cancelled due to sibling tool failure)
- bị hủy do người dùng ngắt (cancelled due to user interrupt)
- bị loại bỏ do rút lui (dropped due to fallback)

Tại `:233` trở xuống, mỗi công cụ có thể định nghĩa thuộc tính `interruptBehavior`, quyết định xem nên hủy (`cancel`) hay chặn (`block`) khi người dùng can thiệp.

Thiết kế này quan trọng vì Claude Code không coi việc ngắt là "một lỗi thực thi đặc biệt". Nó coi việc ngắt là một ngữ nghĩa có tầm quan trọng tương đương với bản thân việc thực thi. Runtime không chỉ phải biết liệu một công cụ có thể bắt đầu hay không, mà còn phải biết nó kết thúc như thế nào khi bị ngắt, các kết quả được đóng lại ra sao và liệu các tin nhắn mới có thể xen kẽ vào hay không.

Đó là một đặc điểm cốt lõi của Kỹ thuật Khung kiểm soát (Harness Engineering): thiết kế cả điểm bắt đầu lẫn điểm dừng. Các hệ thống thực thi không có ngữ nghĩa dừng cuối cùng sẽ phải phụ thuộc vào việc người dùng ngắt cứng từ bên ngoài để hoàn thành thiết kế.

### Ma trận lỗi do chạy đồng thời & ngắt (Concurrency & interrupt failure matrix)

| Trật tự sự kiện | Trạng thái trước | Tác nhân kích hoạt | Bước tiếp theo |
|---|---|---|---|
| một công cụ lỗi trong nhóm song song | các công cụ đồng cấp đang chạy | lỗi đồng cấp | giữ lại các công cụ khác; phát lại `contextModifier` theo thứ tự khối |
| người dùng can thiệp + `interruptBehavior=cancel` | công cụ chưa chạy xong | người dùng ngắt | hủy, tạo kết quả tổng hợp `user interrupted` |
| người dùng can thiệp + `interruptBehavior=block` | công cụ chưa chạy xong | người dùng ngắt | hoàn thành công cụ, chặn tin nhắn mới cho đến khi xong |
| rút lui truyền phát | nhóm đang xếp hàng/đang chạy | rút lui (fallback) | loại bỏ nhóm, sinh kết quả tổng hợp rút lui theo thứ tự |
| hủy bỏ với `tool_use` đang chờ | bất kỳ | tín hiệu hủy | tổng hợp `tool_result`, đóng sổ cái |
| lệnh Bash phức hợp vượt quá giới hạn lệnh con | bộ phân loại từ chối | kiểm tra an toàn | `deny`; không định tuyến tới `ask` |

![Claude Code Tool Execution Lifecycle](diagrams/diag-ch04-02-tool-execution-lifecycle.png)

## 4.7 Tại sao Bash luôn đáng ngờ hơn các công cụ khác

Trong thế giới công cụ của Claude Code, Bash là một bộ khuếch đại rủi ro, chứ không phải là một công cụ bình thường. Nó quá đa năng — một công cụ đọc tệp sẽ không vô tình giết chết các tiến trình, một công cụ grep sẽ không âm thầm đẩy (push) các bản commit, nhưng Bash thì có thể làm hầu hết mọi thứ. Sự không tin tưởng của Claude Code là rất rõ ràng.

Lớp đầu tiên là hướng dẫn bằng prompt trong `src/tools/BashTool/prompt.ts:42` trở xuống: các quy tắc chi tiết cho git, PR, lệnh nguy hiểm, các hook, force push và các cờ tương tác (interactive flags) — một sự dài dòng có kỷ luật ở những nơi hệ quả có thể rất lớn. Lớp thứ hai là phân loại an toàn và quyền hạn. File `src/tools/BashTool/bashPermissions.ts:1` xử lý ngữ nghĩa shell, tiền tố lệnh, chuyển hướng (redirection), các trình bao bọc (wrappers), các biến môi trường an toàn, định tuyến bộ phân loại và khớp quy tắc; sau `:95` một giới hạn số lượng lệnh con sẽ ngăn chặn các lệnh phức hợp thoát khỏi sự kiểm tra.

Bash là một kênh nguy hiểm đòi hỏi sự quản trị đặc biệt, chứ không phải là một giao diện dòng lệnh thông thường. Một nhận định có thể tái sử dụng: năng lực có rủi ro cao xứng đáng nhận được sự quản trị đặc biệt, chứ không phải cách đối xử như một năng lực thông thường; coi Bash như một công cụ bình thường thường là sự lười biếng trong thiết kế.

## 4.8 Các hệ thống công cụ bảo vệ người dùng và bảo vệ chính bản thân runtime

Các cơ chế phân quyền, lập lịch và ngắt trông có vẻ giống như các cơ chế bảo vệ người dùng, nhưng chúng cũng bảo vệ tính nhất quán của chính bản thân runtime. Nếu một hệ thống agent cho phép tồn tại các vấn đề chưa được giải quyết như `tool_result` không hoàn chỉnh, đột biến ngữ cảnh không đúng thứ tự, các tác dụng phụ song song không giới hạn và ngữ nghĩa ngắt mơ hồ, điều đầu tiên bị phá vỡ sẽ là tính nhất quán nội bộ.

Điều này được liên kết chặt chẽ trên các lớp `query.ts` và thực thi công cụ. Chương 3 đã thảo luận về cách vòng lặp truy vấn tổng hợp các kết quả công cụ bị thiếu khi bị ngắt. Chương này cho thấy `StreamingToolExecutor` có các cơ chế riêng cho các hành vi bị loại bỏ/lỗi/hủy đồng cấp/ngắt. Cùng nhau, chúng bảo toàn một chuỗi nhân quả có thể truy vết cho:

- những gì đã được thực thi
- những gì chưa hoàn thành
- tại sao nó dừng lại

Đó là một ý nghĩa cốt lõi khác của khung kiểm soát (harness): giữ gìn trật tự cho chính hệ thống. Nhiều ràng buộc bên ngoài trông giống như ngăn ngừa thao tác sai, nhưng ở cấp độ sâu hơn, chúng ngăn runtime sụp đổ thành các mảnh trạng thái không thể giải thích được.

## 4.9 Nguyên lý thứ tư có thể trích xuất từ mã nguồn

Chương này có thể được nén lại trong một dòng duy nhất:

> Công cụ là các giao diện thực thi được quản lý; quyền hạn là một cơ quan của hệ thống agent.

Mã nguồn Claude Code cùng hỗ trợ luận điểm này:

- `toolOrchestration.ts` phân nhóm trước khi thực thi, vì vậy việc lập lịch diễn ra trước sự thúc đẩy tức thời
- `toolExecution.ts` bao bọc các hook, quyền hạn, phép đo từ xa (telemetry) và các lỗi tổng hợp xung quanh việc thực thi, vì vậy các lệnh gọi không bao giờ bị để trần
- `useCanUseTool.tsx` chia hoạt động ủy quyền thành `allow / deny / ask`, làm cho thẩm quyền trở thành một nhánh ngữ nghĩa cốt lõi
- `StreamingToolExecutor.ts` định nghĩa ngữ nghĩa ngắt, rút lui (fallback) và lỗi đồng cấp, làm cho việc dừng lại cũng quan trọng như việc bắt đầu
- `BashTool/prompt.ts` và `bashPermissions.ts` áp dụng các biện pháp quản trị đặc biệt với áp lực cao lên Bash, chứng minh rằng năng lực có rủi ro cao phải đi kèm với các ràng buộc dày đặc hơn

Là những nguyên lý kỹ thuật có thể di động được: mô hình đề xuất, runtime ủy quyền; bảo toàn trật tự nhân quả ngay cả khi chạy song song; ngắt là một nhánh cốt lõi (first-class), không phải là một ngoại lệ chung chung; đối xử với các công cụ thuộc nhóm Bash như các ngoại lệ rõ ràng; một hệ thống công cụ bảo vệ cả người dùng lẫn chính runtime.

Chương tiếp theo sẽ giải quyết một ảo tưởng phổ biến khác trong hệ thống này: "càng nhiều ngữ cảnh thì càng tốt". Việc triển khai của Claude Code cho thấy điều ngược lại. Các hệ thống có kinh nghiệm đối xử với ngữ cảnh như một tài nguyên, chứ không phải một kho chứa hàng. Bây giờ chúng ta chuyển sang cách bộ nhớ, `CLAUDE.md` và rút gọn (compact) tạo thành một cơ chế quản trị ngữ cảnh.
