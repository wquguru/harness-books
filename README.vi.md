# Sách về Kỹ nghệ Harness (Harness Books)

[English README](./README.md) | [中文 README](./README.zh-CN.md)

[![Read Online](https://img.shields.io/badge/Read%20Online-Harness%20Books-16a34a?style=flat-square&logo=googlechrome&logoColor=white)](https://harness-books.agentway.dev/vi/)
[![About AgentWay](https://img.shields.io/badge/About-AgentWay-22c55e?style=flat-square&logo=bookstack&logoColor=white)](https://agentway.dev)

Hai cuốn sách về kỹ nghệ harness (harness engineering). Chúng cùng theo đuổi một câu hỏi kỹ thuật: một khi mô hình viết mã nguồn được đặt bên trong terminal, kho lưu trữ, hệ thống quyền hạn và quy trình làm việc của nhóm, điều gì giữ cho toàn bộ hệ thống luôn có ranh giới, liên tục và chịu trách nhiệm về các hệ quả?

<table>
  <tr>
    <td align="center" valign="top" width="50%">
      <a href="https://harness-books.agentway.dev/vi/book1-claude-code/">
        <img src="./book1-claude-code/assets/cover-wxb-en.svg" alt="Kỹ nghệ Harness: Hướng dẫn Thiết kế cho Claude Code" width="280">
      </a>
      <br>
      <strong>Kỹ nghệ Harness: Hướng dẫn Thiết kế cho Claude Code</strong>
      <br>
      <a href="https://harness-books.agentway.dev/vi/book1-claude-code/">Đọc trực tuyến</a> ·
      <a href="https://harness-books.agentway.dev/vi/book1-claude-code/exported/book1-claude-code-vi.pdf">Tải PDF</a>
    </td>
    <td align="center" valign="top" width="50%">
      <a href="https://harness-books.agentway.dev/vi/book2-comparing/">
        <img src="./book2-comparing/assets/cover-wxb-en.svg" alt="Triết lý Thiết kế Harness của Claude Code và Codex" width="280">
      </a>
      <br>
      <strong>Triết lý Thiết kế Harness của Claude Code và Codex</strong>
      <br>
      <a href="https://harness-books.agentway.dev/vi/book2-comparing/">Đọc trực tuyến</a> ·
      <a href="https://harness-books.agentway.dev/vi/book2-comparing/exported/book2-comparing-vi.pdf">Tải PDF</a>
    </td>
  </tr>
</table>

Các cuốn sách này không nhằm mục đích đi qua từng dòng mã nguồn. Chúng tập trung vào cách một khung kiểm soát (harness) tổ chức các ràng buộc và việc thực thi, và cách một mô hình vốn không ổn định có thể được đưa vào một trật tự kỹ thuật bền vững. Phân lớp prompt, vòng lặp truy vấn (query loops), quyết định quyền hạn, quản trị ngữ cảnh, khôi phục thất bại, xác minh đa agent, các quy tắc cục bộ và các thể chế của nhóm cùng nhau tạo thành hệ cơ quan của một harness. Mối nguy hiểm thực sự không phải là mô hình thỉnh thoảng đưa ra câu trả lời sai, mà là hệ thống không có cấu trúc để xử lý hậu quả.

## Các Nhận định Cốt lõi

- Kỹ nghệ harness là về cách các cấu trúc ràng buộc tổ chức việc thực thi.
- Một khi mô hình viết mã nguồn đi vào môi trường kỹ thuật thực tế, vấn đề chính không còn là chất lượng câu trả lời mà là hậu quả hành vi.
- Prompt, công cụ, quyền hạn, trạng thái, khôi phục, xác minh và các thể chế không phải là những phụ kiện xung quanh hệ thống. Chúng là các cơ quan trong cùng một cấu trúc kiểm soát.
- Khi so sánh các hệ thống agent, câu hỏi then chốt không phải là danh sách tính năng mà là trật tự thực sự được đặt ở đâu.
- Nếu một nhóm không thể biến kinh nghiệm cá nhân thành các quy tắc có thể tái sử dụng, họ sẽ gặp khó khăn trong việc biến một agent thành một hệ thống ổn định.

## Nội dung Tập trung của Hai Cuốn sách

### Cuốn 1: Hướng dẫn Thiết kế cho Claude Code

Cuốn sách đầu tiên sử dụng Claude Code làm đối tượng quan sát và tập trung vào cấu trúc runtime. Mối quan tâm của nó là tại sao một hệ thống cuối cùng phải phát triển các thành phần như control plane, query loop, quyền của công cụ, quản trị ngữ cảnh, lộ trình khôi phục, xác minh đa agent và các quy tắc nhóm.

Bắt đầu với Cuốn 1 nếu đây là những câu hỏi bạn quan tâm:

- Tại sao kỹ nghệ harness không chỉ là kỹ nghệ prompt (prompt engineering) ở quy mô lớn hơn
- Tại sao prompt về cơ bản là một phần của control plane thay vì là một hộp trò chuyện
- Tại sao các lỗi của mô hình nên được coi là chuẩn mực runtime thay vì một sự kiện ngoại lệ
- Tại sao công việc đa agent và xác minh không nên được trộn lẫn vào một cơ chế mơ hồ
- Làm thế nào một nhóm có thể củng cố trải nghiệm cá nhân thành các thể chế kỹ thuật có thể tái sử dụng

### Cuốn 2: So sánh Claude Code và Codex

Cuốn sách thứ hai đặt Claude Code và Codex cạnh nhau và hỏi xem mỗi harness đặt trật tự ở đâu. Một con đường bắt đầu từ kỷ luật runtime; con đường còn lại bắt đầu từ một lớp điều khiển có cấu trúc hơn. Cả hai hệ thống đều có thể hoạt động, nhưng chúng phân phối thẩm quyền khác nhau.

Bắt đầu với Cuốn 2 nếu bạn quan tâm nhiều hơn đến việc lựa chọn hệ thống, đánh giá kiến trúc hoặc những gì cần học khi xây dựng harness của riêng bạn:

- Sự khác biệt lớn nhất về control plane giữa Claude Code và Codex là gì
- Cách điều chỉnh vai trò của query loop, luồng (threads), rollout và trạng thái (state)
- Quyền hạn, sandbox và ngôn ngữ chính sách đóng vai trò quản trị nào
- Làm thế nào các kỹ năng, hook và quy tắc cục bộ mã hóa các thói quen tổ chức vào hệ thống
- Nếu bạn muốn xây dựng harness của riêng mình, nên học hỏi từ ai trước và nghiên cứu lớp nào trước

## Lộ trình Đọc Khuyến nghị

- Muốn có toàn bộ khung trước: đọc Cuốn 1, sau đó đọc Cuốn 2.
- Đã quen thuộc với các công cụ coding agent và muốn xem trực tiếp sự phân chia kiến trúc: bắt đầu với Cuốn 2.
- Chỉ muốn xem kết luận: đọc Cuốn 1 Chương 9 cùng với Cuốn 2 Chương 7.

<details>
<summary><strong>Mục lục Đầy đủ</strong></summary>

### Cuốn 1 — Kỹ nghệ Harness: Hướng dẫn Thiết kế cho Claude Code

- [Giới thiệu](./book1-claude-code/locales/vi/index.md)
- [Lời nói đầu: Khung kiểm soát (Harness), Terminal và các Ràng buộc Kỹ thuật](./book1-claude-code/locales/vi/preface.md)
- [Chương 1 Tại sao Kỹ thuật Khung kiểm soát (Harness Engineering) lại quan trọng](./book1-claude-code/locales/vi/chapter-01-why-harness-engineering.md)
- [Chương 2 Prompt không phải là Tính cách, Prompt là Mặt phẳng Điều khiển (Control Plane)](./book1-claude-code/locales/vi/chapter-02-prompt-is-control-plane.md)
- [Chương 3 Vòng lặp Truy vấn (Query Loop): Nhịp đập của một Hệ thống Agent](./book1-claude-code/locales/vi/chapter-03-query-loop-heartbeat.md)
- [Chương 4 Công cụ, Quyền hạn và Ngắt (Tools, Permissions, and Interrupts): Tại sao Agent không thể chạm trực tiếp vào thế giới](./book1-claude-code/locales/vi/chapter-04-tools-permissions-interrupts.md)
- [Chương 5 Quản trị Ngữ cảnh (Context Governance): Bộ nhớ, CLAUDE.md và Rút gọn (Compact) như một Cơ chế Ngân sách](./book1-claude-code/locales/vi/chapter-05-context-memory-compact.md)
- [Chương 6 Lỗi và Khôi phục (Errors and Recovery): Một Hệ thống Agent tiếp tục hoạt động sau khi Thất bại](./book1-claude-code/locales/vi/chapter-06-errors-and-recovery.md)
- [Chương 7 Công việc Đa Agent và Xác minh (Multi-Agent Work and Verification): Quản lý sự Không ổn định thông qua Phân công Lao động](./book1-claude-code/locales/vi/chapter-07-multi-agent-and-verification.md)
- [Chương 8 Áp dụng trong Nhóm (Team Adoption): Biến một Công cụ Thông minh thành một Quy trình làm việc Bền vững](./book1-claude-code/locales/vi/chapter-08-team-landing-practices.md)
- [Chương 9 Mười Nguyên lý của Kỹ thuật Khung kiểm soát (Harness Engineering)](./book1-claude-code/locales/vi/chapter-09-ten-principles.md)
- [Phụ lục A Bảng kiểm (Checklists): Biến các Nguyên lý thành các Ràng buộc khả thi](./book1-claude-code/locales/vi/appendix-a-checklists.md)
- [Phụ lục B Sơ đồ: Vẽ Bộ khung Runtime](./book1-claude-code/locales/vi/appendix-b-diagram-notes.md)
- [Phụ lục C Bản đồ Nguồn (Source Map): Những File nào làm Cơ sở cho mỗi Chương](./book1-claude-code/locales/vi/appendix-c-source-map.md)

### Cuốn 2 — Triết lý Thiết kế Harness của Claude Code và Codex

- [Giới thiệu](./book2-comparing/locales/vi/index.md)
- [Bản đồ Đọc: Cách hiểu đồng thời cả Cuốn 1 và Cuốn sách So sánh này](./book2-comparing/locales/vi/chapter-00-reading-map.md)
- [Lời nói đầu: Hai Khung kiểm soát, không phải Phụ kiện trên cùng một con Ngựa](./book2-comparing/locales/vi/preface.md)
- [Chương 1: Tại sao chúng ta so sánh Claude Code và Codex](./book2-comparing/locales/vi/chapter-01-why-this-comparison.md)
- [Chương 2: Two Control Planes: Prompt Assembly and Instruction Fragments](./book2-comparing/locales/vi/chapter-02-two-control-planes.md)
- [Chương 3: Where the Heartbeat Lives: Query Loop Compared with Thread, Rollout, and State](./book2-comparing/locales/vi/chapter-03-loop-thread-and-rollout.md)
- [Chương 4: Tools, Sandboxes, and Policy Languages: Who Stops the Model from Moving Too Fast](./book2-comparing/locales/vi/chapter-04-tools-sandbox-and-exec-policy.md)
- [Chương 5: Skills, Hooks, and Local Rules: How a System Learns Local Discipline](./book2-comparing/locales/vi/chapter-05-skills-hooks-and-local-governance.md)
- [Chương 6: Delegation, Verification, and Persistent State: Who Prevents a System from Grading Itself](./book2-comparing/locales/vi/chapter-06-delegation-verification-and-state.md)
- [Chương 7: Hội tụ qua các Con đường Khác nhau, hoặc các Nhánh riêng biệt](./book2-comparing/locales/vi/chapter-07-convergence-and-divergence.md)
- [Chương 8: Nếu bạn đang tự Xây dựng Harness của riêng mình, nên Nghiên cứu phần nào trước](./book2-comparing/locales/vi/chapter-08-how-to-choose-or-build.md)
- [Phụ lục A: Bản đồ Nguồn làm Cơ sở cho việc So sánh](./book2-comparing/locales/vi/appendix-a-source-map.md)
- [Phụ lục B: Bảng kiểm để Xác định Vị trí Khung kiểm soát của bạn](./book2-comparing/locales/vi/appendix-b-checklists.md)

</details>

## Muốn Tiếp tục Thực hành? Hãy thử AgentWay

<table>
<tr>
<td width="180" align="center" valign="middle">
  <a href="https://agentway.dev/">
    <img src="assets/agentway-logo.svg" alt="AgentWay" width="150">
  </a>
</td>
<td valign="middle">
  <b><a href="https://agentway.dev/">AgentWay</a></b> là một nền tảng thực hành liên quan nhưng độc lập. Harness Books giải thích cấu trúc kiểm soát, đánh giá kỹ thuật và phân kỳ kiến trúc. AgentWay là nơi những ý tưởng này tiếp tục đi vào các lộ trình đào tạo, diễn tập, bài tập dự án và agent PoC.
</td>
</tr>
</table>

## Xây dựng Cục bộ

Xây dựng hai trang web Honkit nhận biết ngôn ngữ và sau đó lắp ráp trang Pages thống nhất:

```bash
python3 tools/book-kit/build_honkit.py book1-claude-code
python3 tools/book-kit/build_honkit.py book1-claude-code --locale vi
python3 tools/book-kit/build_comparing.py
python3 tools/book-kit/build_comparing.py --locale vi
```

Đầu ra cuối cùng được ghi vào `dist/`.

---

<sub>Keywords: Harness Engineering, Claude Code guide, Claude Code vs Codex, AI coding agent, control plane, query loop, agent recovery, agent verification, local governance, approval policy</sub>
