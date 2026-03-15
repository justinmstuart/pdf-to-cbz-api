from flask import Flask

from blueprints.pdf_to_cbz_bp import pdf_to_cbz_bp

app = Flask(__name__)

app.register_blueprint(pdf_to_cbz_bp, url_prefix='/pdf-to-cbz')

if __name__ == '__main__':
    app.run(debug=True)
