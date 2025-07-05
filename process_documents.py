import requests
import json

# Your Render backend URL
BACKEND_URL = "https://personal-chatbot-assistant.onrender.com"

def process_documents():
    """Process documents and add them to the vector database"""
    print("Processing documents...")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/process",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"reset": False})
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_query():
    """Test a query to see if documents are indexed"""
    print("\nTesting query...")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/query",
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                "query": "What are Nikhil's Python skills and qualifications?",
                "chat_history": []
            })
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Query successful!")
            print(f"Answer: {result['answer']}")
            print(f"Sources found: {len(result['sources'])}")
            return True
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("=== Document Processing Script ===")
    
    # Step 1: Process documents
    if process_documents():
        print("\n=== Testing Query ===")
        # Step 2: Test a query
        test_query()
    else:
        print("Document processing failed. Check your backend logs.") 