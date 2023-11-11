
import requests
import csv

# Replace these variables with your own details
personal_access_token = 'YOUR_PERSONAL_ACCESS_TOKEN'
organization = 'YOUR_ORGANIZATION'
project = 'YOUR_PROJECT'

# Base URL for Azure DevOps REST API
azure_devops_url = f'https://dev.azure.com/{organization}/{project}'

# Headers for authentication
headers = {
    'Authorization': f'Basic {personal_access_token}'
}

def get_teams():
    teams_url = f"{azure_devops_url}/_apis/projects/{project}/teams?api-version=6.0"
    response = requests.get(teams_url, headers=headers)
    return response.json()

def get_sprints(team):
    iterations_url = f"{azure_devops_url}/{team}/_apis/work/teamsettings/iterations?api-version=6.0"
    response = requests.get(iterations_url, headers=headers)
    return response.json()

def get_team_members(team):
    team_members_url = f"{azure_devops_url}/_apis/projects/{project}/teams/{team}/members?api-version=6.0"
    response = requests.get(team_members_url, headers=headers)
    return response.json()

def get_capacity(team, iteration_id):
    capacity_url = f"{azure_devops_url}/{team}/_apis/work/teamsettings/iterations/{iteration_id}/capacities?api-version=6.0"
    response = requests.get(capacity_url, headers=headers)
    return response.json()

def save_to_csv(filename, data):
    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def main():
    teams = get_teams()

    for team in teams['value']:
        team_name = team['name']
        print(f"Team: {team_name}")

        sprints = get_sprints(team_name)
        team_members = get_team_members(team_name)

        # Example: Getting capacity for the first sprint
        if sprints['value']:
            first_sprint_id = sprints['value'][0]['id']
            capacity = get_capacity(team_name, first_sprint_id)
        else:
            capacity = []

        # Save data to CSV (customize as needed)
        save_to_csv(f'{team_name}_data.csv', team_members)

if __name__ == "__main__":
    main()
