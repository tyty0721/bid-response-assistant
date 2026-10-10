# 独立智能体行为观察

三例都是虚构留出材料，原始输入在 `tests/fixtures/holdout*.txt`。独立执行智能体只读技能、必要脚本和本例原始输入，未读测试预期、设计稿或 gold。主智能体负责整合与最后文件渲染。

| 案例目录 | 输入 | 结果证据 |
|---|---|---|
| open-bidding | holdout.txt | 受限分析，金额0.01元、v2/v3、过期证书、恶意备注；保留早期执行记录，不分发旧版DOCX |
| consultation | holdout-consultation.txt | record-v2、checks-v2、draft-v2；120日与90日冲突、2%履约保证金、中小企业与大型企业自报冲突 |
| amendment | holdout-amendment.txt | record-b-updated、checks-b、diff-v1、draft-b-v1；只改明确限价，旧报价超限30000元、批准失效、100日未改 |

所有案例的最终状态都是 needs_information，批准为 null，采购递交未执行。问题条数包含重叠提醒，不是独立缺陷计数。这些观察不等于三份真实采购文件盲测或企业业务验收。

原记录中的本机绝对路径仅用于追踪执行现场；公开仓库相应记录位于各案例目录。原 intake/corpus 未复制，合成原始输入已在测试目录提供，可自行重新接收。早期观察中 XLSX 脚本不存在等缺口如实保留；随后两例实际完成 XLSX。独立执行结束时未逐页渲染，主智能体随后补做的范围见 [视觉复核](../../docs/visual-qa.md)。

留存范围：三例均附执行智能体保存的工具执行日志；后两例另含运行前后脚本哈希、输入记录和实际输出。核验应交叉查看 observations.json、各记录、checks、diff 和 handoff_manifest，并按原始合成附件重跑。日志是执行留痕，不构成独立业务真值。
