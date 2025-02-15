from main import BUILD

if __name__ == "__main__":
    app = BUILD()
    app.run("0.0.0.0", 5000, debug=True)