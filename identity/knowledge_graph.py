"""
Nova OS
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""

import json
import os
import difflib
from config.paths import KNOWLEDGE_GRAPH_PATH


class KnowledgeGraph:

    def __init__(self):
        self.file_path = KNOWLEDGE_GRAPH_PATH
        self.graph = {
            "nodes": {},
            "edges": []
        }
        self.load()

    def load(self):
        if not os.path.exists(self.file_path):
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return
                self.graph = json.loads(content)
        except:
            self.graph = {
                "nodes": {},
                "edges": []
            }

    def save(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.graph, f, indent=2, ensure_ascii=False)

    def add_node(self, name):
        if name not in self.graph["nodes"]:
            self.graph["nodes"][name] = {"name": name}

    def add_relation(self, subject, relation, obj):
        self.add_node(subject)
        self.add_node(obj)
        edge = {
            "from": subject,
            "relation": relation,
            "to": obj
        }
        if edge not in self.graph["edges"]:
            self.graph["edges"].append(edge)
            self.save()

    def get_relations(self, name):
        relations = []
        for edge in self.graph["edges"]:
            if edge["from"] == name:
                relations.append(edge)
        return relations

    def find_relation(self, subject, obj):
        for edge in self.graph["edges"]:
            if edge["from"] == subject and edge["to"] == obj:
                return edge["relation"]
        return None

    def find_person_relation(self, name):
        n = name.strip().lower()
        for edge in self.graph["edges"]:
            if edge.get("to", "").strip().lower() == n:
                return edge
        return None

    def find_closest_name(self, name, cutoff=0.70):
        names = list(self.graph["nodes"].keys())
        if not names:
            return None
        matches = difflib.get_close_matches(name, names, n=1, cutoff=cutoff)
        if matches:
            return matches[0]
        return None

    def set_attribute(self, subject, key, value):
        self.add_relation(subject, key, str(value))