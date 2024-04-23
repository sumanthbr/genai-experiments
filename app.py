import feedparser
from datetime import datetime, timedelta
import json
import os
import csv
from azure.storage.blob import BlobServiceClient
import google.generativeai as genai
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from mailjet_rest import Client

def configure_generative_ai(api_key, model_name):
    # Configure the generative AI API
    genai.configure(api_key=api_key)
    # Set up the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 2048,
    }
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]
    model = genai.GenerativeModel(model_name=model_name,
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    return model

def generate_article_list(feed_url):
    # Parse the feed
    feed = feedparser.parse(feed_url)

    # Get the current date and time
    current_time = datetime.now()

    # Create a list to store the article titles and links
    articles = []

    # Loop through all items in the feed
    for entry in feed.entries:
        # Parse the publication date of the item
        pub_date = datetime(*entry.published_parsed[:6])
        
        # Check if the item was published within the last day
        if pub_date >= current_time - timedelta(days=1):
            # Add the article title and link to the list
            articles.append((entry.title, entry.link))
    
    # Return the list of articles
    return articles

def generate_blog_post_summary(model, prompt_parts):
    # Generate the blog post summary
    response = model.generate_content(prompt_parts)
    print(response.text)
    return response.text

# Generate the article list
# Read the URLs from the config json file

def read_config_file(file_path):
    with open(file_path, 'r') as file:
        config_data = json.load(file)
    return config_data

def upload_summary_to_blob_storage(connection_string, container_name, blob_name, summary_file_path):
    # Create a BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    # Get a BlobClient object for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    # Upload the summary markdown file to Azure Blob Storage
    with open(summary_file_path, "rb") as file:
        blob_client.upload_blob(file, overwrite=True)

config_file_path = "config.json"
config_data = read_config_file(config_file_path)
# Configure the generative AI model
api_key = os.environ.get("GENERATIVE_AI_API_KEY")
model_name =  os.environ.get("MODEL_NAME")
#"gemini-1.0-pro"
model = configure_generative_ai(api_key, model_name)

# Generate the article list for each URL
articles = []
for url in config_data["urls"]:
    articles += generate_article_list(url)

# Generate the blog post summary for each article in the list using the generative AI model
# Loop through each article and generate the blog post summary
summary_list = []
for article in articles:
    url = article[1]
    prompt_parts = [
        f"Imagine you are a technical architect with expertise in summarizing blog content. You have been given a URL {url} of a blog post. Your task is to distill the essence of the blog post into a concise summary, not exceeding 150 words. The summary should be comprehensive, capturing all the relevant content from the blog post. Begin with the title of the blog which should have a hyperlink to the url, followed by the summary presented as bullet points. Remember, the goal is to provide a quick glance at the blog's content without losing any significant information. Your summary should be formal and confident, reflecting your expertise. The expected result format is html and ensure you follow the format strictly. Use your creativity and originality to make the summary engaging and informative."
    ]
    summary = generate_blog_post_summary(model, prompt_parts)
    summary_list.append((article[0], url, summary))


# Generate the file path by appending today's date in ddmmyyyy format
today = datetime.now().strftime("%d%m%Y")
markdown_file_path = f"summary_list_{today}.md"
# Write the summary list to a markdown file
with open(markdown_file_path, 'w', encoding='utf-8') as file:
    file.write("# Cloudy with a Chance of AI\n\n")
    file.write("Immerse yourself in Sumanth Badethalav's **Cloudy with a Chance of AI**, your curated lightning bolt of knowledge, condensing top AI and cloud blog highlights into an electrifying summary. \n\n")    
    for summary in summary_list:                
        file.write(f"{summary[2]}\n\n")        

# Define your Azure Blob Storage connection string
connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
# Define the name of your container
container_name = "dailysummaries"
# Define the path of the summary markdown file
summary_file_path = f"summary_list_{today}.md"
# Define the name of the blob in the container
blob_name = f"summaries/{summary_file_path}"
upload_summary_to_blob_storage(connection_string, container_name, blob_name, summary_file_path)


# After uploading the file, you can use the summary_list for sending email

# Use the summary_list for sending email

def send_email(api_key, sender_email, recipient_email, subject, body):
    message = Mail(
        from_email=sender_email,
        to_emails=recipient_email,
        subject=subject,
        plain_text_content=body
    )
    try:
        sg = SendGridAPIClient(api_key=api_key)
        response = sg.send(message)
        print(f"Email sent successfully. Response: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

# Define your SendGrid API key
sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
# Define the sender's email address
sender_email = "sumanthbadethalavr@gmail.com"
# Define the recipient's email address
recipient_email = os.environ.get("RECIPENT_EMAIL_LIST")
# Define the email subject
subject = "Cloudy with a Chance of AI - Newsletter from Sumanth B R"
# Define the email body
# Read the contents of the markdown file
with open(markdown_file_path, 'r', encoding='utf-8') as file:
    body = file.read()
# Send the email
send_email(sendgrid_api_key, sender_email, recipient_email, subject, body)


api_key = os.environ.get("MAILJET_API_KEY")
api_secret = os.environ.get("MAILJET_SECRET")
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
recipient_email = os.environ.get("RECIPENT_EMAIL_LIST")
with open(markdown_file_path, 'r', encoding='utf-8') as file:
    body = file.read()
data = {
  'Messages': [
    {
      "From": {
        "Email": "sumanthbadethalavr@gmail.com",
        "Name": "Sumanth"
      },
      "To": [
        {
          "Email": recipient_email
        }
      ],
      "Subject": "Cloudy with a Chance of AI - Newsletter from Sumanth B R",
      "TextPart": "My first Mailjet email",
      "HTMLPart": body,
      "CustomID": "AppGettingStartedTest"
    }
  ]
}
result = mailjet.send.create(data=data)
print (result.status_code)
print (result.json())

