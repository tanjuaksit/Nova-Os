# Nova OS – Personal AI System

![Python](https://img.shields.io/badge/python-3.11-blue)
![GitHub stars](https://img.shields.io/github/stars/tanjuaksit/Nova_Os)
![GitHub forks](https://img.shields.io/github/forks/tanjuaksit/Nova_Os)
![Profile views](https://komarev.com/ghpvc/?username=tanjuaksit&color=lightgrey)


## 🇹🇷 Türkçe

Nova OS yerel (offline) çalışmak üzere geliştirilen basit bir yapay zeka asistan mimarisi denemesidir.  
Amaç; hafıza sistemleri, bilgi grafı ve araç modülleri gibi farklı AI bileşenlerinin birlikte nasıl çalışabileceğini denemektir.

Proje hâlâ geliştirme aşamasındadır ve öğrenme amaçlı ilerlemektedir.

### Kullanılan Yapılar

- Yerel LLM kullanımı (Ollama)
- Vektör hafıza
- Knowledge graph
- Event memory
- Kimlik (identity) sistemi
- Tool / modül sistemi

Nova OS kendi LLM modelini içermez.  
Yerel model çalıştırmak için **Ollama** kullanılır.

Örnek:

```

ollama run llama3
ollama run nomic-embed-text

```

### Mimari

```

Kullanıcı Mesajı
↓
Event Extraction
↓
Identity Learning
↓
Memory Controller
↓
Agent Router
↓
LLM Fallback

```

### Proje Yapısı

```

nova_os/

├ core
├ identity
├ memory
├ modules
├ config
├ runtime
└ main.py

```

### Kurulum

```

pip install -r requirements.txt

```

### Çalıştırma

```

python main.py

```
---
### Author: Tanju Aksit
### Project: Nova OS – Personal AI System

---

# 🇬🇧 English

Nova OS is a small experiment for building a **local AI assistant architecture**.

The goal of the project is to explore how different AI components such as memory systems, knowledge graphs and tool modules can work together.

The project is still in early development and mainly created for learning and experimentation.

### Components

- Local LLM integration (Ollama)
- Vector memory
- Knowledge graph
- Event memory
- Identity system
- Tool modules

Nova OS does not include its own language model.

Instead it uses **Ollama** to run local models.

Example:

```

ollama run llama3
ollama run nomic-embed-text

```

### Architecture

```

User Input
↓
Event Extraction
↓
Identity Learning
↓
Memory Controller
↓
Agent Router
↓
LLM Fallback

```

### Project Structure

```

nova_os/

├ core
├ identity
├ memory
├ modules
├ config
├ runtime
└ main.py

```

### Installation

```

pip install -r requirements.txt

```

### Run

```

python main.py

```
---
### Author: Tanju Aksit
### Project: Nova OS – Personal AI System

---
