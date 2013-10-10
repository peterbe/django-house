import codecs
import subprocess
from cStringIO import StringIO

from pdfminer.pdfinterp import process_pdf, PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from . import models
from . import utils


def process_document_text(document_or_id):
    """this function is ideal for running as a celery task"""
    if isinstance(document_or_id, models.Document):
        document = document_or_id
    else:
        document = models.Document.objects.get(pk=document_or_id)

    if document.document_type == 'pdf':
        text = _pdf2text(document)
    elif document.document_type == 'txt':
        text = codecs.open(document.file.path, 'r', 'utf-8').read()
    elif document.document_type == 'doc':
        text = _word2text(document)
    else:
        raise NotImplementedError(document.document_type)

    document.searchable_text = text
    document.text_extracted = True
    document.save()

def _pdf2text(document, caching=True, codec='utf-8', password='', maxpages=0):
    rsrcmgr = PDFResourceManager(caching=caching)
    laparams = LAParams()
    outfp = StringIO()
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    with open(document.file.path, 'rb') as fp:
        pagenos = set()
        process_pdf(
            rsrcmgr,
            device,
            fp,
            pagenos,
            maxpages=maxpages,
            password=password,
            caching=caching,
            check_extractable=True
        )
    return unicode(outfp.getvalue(), codec)

def _word2text(document):
    return utils.run('catdoc {path}', path=document.file.path)
