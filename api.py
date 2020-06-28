from flask import Flask, render_template, request
from flask_socketio import SocketIO
from genetic_algorithm import DNA, Settings
from forms import KnapsackForm

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    data = []

    if request.method == 'POST':
        print('ENTRO')
        form = KnapsackForm(request.form)

        settings = Settings()

        settings.set_knapsack_obj_values(form.get_knapsack_obj_values())
        settings.set_knapsack_values(form.get_knapsack_values())
        settings.set_dna_values(form.get_dna_values())
        print(settings)
        dna = DNA(settings)
        dna.reproduction()
        data = dna.population

    return render_template('index.html', knapsacks=data)


if __name__ == '__main__':
    app.run(port=8080, host='localhost')
