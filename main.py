# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import asyncio
import importlib
import os
import sys
from shared_client import start_client

async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [
        f[:-3]
        for f in os.listdir(plugin_dir)
        if f.endswith(".py") and f != "__init__.py"
    ]

    for plugin in plugins:
        try:
            module = importlib.import_module(f"plugins.{plugin}")
            run_func = f"run_{plugin}_plugin"
            if hasattr(module, run_func):
                print(f"Running {plugin} plugin...")
                await getattr(module, run_func)()
        except Exception as e:
            print(f"Errore nel plugin {plugin}: {e}", file=sys.stderr)

async def main():
    await load_and_run_plugins()
    while True:
        await asyncio.sleep(1)  # mantiene il processo vivo su Koyeb

if __name__ == "__main__":
    print("Starting bot client and loading plugins...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    except Exception as e:
        print(f"Errore critico: {e}", file=sys.stderr)
        sys.exit(1)
