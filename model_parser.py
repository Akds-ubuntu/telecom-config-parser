import xml.etree.ElementTree as ET
from typing import Dict, Any, Tuple

def _parse_multiplicity(mult: str) -> Tuple[str, str]:
    if ".." in mult:
        min_val, max_val = mult.split("..")
        return min_val, max_val
    return mult, mult

def parse_xmi(file_path: str) -> Dict[str, Any]:
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    classes = {
        elem.attrib['name']: {
            'name': elem.attrib['name'],
            'isRoot': elem.attrib.get('isRoot', 'false') == 'true',
            'documentation': elem.attrib.get('documentation', ''),
            'attributes': [
                {'name': attr.attrib['name'], 'type': attr.attrib['type']}
                for attr in elem.findall('Attribute')
            ],
            'children': [],
            'min': '1', 
            'max': '1'
        }
        for elem in root.findall('Class')
    }
    
    for agg in root.findall('Aggregation'):
        source = agg.attrib['source']
        target = agg.attrib['target']
        source_mult = agg.attrib.get('sourceMultiplicity', '1')
        min_val, max_val = _parse_multiplicity(source_mult)
        
        if target in classes and source in classes:
            classes[target]['children'].append(source)
            classes[source]['min'] = min_val
            classes[source]['max'] = max_val
            
    return classes