"""
Nova OS
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""

import json
import requests


class InformationExtractor:

    def __init__(self, model="nova"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def _ask(self, prompt: str) -> str:
        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            return response.json().get("response", "")
        except Exception:
            return ""

    def extract(self, text: str):

        prompt = f"""Sen bir veri çıkarma aracısın. Sadece JSON üretirsin. Asla açıklama yapmazsın. Asla Türkçe cümle yazmazsın.

Aşağıdaki cümleden bilgileri çıkar ve SADECE bu JSON formatında döndür:

{{
  "person": null,
  "relation": null,
  "owner": "kullanıcı",
  "school": null,
  "age": null,
  "time": null,
  "intent": "ÖĞRETME"
}}

Kurallar:
- owner: ilişkinin sahibi kim? Kullanıcı mı yoksa başka biri mi? Örnek: "Sudenin arkadaşı Gülpınar" → owner: "Sude". "Arif benim arkadaşım" → owner: "kullanıcı"
- intent değerleri sadece şunlar olabilir: ÖĞRETME, SORU, SOHBET
- age: sadece person'a ait yaş. Kullanıcının yaşı değil.

Cümle: "{text}"

Sadece JSON döndür. Başka hiçbir şey yazma:"""

        raw = self._ask(prompt).strip()

        try:
            raw = raw.replace("```json", "").replace("```", "").strip()

            start = raw.find("{")
            end = raw.rfind("}") + 1

            if start == -1 or end == 0:
                return None

            json_str = raw[start:end]
            result = json.loads(json_str)

            if not any(result.values()):
                return None

            return result

        except Exception:
            return None