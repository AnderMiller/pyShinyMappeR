import importlib.util
import sys
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType


def load_modules(
    directory: Path,
    required_attrs: tuple[str, ...],
    namespace_prefix: str,
) -> dict[str, object]:
    modules: dict[str, object] = {}

    for path in sorted(directory.glob("*.py")):
        if path.stem.startswith("_"):
            # skip files with leading _
            continue

        module_id = path.stem
        spec = importlib.util.spec_from_file_location(
            f"{namespace_prefix}.{module_id}", path
        )
        if isinstance(spec, (ModuleSpec, ModuleType)):
            mod = importlib.util.module_from_spec(spec)
            #  lord the things we do for basedpyright...
            if isinstance(mod, ModuleType) and spec.loader is not None:
                spec.loader.exec_module(mod)

                missing = [a for a in required_attrs if not hasattr(mod, a)]
                if missing:
                    print(
                        f"[warn] {path.name} is missing {missing} — skipping.",
                        file=sys.stderr,
                    )
                    continue

                modules[module_id] = mod

    return modules
