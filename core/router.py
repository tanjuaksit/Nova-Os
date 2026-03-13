"""
Nova OS
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""

import json

class Router:
    def route(self, response_text: str):
        # 1. Eğer model doğrudan JSON döndürdüyse onu al
        try:
            data = json.loads(response_text)
            if isinstance(data, dict):
                return data
        except:
            pass

        # 2. Düz metin geldiyse anahtar kelimelere göre basit niyet (intent) tespiti yap
        clean_text = response_text.strip().lower()

        # Müzik komutu açıkça istenmiş mi?
        if any(kw in clean_text for kw in ["müzik çal", "şarkı aç", "müzik dinle", "şarkı başlat"]):
            return {"intent": "module", "module": "music"}

        # Varsayılan olarak sohbet (chat) niyetine dön
        return {"intent": "chat", "text": response_text}