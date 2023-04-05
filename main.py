import PyPDF2
import re


class PDFManager:
    def __init__(self, filename):
        self.filename = filename
        self.doc = None
        self.text = ""

    def open(self):
        if not self.doc:
            with open(self.filename, 'rb') as f:
                self.doc = PyPDF2.PdfReader(f)
                self.text = self.getTextFromPdf()

    def getTextFromPdf(self):
        pdfReader = self.doc
        count = len(pdfReader.pages)
        print(count)
        myText = ""
        for i in range(count):
            page = pdfReader.pages[i]
            myText += page.extract_text() + "\n"
        return myText

    def filterPages(self, condition):
        pages = [i for i in range(self.doc.getNumPages()) if condition(self.doc.getPage(i))]
        return pages

    def searchText(self, myText):
        results = []
        for i in range(self.doc.getNumPages()):
            page_text = self.doc.getPage(i).extractText()
            if myText in page_text:
                results.append(i)
        return results

    def getMetadata(self):
        info = self.doc.getDocumentInfo()
        metadata = {}
        for myKey, myValue in info.items():
            metadata[myKey] = str(myValue)
        return metadata

    def document(self):
        return self.doc

    def close(self):
        if self.doc:
            self.doc.stream.close()
            self.doc._stream = None


def removePuncAndSplitText(myText):
    myWords = re.findall(r"\w+", myText)
    return myWords


def sortDictAndCountUniqWords(myList):
    uniqWords = {}
    for word in myList:
        if word in uniqWords:
            uniqWords[word] += 1
        else:
            uniqWords[word] = 1
    sortedDict = dict(sorted(uniqWords.items(), key=lambda x: x[0]))
    return sortedDict


if __name__ == '__main__':
    file = input('Input name of the file ')
    pdfManager = PDFManager(file)
    pdfManager.open()
    text = pdfManager.getTextFromPdf()
    words = removePuncAndSplitText(text.lower())
    sortedUniqWords = sortDictAndCountUniqWords(words)
    for key, value in sortedUniqWords.items():
        print(key, ':', value)
