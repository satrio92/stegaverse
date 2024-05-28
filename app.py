from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from cryptography import encrypt_message, decrypt_message
from steganography import hide_message, reveal_message
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('encrypt.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'image' not in request.files:
        flash('No image part')
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)
        message = request.form['message']
        shift = int(request.form['shift'])
        encrypted_message = encrypt_message(message, shift)
        output_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_' + file.filename)
        hide_message(image_path, encrypted_message, output_image_path)
        return redirect(url_for('uploaded_file', filename='output_' + file.filename))

@app.route('/decrypt', methods=['GET','POST'])
def decrypt():
     if request.method == 'GET':
        return render_template('decrypt.html')
     elif request.method == 'POST':
        if 'image' not in request.files:
            flash('No image part')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(image_path)
            shift = int(request.form['shift'])
            try:
                revealed_message = reveal_message(image_path)
                decrypted_message = decrypt_message(revealed_message, shift)
                flash(f'Decrypted Message: {decrypted_message}')
                loading = not bool(decrypted_message) 
                return render_template('decrypt.html', decrypted_message=decrypted_message, image_path=image_path, loading=loading)
            except Exception as e:
                flash(f'Error: {e}')
                return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
