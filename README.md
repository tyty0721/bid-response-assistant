# 供应商投标助手 bid-response-assistant

帮助企业把采购要求、真实证明、响应草稿和审查问题逐条对应。当前版本面向中国大陆政府采购服务类竞争性磋商；其他采购方式可分析材料，但不会给出完整合规或递交就绪结论。

这是运行在 Codex 等支持本地技能的智能体宿主中的 Skill，不是无人值守投标平台。智能体负责读懂条款和写作；Python 负责本地接收、引用与数据校验、十进制金额计算、版本比较、DOCX/CSV/JSON/Markdown 导出；XLSX 导出使用宿主的 Artifact Tool。没有外部模型密钥、采购账号或自动提交功能。

本仓库为公开提交作品，版本 **v0.1.0**。下载 [完整交付包](releases/v0.1.0/bid-response-assistant-delivery-v0.1.0.zip) 或 [独立技能安装包](releases/v0.1.0/bid-response-assistant-skill-v0.1.0.zip)，并用 [SHA256SUMS](releases/v0.1.0/SHA256SUMS.txt) 校验。安装包解压后只有一个 `bid-response-assistant/` 技能目录；完整包包含测试、文档和可复现工具。

## 交付目录

```text
skills/bid-response-assistant/  成品技能 入口及业务参考、脚本、记录示例
tests/                         自动测试、合成原始输入、行为测试集与真值
examples/                      可重跑的合成案例和实际资料包关键条款运行证据
docs/                          原设计、实现对应、测试报告、交付要求核查
tooling/                       演示运行、测试报告和打包工具
```

## 安装与使用

需要 Python 3.11+。安装 `requirements.txt` 中固定版本（本次 Windows 验证使用 Python 3.12.14）。将 `skills/bid-response-assistant` 整个文件夹复制到 `~/.codex/skills/`，重新开始会话即可发现。也可在当前工作中明确指定技能路径，不需要全局安装。

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python tooling/run_demo.py --output work/demo-v1
```

在宿主中说：

> 用 $bid-response-assistant 分析这个采购文件夹，先生成项目要求和证据缺口。有企业材料后再起草响应；引用原页，缺失信息不要编造。

演示是虚构数据，仅检查工作链条。真实使用先运行接收脚本，再由智能体阅读全文并按 `references/schemas.md` 写结构化记录：

```powershell
python skills/bid-response-assistant/scripts/ingest.py "采购文件夹" "work/project-v1"
python skills/bid-response-assistant/scripts/bid.py check "record.json" --workspace "work/project-v1" --as-of 2026-10-10 --output "checks-v1.json"
python skills/bid-response-assistant/scripts/bid.py export "record.json" --workspace "work/project-v1" --as-of 2026-10-10 --output "work/draft-v1"
```

如宿主提供 Node 与 `@oai/artifact-tool`，运行 `node skills/bid-response-assistant/scripts/export_matrix.mjs work/draft-v1/checks.json work/draft-v1/response-matrix.xlsx`。Codex 的 bundled Node 可通过 workspace dependency loader 获取，在工作区建立 node_modules 联接即可；不需要将运行时或联接打包。没有该可选库时 CSV 可用，不能宣称已生成 XLSX。

RAR 不在脚本中自动解压，先用可信本地工具解压；ZIP 支持路径、扩张和类型限制。PDF文字层、DOCX、UTF-8 TXT/MD可解析；扫描件需要获准本地OCR后人工回查，本版不携带OCR模型。短说明附件不会仅因字少被判失败。

## 能自动检查什么

引用是否确在来源块、原件和提取文本是否改变、采购块阅读台账、逐条响应缺口、证据类型/主体/有效期/产品版本、错误项目名称、大小写金额/合计/限价/有效期、保证金/代理费、低价关注和批准是否过期。未知竞争对手时实际价格分始终未知。

程序检查依赖智能体正确提取和分类。阅读台账不代表条款没有漏抽，填入确认人也不是实际授权证明；证据真实性、条款语义、主观方案质量和法律判断仍需人工。没有企业资料时正确输出为 `needs_information`，不是“可提交”。

## 状态与外部动作

审核完成最多为 `reviewed`，有真实人审记录后为 `approved_for_manual_submission`。本技能不报名、签章、加密、上传、解密、付款、联系代理或发送质疑投诉，也不生成已提交回执。版本变更撤销旧批准；输出目录必须是新目录，防止覆盖人工修改。

## 验证与材料来源

详细结果、边界与待验收项见 [测试报告](docs/test-report.md) 和 [设计到实现对应](docs/implementation-map.md)。自动测试、原资料包关键条款回归、独立智能体行为验证与业务人员验收是不同层次，不互相替代。

原始 workshop 包不包含本次技能作品的仓库或提交命名要求；其中递交说明面向真实采购平台。核查依据见 [交付要求](docs/delivery-instructions.md)。仓库不分发原始资料包与企业私密材料；原件留在用户本地。实际样本输出仅包含必要的规则摘录、出处和哈希。

## 许可证与借鉴

本仓库新编写代码和说明使用 MIT；原采购资料及引用不因本许可证改变权属。开源调研借鉴方法，没有复制第三方项目源码。Ponytail 已作为开发约束装载，未把它作为技能运行依赖。依赖与来源见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
