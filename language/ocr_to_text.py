class OCR:
    def read(self, text: str, read: bool) -> str:
        return text if read else ""