from dataclasses import dataclass
from typing import List
from bs4 import BeautifulSoup
import requests

@dataclass
class TeamRecord:
    wins: int
    losses: int
    overtime_losses: int
    
    @classmethod
    def from_string(cls, record_str: str) -> 'TeamRecord':
        # Remove any extra whitespace
        record_str = record_str.strip()
        w, l, ot = map(int, record_str.split('-'))
        return cls(w, l, ot)

@dataclass
class NHLTeam:
    name: str
    record: TeamRecord
    row: int
    points: int
    goals_for: int
    goals_against: int
    home_record: TeamRecord
    away_record: TeamRecord
    division_record: TeamRecord
    conference_record: TeamRecord
    icf_record: TeamRecord

def parse_team_data(lines):
    teams = []
    current_data = []
    
    for line in lines:
        # Skip header lines and empty lines
        if any(header in line for header in ['CONFERENCE', 'Division', 'W-L-OT', 'ROW', 'Pts', 'GF', 'GA', 'Home', 'Away', 'Div', 'Cnf', 'Icf']):
            continue
        
        # Strip whitespace and skip empty lines
        line = line.strip()
        if not line:
            continue
            
        # Add non-empty lines to current_data
        current_data.append(line)
        
        # When we have 11 items (team name + 10 stats), we have a complete team
        if len(current_data) == 11:
            try:
                team_name = current_data[0]
                record = TeamRecord.from_string(current_data[1])
                row = int(current_data[2])
                points = int(current_data[3])
                goals_for = int(current_data[4])
                goals_against = int(current_data[5])
                home = TeamRecord.from_string(current_data[6])
                away = TeamRecord.from_string(current_data[7])
                div = TeamRecord.from_string(current_data[8])
                conf = TeamRecord.from_string(current_data[9])
                icf = TeamRecord.from_string(current_data[10])
                
                team = NHLTeam(
                    name=team_name,
                    record=record,
                    row=row,
                    points=points,
                    goals_for=goals_for,
                    goals_against=goals_against,
                    home_record=home,
                    away_record=away,
                    division_record=div,
                    conference_record=conf,
                    icf_record=icf
                )
                teams.append(team)
            except Exception as e:
                print(f"Error parsing team data: {current_data}")
                print(f"Error: {e}")
            
            current_data = []
            
    return teams


def stats():
  # Main script
  url = "https://www.shrpsports.com/nhl/stand.php?link=Y&season=2025&divcnf=div&date=0&month=xxx"
  response = requests.get(url)
  soup = BeautifulSoup(response.text, features='lxml')
  table = soup.find("table", attrs={"cellpadding": "4", "cellspacing": "0"})

  # Get all lines of text from the table
  lines = []
  for element in table.strings:
      lines.append(element.strip())

  # Parse teams
  teams = parse_team_data(lines)


  json_data = {}

  # Print the data for verification
  for team in teams:
      json_data[team.name] = {
          'record': team.record,
          'ROW': team.row,
          'points': team.points,
          'goalsfor': team.goals_for,
          'goalsagainst': team.goals_against,
          'homerecord': team.home_record,
          'awayrecord': team.away_record,
          'divisionrecord':team.division_record,
          'conferencerecord': team.conference_record,
          'icf': team.icf_record
      }
  return json_data

