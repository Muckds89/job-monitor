import os
import json

def load_config():
    expand_list = []
    config_file_path = os.path.join(os.path.dirname(__file__), "config.json")
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Config file not found: {config_file_path}")
    
    with open(config_file_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    companies = config.get("companies", [])
    for company in companies:
        if "api_url" not in company:
            raise ValueError(f"Missing 'api_url' in company config: {company}")
        if "state_file" not in company:
            raise ValueError(f"Missing 'state_file' in company config: {company}")
        if "ats" not in company:
            raise ValueError(f"Missing 'ats' in company config: {company}")



    return companies
