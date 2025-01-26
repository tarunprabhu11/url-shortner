
from flask import Flask, request, jsonify, redirect
from models import db, URL
import secrets
import validators

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=Db1;Trusted_Connection=yes'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    # Validate the URL
    if not original_url or not validators.url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    # Generate a unique short code
    short_code = secrets.token_urlsafe(6)  # Generates a 6-character short code

    # Ensure the short code is unique
    while URL.query.filter_by(short_code=short_code).first():
        short_code = secrets.token_urlsafe(6)

    # Create the new URL entry
    new_url = URL(url=original_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        "id": new_url.id,
        "url": new_url.url,
        "shortCode": new_url.short_code,
        "createdAt": new_url.created_at.isoformat(),
        "updatedAt": new_url.updated_at.isoformat()
    }), 201


@app.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    
    if not url:
        return jsonify({"error": "URL not found"}), 404
    
    # Increment access count
    url.access_count += 1
    db.session.commit()

    return jsonify({
        "id": url.id,
        "url": url.url,
        "shortCode": url.short_code,
        "createdAt": url.created_at.isoformat(),
        "updatedAt": url.updated_at.isoformat()
    })


@app.route('/shorten/<short_code>', methods=['PUT'])
def update_short_url(short_code):
    data = request.get_json()
    new_url = data.get('url')

    # Validate the new URL
    if not new_url or not validators.url(new_url):
        return jsonify({"error": "Invalid URL"}), 400

    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({"error": "URL not found"}), 404

    url.url = new_url
    db.session.commit()

    return jsonify({
        "id": url.id,
        "url": url.url,
        "shortCode": url.short_code,
        "createdAt": url.created_at.isoformat(),
        "updatedAt": url.updated_at.isoformat()
    })


@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_short_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({"error": "URL not found"}), 404

    db.session.delete(url)
    db.session.commit()

    return '', 204


@app.route('/shorten/<short_code>/stats', methods=['GET'])
def get_url_stats(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({"error": "URL not found"}), 404

    return jsonify({
        "id": url.id,
        "url": url.url,
        "shortCode": url.short_code,
        "createdAt": url.created_at.isoformat(),
        "updatedAt": url.updated_at.isoformat(),
        "accessCount": url.access_count
    })


@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({"error": "URL not found"}), 404

    # Increment access count
    url.access_count += 1
    db.session.commit()

    return redirect(url.url)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
