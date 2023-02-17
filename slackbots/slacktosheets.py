import os
from slack_bolt import App
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Initialize the app with your bot token
app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Initialize the Google Sheets API client
creds = service_account.Credentials.from_service_account_file("path/to/credentials.json")
service = build("sheets", "v4", credentials=creds)
sheet_id = "YOUR_SHEET_ID"

# Define a survey message with interactive components
survey_message = {
    "text": "Please take our survey:",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "How satisfied are you with our product?"
            },
            "accessory": {
                "type": "radio_buttons",
                "action_id": "survey_q1",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Very satisfied"
                        },
                        "value": "very_satisfied"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Somewhat satisfied"
                        },
                        "value": "somewhat_satisfied"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Neutral"
                        },
                        "value": "neutral"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Somewhat dissatisfied"
                        },
                        "value": "somewhat_dissatisfied"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Very dissatisfied"
                        },
                        "value": "very_dissatisfied"
                    }
                ]
            }
        }
    ]
}

# Define a survey response handler
def handle_survey_response(ack, payload):
    # Get the response data
    response_value = payload["actions"][0]["selected_option"]["value"]
    user_id = payload["user"]["id"]
    
    # Write the response data to the Google Sheet
    sheet_range = "Sheet1!A2:C"
    values = [[user_id, response_value, str(payload["action_ts"])]]
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=sheet_range,
        valueInputOption="USER_ENTERED",
        body={"values": values},
    ).execute()
    
    # Acknowledge the response
    ack()

if __name__ == "__main__":
    # Listen for survey responses
    app.action("survey_q1")(handle_survey_response)
    
    # Start the app
    app.start(port=int(os.environ.get("PORT", 3000)))
