from PyQt5.QtWidgets import QApplication

def copyFromText(text):
    QApplication.clipboard().setText(text)

def pasteTextFromClipboard():
    clipboard = QApplication.clipboard()
    mime = clipboard.mimeData()
    cliptext = u""
    if mime.hasImage():
        pixmap = clipboard.pixmap()
    elif clipboard.mimeData().hasText():
        cliptext = str(clipboard.text())
        return cliptext
