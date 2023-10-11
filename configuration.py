import json

def parse_json_file(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def get_enabled_services(data):
    if data and 'services' in data:
        return data['services']
    else:
        return []

def get_team_numbers(data):
    if data and 'teams' in data:
        return [team['number'] for team in data['teams']]
    else:
        return []

def get_team_ip_addresses(data):
    if data and 'teams' in data:
        return [team['ip_address'] for team in data['teams']]
    else:
        return []

if __name__ == "__main__":
    # Replace 'your_json_file.json' with the path to your JSON file
    json_data = parse_json_file('../config.json')

    if json_data:
        team_numbers = get_team_numbers(json_data)
        team_ip_addresses = get_team_ip_addresses(json_data)

        print("Team Numbers:", team_numbers)
        print("Team IP Addresses:", team_ip_addresses)
