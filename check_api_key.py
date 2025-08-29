import os
from dotenv import load_dotenv

load_dotenv()

# Check if API key exists and is valid format
api_key = os.getenv('NEWS_API_KEY')

print("🔍 Checking NewsData.io API Key Configuration")
print("=" * 50)

if not api_key:
    print("❌ ERROR: NEWSDATA_API_KEY not found in environment variables")
    print("Please add it to your .env file:")
    print("NEWS_API_KEY=your_actual_api_key_here")
elif api_key.startswith('your_') or 'example' in api_key.lower():
    print("❌ ERROR: API key appears to be a placeholder")
    print(f"Current value: {api_key}")
    print("Please replace with your actual API key from newsdata.io")
elif len(api_key) < 20:
    print("❌ ERROR: API key seems too short")
    print(f"Key length: {len(api_key)} characters")
    print("A valid API key should be longer")
else:
    print("✅ API key found in environment variables")
    print(f"📋 Key: {api_key[:10]}...{api_key[-10:]}")
    print(f"📏 Length: {len(api_key)} characters")

# Check if .env file exists
env_path = '.env'
if os.path.exists(env_path):
    print(f"\n✅ .env file found at: {os.path.abspath(env_path)}")
    with open(env_path, 'r') as f:
        content = f.read()
        if 'NEWS_API_KEY' in content:
            print("✅ NEWS_API_KEY found in .env file")
        else:
            print("❌ NEWS_API_KEY not found in .env file")
else:
    print(f"\n❌ .env file not found at: {os.path.abspath(env_path)}")

print("\n🔗 Get your free API key from: https://newsdata.io/pricing")