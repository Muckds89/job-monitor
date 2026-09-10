import requests
import urllib
import sys
url_ = sys.argv[1]
url_ = urllib.parse.unquote(url_)

# get key value and key type of a json response from a url
def get_json_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        json_data = response.json()
        fields_dict = {key: type(value) for key, value in json_data.items()}
        list_field = [key for key, value in fields_dict.items() if value == list]
        name_value_dict = {}
        for key, value in json_data.items():
            if isinstance(value, list):
                for item in value:
                    for sub_key, sub_value in item.items():
                        name_value_dict[sub_key] = type(sub_value)
                name_value_dict[key] = type(json_data[key])
        print(f"List fields: {list_field}")
        print(f"Name-value fields: {name_value_dict}")
        return list_field, name_value_dict
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON from {url}: {e}")
        return None, None

get_json_response(url_)