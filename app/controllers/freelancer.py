import requests
import os
from dotenv import load_dotenv
from app.utils.openai_client import generate_openai_response
import json  # Import to parse JSON strings
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

GET_SKILL_API_URL = os.getenv("GET_SKILL_API_URL")
GET_COUNTRY_API_URL = os.getenv("GET_COUNTRY_API_URL")

def chunk_array_with_overlap(skill_array, max_length=100):
    """Chunk the skill array into manageable pieces."""
    for i in range(0, len(skill_array), max_length):
        yield skill_array[i:i + max_length]


def process_single_chunk(chunk, input_skill):
    """Process a single chunk to find matching skills."""
    prompt = f"""
                The user will only send you the query. Based on the query, return the most similar skill(s) from the provided list: {chunk}.
                Respond **only** with a valid JSON object that can be parsed using `json.loads()` in Python. Do not include any additional text, examples, markup, or characters before or after the JSON object.

                The response should strictly adhere to this format:
                {{
                    "skills": ["<Skill1>", "<Skill2>"]
                }}
                
                The above given format is just an example json that you have to generate.
                Replace [`<Skill1>, <Skill2>]` with generated values from the list: {chunk}. If no relevant skills are found, return an empty array.
                No explanation, comments, or additional information should be included. Do not return the markup format also.
                sample output:
                {{
                    "skills": ["Angular Js"]
                }}
            """
    try:
        json_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "skills_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "skills": {
                            "description": "A list of skills relevant to the query",
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "additionalProperties": False
                }
            }
        }
        # Call OpenAI API with the chunked data
        response = generate_openai_response(prompt, input_skill, json_schema)
        parsed_response = json.loads(response)
        
        # Filter to include only skills present in the current chunk
        valid_skills = [skill for skill in parsed_response["skills"] if skill in chunk]
        print("Valid skills::", valid_skills)
        return valid_skills

    except json.JSONDecodeError as err:
        print("Error decoding JSON response:", response)
        return []
    except Exception as e:
        print(f"Error processing chunk: {str(e)}")
        return []


def process_skill_chunks_parallel(skill_chunks, input_skill):
    """Process skill chunks in parallel to improve performance."""
    responses = []
    with ThreadPoolExecutor() as executor:
        future_to_chunk = {executor.submit(process_single_chunk, chunk, input_skill): chunk for chunk in skill_chunks}
        
        for future in as_completed(future_to_chunk):
            try:
                result = future.result()
                if result:
                    responses.extend(result)
            except Exception as e:
                print(f"Error in parallel processing: {str(e)}")
    return responses


def get_freelancer_response(user_query: str) -> str:
    try:
        headers = {"User-Agent": "FastAPI-Client/1.0", "Accept": "application/json"}

        # Fetch and format country data
        country_response = requests.get(GET_COUNTRY_API_URL, headers=headers)
        if country_response.status_code != 200:
            raise Exception(f"Error fetching data from getcountry API: {country_response.status_code}")
        country_data = country_response.json()  # Parse as JSON
        formatted_country = ", ".join(country_data)

        # Fetch and chunk skill data
        skill_response = requests.get(GET_SKILL_API_URL, headers=headers)
        if skill_response.status_code != 200:
            raise Exception(f"Error fetching data from getskills API: {skill_response.status_code}")
        skill_data = skill_response.json()  # Parse as JSON
        skill_chunks = list(chunk_array_with_overlap(skill_data, max_length=500))

        # Step 1: Process each chunk to find the best matches in parallel
        filtered_skills = process_skill_chunks_parallel(skill_chunks, user_query)
        print("filtered_skills:: ", filtered_skills)

        # Step 2: Aggregate results from all chunks
        formatted_skills = ", ".join(filtered_skills)
        print("formatted_skills:: ", formatted_skills)

        # Step 3: Construct the prompt
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
        note:- The keyword should be maximum one or two word only and that word will not in the skills
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

        # Generate OpenAI response
        final_response = generate_openai_response(PROMPT, user_query)
        return final_response

    except Exception as e:
        raise Exception(f"Error while fetching freelancer response: {str(e)}")