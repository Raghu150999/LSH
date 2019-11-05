class DocumentCollection:
    def __init__(self):
        # Mapping from document names to ids
        self.dntid = {}
        # Mapping from document ids to names
        self.idtdn = []
        # Number of documents in the collection
        self.cnt = 0

    def insert_document(self, document):
        self.cnt += 1
        self.dntid[document.name] = document.docid
        self.idtdn.append(document.name) 


class Document:
    def __init__(self, docid, name):
        self.docid = docid
        self.name = name