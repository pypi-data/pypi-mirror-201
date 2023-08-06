import re
import json
import pkg_resources
import requests

__version__ = pkg_resources.get_distribution("ACML").version

def check_version(package_name, current_version):
    """
    Check if a new version of the package is available on PyPI.
    """
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    if response.status_code != 200:
        return False

    data = json.loads(response.content.decode("utf-8"))
    latest_version = data.get("info", {}).get("version")
    if latest_version is None:
        return False

    # Compare version numbers
    current_version = re.sub(r"[^\d\.]", "", current_version)
    latest_version = re.sub(r"[^\d\.]", "", latest_version)
    return current_version != latest_version

if check_version("ACML", __version__):
    print("[OUTDATED] - Please Consider Updating")
    print("`pip install ACML --upgrade`")

def parse(file_path):
    """
    Parses the given configuration file and returns a nested dictionary.
    """
    config = {}

    with open(file_path) as f:
        current_section = None
        current_dict = None
        current_subsection = None
        current_subsection_dict = None

        for line in f:
            line = line.strip()

            # Ignore empty and comment lines
            if not line or line.startswith("#"):
                continue
            
            # Check for subsection header
            match = re.match(r"^\[(.*)\.(.*)\]$", line)
            if match:
                section_name = match.group(1)
                subsection_name = match.group(2)
                if section_name not in config:
                    config[section_name] = {}
                if subsection_name not in config[section_name]:
                    config[section_name][subsection_name] = {}
                current_dict = config[section_name][subsection_name]
                current_subsection = subsection_name
                continue

            # Check for section headers
            match = re.match(r"^\[(.*)\]$", line)
            if match:
                current_section = match.group(1)
                current_dict = config.setdefault(current_section, {})
                current_subsection = None
                continue

            # Parse key-value pairs
            key, value = line.split("=")
            key = key.strip()
            value = convert_value(value)

            # Check if the key belongs to a subsection
            if current_subsection is not None:
                current_dict[key] = value
            else:
                current_dict = config.setdefault(current_section, {})
                current_dict[key] = value

    return config

def convert_value(value):
    """
    Converts the given string value to a Python object.
    """
    conversions = {
        "true": True,
        "false": False,
    }
    if value.isdigit():
        return int(value)
    elif "." in value:
        try:
            return float(value)
        except ValueError:
            pass
    elif value[1] == "[" and value[-1] == "]":
        # Convert comma-separated list to Python list
        value = value.replace("[", ""); value = value.replace("]", "")
        return [convert_value(item.strip()) for item in value[1:-1].split(",")]
    elif value[1] == "{" and value[-1] == "}":
        # Convert JSON-style dictionary to Python dictionary
        return eval(value)
    
    value = value.strip().replace("\"", "")
    return conversions.get(value, value)
