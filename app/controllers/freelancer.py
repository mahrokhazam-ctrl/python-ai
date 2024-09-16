import requests
from app.utils.openai_client import generate_openai_response  # Adjust path if necessary

# Define the third-party API URL
# GET_COUNTRY_API_URL = "http://localhost/connectresearch/get_tax.php?tax=country"

def get_freelancer_response(user_query: str) -> str:
    try:
        # # Step 1: Fetch country data from the third-party API
        # country_response = requests.get(GET_COUNTRY_API_URL)

        # if country_response.status_code != 200:
        #     raise Exception(f"Error fetching data from getcountry API: {country_response}")

        # # Step 2: Extract country list from the response (assuming the response is a JSON array)
        # country_data = country_response.json()

        # Constants
        PROMPT = """
        you are an AI tool, you have to generate the data in this format:
        {
        "Keyword": "<ExampleKeyword>",
        "Skills": ["<ExampleSkill>"],
        "Earnings": "<ExampleEarnings>",
        "Projects Worked": "<ExampleProjectsWorked>",
        "Location": "<ExampleLocation>",
        "Hourly Rate": "<ExampleRate>"
        }

        The above given format is just an example json that you have to generate.

        The user will only send you the description. Based on the description, extract the data from that and check if the extracted data lie in the provided data if it is not there in this then keep it blank. location_Data:- "india, nepal", skills_data=[ "Allergy", "Analytical Chemistry", "Analytical Testing", "Artificial Intelligence", "Asia-Pacific Clinical Trials",], location_data=[Algeria,American Samoa,Andorra,Angola,Anguilla,Antarctica,] . create a json format as given above
        Replace <ExampleKeyword>, <ExampleSkill>, <ExampleEarnings>, <ExampleProjectsWorked>, <ExampleLocation> and <ExampleRate> with generated values if you think the user has not provided any value for a given key keep that key blank. Based on the user query i will the simple string titles ,
        I need the json object in response do not send any other json and character i need  to extract json from your response with json.loads() function in python 
        Gather requirements for the landing page
        sample output:
        {
        "Keyword": "Frontend Developer",
        "Skills": ["Angular js", "React js", "Node", "java"],
        "Earnings": "$30",
        "Projects Worked": "CRM",
        "Location": "Bangalore",
        "Hourly Rate": "$20-$150"
        }
        """

        # Step 4: Pass the modified query to the OpenAI API
        openai_response = generate_openai_response(PROMPT, user_query)

        return openai_response

    except Exception as e:
        # Handle and log exceptions if necessary
        raise Exception(f"Error while fetching freelancer response: {str(e)}")
