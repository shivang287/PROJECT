from pdf_operations import PDFToolkit
import os

tool = PDFToolkit()

files = [
    file for file in os.listdir("PDF_TOOLKIT/sample_pdfs")
    if file.endswith(".pdf") and file != "merged.pdf"
]

#tool.merge(files, "PDF_TOOLKIT/sample_pdfs/merged.pdf")

#tool.split("PDF_TOOLKIT/sample_pdfs/file2.pdf")

#tool.rotate("PDF_TOOLKIT/sample_pdfs/rotated_merged.pdf","PDF_TOOLKIT/sample_pdfs/rotated_merged.pdf", 90)

#tool.delete("PDF_TOOLKIT/sample_pdfs/merged.pdf","PDF_TOOLKIT/sample_pdfs/Updated_m.pdf",list(range(42)))

#tool.extract_pages("PDF_TOOLKIT/sample_pdfs/Updated_m.pdf", "PDF_TOOLKIT/sample_pdfs/Extracted_m.pdf", [1,2,3])

#tool.watermark("PDF_TOOLKIT/sample_pdfs/Updated_m.pdf","PDF_TOOLKIT/sample_pdfs/file3.pdf","PDF_TOOLKIT/sample_pdfs/Watermark.pdf")

#tool.encryption("PDF_TOOLKIT/sample_pdfs/file2.pdf","admin123","PDF_TOOLKIT/sample_pdfs/Locked_file2.pdf")

#tool.decryption("PDF_TOOLKIT/sample_pdfs/Locked.pdf","admin123","PDF_TOOLKIT/sample_pdfs/unlocked.pdf")

#tool.pdf_to_image("PDF_TOOLKIT/sample_pdfs/unlocked.pdf","PDF_TOOLKIT/PDF_TO_IMAGE")

#for i in range (0,8):
    #os.remove(f"PDF_TOOLKIT/PDF_TO_IMAGE/page_{i+1}.png")

#os.rmdir("PDF_TOOLKIT/PDF_TO_IMAGE")

#tool.image_to_pdf("PDF_TOOLKIT/PDF_TO_IMAGE","PDF_TOOLKIT/PDF_TO_IMAGE/GENERATED.pdf")

#tool.extract_text("PDF_TOOLKIT/sample_pdfs/file3.pdf","PDF_TOOLKIT/sample_pdfs/file3_text.txt")

#tool.search_word("PDF_TOOLKIT/sample_pdfs/file3.pdf","nikita mishra")

#text = tool.ocr_pdf("PDF_TOOLKIT/sample_pdfs/file3.pdf")

#tool.create_4up_grid("PDF_TOOLKIT/sample_pdfs/file3.pdf","PDF_TOOLKIT/sample_pdfs/create.pdf")

#tool.highlight_keyword("PDF_TOOLKIT/sample_pdfs/file3.pdf","PDF_TOOLKIT/sample_pdfs/highlighted.pdf","nikita mishra")

