import json
from collections import defaultdict

def load_geojson(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)

def group_features_by_code_usage(features):
    groups = defaultdict(list)
    for feature in features:
        code_usage = feature["properties"]["CODE_USAGE"]
        if code_usage is None:
            code_usage = "unknown"
        groups[code_usage].append(feature)
    return groups


def save_group_to_geojson(group, file_name):
    geojson = {
        "type": "FeatureCollection",
        "features": group
    }
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    input_file = "output.geojson"  # Replace with the name of your input GeoJSON file

    geojson = load_geojson(input_file)
    grouped_features = group_features_by_code_usage(geojson['features'])

    for description_usage, group in grouped_features.items():
        file_name = f"{description_usage.replace('/', '_')}_objects.geojson"
        save_group_to_geojson(group, file_name)
        print(f"Saved {len(group)} features to {file_name}")
