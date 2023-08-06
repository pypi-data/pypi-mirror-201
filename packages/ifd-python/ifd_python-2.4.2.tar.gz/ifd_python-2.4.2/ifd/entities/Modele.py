class Modele():
    label: str
    version: str
    def serialize(self):
        return {
            "label": self.label,
            "version": self.version
        }
    def deserialize(self, data):
        for field in data:
            if field == "label":
                self.label = data[field]
            elif field == "version":
                self.version = data[field]
        return self