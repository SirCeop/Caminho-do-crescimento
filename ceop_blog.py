from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    return render_template('post.html', post_id=post_id)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

## ...

@app.route('/introducao')
def introducao():
    return render_template('introducao.html')

@app.route('/habilidades')
def habilidades():
    return render_template('habilidades.html')

# Rota para a página de contato
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        mensagem = request.form['mensagem']
        print(f'Mensagem Recebida: {mensagem}')
    return render_template('contato.html')


if __name__ == '__main__':
    app.run(debug=True)
