import re
from typing import Dict, Optional
from pythainlp import word_tokenize
from pythainlp.util import thai_digit_to_arabic_digit
from .types import IntentSchema, Slot
from .multi_domain_ontology import MultiDomainOntology

class HybridSymbolicThaiParser:
    def __init__(self):
        self.intents: Dict[str, IntentSchema] = {}
        self.ontology = MultiDomainOntology()
        self._register_intents()

    def _register_intents(self):
        self.intents["BOOK_FLIGHT"] = IntentSchema(
            name="BOOK_FLIGHT",
            trigger_patterns=[r"จอง.*?(เที่ยวบิน|ตั๋ว).*?(จาก|ออกจาก)\s*([ก-๙A-Za-z\s]+?)\s*(?:ไป|ถึง)\s*([ก-๙A-Za-z\s]+?)"],
            slots=[
                Slot(name="origin", type="location", required=True),
                Slot(name="destination", type="location", required=True)
            ]
        )

        self.intents["BOOK_HOTEL"] = IntentSchema(
            name="BOOK_HOTEL",
            trigger_patterns=[r"จอง(โรงแรม|ที่พัก).*?(ใน|ที่)\s*([ก-๙A-Za-z\s]+?)"],
            slots=[Slot(name="location", type="location", required=True)]
        )

        self.intents["CHECK_WEATHER"] = IntentSchema(
            name="CHECK_WEATHER",
            trigger_patterns=[r"(อากาศ|สภาพอากาศ).*(หาดใหญ่|กรุงเทพ|วันนี้)"],
            slots=[Slot(name="location", type="location", required=True)]
        )

    def preprocess_thai(self, text: str) -> str:
        text = thai_digit_to_arabic_digit(text)
        tokens = word_tokenize(text, engine="attacut")
        return " ".join(tokens)

    def parse(self, text: str) -> Optional[Dict]:
        clean_text = self.preprocess_thai(text)
        best = None
        best_score = 0

        for name, schema in self.intents.items():
            for pattern in schema.trigger_patterns:
                if re.search(pattern, clean_text, re.IGNORECASE):
                    confidence = 0.92
                    best = {
                        "intent": name,
                        "confidence": confidence,
                        "slots": {"raw": clean_text},
                        "preprocessed_text": clean_text
                    }
                    break
        return best
