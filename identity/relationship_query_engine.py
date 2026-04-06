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

        pattern = r"(.+?) kim"

        match = re.search(pattern, t)

        if not match:
            return None

        name = match.group(1).strip().title()

        relation = self.graph.find_person_relation(name)

        if not relation:
            closest = self.graph.find_closest_name(name)

            if closest:
                relation = self.graph.find_person_relation(closest)
                name = closest

        if not relation:
            return f"{name} hakkında graph hafızasında kayıt yok."

        subject = relation["from"]
        rel = relation["relation"]

        relation_map = {
            "sevgilim": "sevgilisi",
            "sevgili": "sevgilisi",
            "arkadaşım": "arkadaşı",
            "arkadaş": "arkadaşı",
            "eski sevgilim": "eski sevgilisi",
            "kardeşim": "kardeşi",
            "kardeş": "kardeşi",
            "dostum": "dostu",
            "dost": "dostu"
        }

        rel_text = relation_map.get(rel, rel)

        return f"{name}, {subject}'nun {rel_text}."