import fs from 'node:fs/promises';
import path from 'node:path';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const [input, output, previewDir] = process.argv.slice(2);
if (!input || !output) throw new Error('Usage: node export_matrix.mjs checks.json matrix.xlsx [preview-directory]');
try { await fs.access(output); throw new Error('Output exists; choose a new version'); }
catch (e) { if (e.code !== 'ENOENT') throw e; }
const checks = JSON.parse(await fs.readFile(input, 'utf8'));
if (!Array.isArray(checks.matrix)) throw new Error('Expected a checks.json matrix');
const manifestPath = path.join(path.dirname(output), 'handoff_manifest.json');
let manifest;
try {
  manifest = JSON.parse(await fs.readFile(manifestPath, 'utf8'));
  if (manifest.input_hash !== checks.input_hash || manifest.materials_hash !== checks.materials_hash)
    throw new Error('Handoff and checks belong to different input versions');
} catch (e) { if (e.code !== 'ENOENT') throw e; }
const safe = v => /^[\s]*[=+@-]/u.test(String(v)) ? "'" + v : v;
const rows = [['要求ID', '类型', '要求原文', '状态', '响应审核稿', '证据ID', '来源位置'],
  ...checks.matrix.map(r => [r.id, r.kind, r.text, r.status, r.response || '待补证据或企业确认',
    r.evidence_ids.join(', '), r.sources.map(s => `${s.source_id} ${s.block_id}`).join('; ')].map(safe))];
const workbook = Workbook.create();
const sheet = workbook.worksheets.add('响应矩阵');
sheet.showGridLines = false;
sheet.getRange(`A1:G${rows.length}`).values = rows;
const area = sheet.getRange(`A1:G${rows.length}`);
area.format.font = { name: 'Microsoft YaHei', size: 11 };
area.format.wrapText = true;
area.format.verticalAlignment = 'center';
area.format.borders = { preset: 'all', style: 'thin', color: '#D9D9D9' };
sheet.getRange('A:A').format.columnWidth = 24;
sheet.getRange('B:B').format.columnWidth = 16;
sheet.getRange('C:C').format.columnWidth = 56;
sheet.getRange('D:D').format.columnWidth = 24;
sheet.getRange('E:E').format.columnWidth = 50;
sheet.getRange('F:F').format.columnWidth = 22;
sheet.getRange('G:G').format.columnWidth = 40;
sheet.getRange('A1:G1').format.fill = '#E5EDF5';
sheet.getRange('A1:G1').format.font = { name: 'Microsoft YaHei', bold: true, color: '#000000', size: 11 };
area.format.autofitRows();
sheet.getRange('A1:G1').format.rowHeight = 30;
sheet.freezePanes.freezeRows(1);
sheet.freezePanes.freezeColumns(1);
workbook.recalculate();
const inspected = await workbook.inspect({ kind: 'table', range: `响应矩阵!A1:G${Math.min(rows.length, 6)}`,
  include: 'values,formulas', tableMaxRows: 6, tableMaxCols: 7, maxChars: 2500 });
await fs.mkdir(path.dirname(output), { recursive: true });
await (await SpreadsheetFile.exportXlsx(workbook)).save(output);
if (previewDir) {
  await fs.mkdir(previewDir, { recursive: true });
  const preview = await workbook.render({ sheetName: '响应矩阵', range: `A1:D${Math.min(rows.length, 7)}`, scale: 1.5 });
  await fs.writeFile(path.join(previewDir, 'matrix.png'), new Uint8Array(await preview.arrayBuffer()));
  await fs.writeFile(path.join(previewDir, 'inspection.ndjson'), inspected.ndjson);
}
// XLSX is added after Python export; refresh the handoff hash list if present.
if (manifest) {
  const { createHash } = await import('node:crypto');
  manifest.files[path.basename(output)] = createHash('sha256').update(await fs.readFile(output)).digest('hex');
  await fs.writeFile(manifestPath, JSON.stringify(manifest, null, 2), 'utf8');
}
console.log(JSON.stringify({ output, rows: rows.length - 1, formulas: 0, submission: 'not_performed' }));
