# from __future__ import absolute_import

import jpype
from asposepdf import Assist
from jpype import java

from strenum import StrEnum
from enum import Enum


class License(Assist.BaseJavaClass):
    javaClassName = "com.aspose.python.pdf.License"

    def __init__(self):
        javaLicense = jpype.JClass(self.javaClassName)
        self.javaClass = javaLicense()
        super().__init__(self.javaClass)

    def setLicense(self, licensePath):
        if licensePath is None:
            raise Exception("an argument is required")
        elif licensePath.__class__.__name__ == 'str':
            self.getJavaClass().setLicense(licensePath)

    def init(self):
        return


class ConvertErrorAction(Enum):
    """!
    This class represents action for conversion errors.
    """

    Delete = 0
    """!
    Delete convert errors
    """

    Nothing = 1
    """!
    Do nothing with convert errors
    """


class PdfFormat(StrEnum):
    """!
    This class represents an pdf format.
    """

    PDF_A_1A = 'PDF_A_1A'
    """!
    Pdf/A-1a format
    """

    PDF_A_1B = 'PDF_A_1B'
    """!
    Pdf/A-1b format
    """

    PDF_A_2A = 'PDF_A_2A'
    """!
    Pdf/A-2a format
    """

    PDF_A_3A = 'PDF_A_3A'
    """!
    Pdf/A-3a format
    """

    PDF_A_2B = 'PDF_A_2B'
    """!
    Pdf/A-2b
    """

    PDF_A_2U = 'PDF_A_2U'
    """!
    Pdf/A-2u format
    """

    PDF_A_3B = 'PDF_A_3B'
    """!
    Pdf/A-3b format
    """

    PDF_A_3U = 'PDF_A_3U'
    """!
    Pdf/A-3u format
    """

    v_1_0 = 'v_1_0'
    """!
    Adobe version 1
    """

    v_1_1 = 'v_1_1'
    """!
    Adobe version 1.1
    """

    v_1_2 = 'v_1_2'
    """!
    Adobe version 1.2
    """

    v_1_3 = 'v_1_3'
    """!
    Adobe version 1.3
    """

    v_1_4 = 'v_1_4'
    """!
    Adobe version 1.4
    """

    v_1_5 = 'v_1_5'
    """!
    Adobe version 1.5
    """

    v_1_6 = 'v_1_6'
    """!
    Adobe version 1.6
    """

    v_1_7 = 'v_1_7'
    """!
    Adobe version 1.7
    """

    v_2_0 = 'v_2_0'
    """!
    Adobe version 2.0
    """

    PDF_UA_1 = 'PDF_UA_1'
    """!
    PDF/UA-1 format
    """

    PDF_X_1A_2001 = 'PDF_X_1A_2001'
    """!
    PDF/X-1a-2001 format
    """

    PDF_X_1A = 'PDF_X_1A'
    """!
    PDF/X-1a format
    """

    PDF_X_3 = 'PDF_X_3'
    """!
    PDF/X-3 format
    """

    ZUGFeRD = 'ZUGFeRD'
    """!
    ZUGFeRD format
    """


class SaveFormat(StrEnum):
    """!
    Specifies save format
    """

    Pdf = 'Pdf'
    """!
    means saving without change of format, i.e. as PDF use it please instead of
    'SaveFormat.None', that is obsolete one
    """

    Doc = 'Doc'
    """!
    means saving in DOC format
    """

    Xps = 'Xps'
    """!
    means saving in XPS format
    """

    Html = 'Html'
    """!
    means saving in XML format
    """

    Xml = 'Xml'
    """!
    means saving in TEX format i.e. format suitable for Latex text editor
    """

    TeX = 'TeX'
    """!
    means saving in DOCX format
    """

    DocX = 'DocX'
    """!
    means saving in SVG format
    """

    Svg = 'Svg'
    """!
    means saving in SVG format
    """

    MobiXml = 'MobiXml'
    """!
    means saving in MsExcel format
    """

    Excel = 'Excel'
    """!
    means saving in MsExcel format
    """

    Epub = 'Epub'
    """!
    means saving in EPUB format(special format of e-books)
    """


class LoadFormat(StrEnum):
    """!
    Specifies load format
    """

    CGM = 'CGM'
    """!
    means loading of document in CGM format
    """

    HTML = 'HTML'
    """!
    means loading of document in HTML format
    """

    EPUB = 'EPUB'
    """!
    means loading of document in EPUB format(special format of e-books)
    """

    XML = 'XML'
    """!
    means loading of document in XML format(special XML that represent logical structure of PDF document)
    """

    XSLFO = 'XSLFO'
    """!
    means loading of document in XSLFO format
    """

    PCL = 'PCL'
    """!
    means loading of document in PCL format
    """

    XPS = 'XPS'
    """!
    means loading of document in XPS format
    """

    TEX = 'TEX'
    """!
    means loading of document in TEX format - format of Latex text editor
    """

    SVG = 'SVG'
    """!
    means loading of document in SVG format - format of Latex text editor
    """

    MHT = 'MHT'
    """!
    means loading of document in MHT format(that is packed HTML format)
    """

    PS = 'PS'
    """!
    means loading of document in PS format(format of PostScript document) 
    """

    MD = 'MD'
    """!
    means loading document is in MD format (markdown). 
    """

    TXT = 'TXT'
    """!
    means loading document is in TXT format. 
    """

    PDFXML = 'PDFXML'
    """!
    Internal PDF document structure in XML format. 
    """


class Document(Assist.BaseJavaClass):
    """!
    Class representing PDF document
    """

    javaClassName = "com.aspose.python.pdf.Document"

    def init(self):
        return

    def __init__(self, parameter1, options=None):

        if parameter1 is None:
            raise Exception("an argument is required")
        elif options is None:
            if parameter1.__class__.__name__ == 'bytes':
                javaClass = jpype.JClass(Document.javaClassName)
                # Convert the Python bytearray to a Java byte array
                j_byte_array = java.nio.ByteBuffer.wrap(parameter1)
                # Create a ByteArrayInputStream object from the Java byte array
                byte_input_stream = java.io.ByteArrayInputStream(j_byte_array.array())
                super().__init__(javaClass(byte_input_stream))
                self.init()
            elif parameter1.__class__.__name__ == 'str':
                javaClass = jpype.JClass(Document.javaClassName)
                super().__init__(javaClass(parameter1))
                self.init()
        if parameter1.__class__.__name__ == 'str':
            javaClass = jpype.JClass(Document.javaClassName)
            if isinstance(options, LoadFormat):
                super().__init__(javaClass(parameter1, LoadOptions.getLoadOptions(options)))
            elif isinstance(options, LoadOptions):
                super().__init__(javaClass(parameter1, options.getJClass()))
        elif parameter1.__class__.__name__ == 'bytes':
            javaClass = jpype.JClass(Document.javaClassName)

            # Convert the Python bytearray to a Java byte array
            j_byte_array = java.nio.ByteBuffer.wrap(parameter1)

            # Create a ByteArrayInputStream object from the Java byte array
            byte_input_stream = java.io.ByteArrayInputStream(j_byte_array.array())

            if isinstance(options, LoadFormat):
                super().__init__(javaClass(byte_input_stream, LoadOptions.getLoadOptions(options)))
            elif isinstance(options, LoadOptions):
                super().__init__(javaClass(byte_input_stream, options))

            self.init()

    def close(self):
        """!
        Closes all resources used by this document.
        """
        self.getJavaClass().close()

    def save(self, fileName, options=None):
        """!
        Saves the document with a new name along with a file format.
        """

        if fileName is None:
            self.getJavaClass().save()
        elif options is None:
            self.getJavaClass().save(fileName)
        elif fileName.__class__.__name__ == 'str':
            if isinstance(options, SaveFormat):
                self.getJavaClass().save(fileName, SaveOptions.getSaveOptions(options))
            if isinstance(options, SaveOptions):
                self.getJavaClass().save(fileName, options.getJClass)

    def convert(self, output_log, pdfFormat, convertErrorAction):
        """!
        Convert document and save errors into the specified file.
        """

        SaveFormatClass = "com.aspose.python.pdf.SaveFormat"
        javaClass = jpype.JClass(SaveFormatClass)
        if pdfFormat is None or convertErrorAction is None:
            raise Exception("an argument is required")
        else:
            self.getJavaClass().convert(output_log, jpype.JClass("com.aspose.python.pdf.PdfFormat").valueOf(pdfFormat),
                                        convertErrorAction.value)

    def saveInBytes(self, options=None):
        """!
        Saves the document into byte array with a selected file format.
        """

        SaveFormatClass = "com.aspose.python.pdf.SaveFormat"
        javaClass = jpype.JClass(SaveFormatClass)

        # Create a Java ByteArrayOutputStream object
        byte_output_stream = java.io.ByteArrayOutputStream()

        if options is None:
            self.getJavaClass().save(byte_output_stream);
        else:
            if isinstance(options, SaveFormat):
                self.getJavaClass().save(byte_output_stream, javaClass.valueOf(options))
            if isinstance(options, SaveOptions):
                self.getJavaClass().save(byte_output_stream, options.getJClass)

        # Convert the ByteArrayOutputStream to a Java byte array
        j_byte_array = byte_output_stream.toByteArray()

        # Convert the Java byte array to a Python bytearray
        py_byte_array = bytearray(j_byte_array)

        # Close the ByteArrayOutputStream object
        byte_output_stream.close()

        # Return the Python bytearray
        return py_byte_array

    @property
    def getJClass(self):
        return self.javaClass

    @property
    def getPages(self):
        return PageCollection(self.getJavaClass().getPages())


class PageCollection(Assist.BaseJavaClass):
    """!
    Class representing PDF document's page collection
    """

    javaClassName = "com.aspose.python.pdf.PageCollection"

    def init(self):
        return

    def __init__(self, pageCollection):
        self.pageCollection = pageCollection

    def getPage(self, pageNumber):
        return Page(self.pageCollection.get_Item(pageNumber))

    @property
    def size(self):
        return self.pageCollection.size()


class Page(Assist.BaseJavaClass):
    """!
    Class representing PDF document's page
    """

    javaClassName = "com.aspose.python.pdf.Page"

    def init(self):
        return

    def __init__(self, page):
        self.page = page


class LoadOptions:

    @staticmethod
    def getLoadOptions(loadFormat: LoadFormat):
        if loadFormat == LoadFormat.SVG:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.SvgLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.XPS:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.XpsLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.CGM:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.CgmLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.XSLFO:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.XslFoLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.PS:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.PsLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.XML:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.XmlLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.EPUB:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.EpubLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.HTML:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.HtmlLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.MD:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.MdLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.MHT:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.MhtLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.PCL:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.PclLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.TEX:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.TeXLoadOptions')
            return Options()

    @property
    def getLoadFormat(self):
        return self.__loadFormat

    @property
    def getJClass(self):
        return self.__jClass


class EpubLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.EPUB
    __jClass = jpype.JClass("com.aspose.python.pdf.EpubLoadOptions")


class HtmlLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.HTML
    __jClass = jpype.JClass("com.aspose.python.pdf.HtmlLoadOptions")


class MdLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.MD
    __jClass = jpype.JClass("com.aspose.python.pdf.MdLoadOptions")


class MhtLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.MHT
    __jClass = jpype.JClass("com.aspose.python.pdf.MhtLoadOptions")


class PclLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.PCL
    __jClass = jpype.JClass("com.aspose.python.pdf.PclLoadOptions")


class PdfXmlLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.PDFXML
    __jClass = jpype.JClass("com.aspose.python.pdf.PdfXmlLoadOptions")


class PsLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.PS
    __jClass = jpype.JClass("com.aspose.python.pdf.PsLoadOptions")


class SvgLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.SVG
    __jClass = jpype.JClass("com.aspose.python.pdf.SvgLoadOptions")


class TeXLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.TEX
    __jClass = jpype.JClass("com.aspose.python.pdf.TeXLoadOptions")


class TxtLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.TXT
    __jClass = jpype.JClass("com.aspose.python.pdf.TxtLoadOptions")


class XmlLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.XML
    __jClass = jpype.JClass("com.aspose.python.pdf.XmlLoadOptions")


class XpsLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.XPS
    __jClass = jpype.JClass("com.aspose.python.pdf.XpsLoadOptions")


class XslFoLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.XSLFO
    __jClass = jpype.JClass("com.aspose.python.pdf.XslFoLoadOptions")


class CgmLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.CGM
    __jClass = jpype.JClass("com.aspose.python.pdf.CgmLoadOptions")


class SaveOptions:

    @staticmethod
    def getSaveOptions(saveFormat: SaveFormat):

        if saveFormat == SaveFormat.Svg:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.SvgSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.DocX:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.DocSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.Pdf:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.PdfSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.Excel:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.ExcelSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.Html:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.HtmlSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.Epub:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.EpubSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.DocX:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.DocSaveOptions')()
            Options.setFormat(
                jpype.JClass("com.aspose.python.pdf.DocSaveOptions.DocFormat.DocX"))
            return Options
        elif saveFormat == SaveFormat.Doc:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.DocSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.MobiXml:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.MobiXmlSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.Xml:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.XmlSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.Xps:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.XpsSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.TeX:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.TeXSaveOptions')
            return Options()

    @property
    def getLoadFormat(self):
        return self.__loadFormat

    @property
    def getJClass(self):
        return self.__jClass


class DocSaveOptions(SaveOptions):
    class DocFormat(StrEnum):
        """!
        Allows to specify .doc or .docx file format.
        """

        Doc = 'Doc'
        """!
        [MS-DOC]: Word (.doc) Binary File Format
        """

        Docx = 'Docx'
        """!
        Office Open XML (.docx) File Format
        """

    class RecognitionMode(StrEnum):
        """!
        Allows to control how a PDF document is converted into a word processing document.
        """

        Textbox = 'Textbox'
        """!
        This mode is fast and good for maximally preserving original look of the PDF file, but
        editability of the resulting document could be limited.
        """

        Flow = 'Flow'
        """!
        Full recognition mode, the engine performs grouping and multi-level analysis to restore
        the original document author's intent and produce a maximally editable document. The
        downside is that the output document might look different from the original PDF file.
        """

        EnhancedFlow = 'EnhancedFlow'
        """!
        An early alfa version of a new Flow mode supporting recognition of tables.
        """

    __jClass = jpype.JClass("com.aspose.python.pdf.DocSaveOptions")()
    format = DocFormat.Doc
    mode = RecognitionMode.Flow
    relative_horizontal_proximity = 1.5
    recognize_bullets = False

    @property
    def getJClass(self):

        if self.format == self.DocFormat.Doc:
            self.__jClass.setFormat(0)
        else:
            self.__jClass.setFormat(1)

        if self.mode == self.RecognitionMode.Textbox:
            self.__jClass.setMode(0)
        elif self.mode == self.RecognitionMode.Flow:
            self.__jClass.setMode(1)
        else:
            self.__jClass.setMode(2)

        self.__jClass.setRelativeHorizontalProximity(self.relative_horizontal_proximity)
        self.__jClass.setRecognizeBullets(self.recognize_bullets)
        return self.__jClass


class ExcelSaveOptions(SaveOptions):
    class ExcelFormat(StrEnum):
        """!
        Allows to specify .xls/xml or .xlsx file format. Default value is XLSX;
        """

        XMLSpreadSheet2003 = 'XMLSpreadSheet2003'
        """!
        Excel 2003 XML Format
        """

        XLSX = 'XLSX'
        """!
        Office Open XML (.xlsx) File Format
        """

        CSV = 'CSV'
        """!
        A comma-separated values (CSV) File Format
        """

        XLSM = 'XLSM'
        """!
        A macro-enabled Office Open XML (.xlsm) File Format
        """

        ODS = 'ODS'
        """!
        OpenDocument Spreadsheet
        """

    __jClass = jpype.JClass("com.aspose.python.pdf.ExcelSaveOptions")()
    _format = ExcelFormat.XLSX
    _minimizeTheNumberOfWorksheets = False
    _insertBlankColumnAtFirst = False
    _uniformWorksheets = False

    @property
    def getJClass(self):
        if self._format == self.ExcelFormat.XMLSpreadSheet2003:
            self.__jClass.setFormat(0)
        elif self._format == self.ExcelFormat.XLSX:
            self.__jClass.setFormat(1)
        elif self._format == self.ExcelFormat.CSV:
            self.__jClass.setFormat(2)
        elif self._format == self.ExcelFormat.XLSM:
            self.__jClass.setFormat(3)
        elif self._format == self.ExcelFormat.ODS:
            self.__jClass.setFormat(4)

        self.__jClass.setInsertBlankColumnAtFirst(self._insertBlankColumnAtFirst)
        self.__jClass.setMinimizeTheNumberOfWorksheets(self._minimizeTheNumberOfWorksheets)
        self.__jClass.setUniformWorksheets(self._uniformWorksheets)
        return self.__jClass


class HtmlSaveOptions(SaveOptions):
    class FontSavingModes(StrEnum):
        """!
        Enumerates modes that can be used for saving of fonts referenced in saved PDF
        """

        AlwaysSaveAsWOFF = 'AlwaysSaveAsWOFF'
        """!
        All referenced fonts will be saved and referenced as WOFF-fonts
        """

        AlwaysSaveAsTTF = 'AlwaysSaveAsTTF'
        """!
        All referenced fonts will be saved and referenced as TTF-fonts
        """

        AlwaysSaveAsEOT = 'AlwaysSaveAsEOT'
        """!
        All referenced fonts will be saved and referenced as EOT-fonts
        """

        SaveInAllFormats = 'SaveInAllFormats'
        """!
        All referenced fonts will be saved (and referenced in CSS) as 3 independent files : EOT,
         * TTH,WOFF. It increases size of output data but makes output suitable for overwhelming
         * majority of web browsers
        """

        DontSave = 'DontSave'
        """!
        All referenced fonts will not be saved.
        """

    __jClass = jpype.JClass("com.aspose.python.pdf.HtmlSaveOptions")()
    _fontSavingMode = FontSavingModes.AlwaysSaveAsWOFF
    _splitIntoPages = False
    _splitCssIntoPages = False
    _useZOrder = False

    @property
    def getJClass(self):
        if self._fontSavingMode == self.FontSavingModes.AlwaysSaveAsWOFF:
            self.__jClass.setFontSavingMode(0)
        elif self._fontSavingMode == self.FontSavingModes.AlwaysSaveAsTTF:
            self.__jClass.setFontSavingMode(1)
        elif self._fontSavingMode == self.FontSavingModes.AlwaysSaveAsEOT:
            self.__jClass.setFontSavingMode(2)
        elif self._fontSavingMode == self.FontSavingModes.SaveInAllFormats:
            self.__jClass.setFontSavingMode(3)
        elif self._fontSavingMode == self.FontSavingModes.DontSave:
            self.__jClass.setFontSavingMode(4)

        self.__jClass.setSplitCssIntoPages(self._splitIntoPages)
        self.__jClass.setSplitCssIntoPages(self._splitCssIntoPages)
        self.__jClass.setUseZOrder(self._useZOrder)
        return self.__jClass


class PptxSaveOptions(SaveOptions):

    __jClass = jpype.JClass("com.aspose.python.pdf.PptxSaveOptions")()
    _ImageResolution = 192
    _SlidesAsImages = False
    _SeparateImages = False
    _OptimizeTextBoxes = False

    @property
    def getJClass(self):

        self.__jClass.setSlidesAsImages(self._SlidesAsImages)
        self.__jClass.setSeparateImages(self._SeparateImages)
        self.__jClass.setOptimizeTextBoxes(self._OptimizeTextBoxes)
        return self.__jClass


class PdfFileEditor(SaveOptions):

    __jClass = jpype.JClass("com.aspose.python.pdf.facades.PdfFileEditor")()

    def concatenate(self, firstInputFile, secInputFile, outputFile):
        self.__jClass.concatenate(firstInputFile, secInputFile, outputFile)
