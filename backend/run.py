import os
from app import create_app
from dotenv import load_dotenv

load_dotenv()  

app = create_app()

if __name__ == "__main__":
    app.run(
            host=os.getenv("HOST", "0.0.0.0"), 
            port=os.getenv("PORT","5050"), 
            debug=os.getenv("DEBUG", True)
            ) 
