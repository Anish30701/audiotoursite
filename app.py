from flask import Flask, render_template, request
from gtts import gTTS
import os
import json

app = Flask(__name__)

# Store selected language
language_choice = {}

# Load products from JSON file
with open('products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/language", methods=["POST"])
def set_language():
    # Lowercase the language to avoid mismatches
    language_choice['lang'] = request.form["language"].lower()
    return render_template("scan.html")

@app.route("/product/<product_id>", methods=["GET"])
def show_product(product_id):
    selected_lang = language_choice.get('lang', 'english')
    product_id = product_id.strip()

    print(f"Requesed product ID: {product_id}")
    print(f"Selected language: {selected_lang}")
    print(f"Available products: {list(products.keys())}")

    product = products.get(product_id)

    tts_lang = {
        "english": "en",
        "tamil": "ta",
        "hindi": "hi"
    }

    if product and selected_lang in product:
        name = product[selected_lang]["name"]
        desc = product[selected_lang]["description"]
        text = f"{name}, {desc}"
        tts = gTTS(text=text, lang=tts_lang[selected_lang])
        tts.save("static/audio.mp3")

        return render_template("product.html", product={
            "name": name, 
            "desc": desc,
            "number": product_id})
    else:
        message = {
            "english": "Sorry, this product is not available",
            "tamil": "மன்னிக்கவும், இந்த தயாரிப்பு கிடைக்கவில்லை",
            "hindi": "माफ़ कीजिए, यह उत्पाद उपलब्ध नहीं है"
        }

        msg = message.get(selected_lang, message["english"])

        tts = gTTS(text=msg, lang=tts_lang.get(selected_lang, "en"))
        tts.save("static/audio.mp3")

        return render_template("product.html", product=None, message=msg)

if __name__ == "__main__":
    app.run(debug=True)
