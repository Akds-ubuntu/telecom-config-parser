import json
import os
from model_parser import parse_xmi
from artifact_generator import generate_meta_json, generate_config_xml
from config_manager import calculate_delta, apply_delta

def read_json(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(path: str, data: dict):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def write_text(path: str, data: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)

def main():
    os.makedirs('out', exist_ok=True)

    classes = parse_xmi('input/impulse_test_input.xml')
    
    meta_json = generate_meta_json(classes)
    write_json('out/meta.json', meta_json)
    
    config_xml = generate_config_xml(classes)
    write_text('out/config.xml', config_xml)
    
    config = read_json('input/config.json')
    patched_config = read_json('input/patched_config.json')
    
    delta = calculate_delta(config, patched_config)
    write_json('out/delta.json', delta)
    
    res_patched = apply_delta(config, delta)
    write_json('out/res_patched_config.json', res_patched)

if __name__ == "__main__":
    main()