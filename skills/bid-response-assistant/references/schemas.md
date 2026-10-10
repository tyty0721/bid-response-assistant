# record.json 版本1

[最小实例](../assets/record.example.json)是虚构案例，不是企业证据。

顶层：schema_version、project、procurement_source_ids、reviewed_blocks、requirements、evidence、responses、quote、conflicts、approval。ID唯一，未知业务值用null，空数组表示尚未提供。

- project：id/name/package/version/method/category/jurisdiction/company/deadline/rules/sources。deadline为带时区ISO或null。完整支持method=competitive_consultation、category=services且jurisdiction=CN-government-procurement。
- rules：budget/ceiling/response_deposit为人民币元十进制字符串；performance_deposit_rate/agency_fee_rate/low_price_ratio/price_deduction_rate为比例字符串；min_validity_days为整数。每项规则须在项目来源逐项有据，不套示例默认值。
- requirements[]：id/text/kind/mandatory/phase/response_required_now/proof_type/sources；可加section/product_version/marker/constraints/applicability。kind为qualification/substantive/scoring/contract/procedure。proof_type为none/promise/statement/license/historical_contract/screenshot/live_demo/textbook/copyright/platform_record。
- sources[]：source_id/block_id/quote。quote是连续短原文；NFKC归一化后核对。PDF块ID含物理页码；DOCX是正文/表格位置，不声称排版页码。
- evidence[]：id/type/entity/product_version/valid_until/statement/confirmed_by/confirmed_at/sources。promise需具体statement，历史与产品证明需原始来源。生成草稿不入证据库。
- responses[]：requirement_id/text/status/evidence_ids；not_applicable加applicability_reason和confirmed_by。
- quote：total/uppercase/currency/tax_inclusive/project_version/round/validity_days/approved_by/approved_at/items/price_deduction_rate；items含quantity/unit_price。金额拒绝浮点、负数、非有限数及超过两位小数。
- conflicts[]：description/sources/resolution。未解决冲突阻止就绪。
- approval：实际人审记录及input_hash。脚本不认证身份，不把自动填的人名当人审。

无需当前响应的规则在输出矩阵标 reference_only，仅供查阅，不表示缺证，也不表示企业能力获证。

manifest.json和source_blocks.json来自ingest。procurement_source_ids限定采购范围，企业证明不混入阅读覆盖台账。台账只能证明块被标记阅读，语义漏抽率另用独立真值验证。

命令独占创建输出；修改另存新版本。check/export显式传--as-of复核日期。指纹绑定业务输入，导出清单另有产物哈希；人工编辑产物后需重新复核，旧清单不证明新文件未变。
