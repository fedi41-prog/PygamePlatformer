import cx_Freeze

executables = [cx_Freeze.Executable("GameV1/__init__.py")]

cx_Freeze.setup(
    name="Pygame platformer",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":[""]}},
    executables = executables

    )