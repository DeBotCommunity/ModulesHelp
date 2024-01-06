# Module by @DeBotMod
import os
import importlib.util

from telethon import events
from userbot import client

info = {'category': 'tools', 'pattern': '.m|.mhelp', 'description': '.m - выводит все ваши модули|выводит информацию о '
                                                                    'модуле. Вид: .mhelp [название модуля]'}


@client.on(events.NewMessage(outgoing=True, pattern=r"^\.m$"))
async def m_odules_commands(event):
    try:
        folder_path = 'userbot/modules'
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.py')]
        if files:
            count = len(files)
            message = f"**🛡 Сейчас загружено {int(count) - 1} модулей:**\n\n"
            for file in files:
                if file != '__init__.py':
                    module_name = os.path.splitext(file)[0]
                    message += f"⚙️ ```{module_name}```\n"
            await event.edit(message)
        else:
            await event.edit("**🩸 У вас ещё нет модулей! Вы можете установить модули с канала @DeBotMod**")
    except Exception:
        pass


@client.on(events.NewMessage(pattern=r'.mhelp (.*)'))
async def mhelp_command(event):
    try:
        module_name = event.pattern_match.group(1)
        module_path = f'userbot/modules/{module_name}.py'

        if os.path.isfile(module_path):
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, 'info') and 'description' in module.info:
                description = module.info['description'].replace('|', '\n')
                await event.edit(f"**📚 Описание модуля** ```{module_name}```:\n\n __{description}__")
            else:
                await event.edit(f"🩸 **У модуля** ```{module_name}``` **нет описания.**")
        else:
            await event.edit(f"🎃 **Модуль** ```{module_name}``` **не найден.**")
    except Exception:
        pass
