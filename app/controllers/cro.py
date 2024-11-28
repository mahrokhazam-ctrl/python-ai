import requests
import json
from app.utils.openai_client import generate_openai_response  # Adjust path if necessary
import os
from dotenv import load_dotenv

load_dotenv()
# Define and get the third-party API URL from env
#GET_SKILL_API_URL = os.getenv("GET_SKILL_API_URL")
#GET_COUNTRY_API_URL = os.getenv("GET_COUNTRY_API_URL")


import requests

def get_cro_response(user_query: str) -> str:
    try:
        
        # Constants
        
        PROMPT = f"""
        you are an AI tool, you have to generate the data in this format:
        {{
        "name": "<ExampleName>",
        "location": {{state:<ExampleState>, country:<ExampleCountry>}},
        "specialization": "<ExampleSpecialization>",
        "services": ["<ExampleServices>"],
        "specialties" : ["<ExampleSpecialties>"],
        "description" : "<ExampleDescription>",
        "website": "<ExampleWebsite>"
        }}

        Based on the user query you need to fetch all the Contract Research Organizations (CRO), and provide their details in the defined structured JSON format and if any key value is not there then keep it blank and if there are multiple CRO then return the array of data and maximum possible results.
        Replace <ExampleName>, {{state:<ExampleState>, country:<ExampleCountry>}}, <ExampleSpecialization>, <ExampleServices>, <ExampleSpecialties>, <ExampleDescription> and <ExampleWebsite> with generated values.

        I need the json object in response; do not send any other json or characters. I need to extract json from your response with json.loads() function in python. Please do not create any data from yourself. List minimum 20 records.
        Sample output:
        {{
        "name": "Innovaderm",
        "location":{{state:Montreal, country:QC}},
        "specialization": "Dermatology (atopic dermatitis, psoriasis, acne)",
        "services": ["Clinical trial management", "Phase I-IV trials"],
        "specialties" : ["Dermatology trials", "Phase I-IV clinical research"],
        "description" : "Innovaderm specializes in conducting clinical trials in dermatology, with a focus on skin-related diseases and treatments.",
        "website": "https://www.innovaderm.com"
        }}   
        """

        #print("PROMPT:::::", PROMPT)

        # Step 4: Pass the modified query to the OpenAI API
        openai_response = generate_openai_response(PROMPT, user_query)

        return openai_response

    except Exception as e:
        # Handle and log exceptions if necessary
        raise Exception(f"Error while fetching CROs response: {str(e)}")
