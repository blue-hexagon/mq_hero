from src.v2.application.loaders.yaml_loader import YamlLoader
from src.v2.utils.store import Store

if __name__ == '__main__':
    Store()
    root = YamlLoader()
    for com in root.all_companies():
        print(com)
        for f in com.farms:
            print(" " + str(f))
            for d in f.devices:
                device = f.devices[d]
                print(f"  {device}")
