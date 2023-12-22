from flask import Flask

app = Flask(__name__)

@app.route('/a')
def home():
    return "hi"

if __name__ == '__main__':
    app.run(debug=True, host="14.194.71.227", port=2000)