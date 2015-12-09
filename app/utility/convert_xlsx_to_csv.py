# -*- coding: utf-8 -*-

import xlrd
import re
import os
import os.path
import csv
from app import app


def xlrd_xls2array(infilename):
    """ Returns a list of sheets; each sheet is a dict containing
    * sheet_name: unicode string naming that sheet
    * sheet_data: 2-D table holding the converted cells of that sheet
    """
    book = xlrd.open_workbook(infilename)
    sheets = []
    formatter = lambda(t, v): format_excelval(book, t, v, False)

    for sheet_name in book.sheet_names():
        raw_sheet = book.sheet_by_name(sheet_name)
        data = []
        for row in range(raw_sheet.nrows):
            (types, values) = (raw_sheet.row_types(row),
                               raw_sheet.row_values(row))
            data.append(map(formatter, zip(types, values)))
        sheets.append({'sheet_name': sheet_name,
                       'sheet_data': data})
    return sheets


def tupledate_to_isodate(tupledate):
    """
    Turns a gregorian (year, month, day, hour, minute, nearest_second) into a
    standard YYYY-MM-DDTHH:MM:SS ISO date.  If the date part is all zeros, it's
    assumed to be a time; if the time part is all zeros it's assumed to be a
    date; if all of it is zeros it's taken to be a time, specifically 00:00:00
    (midnight).
    Note that datetimes of midnight will come back as date-only strings.  A date
    of month=0 and day=0 is meaningless, so that part of the coercion is safe.
    For more on the hairy nature of Excel date/times see
    http://www.lexicon.net/sjmachin/xlrd.html"""
    (y, m, d, hh, mm, ss) = tupledate
    nonzero = lambda n: n != 0
    date = "%04d-%02d-%02d"  % (y,m,d)    if filter(nonzero, (y,m,d))                else ''
    time = "T%02d:%02d:%02d" % (hh,mm,ss) if filter(nonzero, (hh,mm,ss)) or not date else ''
    return date+time


def format_excelval(book, type, value, wanttupledate):
    """ Clean up the incoming excel data """
    ##  Data Type Codes:
    ##  EMPTY   0
    ##  TEXT    1 a Unicode string
    ##  NUMBER  2 float
    ##  DATE    3 float
    ##  BOOLEAN 4 int; 1 means TRUE, 0 means FALSE
    ##  ERROR   5
    returnrow = []
    if type == 2:  # TEXT
        if value == int(value):
            value = int(value)
    elif type == 3:  # NUMBER
        datetuple = xlrd.xldate_as_tuple(value, book.datemode)
        value = datetuple if wanttupledate else tupledate_to_isodate(datetuple)
    elif type == 5:  # ERROR
        value = xlrd.error_text_from_code[value]
    return value
#
# Save to CSV
#


def camelize(s):
    """Makes a reasonable attempt at turning an arbitrary string
    into an identifier-safe CamelCasedString"""
    h = unicode(s)
    h = re.sub(r'(?:[_\s]+)([a-z])',
               lambda m: m.group(1).upper(), h)
    h = re.sub(r'[\-\.]+', '_', h)
    h = re.sub(r'\W',      '',  h)
    return h


def utf8ize(l):
    """Make string-like things into utf-8, leave other things alone
    """
    return [unicode(s).encode("utf-8")
            if hasattr(s, 'encode') else s for s in l]


def dump_csv(table, outdir, outfilename):
    stream = file(os.path.join(outdir, outfilename), 'wb')
    csvout = csv.writer(stream, delimiter=';',
                        doublequote=False, escapechar='\\')
    csvout.writerows(map(utf8ize, table))
    stream.close()


def save_csv_tables(tables, outdir):
    for (sheet_idx, sheet) in enumerate(tables):
        outfilename = "%s.csv" % (camelize(sheet['sheet_name']))
        dump_csv(sheet['sheet_data'], outdir, outfilename)


def run_convert():
        path = app.config['TMP_PATH']
        re_excelfilename = re.compile(r'(\.xlsx)$')
        infilenames = filter(re_excelfilename.search, os.listdir(path))
        for infilename in infilenames:
            tables = xlrd_xls2array(path+infilename)
            # (outdir, infilebase) = os.path.split(infilename)
            outdir = path

            save_csv_tables(tables, outdir)
