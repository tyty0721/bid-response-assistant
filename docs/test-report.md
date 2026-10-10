# 版本0.1.0验证记录

日期2026-10-10。结论：本地技能、确定性检查、文件输出和打包流程可运行；这是工程验证版本，尚未通过真实企业业务验收，不提供生产合规保证。

## 已执行的验证

| 层次 | 实际结果 | 证据 |
|---|---|---|
| Skill结构 | 官方quick_validate通过；UTF-8模式用于中文文件 | SKILL.md及references链接、agents配置 |
| 自动化 | 38项，0失败，0错误，0跳过 | tests/results/final-20261010-v2/result.json和unittest.log，含技能文件哈希 |
| 原资料接收 | 12文件，6PDF共52页，6DOCX，哈希及定位保留 | examples/workshop/materials-manifest.json |
| 关键条款回归 | 19个来源锚点匹配，引用错误0；状态needs_information，52个问题含未逐块复核提示 | examples/workshop/regression-result.json及record.json、draft/checks.json |
| 合成链条 | ingest→record→check→export；缺公司、公告、企业报价及承诺时保持待补 | examples/synthetic-demo |
| 独立智能体 | 单独读取原始合成材料和Skill，完成采购方式、金额、证据、恶意备注和更正案例 | examples/forward-evaluation（执行记录与观察） |
| 文件输出 | DOCX实际转PDF渲染，XLSX实际导出并回读值/行数/公式及哈希 | 样例draft与docs/visual-qa.md |
| 打包 | ZIP CRC与重复构建字节一致测试通过，排除原件、来源目录、运行时联接 | test_package.py及交付manifest、SHA256SUMS |

自动测试涉及金额大小写/精度/限价/合计/90日边界、低价严格小于、保证金和代理费区分、价格扣除、未知基准价、错误主体/过期/版本/类型证据、禁止自我证明、引用与文件/文本哈希、阅读覆盖、冲突、变更及批准失效、防覆盖、ZIP路径穿越/执行文件/扩张、短DOCX说明、CSV公式注入和法域/包号隔离。

tests/behavior-cases.json保存原设计T01–T28的场景和期望。它们并非28项全部通过独立业务验收：每条注明目前是程序测试、来源回查、技能审阅还是独立模型行为观察。尤其跨页表格理解、模板新企业填0条件、仅标题方案缺陷等仍不能仅凭程序断言准确。

## 独立验证与修复

第一次独立公开招标案例正确保留未知截止时间，识别报价超限0.01元、大写差0.01元、v2无法证明v3及过期材料；最终无批准、无递交。该轮发现XLSX辅助脚本当时尚未存在，且未逐页渲染；这些缺口保留在原观察，不改写为当时通过。

随后补齐XLSX脚本，执行最终合成留出案例：专门面向中小企业但企业自报大型、另一项目120日有效期、限价更正只影响明确范围和旧报价批准。最终观察文件记录实际执行版本哈希及未完成项，不把这些合成案例当作三份不同真实采购项目盲测。

复核额外修复了提取文本快照改变仍可能复用批准、非标准法域误入完整支持、规则缺失默认0日、空要求集假通过、更正范围漏撤批准、DOCX标题边框残留，以及无需当前响应的规则误标缺证。

## 环境与复现

Windows 11，Python 3.12.14；pypdf6.10.0、python-docx1.2.0。DOCX用已安装LibreOffice及技能render_docx.py渲染；XLSX用Codex bundle26.1007.11041提供的Node与Artifact Tool。库不打包进成品，无该宿主能力可保留CSV。

```powershell
python -m pip install -r requirements.txt
python tooling/run_tests.py --output work/test-rerun
python tooling/run_demo.py --output work/demo-rerun
python tooling/run_workshop_regression.py --materials "本机原解压目录" --workspace work/workshop-intake-rerun --output work/workshop-rerun
python tooling/package.py --output dist/rebuild
```

输出目录必须不存在。初次Windows沙盒临时目录权限错误已通过授权运行/显式工作区临时目录解决；中文官方校验器用Python UTF-8模式。原文件没有被覆盖或上传第三方OCR。

## 待完成的业务验收

需要三份不同真实采购文件的独立盲测、业务人员独立标注要求真值和两名业务用户试用，才能核实完整抽取召回、资格/实质条款漏项与方案可用性。未执行采购平台制作、签章、加密、上传、解密和回执核验；没有真实企业证据防伪验证。当前不报告无依据的准确率、节省工时、满分或中标提升数据。
