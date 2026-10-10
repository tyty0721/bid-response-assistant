# 第三方依赖与参考

运行依赖：pypdf 6.10.0（BSD-3-Clause）、python-docx 1.2.0（MIT，间接依赖lxml、typing_extensions）。XLSX 为可选的宿主能力，使用 Codex bundled @oai/artifact-tool，不分发其包或运行时；实际版本记录在测试报告。本仓库新代码没有复制这些库源码。

方法参考：tender-review-kit（MIT）的引用锚点及覆盖候选扫描；BidPilot（MIT）的要求/证据/响应数据关系。研究仅作设计参考，未复制实现。详细检索证据和其他候选许可在 docs/design.md。

[Ponytail](https://github.com/DietrichGebert/ponytail)（MIT）作为开发阶段的简洁实现和复核指引，三个技能装载在开发者本机，不打入本成品，也不是运行依赖。完整插件生命周期钩子未安装。

采购文件摘录用于分析与验证，权利仍属原权利人。原始RAR、PDF、DOCX不随GitHub交付；本库MIT许可不授权重新分发第三方资料。
