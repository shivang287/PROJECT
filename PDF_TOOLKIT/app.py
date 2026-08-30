from flask import Flask, request, send_file, jsonify, render_template
from google import genai
from embedding_rag import EmbeddingRAG
from werkzeug.utils import secure_filename
from pathlib import Path
import tempfile
import shutil
import zipfile
import os
from pathlib import Path

from pdf_operations import PDFToolkit

app = Flask(__name__)

OUTPUT_FOLDER = Path("outputs")
OUTPUT_FOLDER.mkdir(exist_ok=True)
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB

tool = PDFToolkit()
gemini = genai.Client()
rag = EmbeddingRAG()

def save_upload(file, folder=UPLOAD_DIR):
    if not file or not file.filename:
        raise ValueError("No file selected.")
    filename = secure_filename(file.filename)
    path = Path(folder) / filename
    file.save(path)
    return path


def output_path(name):
    return OUTPUT_DIR / secure_filename(name)


@app.route("/")
def home():
    return render_template("index.html")


@app.post("/merge")
def merge():
    files = request.files.getlist("files")
    if len(files) < 2:
        return jsonify(error="Upload at least two PDFs using field name 'files'."), 400

    # Your merge() currently expects filenames inside
    # PDF_TOOLKIT/sample_pdfs, so for Flask we merge uploaded paths here.
    from pypdf import PdfReader, PdfWriter

    out = output_path(request.form.get("output_name", "merged.pdf"))
    writer = PdfWriter()

    try:
        for f in files:
            path = save_upload(f)
            reader = PdfReader(str(path))
            for page in reader.pages:
                writer.add_page(page)

        with open(out, "wb") as fp:
            writer.write(fp)

        return send_file(out, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.post("/ai-upload")
def ai_upload():

    file = request.files.get("file")

    if not file:

        return jsonify(
            error="Please upload a PDF."
        ), 400


    try:

        # Save PDF

        pdf_path = save_upload(file)


        # Extract page-by-page text

        pages = tool.extract_text_by_page(
            str(pdf_path)
        )


        # Create embeddings +
        # save FAISS index

        document_id = (
            rag.create_document_index(
                pages
            )
        )


        return jsonify({

            "message":
                "PDF processed successfully.",

            "document_id":
                document_id

        })


    except Exception as e:

        print(
            "AI UPLOAD ERROR:",
            e
        )

        return jsonify(
            error=str(e)
        ), 500

@app.post("/ai-question")
def ai_question():

    data = request.get_json()

    if not data:

        return jsonify(
            error="Invalid request."
        ), 400


    document_id = data.get(
        "document_id"
    )

    question = data.get(
        "question"
    )


    if not document_id:

        return jsonify(
            error="Document ID missing."
        ), 400


    if not question:

        return jsonify(
            error="Question missing."
        ), 400


    try:

        # =================================
        # VECTOR SEARCH
        # =================================

        relevant_chunks = rag.retrieve(

            document_id,

            question,

            top_k=5

        )


        # =================================
        # BUILD CONTEXT
        # =================================

        context_parts = []


        for chunk in relevant_chunks:

            context_parts.append(

                f"""
[PAGE {chunk["page"]}]

{chunk["text"]}
"""

            )


        context = "\n".join(
            context_parts
        )


        # =================================
        # GEMINI
        # =================================

        prompt = f"""
You are a PDF question-answering assistant.

Answer using ONLY the provided PDF context.

Do not use outside information.

If the answer is not available in the context,
say:

"I could not find this information in the PDF."

Mention supporting page numbers when appropriate.


PDF CONTEXT:

{context}


QUESTION:

{question}
"""


        response = (
            gemini.models.generate_content(

                model="gemini-3.5-flash",

                contents=prompt

            )
        )


        pages_used = sorted(
            set(
                chunk["page"]
                for chunk
                in relevant_chunks
            )
        )


        return jsonify({

            "answer":
                response.text,

            "pages":
                pages_used

        })


    except Exception as e:

        print(
            "AI QUESTION ERROR:",
            e
        )

        return jsonify(
            error=str(e)
        ), 500



@app.post("/split")
def split():
    file = request.files.get("file")
    if not file:
        return jsonify(error="Upload a PDF using field name 'file'."), 400

    from pypdf import PdfReader, PdfWriter

    try:
        path = save_upload(file)
        reader = PdfReader(str(path))

        temp_dir = Path(tempfile.mkdtemp(prefix="split_", dir=OUTPUT_DIR))
        for i, page in enumerate(reader.pages, start=1):
            writer = PdfWriter()
            writer.add_page(page)
            with open(temp_dir / f"page_{i}.pdf", "wb") as fp:
                writer.write(fp)

        zip_path = output_path("split_pages.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for pdf in temp_dir.glob("*.pdf"):
                z.write(pdf, pdf.name)

        shutil.rmtree(temp_dir, ignore_errors=True)
        return send_file(zip_path, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.post("/rotate")
def rotate():
    file = request.files.get("file")
    angle = request.form.get("angle", type=int)
    if not file or angle is None:
        return jsonify(error="Required: file and angle."), 400

    if angle not in (90, 180, 270, -90, -180, -270):
        return jsonify(error="Angle must be 90, 180, 270 or their negative values."), 400

    try:
        path = save_upload(file)
        out = output_path("rotated.pdf")
        tool.rotate(str(path), str(out), angle)
        return send_file(out, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.post("/delete-pages")
def delete_pages():
    file = request.files.get("file")
    pages = request.form.get("pages", "")
    if not file or not pages:
        return jsonify(error="Required: file and pages, e.g. 1,3,5."), 400

    try:
        # Convert human page numbers (1,3,5) to Python indexes (0,2,4)
        page_indexes = [int(x.strip()) - 1 for x in pages.split(",")]
        path = save_upload(file)
        out = output_path("pages_deleted.pdf")
        tool.delete(str(path), str(out), page_indexes)
        return send_file(out, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.post("/extract-pages")
def extract_pages():
    file = request.files.get("file")
    pages = request.form.get("pages", "")
    if not file or not pages:
        return jsonify(error="Required: file and pages, e.g. 1,2,5."), 400

    try:
        page_indexes = [int(x.strip()) - 1 for x in pages.split(",")]
        path = save_upload(file)
        out = output_path("extracted_pages.pdf")
        tool.extract_pages(str(path), str(out), page_indexes)
        return send_file(out, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.post("/watermark")
def watermark():
    file = request.files.get("file")
    watermark_file = request.files.get("watermark")
    if not file or not watermark_file:
        return jsonify(error="Required: file and watermark."), 400

    try:
        path = save_upload(file)
        wm_path = save_upload(watermark_file)
        out = output_path("watermarked.pdf")
        tool.watermark(str(path), str(wm_path), str(out))
        return send_file(out, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.post("/add-signature")
def add_signature():

    pdf_file = request.files.get("file")
    signature_file = request.files.get("signature")

    page_number = int(
        request.form.get("page", 1)
    )

    x = float(
        request.form.get("x", 100)
    )

    y = float(
        request.form.get("y", 100)
    )

    width = float(
        request.form.get("width", 150)
    )

    height = float(
        request.form.get("height", 60)
    )

    if not pdf_file:
        return jsonify(
            error="Please upload a PDF."
        ), 400

    if not signature_file:
        return jsonify(
            error="Please upload a signature image."
        ), 400

    try:

        pdf_path = save_upload(pdf_file)

        signature_path = save_upload(
            signature_file
        )

        output_path = (
            OUTPUT_FOLDER /
            "signed.pdf"
        )

        tool.add_signature(
            str(pdf_path),
            str(signature_path),
            str(output_path),
            page_number,
            x,
            y,
            width,
            height
        )

        return send_file(
            output_path,
            as_attachment=True,
            download_name="signed.pdf"
        )

    except Exception as e:

        print(
            "SIGNATURE ERROR:",
            e
        )

        return jsonify(
            error=str(e)
        ), 500


@app.post("/encrypt")
def encrypt():
    file = request.files.get("file")
    password = request.form.get("password")
    if not file or not password:
        return jsonify(error="Required: file and password."), 400

    try:
        path = save_upload(file)
        out = output_path("encrypted.pdf")
        tool.encryption(str(path), password, str(out))
        return send_file(out, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.post("/decrypt")
def decrypt():
    file = request.files.get("file")
    password = request.form.get("password")
    if not file or password is None:
        return jsonify(error="Required: file and password."), 400

    try:
        path = save_upload(file)
        out = output_path("decrypted.pdf")
        result = tool.decryption(str(path), password, str(out))
        if result is False:
            return jsonify(error="The uploaded PDF is not encrypted."), 400
        if not out.exists():
            return jsonify(error="Could not decrypt PDF. Check the password."), 400
        return send_file(out, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.post("/pdf-to-images")
def pdf_to_images():
    file = request.files.get("file")
    if not file:
        return jsonify(error="Upload a PDF using field name 'file'."), 400

    try:
        path = save_upload(file)
        image_dir = Path(tempfile.mkdtemp(prefix="images_", dir=OUTPUT_DIR))
        tool.pdf_to_image(str(path), str(image_dir))

        zip_path = output_path("pdf_images.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for image in image_dir.glob("*.png"):
                z.write(image, image.name)

        shutil.rmtree(image_dir, ignore_errors=True)
        return send_file(zip_path, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.post("/images-to-pdf")
def images_to_pdf():
    files = request.files.getlist("files")
    if not files:
        return jsonify(error="Upload images using field name 'files'."), 400

    try:
        image_dir = Path(tempfile.mkdtemp(prefix="uploaded_images_", dir=UPLOAD_DIR))
        for f in files:
            save_upload(f, image_dir)

        out = output_path("images.pdf")
        tool.image_to_pdf(str(image_dir), str(out))
        shutil.rmtree(image_dir, ignore_errors=True)

        if not out.exists():
            return jsonify(error="PDF was not created."), 500
        return send_file(out, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.post("/extract-text")
def extract_text():
    file = request.files.get("file")
    if not file:
        return jsonify(error="Upload a PDF using field name 'file'."), 400

    try:
        path = save_upload(file)
        text = tool.extract_text(str(path))
        return jsonify(text=text)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.post("/search")
def search():
    file = request.files.get("file")
    keyword = request.form.get("keyword")
    if not file or not keyword:
        return jsonify(error="Required: file and keyword."), 400

    # Return useful web data rather than relying on print() in search_word().
    import fitz

    try:
        path = save_upload(file)
        doc = fitz.open(str(path))
        results = []

        for page_number, page in enumerate(doc, start=1):
            matches = page.search_for(keyword)
            if matches:
                results.append({
                    "page": page_number,
                    "occurrences": len(matches)
                })

        doc.close()
        return jsonify(
            keyword=keyword,
            total_occurrences=sum(r["occurrences"] for r in results),
            results=results
        )
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.post("/highlight")
def highlight():
    file = request.files.get("file")
    keyword = request.form.get("keyword")
    if not file or not keyword:
        return jsonify(error="Required: file and keyword."), 400

    # Implemented here because highlight_keyword() in the supplied file
    # currently saves/closes the document inside the page loop.
    import fitz

    try:
        path = save_upload(file)
        out = output_path("highlighted.pdf")
        doc = fitz.open(str(path))

        for page in doc:
            for rect in page.search_for(keyword):
                annot = page.add_highlight_annot(rect)
                annot.update()

        doc.save(str(out))
        doc.close()
        return send_file(out, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.post("/ocr")
def ocr():
    file = request.files.get("file")
    if not file:
        return jsonify(error="Upload a PDF using field name 'file'."), 400

    try:
        path = save_upload(file)
        text = tool.ocr_pdf(str(path))

        out = output_path("ocr_text.txt")
        out.write_text(text, encoding="utf-8")
        return send_file(out, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.post("/four-up")
def four_up():
    file = request.files.get("file")
    if not file:
        return jsonify(error="Upload a PDF using field name 'file'."), 400

    try:
        path = save_upload(file)
        out = output_path("4up.pdf")
        tool.create_4up_grid(str(path), str(out))
        return send_file(out, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.errorhandler(413)
def too_large(_):
    return jsonify(error="File is too large. Maximum request size is 100 MB."), 413


if __name__ == "__main__":
    app.run(debug=True)
