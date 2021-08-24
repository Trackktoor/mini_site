def index():
    with open('templates/index.html') as template:
        return template.read()

def home():
    with open('templates/home.html') as template:
        return template.read()