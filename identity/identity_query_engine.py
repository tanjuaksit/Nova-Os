"""
Nova OS
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""

import re
import difflib
from config.loader import config


class IdentityQueryEngine:

    def __init__(self, identity_engine):
        self.identity = identity_engine

    def find_person(self, name):
        people = list(self.identity.people.nodes.keys())

        if not people:
            return None

        match = difflib.get_close_matches(
            name,
            people,
            n=1,
            cutoff=0.7
        )

        if match:
            return match[0]

        return None

    def process(self, text: str):

        t = text.lower().strip()

        # yaş sorusu
        if "kaç yaş" in t:
            # İsim var mı kontrol et
            name_match = re.search(r"(.+?)\s+kaç yaş", t)
            if name_match:
                name = name_match.group(1).strip().title()
                # Graph'ta yaş ara
                from identity.knowledge_graph import KnowledgeGraph
                graph = KnowledgeGraph()
                for edge in graph.graph["edges"]:
                    if edge["from"].lower() == name.lower() and edge["relation"] == "yaş":
                        return f"{name} {edge['to']} yaşında."
                return f"{name} hakkında yaş bilgisi yok."

            # İsim yoksa kullanıcının yaşı
            age = self.identity.get_value("age")
            if age:
                return f"{config.get('name', 'Kullanıcı')} {age} yaşında."
            return "Yaş bilgisi hafızamda bulunmuyor."

        # kişi sorgusu
        match = re.search(r"(.+?) kim", t)

        if match:

            name = match.group(1).strip().capitalize()

            person_name = self.find_person(name)

            if not person_name:
                return f"{name} hakkında hafızamda kayıt bulunmuyor."

            person = self.identity.people.get_person(person_name)

            relation = person.get("relation", "")

            if relation:
                return f"{person_name}, {config.get('name', 'Kullanıcı')}nın {relation}."
            else:
                return f"{person_name} hakkında sınırlı bilgi var."

        return None