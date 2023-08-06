from setuptools import setup, Extension


def main():
    setup(
        name="pure-checker",
        description="A static analysis file format checker.",
        ext_modules=[Extension("pure_checker", ["pure_checker.c"], libraries=["z"])],
        include_package_data=True,
        packages=[],
    )


if __name__ == "__main__":
    main()
