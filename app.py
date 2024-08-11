from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaluation.db'
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    cleanliness = db.Column(db.Integer)
    organization = db.Column(db.Integer)
    presentation = db.Column(db.Integer)
    food_quality = db.Column(db.Integer)
    comments = db.Column(db.String(500))

# Função para gerar um nome aleatório
def gerar_nome_aleatorio():
    nomes = [
        "GreenLeaf", "VibePositive", "EcoFriendly", "PeaceLover",
        "HerbGarden", "PlantPower", "NatureSpirit", "ZenSpace",
        "EcoWarrior", "GreenBliss", "CannaCulture", "VeganVibes",
        "LeafyGreen", "ChillZone", "HighSpirits", "BotanicalBliss"
    ]
    return random.choice(nomes)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit_evaluation', methods=['POST'])
def submit_evaluation():
    # Lista de prefixos para as diferentes seções do formulário
    sections = ['casa_verde', 'jerimum']

    # Iterar sobre as seções para capturar e salvar as avaliações
    for section in sections:
        company = request.form.get(f'company_{section}')
        if not company:
            company = gerar_nome_aleatorio()  # Gera um nome aleatório se nenhum for fornecido

        cleanliness = request.form.get(f'cleanliness_{section}')
        organization = request.form.get(f'organization_{section}')
        presentation = request.form.get(f'presentation_{section}', 0)
        food_quality = request.form.get(f'food_quality_{section}', 0)
        comments = request.form.get(f'comments_{section}')

        # Debug prints
        print(f"Received data for {company} - Cleanliness: {cleanliness}, Organization: {organization}, Presentation: {presentation}, Food Quality: {food_quality}, Comments: {comments}")

        # Certifique-se de que todas as entradas estão sendo convertidas para o tipo correto
        cleanliness = int(cleanliness) if cleanliness is not None and cleanliness != '' else 0
        organization = int(organization) if organization is not None and organization != '' else 0
        presentation = int(presentation) if presentation is not None and presentation != '' else 0
        food_quality = int(food_quality) if food_quality is not None and food_quality != '' else 0

        # Debug prints after conversion
        print(f"Converted data for {company} - Cleanliness: {cleanliness}, Organization: {organization}, Presentation: {presentation}, Food Quality: {food_quality}, Comments: {comments}")

        # Criar uma nova instância de Evaluation com os valores recebidos
        new_evaluation = Evaluation(
            company=company,
            cleanliness=cleanliness,
            organization=organization,
            presentation=presentation,
            food_quality=food_quality,
            comments=comments
        )

        # Adicionar e confirmar a nova avaliação no banco de dados
        db.session.add(new_evaluation)

    # Confirmar todas as avaliações de uma vez
    db.session.commit()

    flash('Obrigado, avaliação enviada!')
    return redirect(url_for('home'))

@app.route('/evaluate/<company>')
def evaluate(company):
    return render_template('evaluate.html', company=company)

@app.route('/admin/evaluations', methods=['GET'])
def admin_evaluations():
    evaluations = Evaluation.query.all()
    return render_template('admin_evaluations.html', evaluations=evaluations)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Adicione esta linha para garantir que a base de dados será limpa
        db.create_all()  # Cria a tabela novamente com a estrutura atualizada
    app.run(debug=True)
