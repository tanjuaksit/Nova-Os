"""
Nova OS
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""

import re
from identity.knowledge_graph import KnowledgeGraph


class RelationshipQueryEngine:

    def __init__(self):
        self.graph = KnowledgeGraph()

    def process(self, text: str):

        t = text.lower()

        relation_map = {
            "sevgilim": "sevgilisi", "sevgili": "sevgilisi",
            "arkadaşım": "arkadaşı", "arkadaş": "arkadaşı",
            "eski sevgilim": "eski sevgilisi",
            "kardeşim": "kardeşi", "kardeş": "kardeşi",
            "dostum": "dostu", "dost": "dostu",
            "baldız": "baldızı", "baldızım": "baldızı",
            "bacanak": "bacanağı", "bacanağım": "bacanağı",
            "ağabey": "ağabeyi", "abla": "ablası",
            "anne": "annesi", "baba": "babası"
        }

        # İsme göre arama — "X kim"
        name_match = re.search(r"(.+?)\s+kim", t)
        if name_match:
            name = name_match.group(1).strip().title()
            result = self._find_by_name(name, relation_map)
            if result:
                return result

        # Yaş sorusu — "X kaç yaşında"
        age_match = re.search(r"(.+?)\s+kaç yaş", t)
        if age_match:
            name = age_match.group(1).strip().title()
            result = self._find_age(name, relation_map, t)
            if result:
                return result

        # İlişkiye göre arama
        for rel_key in relation_map:
            if rel_key in t:
                result = self._find_by_relation(rel_key, relation_map, t)
                if result:
                    return result

        return None

    def _find_by_name(self, name, relation_map):

        relation = self.graph.find_person_relation(name)

        if not relation:
            closest = self.graph.find_closest_name(name)
            if closest:
                relation = self.graph.find_person_relation(closest)
                name = closest

        if not relation:
            return None

        subject = relation["from"]
        rel = relation["relation"]
        rel_text = relation_map.get(rel, rel)

        return f"{name}, {subject}'nun {rel_text}."

    def _find_age(self, name, relation_map, text):

        # Direkt isimle ara
        for edge in self.graph.graph["edges"]:
            if edge["from"].lower() == name.lower() and edge["relation"] in ["yaş", "age"]:
                return f"{name} {edge['to']} yaşında."

        # İlişki kelimesi üzerinden ara
        for rel_key in relation_map:
            if rel_key in text:
                for edge in self.graph.graph["edges"]:
                    if edge.get("relation", "").lower() in [rel_key, rel_key + "ım", rel_key + "im"]:
                        person = edge["to"]
                        for e in self.graph.graph["edges"]:
                            if e["from"].lower() == person.lower() and e["relation"] in ["yaş", "age"]:
                                return f"{person.title()} {e['to']} yaşında."
                        return f"{person.title()} hakkında yaş bilgisi yok."

        return None

    def _find_by_relation(self, rel_key, relation_map, text):

        for edge in self.graph.graph["edges"]:
            edge_rel = edge.get("relation", "").lower()
            if edge_rel == rel_key:
                name = edge["to"]
                subject = edge["from"]
                rel_text = relation_map.get(rel_key, rel_key)
                return f"{subject}'nun {rel_text} {name.title()}."

        return None