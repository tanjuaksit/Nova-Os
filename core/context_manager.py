"""
Nova OS
Author: Tanju Aksit
Copyright (c) 2026 Tanju Aksit

This source code is licensed under the Nova OS Author Credit License.
"""şerifcan befrom config.loader import config


class ContextManager:

    def build_context(self, user_input, memory_context, identity_context):

        system_prompt = config.get("system_prompt", "")

        return f"""
{system_prompt}

Kimlik:
{identity_context}

İlgili Hafıza:
{memory_context}

Kullanıcı Mesajı:
{user_input}
"""