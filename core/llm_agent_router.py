"""
Nova OS
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""

import asyncio


class LLMAgentRouter:

    def __init__(self, brain):
        self.brain = brain

    async def route(self, user_input: str) -> str:
        """
        Kullanıcı girdisini analiz eder ve çalıştırması gereken aracı/modülü seçer.
        Asenkron olarak Brain.think'i çağırır.
        """
        # Kod yazma, analiz veya genel bilgi isteklerinde yönlendiriciyi bypass et
        code_keywords = ["kod", "script", "betik", "python", "fonksiyon", "class", "yaz"]
        text_lower = user_input.lower()

        # Eğer kullanıcı açıkça bir kod/yazılım talebinde bulunuyorsa araca gitme, doğrudan LLM'e bırak
        if any(k in text_lower for k in code_keywords) and not any(m in text_lower for m in ["müzik", "şarkı", "çal", "aç"]):
            return "none"

        prompt = f"""
Aşağıdaki kullanıcı mesajını incele. Eğer kullanıcı KESİN VE AÇIK bir şekilde donanım/sistem komutu (müzik çalma, ses ayarlama vb.) veriyorsa ilgili araç adını döndür.
Aksi takdirde (kod yazma, sohbet, soru sorma, bilgi alma isteklerinde) SADECE "none" yaz.

Kullanıcı Mesajı: "{user_input}"

Seçenekler: [music, system, none]
Cevap (sadece araç adını yaz):
""".strip()

        try:
            # Asenkron Brain çağrısı
            raw_result = await self.brain.think(prompt)
            result = raw_result.strip().lower()

            if "music" in result:
                return "music"
            elif "system" in result:
                return "system"
            else:
                return "none"

        except Exception as e:
            print(f"[Router Hatası]: {e}")
            return "none"