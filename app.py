from app import create_app as create_flask_app

app = create_flask_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)