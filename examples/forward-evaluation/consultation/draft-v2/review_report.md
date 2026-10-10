# 响应审查报告

项目：C-SYN-02；状态：needs_information

程序检查不能证明证据真实或保证合规；需复核全文语义和正式公告。

| 等级 | 问题 | 要求 | 处理 |
|---|---|---|---|
| blocker | PROJECT_FIELD_MISSING | 项目 | Project or supplier field is unknown: name |
| blocker | DEADLINE_MISSING | 项目 | Supply the official notice and deadline; do not infer a date from the version ID |
| blocker | RESPONSE_GAP | C1-R001 | Missing, partial, conflicting or unconfirmed response |
| blocker | RESPONSE_GAP | C1-R002 | Missing, partial, conflicting or unconfirmed response |
| blocker | RESPONSE_GAP | C1-R004 | Missing, partial, conflicting or unconfirmed response |
| blocker | RESPONSE_GAP | C1-R005 | Missing, partial, conflicting or unconfirmed response |
| blocker | RESPONSE_GAP | C1-R006 | Missing, partial, conflicting or unconfirmed response |
| blocker | RESPONSE_GAP | C1-R007 | Missing, partial, conflicting or unconfirmed response |
| blocker | RESPONSE_GAP | C1-R008 | Missing, partial, conflicting or unconfirmed response |
| blocker | QUOTE_BASIS | 项目 | Currency or tax basis is unknown or differs; confirm the documented project basis |
| blocker | QUOTE_UPPERCASE | 项目 | Uppercase and numeric quote differ; do not silently correct an approved quote |
| blocker | QUOTE_UNAPPROVED | 项目 | Pricing decision needs company approval |
| blocker | VALIDITY_SHORT | 项目 | Response validity is missing or shorter than the documented minimum |
| blocker | DOCUMENT_CONFLICT | 项目 | 专门面向中小企业要求与企业自述大型企业冲突；不得虚填声明函，需先核实可参与性。 |
| blocker | DOCUMENT_CONFLICT | 项目 | 响应有效期90日不足至少120日，少30日，待企业批准修正并同步响应位置。 |
