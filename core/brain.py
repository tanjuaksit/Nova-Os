"""
Nova OS
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""

import aiohttp
import json


class Brain:

    def __init__(self, model="nova:latest", api_url="http://localhost:11434/api/generate"):
        self.model = model
        self.url = api_url

    async def think(self, prompt: str, system_prompt: str = None) -> str:
        """
        Asenkron LLM çağrısı yapar.
        Metnin TAMAMINI üretip tek bir string olarak döndürür (Bloklama yapmaz).
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 4096,  # VRAM'i korumak için ideal bağlam boyutu
                "num_gpu": 99     # Katmanları RX 6600 GPU'ya kilitler
            }
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, json=payload, timeout=60) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("response", "Model cevap veremedi.")
                    return f"Ollama Hatası: HTTP {resp.status}"
        except Exception as e:
            return f"Model hatası: {e}"

    async def think_stream(self, prompt: str, system_prompt: str = None):
        """
        Token'ları anlık akış (stream) olarak fırlatan jeneratör.
        Gelecekte canlı seslendirme (TTS) ve UI üzerinde harf harf yazdırmak için kullanılır.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "num_ctx": 4096,
                "num_gpu": 99
            }
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, json=payload) as resp:
                    async for line in resp.content:
                        if line:
                            data = json.loads(line.decode('utf-8'))
                            chunk = data.get("response", "")
                            if chunk:
                                yield chunk
                            if data.get("done", False):
                                break
        except Exception as e:
            yield f"Model akış hatası: {e}"