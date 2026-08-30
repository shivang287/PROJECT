from google import genai
client = genai.Client()
response = client.models.generate_content(
    model = "gemini-3.5-flash",
    contents="Reply exactly with: Gemini connection successful"
)

print(response.text)