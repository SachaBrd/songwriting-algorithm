from fpdf import FPDF

# save FPDF() class into a
# variable pdf
pdf = FPDF()

# Add a page
pdf.add_page()

# Title
pdf.set_font("Times", size=20)
pdf.cell(200, 10, txt="Song title",
         ln=1, align='C')

# Subtitle
pdf.set_font("Times", size=8)
pdf.cell(200, 10, txt="A randomly generated song",
         ln=2, align='L')

# save the pdf with name .pdf
pdf.output("../../assets/PDF_bin/Randomly_generated_song.pdf")