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

def safeFont(canvas, font, size, maxWidth, text, unit):
    textWidth = (stringWidth(text, font, size) / unit)
    #print ("Max Width: %s textWidth: %s" % (maxWidth, textWidth))
    if textWidth < maxWidth:
        canvas.setFont(font,size)
    else:
        safeFont(canvas,font, size - 1, maxWidth, text, unit)

def drawRow(canvas, x, y, height, data):
    cardWidth = 10
    indent = 0.2
    canvas.rect((x) * cm,(y)*cm,(cardWidth) *cm,height*cm,fill=False, stroke=True)
    text = "Name: %s" % data[0]
    safeFont(canvas,'Times-Bold', 16, cardWidth - indent, text,cm)
    canvas.drawString((indent + x) * cm, (2.5 + y)*cm, text)

    text = "Wifi User: %s Pass: %s" % (data[1], data[2])
    safeFont(canvas,'Times-Bold', 16, cardWidth - indent, text,cm)
    canvas.drawString((indent + x) * cm, (y+1.5)*cm, text)

    text = "Afternoon Session: %s" % data[3]
    safeFont(canvas,'Times-Bold', 14, cardWidth - indent, text,cm)
    canvas.drawString((indent + x) * cm, (y + 0.5)*cm, text)

def drawPage(canvas, data, reverse=False):
    pageWidth, pageHeight = A4
    print ("Width %s, height %s" % (pageWidth/cm,pageHeight/cm))
    height = 3
    x = 0.5
    y = 0
    for i in range(math.ceil(len(data) / 2)):
        drawRow(canvas, x, y, height, data[i*2])
        drawRow(canvas, x+10, y, height, data[i*2+1])
        y += height

if __name__ == "__main__":

    csvfile_name = 'test-wifi.csv'
    if len(sys.argv) == 2:
        csvfile_name = sys.argv[1]

    namesPerPage = 2 
    c = canvas.Canvas("wifi_users.pdf", pagesize=A4)
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
            #    drawPage(c, pageWorth, True)
             #   c.showPage()
                pageWorth = []
                count = 0
        if count != 0:
            drawPage(c, pageWorth)
            c.showPage()
            #drawPage(c, pageWorth, True)
            #c.showPage()
            
    c.save()

