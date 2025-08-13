from flask import Flask, render_template, request

app = Flask(__name__)

tarefas = []
proximo_id = 1

@app.route("/", methods=["POST", "GET"])
def index():
    global proximo_id

    if request.method == "POST":
        nome_tarefa = request.form.get("tarefa")
        data_limite = request.form.get("data_limite")
        
        tarefa = {
            'id': proximo_id,
            'tarefa': nome_tarefa,
            'data_limite': data_limite
        }
        tarefas.append(tarefa)
        proximo_id += 1
        
        return render_template("/sucesso.html", tarefa=nome_tarefa, data_limite=data_limite)
        
    return render_template("/index.html", tarefas=tarefas) 

if __name__ == '__main__':
    app.run(debug=True)