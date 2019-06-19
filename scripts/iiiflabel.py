#!/usr/local/bin/python3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import Color, black, blue, red
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth 
import sys
import csv
import math

# 6.3 height  + 0.4 6.7
def drawCard(canvas, cardX, cardY, data=[]):
    cardWidth, cardHeight = (10.5, 6.7)
    eventIndent = (0.4)
    eventWidth, eventHeight = (cardWidth - (eventIndent * 2),1)
    canvas.setFillColor(HexColor(0x000000))
    canvas.setStrokeColor(HexColor(0x000000))
    canvas.setDash(1)
    # logo
    x = cardX + eventIndent
    y = cardHeight + cardY - eventIndent - 1
    canvas.drawImage('images/IIIF-logo-500w.png',x=x*cm, y=(y*cm), width=1*cm, height=1*cm, preserveAspectRatio=True)
    # Card rect
    canvas.setLineWidth(0.5)
    #canvas.rect(cardX * cm,cardY*cm,cardWidth * cm,cardHeight * cm,fill=False, stroke=True)
    # event rect
    canvas.setLineWidth(1)
    canvas.rect((cardX + eventIndent) * cm,(cardY + eventIndent)*cm,eventWidth *cm,eventHeight*cm,fill=True, stroke=True)

    if data:
        #canvas.setFont("Open Sans", 3*cm)
        # 5.5cm
        # Pronoum
        print('Pronoum')
        safeFont(canvas,'Times-Bold', 16, (cardWidth - 4 - 0.8), data[1],cm)
        canvas.drawCentredString((cardX + (cardWidth / 2)) * cm, (cardY + 5.3)*cm, data[1])
        # name
        print('Name')
        safeFont(canvas,'Times-Bold', 36, cardWidth, data[0],cm)
        canvas.drawCentredString((cardX + (cardWidth / 2)) * cm, (cardY + 3.8)*cm, data[0])
        # company
        safeFont(canvas,'Times-Bold', 20, cardWidth, data[2],cm)
        canvas.drawCentredString((cardX + (cardWidth / 2)) * cm, (cardY + 2.8)*cm, data[2])
        # event
        canvas.setFillColor(HexColor("#FFFFFF"))
        safeFont(canvas,'Times-Bold', 16, cardWidth - 0.8, data[4],cm)
        canvas.drawCentredString((cardX + (cardWidth / 2)) * cm, (cardY + eventIndent + (eventHeight / 2) - 0.2) * cm, data[4])
        if data[3] == 'Volunteer':
            canvas.setFillColor(HexColor("#50f442"))
            canvas.setStrokeColor(HexColor("#50f442"))
            canvas.setLineWidth(1)
            canvas.rect((cardX + eventIndent) * cm,(cardY + eventIndent + eventHeight + 0.04)*cm,(eventWidth) *cm,0.7*cm,fill=True, stroke=True)

            #canvas.setFillColor(HexColor("#FFFFFF"))
            canvas.setFillColor(HexColor(0x000000))
            safeFont(canvas,'Times-Bold', 16, cardWidth - 0.8, "Volunteer",cm)
            canvas.drawCentredString((cardX + (cardWidth / 2)) * cm, (cardY + eventIndent +  eventHeight + (eventHeight / 2)- 0.3) * cm, "Volunteer")
            
        canvas.setFillColor(HexColor(0x000000))
        canvas.setStrokeColor(HexColor(0x000000))
            

def safeFont(canvas, font, size, maxWidth, text, unit):
    textWidth = (stringWidth(text, font, size) / unit)
    print ("Max Width: %s textWidth: %s" % (maxWidth, textWidth))
    if textWidth < maxWidth:
        canvas.setFont(font,size)
    else:
        safeFont(canvas,font, size - 1, maxWidth, text, unit)
    

def drawPage(canvas, data, reverse=False):
    pageWidth, pageHeight = A4
    #canvas.drawString(100,pageHeight - 100,"Hello World")
    canvas.setFillColor(black)
    # rect (x,y, width,height, fill, stroke)
    print ('Page width %s data length %s' % (pageWidth / cm, len(data)))
    print ('Page height %s ' % (pageHeight / cm))
    leftX = 0.0
    rightX = 10.5
    Y = 1.45
    name = []
    guideWidth = 0.1
    for i in range(math.ceil(len(data) / 2)):
        # left 
        if len(data) >= i * 2 + 2 or not reverse:
            if reverse:
                name = data[i * 2 + 1]
            else:
                name = data[i* 2]
            drawCard(canvas,leftX, Y, name)
        # right
        if len(data) >= i * 2 + 2 or reverse:
            if reverse:
                name = data[i * 2]
            else:
                name = data[i * 2 + 1]
            drawCard(canvas,rightX, Y, name)

        # draw cutting line
        canvas.setLineWidth(0.3)
        canvas.setDash(1,2)
        canvas.line((0)*cm, Y*cm, (guideWidth)*cm, Y*cm)
        canvas.line((10.5 - guideWidth)*cm, Y*cm, (10.5 + guideWidth)*cm, Y*cm)
        canvas.line(((pageWidth / cm) - guideWidth)*cm, Y*cm, pageWidth, Y*cm)

        Y += 6.7 # Card height
        
    canvas.setLineWidth(0.3)
    canvas.setDash(1,2)
    canvas.line((0)*cm, Y*cm, (guideWidth)*cm, Y*cm)
    canvas.line((10.5 - guideWidth)*cm, Y*cm, (10.5 + guideWidth)*cm, Y*cm)
    canvas.line(((pageWidth / cm) - guideWidth)*cm, Y*cm, pageWidth, Y*cm)
        
    canvas.setLineWidth(1)
    canvas.setDash(1)
    # draw vertical lines
    canvas.line((0)*cm, 0, (0)*cm, 1*cm)
    canvas.line((0)*cm, pageHeight - (1 *cm), (0)*cm, pageHeight)

    canvas.line((10.5)*cm, 0, (10.5)*cm, 1*cm)
    canvas.line((10.5)*cm, pageHeight - (1 *cm), (10.5)*cm, pageHeight)

    canvas.line((21)*cm, 0, (21)*cm, 1*cm)
    canvas.line((21)*cm, pageHeight - (1 *cm), (21)*cm, pageHeight)

    #canvas.line((10.5 - 5.5 - 0.1)*cm, (1 + 6.7 + 1)*cm, (10.5 - 5.5 - 0.1)*cm, (1 + 6.7 + 2)*cm)
    #canvas.line((10.5 - 5.5 - 0.1)*cm, (17.7 + 2)*cm, (10.5 - 5.5 - 0.1)*cm, (17.7 + 3)*cm)
    #canvas.line((10.5 - 5.5 - 0.1)*cm, (26.7 + 1)*cm, (10.5 - 5.5 - 0.1)*cm, (26.7 + 2)*cm)

if __name__ == "__main__":

    csvfile_name = 'data_files/test-set.csv'
    if len(sys.argv) == 2:
        csvfile_name = sys.argv[1]

    namesPerPage = 8 
    c = canvas.Canvas("output/name_tags.pdf", pagesize=A4)
    with open(csvfile_name, 'rt') as csvfile:
        csvreader = csv.reader(csvfile)
        count = 0
        pageWorth = []
        for row in csvreader:
            pageWorth.append(row)
            count += 1
            if count == namesPerPage:
                drawPage(c, pageWorth)
                c.showPage()
                drawPage(c, pageWorth, True)
                c.showPage()
                pageWorth = []
                count = 0
        if count != 0:
            drawPage(c, pageWorth)
            c.showPage()
            drawPage(c, pageWorth, True)
            c.showPage()
            
    c.save()
    for faceName in pdfmetrics.standardFonts:
        print(faceName)
