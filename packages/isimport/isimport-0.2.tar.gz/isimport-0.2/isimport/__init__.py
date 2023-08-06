import importlib, subprocess, os, sys

def myModule(a):
    modules = a

    missing_modules = []
    present_modules = []
    missing_module_count = 0

    try:
        if sys.argv[1] == "install":
            skip = True
    except Exception:
        skip = 0

    def module_installer(module_name):
        not_install_modules = []
        not_install_count = 0
        for count, module in enumerate(module_name):
            print(f"\r({count+1}/{missing_module_count}) [Installing external modules]: {module}...", end="")
            subprocess.getoutput(f"pip install {module}")
            try:
                importlib.import_module(module)
                globals()[module] = __import__(module)
                present_modules.append(module)
            except ImportError:
                not_install_count += 1
                not_install_modules.append(module)
            print("\r                                                       ",end="")
            print("\r",end="")

        if "rich" in present_modules:
            from rich import box
            from rich.console import Console
            from rich.panel import Panel
            from rich.align import Align
            console = Console()
            def show_required_modules():
                required_modules = ", ".join(not_install_modules)
                panel = Panel(Align(required_modules, align="center", style="yellow"), title="These modules are not installed properly", border_style="red")
                console.print(panel, justify="center")
        else:
            def show_required_modules():
                print(f"These modules are not installed properly: {required_modules}")
        if not_install_count < 1:
            pass
        else:
            show_required_modules()
            sys.exit(1)


    def module_manager(info, status):
        if skip == True:
            module_installer(missing_modules)
        else:
            print(f"{info} | {status} not installed.\nuse: install argument to install.")
            sys.exit(1)

    for module in modules:
        try:
            importlib.import_module(module)
            globals()[module] = __import__(module)
            present_modules.append(module)
        except ImportError:
            missing_module_count += 1
            missing_modules.append(module)
    else:
        required_modules = ", ".join(missing_modules)

        if missing_module_count == 1:
            module_manager(required_modules, "module")
        elif missing_module_count > 1:
            module_manager(required_modules, "modules")
        elif missing_module_count < 1 and skip == True:
            from rich.console import Console as console
            console().rule("[white on green black][ Required modules are already installed ][/]")
            sys.exit(0)
