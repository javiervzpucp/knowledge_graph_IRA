import os
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
import pandas as pd
import re
import json

# === CONFIGURACIÓN ===
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # ⚠️ AJUSTAR según el sistema
PDF_DIR = Path("documentos")
TAB_PATH = Path("metadatos/La Bella Limeña.tab")
OUTPUT_JSON = Path("output/ocr_con_metadatos.jsonl")
OUTPUT_JSON.parent.mkdir(exist_ok=True)

# === Cargar metadatos (.tab) ===
df = pd.read_csv(TAB_PATH, sep="\t")
df = df[[
    "dc.date.issued",
    "dc.subject[es_ES]",
    "dc.title[es_ES]",
    "dc.identifier.uri"
]].copy()
df["id"] = df["dc.date.issued"].str.replace("-", "", regex=False)
meta_lookup = {row["id"]: row for _, row in df.iterrows()}

# === Limpieza OCR ===
def limpiar_texto(text):
    text = re.sub(r"[‐–—−]+", "\n", text)
    text = re.sub(r"\.{3,}", "…", text)
    text = re.sub(r"[^\S\r\n]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()

# === OCR + Integración ===
output = []

for pdf_file in PDF_DIR.glob("*.pdf"):
    print(f"📄 Procesando: {pdf_file.name}")
    match = re.search(r"(\d{4})-(\d{2})-(\d{2})", pdf_file.name)
    if not match:
        print("  ⚠️ No se encontró fecha en el nombre.")
        continue

    fecha_id = "".join(match.groups())  # yyyyMMdd
    if fecha_id not in meta_lookup:
        print(f"  ⚠️ No hay metadatos para {fecha_id}")
        continue

    # OCR con PyMuPDF
    doc = fitz.open(pdf_file)
    full_text = ""
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        page_text = pytesseract.image_to_string(img, lang="spa")
        full_text += f"\n\n--- Página {i+1} ---\n\n{page_text}"

    full_text = limpiar_texto(full_text)

    row = meta_lookup[fecha_id]
    output.append({
        "id": fecha_id,
        "date": row["dc.date.issued"],
        "title": row["dc.title[es_ES]"],
        "labels": row["dc.subject[es_ES]"],
        "source": row["dc.identifier.uri"],
        "text": full_text
    })
    print(f"✅ OCR + metadatos para {fecha_id}")

# === Guardar como JSONL ===
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    for item in output:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"🎉 {len(output)} documentos guardados en: {OUTPUT_JSON}")
