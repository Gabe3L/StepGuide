from typing import Optional

class Ocr:
    def read(self, text: str, read: bool) -> Optional[str]:
        return text if read else None