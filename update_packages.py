#!/usr/local/bin/python3.7
import subprocess
from typing import Dict, cast

import toml


def update_deps(name: str, version: str, t: Dict) -> Dict:
    def update(deps: Dict) -> None:
        for key in deps:
            v = deps[key]
            if (
                type(v) is str
                and name.lower() == key.lower()
                and v[0] in ("~", "^")
            ):
                deps[key] = f"{v[0]}{version}"

    update(t["tool"]["poetry"]["dependencies"])
    update(t["tool"]["poetry"]["group"]["development"]["dependencies"])

    return t


with open("./pyproject.toml", "r") as f:
    t = cast(Dict, toml.loads(f.read()))
    output = subprocess.run(["poetry", "show"], capture_output=True)
    lines = cast(str, output.stdout.decode()).split("\n")

    for line in filter(lambda l: bool(l), lines):
        name, version, *_ = line.split()
        t = update_deps(name, version, t)

    print(toml.dumps(t))
