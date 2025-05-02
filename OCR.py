import os
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

# === CONFIGURACIÓN GENERAL ===

# Ruta a tesseract.exe si NO lo agregaste al PATH (ajústalo según tu instalación)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # ⚠️ AJUSTAR si es necesario

INPUT_DIR = Path("documentos")
OUTPUT_DIR = Path("ocr_resultados")
OUTPUT_DIR.mkdir(exist_ok=True)

# === PROCESAMIENTO DE TODOS LOS PDFs ===

pdf_files = list(INPUT_DIR.glob("*.pdf"))

for pdf_file in pdf_files:
    print(f"📄 Procesando: {pdf_file.name}")
    doc = fitz.open(pdf_file)
    ocr_text = ""

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)  # renderiza en alta resolución
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # OCR con idioma español
        text = pytesseract.image_to_string(img, lang="spa")
        ocr_text += f"\n\n--- Página {i + 1} ---\n\n{text}"
        print(f"  ✅ Página {i + 1} procesada")

    # Guardar resultado .txt
    output_path = OUTPUT_DIR / (pdf_file.stem.replace(" ", "_") + "_tesseract.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ocr_text)

    print(f"✅ Guardado: {output_path.name}\n")

print("🎉 OCR completado con Tesseract para todos los PDFs.")
