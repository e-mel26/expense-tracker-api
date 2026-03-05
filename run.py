from app import create_app

app = create_app()

@app.route("/")
def home():
    return {
        "service": "Expense Tracker API",
        "status": "running",
        "version": "1.0"
    }

if __name__ == "__main__":
    app.run()
