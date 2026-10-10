# 文件输出复核记录

2026-10-10，Windows 11。DOCX 使用安装在本机的 LibreOffice，经文档技能的 `render_docx.py --emit_pdf` 转成逐页 PNG；XLSX 使用 Artifact Tool 导出、再次导入渲染，并用只读 XML / openpyxl 复核单元格值和公式。没有用 openpyxl 修改或生成工作簿。

## 实际查看范围

| 产物 | 已查看范围 | 结果 |
|---|---|---|
| synthetic-demo/draft/response-draft.docx | 1页全部 | 中文、标题、待补信息、页脚清楚；无文字重叠或裁切 |
| workshop/draft/response-draft.docx | 4页全部；最后一次修订另看发生变化的第2、3页 | 来源定位可读，长要求正常换行；无需当前响应的规则显示 reference_only |
| forward-evaluation/consultation/draft-v2/response-draft.docx | 3页全部 | 120日、60日、2%、大型企业与中小企业资格冲突均可读；第3页为结尾人工操作提醒 |
| forward-evaluation/amendment/draft-b-v1/response-draft.docx | 1页全部 | 新限价420000、保留旧报价450000用于提示、100日未改，状态及人工操作提醒清楚 |
| synthetic-demo/draft/response-matrix.xlsx | A:D顶部预览、结构回读 | 要求与状态清楚，无公式 |
| workshop/draft/response-matrix.xlsx | A:D顶部、E:G顶部渲染；全部20行7列结构及公式回读 | 中文正常，来源位置可读，0公式，19条要求 |
| consultation/draft/response-matrix.xlsx | A:D顶部、E:G第1–5行渲染；全部8条数据7列回读 | 长审核稿自动换行，0公式，全部值与 checks.json 一致 |
| amendment/draft/response-matrix.xlsx | A:D顶部预览；全部2条数据7列回读 | 值与 checks.json 一致，0公式 |

独立智能体原始观察中的 `docx_rendered: false` 是该智能体执行结束时的真实状态，保留不改。上表记录主智能体随后补做的渲染，不能回填成当时已完成。第一次公开招标留出案例只保留文本/JSON和执行记录，未将旧版 DOCX 作为最终样例分发。

## 修复与边界

首次渲染发现默认标题下沿出现多余边框，已在导出样式中移除并重新渲染。复核还修正了“无需当前单独响应”的规则在矩阵里误显示缺证的问题，并重导相关样例。

XLSX视觉抽查不等于逐单元格视觉验收；全部值/公式检查与抽查范围分别列出。DOCX是通用内部审核稿，不是平台正式响应文件模板。没有逐一复刻原资料包全部 Word 模板，没有验证采购平台格式、签章、加密或提交成功。这些输出也不能证明企业承诺、证据真实性或业务合规。
