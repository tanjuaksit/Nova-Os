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

        intent = result.get("intent", "")
        if intent == "SORU":
            return None

        person = result.get("person")
        relation = result.get("relation")
        owner = result.get("owner", "kullanıcı")
        school = result.get("school")
        age = result.get("age")
        time = result.get("time")

        if age:
            if person:
                self.graph.set_attribute(person, "yaş", str(age))
                if relation:
                    subject = "Kullanıcı" if not owner or owner == "kullanıcı" else owner.title()
                    self.graph.add_relation(subject, relation, person)
                return f"{person} yaşı kaydedildi: {age}"
            else:
                # İlişki kelimesi üzerinden kişiyi bul
                relation_keywords = [
                    "baldız", "baldızım", "sevgili", "sevgilim",
                    "arkadaş", "arkadaşım", "bacanak", "kardeş",
                    "kardeşim", "dost", "dostum"
                ]
                found_person = None
                for keyword in relation_keywords:
                    if keyword in t:
                        for edge in self.graph.graph["edges"]:
                            if edge.get("relation", "").lower() == keyword:
                                found_person = edge["to"]
                                break
                    if found_person:
                        break

                if found_person:
                    self.graph.set_attribute(found_person, "yaş", str(age))
                    return f"{found_person} yaşı kaydedildi: {age}"
                else:
                    self.identity.set_value("age", str(age))
                    return f"Yaş kaydedildi: {age}"

        if person and relation:
            subject = "Kullanıcı" if not owner or owner == "kullanıcı" else owner.title()
            self.graph.add_relation(subject, relation, person)
            if school:
                self.graph.set_attribute(person, "okul", school)
            if time:
                self.graph.set_attribute(person, "tanışma_zamanı", time)
            return f"{person} kaydedildi: {relation}"

        return None