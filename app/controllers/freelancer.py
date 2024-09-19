import requests
import json
from app.utils.openai_client import generate_openai_response  # Adjust path if necessary
import os
from dotenv import load_dotenv

load_dotenv()
# Define and get the third-party API URL from env
GET_SKILL_API_URL = os.getenv("GET_SKILL_API_URL")
GET_COUNTRY_API_URL = os.getenv("GET_COUNTRY_API_URL")


import requests

def get_freelancer_response(user_query: str) -> str:
    try:
        # API URLs
        #GET_SKILL_API_URL = 'http://localhost/connectresearch/get_tax.php?tax=skill'
        #GET_COUNTRY_API_URL = 'http://localhost/connectresearch/get_tax.php?tax=country'

        headers = {
            "User-Agent": "FastAPI-Client/1.0",
            "Accept": "application/json"  # Expect JSON responses
        }

        # Fetch country data
        country_response = requests.get(GET_COUNTRY_API_URL, headers=headers)
        if country_response.status_code != 200:
            raise Exception(f"Error fetching data from getcountry API: {country_response.status_code}")
        country_data = country_response.json()  # Parse as JSON
        #print("Country data:", country_data)
         # Format country_data into a comma-separated string for the prompt
        formatted_country = ", ".join(country_data)  # Assuming `skill_data` is a list of skill strings
        #print("Formatted country:", formatted_country)
        

        # Fetch skill data
        skill_response = requests.get(GET_SKILL_API_URL, headers=headers)
        if skill_response.status_code != 200:
            raise Exception(f"Error fetching data from getskills API: {skill_response.status_code}")
        skill_data = skill_response.json()  # Parse as JSON
        #print("Skill data:", skill_data)

        # Format skill_data into a comma-separated string for the prompt
        formatted_skills = ", ".join(skill_data)  # Assuming `skill_data` is a list of skill strings
        #print("Formatted Skills:", formatted_skills)

        #earnings_data = ["Any amount", "0-100", "100-1000", "1000-10000", "Greater than 10000"]


        # Constants
        PROMPT = f"""
        you are an AI tool, you have to generate the data in this format:
        {{
        "keyword": "<ExampleKeyword>",
        "skills": ["<ExampleSkill>"],
        "earnings": "<ExampleEarnings>",
        "projects_worked": "<ExampleProjectsWorked>",
        "location": "<ExampleLocation>",
        "hourly_rate": "<ExampleRate>"
        }}

        The above given format is just an example json that you have to generate.

        The user will only send you the description. Based on the description, extract the data from that and check if the extracted data lie in the provided data if it is not there in this then keep it blank. skills_data=[{formatted_skills}], location_data=[{formatted_country}], earnings_data=[ "Any amount", "0 - 100", "100 - 1000", "1000 - 10000", "Greater than 10000" ], projects_worked_data=[ "Any projects worked", "0 - 10", "11 - 20, "21 - 30", "Greater than 30" ]. create a json format as given above.
        Replace <ExampleKeyword>, <ExampleSkill>, <ExampleEarnings>, <ExampleProjectsWorked>, <ExampleLocation> and <ExampleRate> with generated values. If you think the user has not provided any value for a given key, keep that key blank.
        Based on the user query, provide simple string titles.
        I need the json object in response; do not send any other json or characters. I need to extract json from your response with json.loads() function in python.
        Sample output:
        {{
        "keyword": "Frontend Developer",
        "skills": ["Angular js"],
        "earnings": "$30",
        "projects_worked": "CRM",
        "location": "Bangalore",
        "hourly_rate": "$20-$150"
        }}
        """
        #print("PROMPT:::::", PROMPT)

        # Step 4: Pass the modified query to the OpenAI API
        openai_response = generate_openai_response(PROMPT, user_query)

        return openai_response

    except Exception as e:
        # Handle and log exceptions if necessary
        raise Exception(f"Error while fetching freelancer response: {str(e)}")
