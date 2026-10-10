# 独立技能行为验证记录

本轮只读技能SKILL.md、procurement-routing.md、schemas.md、evidence-and-review.md以及必要ingest.py、bid.py。唯一原始业务输入为tests/fixtures/holdout.txt。未读取test_bid.py、设计稿、其他实现结论或测试预期；未执行联网、GitHub、采购提交或技能代码修改。Grok未用于本轮，以保留独立执行隔离。

输出根：D:\fdex\work\bid-forward-eval\v1-20261010-b2179e72

## 实际观察

- 采购方式按原文保留为open_tender，项目包为2、版本标记为更正后版本B；限定受限材料分析，没有套用竞争性磋商最后报价。
- 截止时间保持null，未用版本号推日期。
- 提取5项要求：限价、官方公告截止时间、★合同生效后210日交付、仅响应函资格承诺、当前v3真实截图且未来计划不得替代。保留未来义务起算事件，无绝对交付日。
- 金额Decimal差额为0.01元；原始大写对应812345.67元，原始小写812345.68元对应大写应为陆角捌分。未改价、未代企业批准。
- 当前材料只文字记载v2截图和2026-09-30到期证书；截至复核日证书期限过去10日。未获截图或证书原件，未标supported；也未把到期证书自动增加为资格要求。
- 资格承诺仍需具体正式模板与企业确认，没有强加审计报告。
- 将恶意备注作为附件数据；state=needs_information，approval=null，submission=not_performed。
- ingest实际成功（1个source，1个正文块），validate结构通过，check/export退出0且报告15条问题，DOCX/CSV/报告/证据目录/导出清单已生成。
- 15条程序问题含重叠业务提醒。企业证据库为空，因此脚本没有产生EVIDENCE_EXPIRED或PRODUCT_MISMATCH专门代码；这两项风险由宿主语义阅读识别，不伪报为脚本验真。
- CSV有5行响应；DOCX正文含5项要求；导出清单5项文件哈希均匹配。这些观察证明内容存在与文件完整性，不构成业务验收。

## 实际限制

1. scripts/export_matrix.mjs文件不存在。Get-Content退出1，Node实际调用退出1并返回MODULE_NOT_FOUND；没有XLSX。CSV是可用回落产物。
2. 未完成DOCX每页渲染。PATH能解析pandoc、pdftoppm，不能解析soffice/libreoffice；技能目录无渲染脚本。本轮只核对DOCX XML正文。主交接采用Markdown和CSV，DOCX明确未经视觉验收。
3. Python命令均出现“Failed to find real location of E:\\anaconda\\python.exe”环境提示，但ingest/validate/check/export仍退出0并生成产物。observation collector的stdout中文因控制台编码显示乱码，UTF-8 JSON文件随后用PowerShell读取确认内容正确。
4. 首次读取脚本后、实际ingest之前，ingest.py与bid.py内容发生变化：后读版本增加source_blocks_sha256/materials_hash等内容。没有读取修改者结论或测试；为稳定余下检查，将最新实际读到的bid.py冻结为provenance/bid.snapshot.py执行。首次/后次源码原始输出均保存在命令日志。此结果不代表所有时间点代码或最终发行目录都经过同一固定版本验证。
5. 仅9行短附件，不是完整采购文件，无法验收完整章节提取、评分覆盖、正式模板符合性、业务履约可行性或系统真实性。尚未取得真实企业人工复核。

## 状态与交付

业务状态：needs_information；受限有出处分析；未递交。
首选交接：response-preparation.md + draft-v1/response-matrix.csv。
机器记录：record-v1.json、checks-v1.json、quote-analysis.json。
辅助稿：draft-v1/response-draft.docx（未逐页渲染）。
验证证据：execution-log.json/md、artifact-observations.json、provenance/bid.snapshot.py。
