from flask import Flask, render_template, request
from flask_socketio import SocketIO
from genetic_algorithm import DNA, Settings
from forms import KnapsackForm

app = Flask(__name__)

settings = Settings()


@app.route('/', methods=['GET', 'POST'])
def index():

    form = KnapsackForm(settings)
    data = []

    if request.method == 'POST':
        form.set_from_request(request.form)

        settings.set_knapsack_obj_values(form.get_knapsack_obj_values())
        settings.set_knapsack_values(form.get_knapsack_values())
        settings.set_dna_values(form.get_dna_values())

        dna = DNA(settings)
        dna.reproduction()
        data = dna.population

    return render_template('index.html', population=data, form=form)


if __name__ == '__main__':
    app.run(port=8080, host='localhost')
