from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/display', methods=['POST'])
def display_file():
  file = request.files['file']
  if not file:
    return "No file found"

  # Tentar ler o arquivo em diferentes codificações possiveis
  try:
    df = pd.read_csv(file, delimiter=";")
  except UnicodeDecodeError:
    file.seek(0) #resetar o ponteiro do arquivo caso não desa decodificação padrão
    try:
      df = pd.read_csv(file, encoding='latin1', delimiter=";")
    except UnicodeDecodeError:
      file.seek(0) #reseta denovo se não foi latin1
      df = pd.read_csv(file, encoding='ISO-8859-1', delimiter=";")

  return render_template('display.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == '__main__':
  app.run(debug=True)
  