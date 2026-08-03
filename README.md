# Nova OS – Personal AI System
## 🇹🇷 Türkçe
**Nova OS**, tamamen yerel (offline) çalışan, insan benzeri hafıza ve çağrışım mekanizmalarını yerel yapay zeka ile bulduran kişisel bir asistan mimarisidir.
Bu projenin temel amacı; standart LLM sınırlarını aşarak, verileri sadece kelime tabanlı (keyword/vector) değil, anlam ağları (Knowledge Graph) ve niyet odaklı (Intent-driven) bir yapıyla harmanlayan akıllı bir aidiyet sistemi kurmaktır.
### 🚀 Öne Çıkan Özellikler & Gelişmeler
 * **Yerel Altyapı (Ollama):** Harici hiçbir bulut bağımlılığı olmadan tamamen lokal modellerle tam gizlilik.
 * **Çarışımsal Hafıza (Associative Memory):** İnsan beyninin bağlam kurma mantığına benzer şekilde; kavramları, ilişkileri ve kişileri birbirine bağlayan yapı.
 * **Niyet Odaklı Mimarî (Intent-Driven):** Ham metinleri ezbere aramak yerine kullanıcının niyetini çözerek doğru veritabanına nokta atışı yazma/okuma.
 * **Modüler Yapı:** Dinamik kimlik yönetimi (Identity), olay hafızası (Event Memory) ve esnek modül/araç yönlendiricisi (Router).
### Mimari Akış
```text
Kullanıcı Mesajı
       ↓
Niyet & Bağlam Analizi (Intent/Context)
       ↓
Bellek & Bilgi Grafiği Entegrasyonu (Graph / Vector)
       ↓
Dinamik Kimlik & Hafıza Güncelleme
       ↓
Ollama Yerel Model / LLM Yanıt Üretimi

```
### Proje Yapısı
```text
nova_os/
├ core/         # Orkestratör ve niyet/yönlendirme mekanizmaları
├ identity/     # Kullanıcı kimliği ve dinamik profil yönetimi
├ memory/       # Vektör ve bilgi grafiği hafıza katmanları
├ modules/      # Harici araçlar ve modüler sistemler
├ config/       # Sistem ayarları
└ main.py       # Giriş noktası

```
### Kurulum
Gerekli Python kütüphanelerini yükleyin:
```bash
pip install -r requirements.txt

```
Ollama üzerinden gerekli modellerin ayarlı olduğundan emin olun (Örn: llama3, nomic-embed-text).
### Çalıştırma
```bash
python main.py

```
### Author: Tanju Akşit
### Project: Nova OS – Personal AI System
## 🇬🇧 English
**Nova OS** is a local, offline-first personal AI assistant architecture designed to simulate human-like associative memory and context retention.
The primary goal of this project is to push beyond standard vector searches by integrating Knowledge Graphs and intent-driven logic, creating a truly adaptive and context-aware local AI companion.
### 🚀 Core Features
 * **Local Execution (Ollama):** Fully offline operation ensuring complete data privacy.
 * **Associative Memory:** Mimicking human cognitive recall by connecting concepts, relationships, and context dynamically.
 * **Intent-Driven Architecture:** Moving away from rigid keyword matching toward understanding user intent for precise data storage and retrieval.
 * **Modular Ecosystem:** Built-in dynamic identity management, event tracking, and flexible tool routing.
### Architecture Flow
```text
User Input
    ↓
Intent & Context Analysis
    ↓
Memory & Knowledge Graph Integration
    ↓
Dynamic Identity & State Update
    ↓
Ollama Local Model / LLM Response Generation

```
### Project Structure
```text
nova_os/
├ core/         # Orchestrator and intent/routing logic
├ identity/     # User identity and dynamic profile management
├ memory/       # Vector and knowledge graph memory layers
├ modules/      # External tools and modular components
├ config/       # System configurations
└ main.py       # Entry point

```
### Installation
Install the required dependencies:
```bash
pip install -r requirements.txt

```
Ensure your local Ollama instance has the necessary models pulled (e.g., llama3, nomic-embed-text).
### Run
```bash
python main.py

```
### Author: Tanju Akşit
### Project: Nova OS – Personal AI System

