"""
Nova OS
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""

import asyncio
from config.loader import config


class NovaOrchestrator:

    def __init__(
        self,
        brain,
        memory=None,
        vector_store=None,
        identity=None,
        identity_query=None,
        relationship_engine=None,
        auto_learner=None,
        memory_controller=None,
        event_memory=None,
        event_extractor=None,
        event_query=None,
        agent_router=None,
        agent=None,
        perf_module=None
    ):
        self.brain = brain
        self.memory = memory
        self.vector_store = vector_store
        self.identity = identity
        self.identity_query = identity_query
        self.relationship_engine = relationship_engine
        self.auto_learner = auto_learner
        self.memory_controller = memory_controller
        self.event_memory = event_memory
        self.event_extractor = event_extractor
        self.event_query = event_query
        self.agent_router = agent_router
        self.agent = agent
        self.perf_module = perf_module

    def _should_use_vector_search(self, text: str) -> bool:
        t = text.strip().lower()
        if len(t) >= 10:  # Karakter sınırı 25'ten 10'a düşürüldü
            return True
        if "?" in t:
            return True
        keywords = [
            "hatırla", "geçen", "önce", "daha önce", "kim",
            "neydi", "nerede", "ne zaman", "konuşmuştuk", "peki", "hakkında"
        ]
        return any(k in t for k in keywords)

    async def _async_extract_and_save_event(self, user_input: str):
        """Kullanıcı mesajını arka planda asenkron olarak analiz eder."""
        if not self.event_extractor or not self.event_memory:
            return

        try:
            if asyncio.iscoroutinefunction(self.event_extractor.extract):
                event = await self.event_extractor.extract(user_input)
            else:
                event = self.event_extractor.extract(user_input)

            if event and isinstance(event, dict):
                self.event_memory.add_event(
                    event.get("subject", ""),
                    event.get("action", ""),
                    event.get("target", "")
                )
                print(f"  └─ [EVENT EXTRACTOR]: Yeni olay kaydedildi -> {event}")
        except Exception as e:
            print(f"  └─ [Arka Plan Hafıza Hatası]: {e}")

    async def handle(self, user_input: str) -> str:
        clean_input = user_input.strip().lower()

        # 0. GPU / LLM STRES TESTİ YÖNLENDİRMESİ
        if any(k in clean_input for k in ["gpu", "llm test", "gpu testi", "ekran kartı testi"]):
            if self.perf_module:
                return await self.perf_module.run_gpu_stress_test(self.brain, concurrent_tasks=4)
            return "Performans modülü (PerformanceModule) orkestratöre yüklenmemiş."

        # 0.1 NETWORK / I/O STRES TESTİ YÖNLENDİRMESİ
        if any(k in clean_input for k in ["stres", "stress", "performans"]):
            if self.perf_module:
                return await self.perf_module.run_stress_test(concurrent_tasks=25)
            return "Performans modülü (PerformanceModule) orkestratöre yüklenmemiş."

        # 0.2 EVENT EXTRACTION (Arka Plan Görevi)
        if self.event_extractor and self.event_memory:
            asyncio.create_task(self._async_extract_and_save_event(user_input))

            # 1. AGENT ROUTER (Donanım/Modül Yönlendiricisi)
            tool = "none"
            if self.agent_router:
                try:
                    if hasattr(self.agent_router, 'route_async'):
                        tool = await self.agent_router.route_async(user_input)
                    elif asyncio.iscoroutinefunction(self.agent_router.route):
                        tool = await self.agent_router.route(user_input)
                    else:
                        tool = self.agent_router.route(user_input)

                    # Eğer router'dan dönen veri sözlük (dict) formatındaysa modülü ayıkla
                    if isinstance(tool, dict):
                        if tool.get("intent") == "module":
                            tool = tool.get("module", "none")
                        else:
                            tool = "none"

                    if tool and tool != "none":
                        print(f"  [ROUTER]: Özel modül tetiklendi -> Modül: '{tool}'")
                except Exception as e:
                    print(f"  [Agent Router Hatası]: {e}")

            if tool and tool != "none" and self.agent:
                try:
                    result = self.agent.execute(tool)
                    if result:
                        if self.memory and hasattr(self.memory, 'save_message'):
                            self.memory.save_message("user", user_input)
                            self.memory.save_message("assistant", str(result))
                        return str(result)
                except Exception as e:
                    print(f"  [Agent Execution Hatası]: {e}")

        # 2. VEKTÖR VE ANILARI HAZIRLAMA (LOGLANDI)
        memory_lines = []
        if self.vector_store and self._should_use_vector_search(user_input):
            print("  [MEMORY SEARCH]: Vektör veritabanında geçmiş anılar sorgulanıyor...")
            try:
                related = self.vector_store.search(user_input, top_k=3)
                if related:
                    print(f"  [MEMORY FOUND]: {len(related)} adet ilgili geçmiş anı bulundu!")
                    for text, sim in related:
                        memory_lines.append(f"- {text}")
                        print(f"   ├─ Anı: {text}")
                else:
                    print("  [MEMORY SEARCH]: İlgili anı bulunamadı.")
            except Exception as e:
                print(f"  [Vektör Arama Hatası]: {e}")

        memory_context = "\n".join(memory_lines)

        # 3. SON KONUŞMALAR VE KİMLİK
        chat_context = ""
        if self.memory and hasattr(self.memory, 'get_last_messages'):
            try:
                context = self.memory.get_last_messages(6)
                if context:
                    chat_context = "\n".join([f"{r}: {c}" for r, c in reversed(context)])
            except Exception as e:
                print(f"  [Hafıza Okuma Hatası]: {e}")

        identity_context = ""
        if self.identity and hasattr(self.identity, 'get_summary'):
            try:
                identity_context = self.identity.get_summary()
            except Exception as e:
                print(f"  [Kimlik Okuma Hatası]: {e}")

        # 4. PROMPT OLUŞTURMA
        final_prompt = f"""SYS_START
[SİSTEM TALİMATI]
- Sen Nova'sın: Tanju Akşit tarafından geliştirilen yerel bir yapay zeka asistanısın.
- İnsan değilsin; üniversite okumak, büyümek gibi insan hedeflerin YOKTUR.
- Her zaman Türkçe konuş.
- Yalnızca size verilen hafıza ve bağlamdan yanıt üret.
- Hafızanda veya bağlamda olmayan bilgiler için kesinlikle uydurma yapma. "Bu bilgi hafızamda bulunmuyor" de.

[KİMLİK & SİSTEM BİLGİSİ]
{identity_context}

[İLGİLİ GEÇMİŞ ANILAR]
{memory_context if memory_context else "İlgili geçmiş anı bulunamadı."}

[SON SOHBET GEÇMİŞİ]
{chat_context}
SYS_END

Kullanıcı: {user_input}
Nova:""".strip()

        # 5. ASENKRON LLM ÇAĞRISI
        print(f"  [BRAIN]: LLM ({self.brain.model}) yanıt oluşturuyor...")
        if hasattr(self.brain, 'think_async'):
            response = await self.brain.think_async(final_prompt)
        elif asyncio.iscoroutinefunction(self.brain.think):
            response = await self.brain.think(final_prompt)
        else:
            response = self.brain.think(final_prompt)

        # 6. SOHBET HAFIZASI KAYDI (Short-Term Memory)
        if self.memory and hasattr(self.memory, 'save_message'):
            try:
                self.memory.save_message("user", user_input)
                self.memory.save_message("assistant", response)
            except Exception as e:
                print(f"  [Hafıza Kayıt Hatası]: {e}")

        # 7. VEKTÖR VERİTABANI KALICI KAYDI (Long-Term Vector Store)
        if self.vector_store:
            try:
                store_keywords = [
                    "aklında tut", "kaydet", "planım", "benim", "hatırla",
                    "yaşıyorum", "çalışıyorum", "taşınmak", "seviyorum", "adım"
                ]
                if any(k in clean_input for k in store_keywords):
                    if hasattr(self.vector_store, 'add_text'):
                        self.vector_store.add_text(user_input)
                        print(f"  [MEMORY STORE]: Bilgi vektör veritabanına kaydedildi -> '{user_input}'")
            except Exception as e:
                print(f"  [Vektör Kayıt Hatası]: {e}")

        return response