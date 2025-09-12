def init_module() -> None:
    print(f'Default module initialized!')


if locals().get('RUN_MODULE'):
    init_module()
