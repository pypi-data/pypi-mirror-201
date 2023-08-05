from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            name="numlpa.kits.diffractometers.cpu.displacement",
            sources=["src/numlpa/kits/diffractometers/cpu/displacementmodule.c"],
        ),
        Extension(
            name="numlpa.kits.analyzers.cpu.interaction",
            sources=["src/numlpa/kits/analyzers/cpu/interactionmodule.c"],
        ),
    ]
)
