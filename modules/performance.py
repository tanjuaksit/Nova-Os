"""
Nova OS - Performance & Stress Test Module
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""

import asyncio
import time
import sqlite3
from datetime import datetime

try:
    import aiohttp
except ImportError:
    aiohttp = None


class PerformanceModule:
    """
    Nova OS Stres Testi ve Performans Ölçüm Modülü.
    Asenkron HTTP istekleri (I/O) veya paralel LLM çağrıları (GPU) ile sistem performansını test eder.
    """

    def __init__(self, db_path="stress_test_results.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Test sonuçlarının kaydedileceği SQLite tablosunu hazırlar."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stress_test_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                status INTEGER,
                response_time_ms REAL,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()

    def _save_log(self, url: str, status: int, response_time: float):
        """SQLite kayıt işlemini gerçekleştirir."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO stress_test_logs (url, status, response_time_ms, timestamp) VALUES (?, ?, ?, ?)",
            (url, status, response_time, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    async def _fetch_and_save(self, session, task_id: int, url: str):
        """Tek bir HTTP isteğini atar, süreyi ölçer ve non-blocking olarak veritabanına kaydeder."""
        start_time = time.perf_counter()
        try:
            async with session.get(url, timeout=10) as response:
                await response.text()
                elapsed = (time.perf_counter() - start_time) * 1000

                await asyncio.to_thread(
                    self._save_log, url, response.status, round(elapsed, 2)
                )
                return elapsed, response.status
        except Exception as e:
            return 0, 500

    async def run_stress_test(self, concurrent_tasks: int = 25, target_url: str = "https://httpbin.org/delay/1") -> str:
        """
        Asenkron HTTP/I/O stres testini çalıştırır ve biçimlendirilmiş bir rapor döndürür.
        """
        if aiohttp is None:
            return "Hata: 'aiohttp' kütüphanesi yüklü değil. Lütfen 'pip install aiohttp' çalıştırın."

        total_start = time.perf_counter()

        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_and_save(session, i + 1, target_url) for i in range(concurrent_tasks)]
            results = await asyncio.gather(*tasks)

        total_time = time.perf_counter() - total_start
        successful = [r for r in results if r[1] == 200]
        avg_latency = sum(r[0] for r in successful) / len(successful) if successful else 0
        rps = len(results) / total_time if total_time > 0 else 0

        report = (
            f"==================================================\n"
            f"          PERFORMANS VE STRES TESTİ RAPORU        \n"
            f"==================================================\n"
            f"Toplam İstek Sayısı     : {len(results)}\n"
            f"Başarılı İstek (200 OK) : {len(successful)}\n"
            f"Hatalı / Başarısız      : {len(results) - len(successful)}\n"
            f"Toplam Tamamlanma Süresi: {total_time:.2f} saniye\n"
            f"Saniye Başına İstek(RPS): {rps:.2f}\n"
            f"Ortalama Yanıt Süresi   : {avg_latency:.2f} ms\n"
            f"Veritabanı Kayıt Yeri   : {self.db_path}\n"
            f"=================================================="
        )
        return report

    async def run_gpu_stress_test(self, brain_instance, concurrent_tasks: int = 4) -> str:
        """
        Local LLM (Brain) katmanına aynı anda paralel ağır prompt'lar fırlatarak GPU / VRAM kullanımını test eder.
        """
        if not brain_instance:
            return "Hata: Brain nesnesi bulunamadı."

        heavy_prompt = "Bana kuantum fiziği ile genel görelilik arasındaki çelişkileri anlatan ve çözüm önerilerini tartışan 300 kelimelik teknik bir makale yaz."

        total_start = time.perf_counter()

        async def _call_brain():
            start = time.perf_counter()
            try:
                if hasattr(brain_instance, 'think_async'):
                    res = await brain_instance.think_async(heavy_prompt)
                elif asyncio.iscoroutinefunction(brain_instance.think):
                    res = await brain_instance.think(heavy_prompt)
                else:
                    res = await asyncio.to_thread(brain_instance.think, heavy_prompt)
                elapsed = (time.perf_counter() - start) * 1000
                return elapsed, True
            except Exception as e:
                return 0, False

        tasks = [_call_brain() for _ in range(concurrent_tasks)]
        results = await asyncio.gather(*tasks)

        total_time = time.perf_counter() - total_start
        successful = [r for r in results if r[1]]
        avg_latency = sum(r[0] for r in successful) / len(successful) if successful else 0

        report = (
            f"==================================================\n"
            f"          GPU / LLM STRES TESTİ RAPORU            \n"
            f"==================================================\n"
            f"Paralel LLM İstek Sayısı : {concurrent_tasks}\n"
            f"Başarılı Tamamlanan      : {len(successful)}\n"
            f"Hatalı / Başarısız      : {len(results) - len(successful)}\n"
            f"Toplam Geçen Süre        : {total_time:.2f} saniye\n"
            f"Ortalama İstek Yanıt Süresi: {avg_latency / 1000:.2f} saniye\n"
            f"=================================================="
        )
        return report