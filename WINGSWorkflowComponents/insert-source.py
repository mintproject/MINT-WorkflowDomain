import csv
from yaml import load

def read_model_csv(csv_path):
    with open(csv_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        components = []
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            line_count += 1
            components.append(row)
    return components

def yaml_file(component_dir, model_catalog_uri):
    yaml_data = {}
    yaml_file = "wings-component.yml"
    try:
        spec = load((component_dir / "wings-component.yml").open(), Loader=Loader)
    except FileNotFoundError:
        yaml_file = "wings-component.yaml"
        spec = load((component_dir / yaml_file).open(), Loader=Loader)
    spec["wings"]["source"] = model_catalog_uri
    stream = open(os.path.join(compoent_dir, yaml_file), 'w+')
    yaml.dump(spec, stream, sort_keys=False)

csv_path="model.csv"
components = read_model_csv(csv_path)
for component in components:
    yaml_file(component["folder"], component["model"])
