from xml.sax.handler import ContentHandler
from xml.sax import make_parser


class myContentHandler(ContentHandler):

    def __init__(self):
        self.inEvento = False
        self.eventDict = {}
        self.listEvents = []
        self.inContent = False
        self.attrName = ""
        self.theContent = ""

    def startElement(self, name, attrs):
        if name == 'contenido':
            self.inEvento = True
        elif self.inEvento and name == 'atributo':
            self.attrName = attrs['nombre']
            self.inContent = True

    # Incluyo ifs para sacar menos informacion de la que hay
    def endElement(self, name):
        if name == 'contenido':
            self.listEvents.append(self.eventDict)
            self.eventDict = {}
            self.inEvento = False
        elif self.inEvento and name == 'atributo':
            lineEnc = self.theContent
            if self.attrName == 'TIPO':
                self.eventDict['TIPO'] = lineEnc.split("/")[-1]
            elif self.attrName == 'FECHA-EVENTO':
                self.eventDict['FECHA-EVENTO'] = lineEnc.split()[0]
            elif self.attrName == 'HORA-EVENTO':
                self.eventDict['HORA-EVENTO'] = lineEnc
            elif self.attrName == 'TITULO':
                self.eventDict['TITULO'] = lineEnc
            elif self.attrName == 'EVENTO-LARGA-DURACION':
                self.eventDict['EVENTO-LARGA-DURACION'] = lineEnc
            elif self.attrName == 'CONTENT-URL':
                self.eventDict['CONTENT-URL'] = lineEnc
            elif self.attrName == 'PRECIO':
                self.eventDict['PRECIO'] = lineEnc

            self.inContent = False
            self.theContent = ""
            self.attrName = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


def getListEvents(urlXmlData):
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    theParser.parse(urlXmlData)
    return theHandler.listEvents
