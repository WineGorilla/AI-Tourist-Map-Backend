from flask import Flask
from flask_cors import CORS
from pyngrok import ngrok
from app.routes import main_routes
from app.models import image_model
from app.models import text_model

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(main_routes.bp)
    return app

if __name__ == "__main__":
    ngrok.set_auth_token("Your Tokens")
    public_url = ngrok.connect(5000)
    print(f"Public URL: {public_url}")

    app = create_app()
    app.run(port=5000)
