"""
Nova OS
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""

from identity.information_extractor import InformationExtractor
from identity.knowledge_graph import KnowledgeGraph


class AutoLearner:

    def __init__(self, identity_engine):
        self.identity = identity_engine
        self.extractor = InformationExtractor()
        self.graph = KnowledgeGraph()

    def process(self, text: str):

        t = text.lower()

        if "böyle deme" in t or "yanlış" in t:
            return "Uyarı kaydedildi."

        result = self.extractor.extract(text)

        if not result:
            return None

        # SORU ise öğrenme değil, sorguya bırak
        intent = result.get("intent", "")
        if intent == "SORU":
            return None

        person = result.get("person")
        relation = result.get("relation")
        school = result.get("school")
        age = result.get("age")
        time = result.get("time")

        if age and not person:
            self.identity.set_value("age", str(age))
            return f"Yaş kaydedildi: {age}"

        if person and relation:
            self.graph.add_relation("Kullanıcı", relation, person)
            if school:
                self.graph.set_attribute(person, "okul", school)
            if time:
                self.graph.set_attribute(person, "tanışma_zamanı", time)
            return f"{person} kaydedildi: {relation}"

        return None