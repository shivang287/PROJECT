from pypdf import PdfReader, PdfWriter, PageObject,Transformation
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
import fitz
import os

class PDFToolkit:

    from pypdf import PdfReader, PdfWriter
import os


class PDFToolkit:

    def merge(self, input_files, output_file):
        writer = PdfWriter()

        # Loop through every PDF
        for pdf_file in input_files:

            # Create complete path
            full_path = os.path.join("PDF_TOOLKIT", "sample_pdfs", pdf_file)

            # Read the PDF
            reader = PdfReader(full_path)

            # Add every page to writer
            for page in reader.pages:
                writer.add_page(page)

        # Save merged PDF
        with open(output_file, "wb") as f:
            writer.write(f)

        print("PDFs merged successfully.")

    def split(self,input_file):
        reader = PdfReader(input_file)
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)

            output = f"{input_file}_page_{i+1}.pdf"

            with open(output, "wb") as f:
                writer.write(f)

        print("PDF split successfully.")

    def rotate(self, input_file, output_file, angle):
        reader = PdfReader(input_file)
        writer = PdfWriter()

        for page in reader.pages:
            page.rotate(angle)
            writer.add_page(page)

        with open(output_file, "wb") as f:
            writer.write(f)

        print(f"Rotate at {angle} degree successfully")

    def delete(self,input_file, output_file, pages_to_delete):
        reader = PdfReader(input_file)
        writer = PdfWriter()

        for i,page in enumerate(reader.pages):
            if i not in pages_to_delete:
                writer.add_page(page)

        with open(output_file, "wb") as f:
            writer.write(f)

        print("Pages Deleted.")

    def extract_pages(self, input_file, output_file, pages):
        reader = PdfReader(input_file)
        writer = PdfWriter()

        for page_num in pages:
            writer.add_page(reader.pages[page_num])

        with open(output_file, "wb") as f:
            writer.write(f)

        print("Pages extracted.")

    def watermark(self,input_file,watermark_file,output_file):
        reader = PdfReader(input_file)
        writer = PdfWriter()

        watermark_reader = PdfReader(watermark_file)

        watermark = watermark_reader.pages[0]

        for page in reader.pages:
            page.merge_page(watermark)
            writer.add_page(page)

        with open(output_file,"wb") as f:
            writer.write(f)
        print("Watermark added successfully.")

    def add_signature(self,input_file,sign,output_file,page_number=1,x=100,y=100,width=150,height=60):
        doc = fitz.open(input_file)
        try:
            if page_number<1 or page_number >len(doc):
                raise ValueError(
                    f"page number must be between 1 to {len(doc)}"
                )
            page = doc[page_number-1]

            rect = fitz.Rect(x,y,x+width,y+height)
            page.insert_image(rect,filename=sign,keep_proportion=True,overlay=True)
            doc.save(output_file)

        finally:
            doc.close()
        return output_file

    def encryption(self,input_file,password,output_file):
        reader = PdfReader(input_file)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(user_password=password,owner_password=None)

        with open(output_file, "wb") as f:
            writer.write(f)

        print("PDF Locked")

    def decryption(self,input_file,password,output_file):
        reader = PdfReader(input_file)
        writer = PdfWriter()

        if reader.is_encrypted:
            print("file is encrypted, Attempting to decrypt..")
            reader.decrypt(password)
        else:
            print("file is not encrypted..")
            return False

        for page in reader.pages:
            writer.add_page(page)

        with open(output_file,"wb") as f:
            writer.write(f)
        print("Decryption is done..")


    def pdf_to_image(self, input_file_path, output_folder):

     os.makedirs(output_folder, exist_ok=True)

     pdf = fitz.open(input_file_path)

     for i, page in enumerate(pdf):

        pix = page.get_pixmap(dpi=300)

        image_name = os.path.join(
            output_folder,
            f"page_{i+1}.png"
        )

        pix.save(image_name)

        print(f"Saved: {image_name}")

     pdf.close()

    def image_to_pdf(self,input_folder,output_file):
        images = []
        for file in sorted(os.listdir(input_folder)):
            if file.lower().endswith((".png",".jpg",".jpeg")):
                image_path = os.path.join(input_folder,file)
                image = Image.open(image_path)

                if image.mode == "RGBA":
                    image = image.convert("RGB")
                images.append(image)
            if not images:
                print("No Image Found")
                return
            images[0].save(output_file,save_all=True,append_images=images[1:])

        print("PDF created successfully.")

    def extract_text(self,input_file,output_file=None):
        doc = fitz.open(input_file)

        extracted_text = ""

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            extracted_text += f"\n-----page{page_num+1}----\n"
            extracted_text+=page.get_text()
        doc.close()

        if output_file:
            with open(output_file,"w",encoding="utf-8") as f:
                f.write(extracted_text)
            print(f"text saved to{output_file}")
        return extracted_text

    def extract_text_by_page(self,input_file):
        doc = fitz.open(input_file)
        pages = []
        for page_number in range(len(doc)):
            page = doc.load_page(page_number)
            text = page.get_text()
            pages.append((page_number+1,text))
        doc.close()
        return pages

    def search_word(self,input_file,keyword):
        doc = fitz.open(input_file)
        found = False
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            matches= page.search_for(keyword)
        if matches:
            found=True
            print(f"{keyword} is found on page {page_num+1}")
            print(f"occurrences: {len(matches)}")
        doc.close()

        if not found:
            print(f"{keyword} not found")

    def highlight_keyword(self,input_file,output_file,keyword):
        try:
            doc = fitz.open(input_file)
            total_matches = 0
            for page in doc:
                matches = page.search_for(keyword)
                for match in matches:
                    highlight = page.add_highlight_annot(match)
                    highlight.update()
                    total_matches+=1
                doc.save(output_file)
                doc.close()

                print(f"{total_matches} occurrences highlighted")
                print(f"saved as {output_file}")
        except Exception as e:
            print("Error: ",e)



    def ocr_pdf(self,input_file):
        pdf = fitz.open(input_file)
        text=""
        for page in pdf:
            pix = page.get_pixmap(dpi=300)
            image = Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
            text+=pytesseract.image_to_string(image)
        pdf.close()
        print("scanning done")
        return text

    def create_4up_grid(self,input_path, output_path):
    
        reader = PdfReader(input_path)
        writer = PdfWriter()
    
        first_page = reader.pages[0]
        width = float(first_page.mediabox.width)
        height = float(first_page.mediabox.height)
    
        for i in range(0, len(reader.pages), 4):
            grid_page = PageObject.create_blank_page(width=width, height=height)
        
            positions = [
                (0, height / 2),           
                (width / 2, height / 2),   
                (0, 0),                    
                (width / 2, 0)             
            ]
        
            for j in range(4):
                if i + j < len(reader.pages):
                    page = reader.pages[i + j]
                
                    transform = Transformation().scale(sx=0.5, sy=0.5).translate(tx=positions[j][0], ty=positions[j][1])
                    page.add_transformation(transform)
                
                    grid_page.merge_page(page)
                
            writer.add_page(grid_page)
        
        with open(output_path, "wb") as out_file:
            writer.write(out_file)
        
        print(f"Success: N-Up Grid PDF saved to {output_path}")

    

    

    