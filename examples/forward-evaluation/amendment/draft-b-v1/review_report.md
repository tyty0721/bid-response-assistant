# 响应审查报告

项目：D-SYN-03；状态：needs_information

程序检查不能证明证据真实或保证合规；需复核全文语义和正式公告。

| 等级 | 问题 | 要求 | 处理 |
|---|---|---|---|
| blocker | PROJECT_FIELD_MISSING | 项目 | Project or supplier field is unknown: name |
| blocker | PROJECT_FIELD_MISSING | 项目 | Project or supplier field is unknown: company |
| blocker | DEADLINE_MISSING | 项目 | Supply the official notice and deadline; do not infer a date from the version ID |
| blocker | RESPONSE_GAP | D1-R001 | Missing, partial, conflicting or unconfirmed response |
| blocker | RESPONSE_GAP | D1-R002 | Missing, partial, conflicting or unconfirmed response |
| blocker | QUOTE_BASIS | 项目 | Currency or tax basis is unknown or differs; confirm the documented project basis |
| blocker | QUOTE_STALE | 项目 | Quote uses another procurement version |
| blocker | QUOTE_UPPERCASE | 项目 | Uppercase and numeric quote differ; do not silently correct an approved quote |
| blocker | QUOTE_UNAPPROVED | 项目 | Pricing decision needs company approval |
| blocker | QUOTE_CEILING | 项目 | Quote exceeds the package ceiling |
| blocker | VALIDITY_RULE_MISSING | 项目 | Documented validity requirement is unknown; do not infer a minimum |
| blocker | DOCUMENT_CONFLICT | 项目 | A版报价450000元比B版新限价420000元高30000元，必须重新定价和批准，当前未调整。 |
| blocker | DOCUMENT_CONFLICT | 项目 | 企业报价批准据附件仅适用于A版，不能沿用到B版；真实历史批准记录未提供，本轮不验证或重建批准。 |
