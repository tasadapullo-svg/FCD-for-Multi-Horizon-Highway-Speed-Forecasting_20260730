import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = "D:/2026_AJSE_FINAL/05_COMPREHENSIVE_DATA_RESULT_AUDIT_20260730";
const output = `${root}/AJSE_DATA_RESULT_AUDIT_MASTER.xlsx`;
const previewDir = `${root}/06_REPORTS/workbook_previews`;
await fs.mkdir(previewDir, { recursive: true });

const sources = [
  ["Executive_Summary", `${root}/06_REPORTS/executive_summary_for_workbook.csv`],
  ["A0_A13_Crosswalk", `${root}/02_EXPERIMENT_RESULT_CROSSWALK/outline_experiment_result_crosswalk.csv`],
  ["Result_Families", `${root}/02_EXPERIMENT_RESULT_CROSSWALK/result_family_definition_comparison.csv`],
  ["D_Drive_Top", `${root}/01_D_DRIVE_INVENTORY/d_drive_top_level_inventory.csv`],
  ["Project_Families", `${root}/01_D_DRIVE_INVENTORY/research_family_summary.csv`],
  ["Window_Index", `${root}/03_DATASET_VALIDATION/legacy_window_index_summary.csv`],
  ["Boundary_Audit", `${root}/03_DATASET_VALIDATION/phase13_complete_hour_boundary_summary.csv`],
  ["Phase13_Ranking", `${root}/04_METRIC_RECALCULATION/phase13_model_ranking.csv`],
  ["Metric_Recompute", `${root}/04_METRIC_RECALCULATION/phase13_prediction_metric_recalculation.csv`],
  ["Target_Recompute", `${root}/04_METRIC_RECALCULATION/target_recalculation_summary.csv`],
  ["Stats_Diagnostic", `${root}/05_BIAS_AND_DEVIATIONS/dependency_aware_day_level_diagnostic.csv`],
  ["Bias_Deviations", `${root}/05_BIAS_AND_DEVIATIONS/bias_and_deviation_register.csv`],
  ["Claims", `${root}/02_EXPERIMENT_RESULT_CROSSWALK/claim_evidence_matrix.csv`],
  ["Critical_Hashes", `${root}/07_HASHES/critical_hashes_for_workbook.csv`],
  ["Duplicate_Groups", `${root}/07_HASHES/duplicate_group_summary_for_workbook.csv`],
  ["Evidence_Registry", `${root}/08_REUSABLE_EVIDENCE/reusable_evidence_registry.csv`],
];

const wb = Workbook.create();

for (const [sheetName, csvPath] of sources) {
  const csvText = await fs.readFile(csvPath, "utf8");
  await wb.fromCSV(csvText, { sheetName });
}

const criticalStatusSheets = new Set(["Executive_Summary", "A0_A13_Crosswalk", "Bias_Deviations", "Claims"]);

for (let i = 0; i < sources.length; i++) {
  const [sheetName] = sources[i];
  const sheet = wb.worksheets.getItem(sheetName);
  sheet.showGridLines = false;
  sheet.freezePanes.freezeRows(1);
  const used = sheet.getUsedRange();
  used.format = {
    fill: "#FFFFFF",
    font: { name: "Arial", size: 9, color: "#000000" },
    verticalAlignment: "top",
    wrapText: true,
    borders: { preset: "all", style: "thin", color: "#D9E2F3" },
  };
  const header = used.getRow(0);
  header.format = {
    fill: criticalStatusSheets.has(sheetName) ? "#17365D" : "#1F4E78",
    font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
    verticalAlignment: "center",
    wrapText: true,
    borders: { preset: "all", style: "thin", color: "#A6B7CC" },
    rowHeight: 30,
  };
  used.format.autofitColumns();
  used.format.autofitRows();

  // Keep prose and path fields readable without allowing extremely wide sheets.
  const matrix = used.values;
  if (Array.isArray(matrix) && matrix.length > 0) {
    const headers = matrix[0].map((x) => String(x ?? ""));
    for (let c = 0; c < headers.length; c++) {
      const h = headers[c].toLowerCase();
      const col = used.getColumn(c);
      if (/path|source|evidence|note|issue|impact|action|claim|wording|summary|interpretation/.test(h)) {
        col.format.columnWidth = 44;
      } else if (/sha256|hash/.test(h)) {
        col.format.columnWidth = 56;
      } else if (/time|timestamp|last_write|creation|modified|(^|_)date($|_)/.test(h)) {
        col.format.columnWidth = 22;
        col.format.numberFormat = "yyyy-mm-dd hh:mm:ss";
      } else if (/mae|rmse|smape|mape|r2|bias|difference|change|ci_|p_value|raw_p|adjusted_p|mean|std/.test(h)) {
        col.format.columnWidth = 16;
        col.format.numberFormat = "0.000000";
      } else if (/^n$|count|rows|files|seeds|horizon|rank/.test(h)) {
        col.format.columnWidth = 14;
        col.format.numberFormat = "0";
      } else {
        col.format.columnWidth = 16;
      }
    }
  }

  // Add a filterable table for each evidence matrix.
  if (used.rowCount >= 2 && used.columnCount >= 1) {
    try {
      sheet.tables.add(used.address, true, `T_${i + 1}`);
    } catch (err) {
      // Formatting and content remain valid even if a table name/range is rejected.
    }
  }
}

// Highlight important status fields without changing any data.
const execSheet = wb.worksheets.getItem("Executive_Summary");
execSheet.getRange("A1:C14").format.rowHeight = 32;
execSheet.getRange("A2:A14").format.font = { name: "Arial", size: 9, bold: true, color: "#000000" };
execSheet.getRange("B2:B14").conditionalFormats.add("containsText", {
  text: "NOT",
  format: { fill: "#FCE4D6", font: { color: "#9C0006", bold: true } },
});
execSheet.getRange("B2:B14").conditionalFormats.add("containsText", {
  text: "PROHIBITED",
  format: { fill: "#FFC7CE", font: { color: "#9C0006", bold: true } },
});

const inspect = await wb.inspect({
  kind: "workbook,sheet,table",
  maxChars: 12000,
  tableMaxRows: 4,
  tableMaxCols: 8,
  tableMaxCellChars: 80,
});
await fs.writeFile(`${root}/06_REPORTS/workbook_structure_inspection.ndjson`, inspect.ndjson ?? String(inspect), "utf8");

const formulaErrors = await wb.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 200 },
  maxChars: 12000,
});
await fs.writeFile(`${root}/06_REPORTS/workbook_formula_error_scan.ndjson`, formulaErrors.ndjson ?? String(formulaErrors), "utf8");

for (const [sheetName] of sources) {
  const preview = await wb.render({ sheetName, autoCrop: "all", scale: 0.75, format: "png" });
  const safe = sheetName.replace(/[^A-Za-z0-9_-]/g, "_");
  await fs.writeFile(`${previewDir}/${safe}.png`, new Uint8Array(await preview.arrayBuffer()));
}

const xlsx = await SpreadsheetFile.exportXlsx(wb);
await xlsx.save(output);

console.log(JSON.stringify({ output, sheets: sources.map((x) => x[0]), previewDir }, null, 2));
