from .Abstract import ADetection

class OCR(ADetection):
    score_ocr: float
    label_ocr: str

    def serialize(self):
        data = super().serialize()
        data["score_ocr"] = self.score_ocr
        data["label_ocr"] = self.label_ocr
        return data
        
    def deserialize(self, data):
        super().deserialize(data)

        for field in data:
            if field == "score_ocr":
                self.score_ocr = data[field]
            elif field == "label_ocr":
                self.label_ocr = data[field]
        return self