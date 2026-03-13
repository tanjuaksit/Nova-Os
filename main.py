"""
Nova OS
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""

import asyncio
import sys

# 1. TÜM PROJE MODÜLLERİNİ IMPORT EDİYORUZ
from core.brain import Brain
from core.nova_orchestrator import NovaOrchestrator
from core.llm_agent_router import LLMAgentRouter

from memory.database import MemoryDB
from memory.vector_store import VectorStore
from memory.event_memory import EventMemory
from memory.event_extractor import EventExtractor
from memory.event_query_engine import EventQueryEngine
from memory.memory_controller import MemoryController

from identity.identity_engine import IdentityEngine
from identity.identity_query_engine import IdentityQueryEngine
from identity.relationship_query_engine import RelationshipQueryEngine
from identity.auto_learn import AutoLearner

from modules.system import SystemModule
from modules.performance import PerformanceModule


async def stream_print(prefix: str, text: str, delay: float = 0.008):
    """Metni terminale takılmadan, akıcı bir daktilo efektiyle yazdırır."""
    print(prefix, end="", flush=True)
    for char in text:
        print(char, end="", flush=True)
        await asyncio.sleep(delay)
    print("\n")


async def main():
    print("=" * 50)
    print("      NOVA OS Bilişsel Ajan Sistemi Başlatılıyor...      ")
    print("=" * 50)

    # 2. NESNELERİ OLUŞTURUYORUZ
    brain = Brain(model="nova:latest")
    agent_router = LLMAgentRouter(brain=brain)

    memory = MemoryDB()
    vector_store = VectorStore()
    identity = IdentityEngine()

    event_memory = EventMemory()
    event_extractor = EventExtractor()
    event_query = EventQueryEngine(event_memory=event_memory)

    identity_query = IdentityQueryEngine(identity_engine=identity)

    perf_module = PerformanceModule()

    try:
        relationship_engine = RelationshipQueryEngine(identity)
    except TypeError:
        try:
            relationship_engine = RelationshipQueryEngine(identity_engine=identity)
        except TypeError:
            relationship_engine = RelationshipQueryEngine()

    auto_learner = AutoLearner(identity_engine=identity)

    try:
        memory_controller = MemoryController(identity_engine=identity)
    except TypeError:
        memory_controller = MemoryController(identity)

    agent = SystemModule()

    # 3. ORCHESTRATOR'A NESNELERİ ENJEKTE EDİYORUZ
    orchestrator = NovaOrchestrator(
        brain=brain,
        memory=memory,
        vector_store=vector_store,
        identity=identity,
        identity_query=identity_query,
        relationship_engine=relationship_engine,
        auto_learner=auto_learner,
        memory_controller=memory_controller,
        event_memory=event_memory,
        event_extractor=event_extractor,
        event_query=event_query,
        agent_router=agent_router,
        agent=agent,
        perf_module=perf_module
    )

    print("\nNOVA OS Hazır. (Çıkış için 'q' veya 'exit' yazın)\n")

    while True:
        try:
            user_input = await asyncio.to_thread(input, "User > ")

            if user_input.strip().lower() in ["exit", "q", "çıkış"]:
                print("Nova OS kapatılıyor...")
                break

            if not user_input.strip():
                continue

            # Yanıtı alıyoruz
            response = await orchestrator.handle(user_input)

            # Rapor veya kısa yanıt durumuna göre canlı akış
            if response.startswith("="):
                print(f"\nNova >\n{response}\n")
            else:
                await stream_print("\nNova > ", response)

        except (KeyboardInterrupt, SystemExit):
            print("\nNova OS durduruldu.")
            break
        except Exception as e:
            print(f"\n[Sistem Hatası]: {e}\n")


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())