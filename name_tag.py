from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.colors import blue, white, grey
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import inch
import csv
import traceback,sys,os

img1path = "name_tag.png"
img2path = "name_tag2.png"
temp_name_pdf = "temp/name.pdf"
temp_tag_pdf = "temp/tag.pdf"
final_folder = "final/"


def generate_pdf(fname,lname,org):
	pWidth,pHeight = A4
	
	imgDoc = canvas.Canvas(temp_tag_pdf, pagesize=portrait(A4))
	imgDoc.setFillColor(grey)
	imgDoc.rect(0,0,pWidth,pHeight, fill=1) 
	imgPath = img1path
	imgDoc.drawImage(imgPath,1.5*inch,6*inch,5.5*inch,4*inch)   
	imgPath = img2path
	imgDoc.drawImage(imgPath,1.5*inch,1.5*inch,5.5*inch,4*inch)   
	imgDoc.save()

	c = canvas.Canvas(temp_name_pdf)
	c.setFont('Helvetica', 20)
	text = fname + ' '  + lname
	text_width = stringWidth(text, 'Helvetica', 20)
	y = 7.3*inch
	pdf_text_object = c.beginText((pWidth - text_width) / 2.0, y)
	pdf_text_object.textOut(text)
	c.drawText(pdf_text_object)

	c.setFont('Helvetica', 15)
	text = org
	text_width = stringWidth(text, 'Helvetica', 15)
	y = 7*inch
	c.setFillColorRGB(0.5,0.5,0.5)
	pdf_text_object = c.beginText((pWidth - text_width) / 2.0, y)
	pdf_text_object.textOut(text)
	c.drawText(pdf_text_object)

	c.setFont('Helvetica', 45)
	text = fname
	text_width = stringWidth(text, 'Helvetica', 45)
	y = 3*inch
	c.setFillColorRGB(1,1,1)
	pdf_text_object = c.beginText(1.7*inch, y)
	pdf_text_object.textOut(text)
	c.drawText(pdf_text_object)

	c.setFont('Helvetica', 35)
	text = lname
	text_width = stringWidth(text, 'Helvetica', 35)
	y = 2.5*inch
	c.setFillColorRGB(1,1,1)
	pdf_text_object = c.beginText(1.7*inch, y)
	pdf_text_object.textOut(text)
	c.drawText(pdf_text_object)

	c.setFont('Helvetica', 15)
	text = org
	text_width = stringWidth(text, 'Helvetica', 15)
	y = 2*inch
	c.setFillColorRGB(0.5,0.5,0.5)
	pdf_text_object = c.beginText(1.7*inch, y)
	pdf_text_object.textOut(text)
	c.drawText(pdf_text_object)

	c.save()

	# Use PyPDF to merge the image-PDF into the template
	overlay = PdfFileReader(file(temp_name_pdf,"rb")).getPage(0)
	page = PdfFileReader(file(temp_tag_pdf,"rb")).getPage(0)
	page.mergePage(overlay)

	#Save the result
	output = PdfFileWriter()
	output.addPage(page)
	output.write(file(final_folder + fname.replace(" ","_") +'_' + lname.replace(" ","_") +".pdf","w"))


try:       
	datafile=open('invitees.csv','rb')
	csvbuffer = csv.reader(datafile, delimiter='|')
	header = csvbuffer.next()
	for row in csvbuffer:
                print row
		generate_pdf(row[0],row[1],row[2])
	datafile.close()
except:
	print "Unexpected error:", sys.exc_info()
	print "Exception in user code:"
	print '-'*60
	traceback.print_exc(file=sys.stdout)
	print '-'*60
finally:
	pass

  
