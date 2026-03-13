"""
Nova OS
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""

import os
import webbrowser


class SystemModule:

    def open_chrome(self):

        webbrowser.open("https://google.com")
        return "Chrome açıldı."

    def shutdown(self):

        os.system("shutdown /s /t 5")
        return "Bilgisayar 5 saniye içinde kapanacak."

    def execute(self, tool_name: str, **kwargs):
        """Router tarafından çağrılan modül yürütücüsü"""
        if tool_name == "music":
            return "Müzik modülü henüz aktif değil veya entegrasyon aşamasında."
        # Diğer araçlar...
        return f"SystemModule: {tool_name} komutu çalıştırıldı."