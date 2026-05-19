from typing import Dict, Any

def calculate_delta(config: Dict[str, str], patched: Dict[str, str]) -> Dict[str, Any]:
    conf_keys = frozenset(config.keys())
    patch_keys = frozenset(patched.keys())
    
    additions = [{"key": k, "value": patched[k]} for k in patch_keys - conf_keys]
    deletions = sorted(list(conf_keys - patch_keys))
    updates = [
        {"key": k, "from": config[k], "to": patched[k]}
        for k in conf_keys & patch_keys if config[k] != patched[k]
    ]
    
    return {
        "additions": additions,
        "deletions": deletions,
        "updates": updates
    }

def apply_delta(config: Dict[str, str], delta: Dict[str, Any]) -> Dict[str, str]:
    new_config = {k: v for k, v in config.items() if k not in delta["deletions"]}
    
    for update in delta["updates"]:
        if update["key"] in new_config:
            new_config[update["key"]] = update["to"]
            
    for addition in delta["additions"]:
        new_config[addition["key"]] = addition["value"]
        
    return new_config