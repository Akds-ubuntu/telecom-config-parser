import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, Any, List

def generate_meta_json(classes: Dict[str, Any]) -> List[Dict[str, Any]]:
    
    def create_meta_node(cls_data: Dict[str, Any]) -> Dict[str, Any]:
        parameters = [
            {"name": attr["name"], "type": attr["type"]}
            for attr in cls_data["attributes"]
        ] + [
            {"name": child, "type": "class"}
            for child in cls_data["children"]
        ]
        
        node = {
            "class": cls_data["name"],
            "documentation": cls_data["documentation"],
            "isRoot": cls_data["isRoot"],
            "parameters": parameters
        }
        
        if not cls_data["isRoot"]:
            node["max"] = cls_data["max"]
            node["min"] = cls_data["min"]
            
        return node

    return [create_meta_node(data) for data in classes.values()]

def generate_config_xml(classes: Dict[str, Any]) -> str:
    roots = [name for name, data in classes.items() if data['isRoot']]
    if not roots:
        return ""
    
    def build_element(cls_name: str) -> ET.Element:
        elem = ET.Element(cls_name)
        cls_data = classes[cls_name]
        
        for attr in cls_data["attributes"]:
            attr_elem = ET.SubElement(elem, attr["name"])
            attr_elem.text = attr["type"]
            
        for child in cls_data["children"]:
            elem.append(build_element(child))
            
        return elem

    root_elem = build_element(roots[0])
    xml_str = ET.tostring(root_elem, encoding='utf-8')
    
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="    ")
    return '\n'.join(pretty_xml.split('\n')[1:]).strip()