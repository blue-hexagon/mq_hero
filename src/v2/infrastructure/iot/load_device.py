import importlib


def load_sensor_model(model_name: str, config: dict):
    module_name = f"src.v2.infrastructure.models.{model_name.replace('.py', '')}"
    module = importlib.import_module(module_name)

    # Convention: class name == file name in CamelCase
    class_name = ''.join(part.capitalize() for part in model_name.replace('.py', '').split('_'))
    model_class = getattr(module, class_name)

    return model_class(config)
