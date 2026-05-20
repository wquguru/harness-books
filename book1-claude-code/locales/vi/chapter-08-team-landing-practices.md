# Chương 8 Áp dụng trong Nhóm: Biến một Công cụ Thông minh thành một Quy trình làm việc Bền vững

## 8.1 Thành công của chuyên gia không tự động chuyển hóa thành sự tái sử dụng an toàn trong nhóm

Nhiều công cụ lập trình AI trông rất ấn tượng trong tay các chuyên gia: những người dùng thành thạo biết khi nào cần vá ngữ cảnh, khi nào cần theo dõi sát sao mô hình, và khi nào chỉ cần một dòng lệnh "không chạm vào thư mục này" là có thể giữ hành vi của mô hình đi đúng hướng. Điều đó dễ dàng tạo ra một ảo tưởng — rằng nếu những người dùng quyền lực (power users) vận hành nó một cách trơn tru, thì việc triển khai cho cả nhóm chỉ đơn thuần là viết thêm vài ghi chú về các thực tiễn tốt nhất (best practices).

Vấn đề là kỹ thuật cá nhân hoạt động hiệu quả chính xác là vì nó phụ thuộc vào sự giám sát liên tục, kiến thức nền tảng và phán đoán tình huống. Một khi nhóm áp dụng công cụ này, các giả định sẽ thay đổi: bạn không còn có thể giả định rằng mọi người đều biết lệnh nào là nguy hiểm, bộ nhớ nào đã lỗi thời, kỹ năng nào sẽ phân nhánh subagent, bước nào có thể bỏ qua phê duyệt và bước nào tuyệt đối không được. Vấn đề thực tế của nhóm là biến trật tự vốn chỉ tồn tại trong đầu của chuyên gia thành một quy trình làm việc mà các thành viên bình thường có thể lặp lại mà không cần đến những nỗ lực phi thường.

Mã nguồn Claude Code rất hữu ích ở đây vì nó làm cho hành vi của chuyên gia trở nên rõ ràng: các hướng dẫn có các lớp tải, quyền hạn có các điểm quyết định, các subagent có các ranh giới cô lập, runtime để lộ ra các hook vòng đời. Áp dụng một coding agent vừa là việc đưa vào một tính năng tự động hoàn thành (autocomplete) thông minh hơn, vừa là việc sắp xếp lại xem ai có thể làm gì bên trong ranh giới nào.

## 8.2 Bước đầu tiên của nhóm là làm rõ các ranh giới tối thiểu

Chương này rất dễ bị hiểu sai nếu việc áp dụng trong nhóm được hình dung như một dự án quản trị quy mô lớn ngay từ ngày đầu tiên. Trong thực tế, hầu hết các nhóm không bắt đầu với các hook, chuỗi kiểm toán (audit chains) và các danh mục kỹ năng phức tạp. Điểm khởi đầu của họ thường nhỏ hơn nhiều:

- những loại tác vụ nào được phép có sự tham gia của agent
- những thay đổi nào vẫn bắt buộc phải có sự soát xét của con người (human review)
- bước xác minh tối thiểu nào phải diễn ra trước khi công việc được coi là hoàn thành
- tài nguyên nào là hoàn toàn cấm kỵ (off limits)

Những điều này nghe có vẻ cơ bản, nhưng chúng quan trọng hơn những khẩu hiệu đầy tham vọng. Trong giai đoạn đầu, các nhóm thường được lợi nhiều nhất từ việc có một ranh giới kiểm soát tối thiểu được định nghĩa rõ ràng.

Nếu ranh giới đó bị xác định sai, mọi lớp tự động hóa sau này đều sẽ bị bóp méo:

- nếu phạm vi sử dụng được phép bị mơ hồ, mọi người sẽ sử dụng agent ở những nơi chưa bao giờ được thiết kế để tự động hóa
- nếu trách nhiệm soát xét bị mơ hồ, không ai biết ai là người sở hữu điểm kiểm tra (checkpoint) có ý nghĩa cuối cùng
- nếu việc xác minh bị mơ hồ, hệ thống sẽ học cách đáp ứng tiêu chuẩn thấp nhất trong phòng
- nếu các khu vực cấm bị mơ hồ, hiệu quả tăng thêm sẽ trở thành sự mở rộng bán kính thiệt hại (blast-radius)

Vì vậy, trình tự triển khai thực tế hơn hiếm khi là "xây dựng nhiều kỹ năng trước, rồi thêm quản trị sau". Nó thường là:

1. định nghĩa phạm vi sử dụng được chấp nhận  
2. định nghĩa các kỳ vọng về soát xét và xác minh  
3. sau đó mới quyết định quy trình lặp đi lặp lại nào xứng đáng được tái sử dụng chính thức

Các nhóm thường thất bại vì họ đã bỏ qua bước này, ngay cả khi bản thân agent đó có năng lực khá tốt.

### Bảng kiểm triển khai theo giai đoạn (Staged rollout checklist - dành cho người xây dựng)

```
- [ ] Tuần 1: CLAUDE.md phân lớp đi vào hoạt động — các mức độ nhóm / cá nhân / dự án đều có thể xác thực
- [ ] Tuần 1: Xác minh chung được định nghĩa (các lệnh lint / type / test trong CLAUDE.md)
- [ ] Tuần 1: Các khu vực cấm được mã hóa thành các ràng buộc cứng cấp repo (thư mục, lệnh nguy hiểm)
- [ ] Tuần 2: Phê duyệt được phân tầng theo hệ quả (allow / deny / ask), Bash có quy tắc riêng
- [ ] Tuần 2: Bàn giao ≤3 kỹ năng đầu tiên, mỗi kỹ năng có tiền điều kiện / hậu điều kiện / sản phẩm có thể xác thực
- [ ] Tuần 2: Chính sách rõ ràng cho việc "hoàn thành với các lỗi đã biết"
- [ ] Tuần 3: Đưa vào các hook dừng / sau khi sử dụng công cụ, thu thập bản ghi hội thoại + đầu ra tác vụ
- [ ] Tuần 3: Thực hiện bảo trì bộ nhớ cũ hàng tháng
- [ ] Tuần 3: Phát lại cơ bản (Git diff / PR / CI) không có lỗ hổng trước khi theo đuổi kiểm toán nâng cao
Gate: một người mới có thể sử dụng mà không cần chuyên gia đứng cạnh — quy trình làm việc đã trưởng thành.
```

## 8.3 CLAUDE.md quan trọng vì nó duy trì tính ổn định, phân lớp và ít gây tranh cãi

Các chương trước đã đề cập đến việc tải phân lớp trong `claudemd.ts`. Điều đó vẫn quan trọng trong quá trình áp dụng ở nhóm, nhưng nó nên được diễn giải với một chút kiềm chế.

Tệp `CLAUDE.md` cấp độ nhóm được sử dụng tốt nhất cho các quy tắc ổn định. Nó không cần phải mang theo mọi chi tiết quy trình. Các ví dụ bao gồm:

- các ràng buộc cứng ở cấp độ kho lưu trữ, chẳng hạn như các thư mục bị cấm hoặc các nhóm lệnh nguy hiểm
- các kỳ vọng xác minh chung, chẳng hạn như các kiểm tra tối thiểu bắt buộc phải chạy
- kỷ luật cộng tác, chẳng hạn như không ghi đè lên các thay đổi mà người dùng không yêu cầu và không thiết lập lại các cây làm việc chưa sạch (dirty worktrees) nếu không có hướng dẫn rõ ràng
- kỷ luật đầu ra, chẳng hạn như báo cáo soát xét ưu tiên kết quả tìm kiếm trước (findings-first review reporting)

Những gì không phù hợp: các quy trình tạm thời thay đổi nhanh chóng, các hướng dẫn chỉ liên quan đến một tập hợp tác vụ hẹp và các chi tiết được thể hiện tốt hơn dưới dạng các lệnh, kỹ năng hoặc tập lệnh. Một khi `CLAUDE.md` trở thành một cuốn bách khoa toàn thư, nó sẽ mất đi cả tính ổn định lẫn độ tin cậy cùng một lúc: các thành viên trong nhóm không còn biết liệu một quy tắc là hiện hành hay là tàn dư từ nhiều tháng trước, và hệ thống sẽ học cách coi các chuẩn mực đã lỗi thời như luật pháp hiện hành.

Vì vậy, tệp `CLAUDE.md` lý tưởng của nhóm không đơn giản là "lớn". Nó phải đủ ổn định để mọi người hiếm khi cần phải tranh luận về nó. Nó hoạt động giống như một nền móng, chứ không phải một bảng tin.

## 8.4 Định nghĩa xác minh thường quan trọng sớm hơn số lượng kỹ năng

Một trong những thất bại phổ biến nhất trong việc triển khai coding-agent là nhóm không có một định nghĩa chung về sự hoàn thành (definition of done).

Một người nghĩ "nó chạy được" là đủ. Người khác chấp nhận một cái gì đó được kiểm thử một nửa. Người khác nữa chấp nhận một lời giải thích trông có vẻ hợp lý từ mô hình. Trong môi trường đó, ngay cả một hệ thống thông minh cũng học cách đáp ứng mức tiêu chuẩn thấp nhất có sẵn.

Claude Code liên tục đẩy lùi sự trượt dốc đó. Trước đó, chúng ta đã thấy chế độ điều phối viên (coordinator mode) tách xác minh thành một giai đoạn riêng biệt; các hướng dẫn liên quan đến xác minh không chỉ là để chứng minh các tệp tồn tại, mà là để chứng minh rằng thay đổi thực sự hoạt động.

Điều này đặc biệt quan trọng đối với các nhóm vì các kỹ năng có thể tái tạo quy trình, nhưng chỉ có định nghĩa xác minh mới tái tạo được chất lượng.

Một bước đi thực tế hơn của nhóm là xác định ba điều này trước khi xây dựng nhiều kỹ năng:

- loại tác vụ nào yêu cầu xác minh độc lập
- hành động tối thiểu nào mà việc xác minh phải bao gồm, chẳng hạn như kiểm thử, chạy cục bộ, nhật ký (logs) hoặc sự chấp nhận của con người
- liệu việc xác minh thất bại vẫn có thể được đánh dấu là "hoàn thành với các lỗi đã biết"

Nếu những điều này vẫn chưa rõ ràng, bất kỳ hoạt động tự động hóa nào sau đó chỉ đẩy nhanh sự mơ hồ. Nếu chúng được làm rõ sớm, thì ngay cả một nhóm có rất ít kỹ năng vẫn có thể duy trì một mức chất lượng tối thiểu nhất quán.

Vì vậy, trình tự triển khai bền vững hơn thường là:

- chuẩn hóa định nghĩa xác minh trước
- sau đó đóng gói các quy trình làm việc lặp đi lặp lại thành các kỹ năng hoặc câu lệnh
- chỉ sau đó mới xem xét đến tự động hóa phức tạp hơn

## 8.5 Kỹ năng nên được hiểu là các mô-đun quy trình làm việc hơn là bản thân các thể chế

Khi các nhóm lần đầu tiên thiết kế các kỹ năng, họ dễ rơi vào hai mô hình tồi tệ: hoặc coi kỹ năng "chỉ là một mẫu prompt dài", hoặc nâng tầm nó quá mức thành một đối tượng thể chế. Cả hai đều không phù hợp.

Claude Code rõ ràng coi các kỹ năng không chỉ đơn thuần là các đoạn prompt: nếu ý định khớp với một kỹ năng, công cụ `Skill` phải được gọi; các kỹ năng đã được tải không được phép tải lại; một kỹ năng có thể chạy trong ngữ cảnh subagent phân nhánh với ranh giới và tập hợp công cụ riêng của nó. Vì vậy, một kỹ năng ít nhất là một mô-đun quy trình làm việc có thể thực thi. Nhưng đối với thực tiễn nhóm, cách diễn giải an toàn hơn nên hẹp hơn — các kỹ năng trước hết nên giải quyết câu hỏi "làm thế nào để tái sử dụng quy trình làm việc lặp đi lặp lại này một cách đáng tin cậy", chứ không phải là mã hóa toàn bộ tổ chức thành dạng agent.

Các câu hỏi đáng để trả lời trong quá trình thiết kế kỹ năng: nó phục vụ loại tác vụ nào, nó có thể sử dụng những công cụ nào theo mặc định, nó nên thực thi trực tiếp hay phân nhánh sang một subagent, kết quả có thể xác minh nào phải tồn tại sau đó. Nếu không được trả lời, các kỹ năng sẽ suy thoái thành các khẩu hiệu nghe tên thì hay nhưng mơ hồ về mặt ngữ nghĩa.

## 8.6 Phê duyệt hoạt động tốt nhất khi được phân tầng theo mức độ rủi ro

Claude Code liên tục quay trở lại một sự phân biệt: việc có khả năng làm điều gì đó khác với việc được ủy quyền để làm điều đó. Việc sử dụng cá nhân thường đánh giá thấp điều này vì các cá nhân tự cấp cho mình quyền hạn tạm thời; các nhóm thì không thể làm vậy. Một khi agent ghi tệp, thay đổi trạng thái Git, chạm vào mạng hoặc các hệ thống bên ngoài, mỗi bước đi cũng là một sự chuyển giao trách nhiệm.

Các nhóm thường mắc sai lầm ngược lại: thiết kế một bảng phân loại phê duyệt phức tạp ngay lập tức, và chi phí triển khai trở nên không thể gánh nổi. Thực tế hơn là phân tầng theo rủi ro, chứ không phải theo tên công cụ — các hoạt động đọc / liệt kê / phân tích thuần túy có rủi ro thấp hơn; đột biến không gian làm việc (workspace mutation) và các thao tác ghi có rủi ro cao hơn rõ rệt; Git push, mạng bên ngoài và các môi trường nhạy cảm có rủi ro cao hơn nữa. Những gì các nhóm thực sự cần kiểm soát là tính không thể đảo ngược (irreversibility) và tính nhạy cảm của môi trường, chứ không phải nhãn của nút bấm. Một khi các ranh giới đó rõ ràng, tự động hóa sẽ ít có khả năng khuếch đại thiệt hại ở những nơi không mong muốn.

### Mẫu quy tắc phê duyệt (Approval rule template)

```
// mẫu: quy tắc phê duyệt (phản ánh quyết định ba giá trị của useCanUseTool)
rule {
    name:           <short>
    match:          { tool, args_pattern, cwd_scope }
    risk_tier:      read | write | irreversible      // phân tầng theo hệ quả, không phải tên công cụ
    decision:       allow | deny | ask
    ask_to:         coordinator | reviewer | operator
    ttl:            session | turn | persistent
    audit:          transcript + PR comment + CI log
}
assert every irreversible action ⇒ decision ∈ {deny, ask}    # hành động không thể đảo ngược bắt buộc phải được kiểm soát (gated)
assert Bash compound commands > subcommand_cap ⇒ deny        # các lệnh gộp chung không được phát hành
assert ask never auto-escalates to allow                     # giá trị ba trạng thái không bao giờ bị thu hẹp
```

## 8.7 Hooks rất mạnh mẽ, nhưng thường thuộc về giai đoạn sau của quá trình triển khai

File `hooksConfigManager.ts` để lộ ra nhiều sự kiện vòng đời: `SessionStart`, `SessionEnd`, `SubagentStart`, `SubagentStop`, `PreCompact`, `PostCompact`, `FileChanged`, `DirectoryChange`, và các sự kiện khác. Khi đọc cùng nhau, giá trị thực sự của các hook trở nên rõ ràng: các quy tắc có thể được thực thi đúng thời điểm.

Các ví dụ bao gồm:

- tiêm ngữ cảnh ở cấp độ tổ chức khi các tệp hướng dẫn được tải
- chạy thêm một bước xác minh trước khi subagent dừng lại
- ghi lại tóm tắt xung quanh các ranh giới rút gọn (compact boundaries)
- thực hiện công việc lưu trữ hoặc dọn dẹp khi kết thúc phiên

Tất cả những điều đó đều hữu ích. Nhận định quan trọng hơn là hữu ích không nhất thiết có nghĩa là phải làm trước tiên.

Đối với hầu hết các nhóm kỹ thuật thông thường, bước đi đầu tiên thường đơn giản hơn: các tệp hướng dẫn ở cấp độ kho lưu trữ, các quy tắc soát xét mã nguồn (code-review), các kỳ vọng về CI và kiểm thử, cùng một tập hợp nhỏ các lệnh hoặc kỹ năng lặp đi lặp lại. Các hook chỉ bắt đầu mang lại hiệu quả khi quy mô, rủi ro hoặc áp lực tuân thủ tăng cao hơn nữa; trước đó, chúng thường đưa vào nhiều bộ phận chuyển động hơn mức nhóm có thể quản lý — các tập lệnh không được bảo trì, thời điểm kích hoạt không rõ ràng và chi phí gỡ lỗi vượt quá cả bước thủ công mà chúng thay thế.

Vì vậy, kết luận chín chắn hơn là các hook là một giao diện tự động hóa nâng cao. Chúng phù hợp cho các hành động bị giới hạn về thời gian và thường thuộc về giai đoạn sau khi quản trị cơ bản (baseline governance) đã đi vào ổn định.

## 8.8 Khả năng phát lại (Replayability) là quan trọng, nhưng các nhóm nên tách biệt dấu vết cơ bản khỏi nhật ký kiểm toán nâng cao

Khả năng quan sát (observability) và khả năng kiểm toán (auditability) là những thứ dễ bị phóng đại nhất trong chương này. Tất nhiên, các nhóm muốn biết tại sao một điều gì đó đã xảy ra, sự trôi lệch bắt đầu từ đâu và ai đã ủy quyền cho bước đi có tính hệ quả đó. Nhật ký, phép đo từ xa, kết quả tác vụ, đường dẫn bản ghi hội thoại, sự kiện hook và thông báo agent của Claude Code thực sự tạo ra khả năng phát lại mạnh mẽ hơn.

But two layers must be separated. The baseline layer — Git diffs and commit history, PR comments and reviewer decisions, CI and test logs, issue trackers and acceptance notes — most teams already have, and it is usually enough for day-to-day reconstruction. The advanced layer — transcript paths, tool-call records, hook events, compact summaries, subagent usage and state transitions — pays off when scale or compliance justifies it. The key is to make layer one gap-free before investing in layer two; many teams lack a clean review or verification standard, and chasing full agent auditability too early turns governance into an expensive display.

Nhưng bắt buộc phải phân tách hai lớp này. Lớp cơ bản (baseline layer) — các bản phân biệt Git (Git diffs) và lịch sử commit, các bình luận PR và quyết định của người soát xét, nhật ký CI và kiểm thử, trình theo dõi vấn đề (issue trackers) và ghi chú nghiệm thu — hầu hết các nhóm đã có sẵn, và nó thường đủ cho việc tái dựng hàng ngày. Lớp nâng cao (advanced layer) — đường dẫn bản ghi hội thoại, bản ghi cuộc gọi công cụ (tool-call records), sự kiện hook, tóm tắt rút gọn, việc sử dụng subagent và chuyển đổi trạng thái — chỉ mang lại hiệu quả khi quy mô hoặc tính tuân thủ yêu cầu. Chìa khóa là làm cho lớp một hoàn chỉnh không có kẽ hở trước khi đầu tư vào lớp hai; nhiều nhóm thiếu một tiêu chuẩn soát xét hoặc xác minh sạch sẽ, và việc theo đuổi khả năng kiểm toán toàn diện cho agent quá sớm sẽ biến quản trị thành một thứ trưng bày đắt đỏ.

Vì vậy, khả năng phát lại cơ bản là một yêu cầu bắt buộc đối với việc áp dụng trong nhóm; nhật ký kiểm toán nâng cao (advanced audit trails) là một sự nâng cấp dành cho các nhóm có rủi ro cao, quy mô lớn hoặc yêu cầu tuân thủ nghiêm ngặt. Sự phân biệt đó giúp ngăn chặn việc quản trị của đội ngũ nền tảng (platform-team) bị viết sai thành điểm khởi đầu của tất cả mọi người.

## 8.9 Nguyên lý thứ tám có thể trích xuất từ mã nguồn

Câu kết luận của chương này sẽ chính xác hơn dưới dạng:

> Việc áp dụng trong nhóm hoạt động tốt nhất khi các ranh giới được chấp nhận, tiêu chuẩn xác minh và quy trình làm việc lặp đi lặp lại đạt được sự ổn định từ sớm.

Những gì mã nguồn Claude Code thực sự gợi ý, ở dạng có thể mang đi được, gần với điều này hơn:

- các hướng dẫn phải được phân lớp để các quy tắc ổn định và chi tiết quy trình tạm thời không bị trộn lẫn vào nhau
- các kỹ năng là hữu ích cho các quy trình làm việc lặp đi lặp lại, nhưng chỉ khi tính khả dụng, phạm vi công cụ và đầu ra được làm rõ
- phê duyệt nên được phân tầng theo rủi ro và môi trường thay vì phân loại thô sơ theo tên công cụ
- các hook rất mạnh mẽ, nhưng chúng thuộc về giai đoạn sau khi quản trị cơ bản đã ổn định
- khả năng phát lại nên được xây dựng theo từng lớp: khả năng truy vết cơ bản trước, khả năng kiểm toán nâng cao khi bối cảnh yêu cầu

Được dịch thành các nguyên lý vận hành nhóm: định nghĩa phạm vi sử dụng được chấp nhận trước khi triển khai quy mô lớn; chuẩn hóa định nghĩa xác minh trước khi tăng số lượng kỹ năng; sử dụng soát xét, CI và một tập hợp nhỏ các tệp hướng dẫn ổn định để thiết lập nền móng trước khi thêm các hook và điều phối; yêu cầu mọi đường dẫn tự động hóa phải có thể giải thích được mà không đòi hỏi khả năng kiểm toán nặng nề ngay từ ngày đầu tiên; tối ưu hóa không phải cho trọng lượng thể chế lớn nhất mà là cho các ranh giới rõ ràng hơn và một hệ thống dễ dung thứ hơn.

Chương tiếp theo sẽ khép lại cuốn sách. Xuyên suốt các chương trước, một nhận định liên tục quay trở lại: mô hình là thành phần kém ổn định nhất, vì vậy những gì chúng ta thực sự thiết kế là làm thế nào để giữ cho hệ thống xung quanh dễ chịu đựng hơn, có thể xác minh và có thể sửa chữa khi mô hình không đáng tin cậy.
