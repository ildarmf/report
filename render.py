#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import json
from PIL import Image, ImageDraw, ImageFont

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextLineHorizontal
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def open_pdf(name):
    try:
        fp = open(name, 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        if document.is_extractable:
            return document

        fp.close()
    except IOError:
        pass

    return None


def get_layout(document, page_no):
    laparams = LAParams(
        line_overlap=0.5,
        char_margin=1.0,
        line_margin=0.5,
        word_margin=0.1,
        boxes_flow=0.5)
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = list(PDFPage.create_pages(document))

    page = pages[page_no - 1]

    interpreter.process_page(page)
    layout = device.get_result()

    return layout


def get_elements(layout, clazz):
    result = []

    for elem in iter(layout):
        if isinstance(elem, clazz):
            result.append(elem)
        elif isinstance(elem, collections.Iterable):
            result.extend(get_elements(elem, clazz))

    return result


def render(layout, elements):
    size = (layout.bbox[2], layout.bbox[3])
    height = size[1]

    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 10)

    for el in elements:
        rect = list(el.bbox)
        rect[1] = height - rect[1]
        rect[3] = height - rect[3]

        draw.rectangle(rect, outline='red')
        draw.text(
            [rect[0], rect[3]], el.get_text(), font=font, fill='black')

    img.save('render.png')


if __name__ == '__main__':
    document = open_pdf("data/AMZN_2016.pdf")
    layout = get_layout(document, 46)
    els = get_elements(layout, LTTextLineHorizontal)
    #render(layout, els)

    data  = [{'x0': el.x0, 'x1': el.x1, 'y0': el.y0, 'y1': el.y1, 'text': el.get_text()} for el in els]
    with open('file.json', 'w') as fl:
        json.dump(data, fl)