import pathlib

import pop.hub

if __name__ == "__main__":
    root_directory = pathlib.Path.cwd()

    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="pop_create")
    hub.pop.sub.add(dyne_name="cloudspec")
    hub.pop.sub.add(dyne_name="config")
    hub.config.integrate.load(
        ["cloudspec", "pop_create"], "cloudspec", parse_cli=False, logs=False
    )
