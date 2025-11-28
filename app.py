from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        req_data = request.get_json()

        cep = req_data.get("cep") or req_data.get("input", {}).get("cep")

        if not cep:
            return jsonify({"err": True, "message": "CEP não enviado"}), 400

        r = requests.get(f"https://brasilapi.com.br/api/cep/v1/{cep}")
        data = r.json()

        return jsonify({
            "err": False,
            "cidade": data.get("city"),
            "rua": data.get("street"),
            "estado": data.get("state"),
            "bairro": data.get("neighborhood")
        })

    except Exception as e:
        return jsonify({"err": True, "message": str(e)})

@app.route("/")
def home():
    return "Webhook ativo!"
