import logging
from flask import Flask, request, jsonify

from model import LRModel

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

model = LRModel()
model.initialize_model()

@app.route('/')
def test():
    '''
    Used for easy testing (avoid command lines to check if API works).
    When running the api, you can copy the address on your browser first to see if you see the message below.
    Alternatively: You can just CURL the url from command line to see if it returns the message below.
    If you can see it, it means the API works, and you can move on to query some features for predictions.
    '''
    return jsonify({
      'Testing': 'It works!'
    })


@app.route('/predict', methods=['POST'])
def predict():
    '''
    Return A Prediction.
    '''
    data = request.get_json()
    app.logger.info("Record To predict: {}".format(data))
    app.logger.info(type(data))
    input_data = [data["data"]]
    app.logger.info(input_data)

    input_data = model.scale_input(input_data)
    prediction = model.predict(input_data)

    app.logger.info(prediction)
    response_data = prediction[0]
    return {"prediction": str(response_data)}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


# Some input data for testing
#[40981.0, -0.7842910186562471, -2.7012257535647324, -0.0967386127210913, 0.521375119473271, -1.70573851640263, 1.10351855890133, 0.431322198687247, 0.22802116977057896, 1.4652977928665, -1.3066944304644599, 1.33128250555487, 1.57790719991889, -0.440560604628892, 0.128074950688203, 0.0286489136111531, -0.9625872691461059, 0.519210020956086, -0.38704390740026795, -0.0490091299964628, 0.6502217079234472, 0.516072072435101, -0.338177074515334, -0.6258812915555879, -0.22207187222957603, -0.0298968921431093, -0.6783181524614119, -0.0659639052697792, 0.18338004089478102, 185.375]
# target: 0

# input: [26899.0, -4.263979957375013, 2.901188080680856, -3.7646449731967673, 3.124319110867031, -2.6429012689627394, -2.5177651329422983, -2.236984407382579, 1.1275019172451173, -2.504517212462476, -2.019373365934702, 2.991421924993211, -1.9409590671956645, 0.461807829323489, -1.802834475317419, -0.0228148529460228, -1.952416410433839, -1.8082765194756663, -1.997969244031534, 1.10435473489394, 0.6502217079234472, 0.8079413701109316, -1.57905510076487, -0.6258812915555879, 0.13456529188962, 1.3528964721899515, -0.22267085685559398, 0.3339816451473099, 0.2749172881886554, 99.99]
# target: 1

# [56887.0, -0.0754834663888726, 1.8123545842275102, -2.5669808101696203, 3.124319110867031, -1.62853157024518, -0.805895445766318, -2.236984407382579, 1.01935326231828, -2.45125125188341, -2.019373365934702, 2.991421924993211, -1.9409590671956645, -2.11550315600957, -1.802834475317419, 0.280108069299552, -1.952416410433839, -1.8082765194756663, -1.997969244031534, -0.440434552920779, 0.338598140549314, 0.7943724518977819, 0.27047123229786607, -0.143624140755259, 0.0135659145316466, 0.634203128800614, 0.213693187250942, 0.3339816451473099, 0.2749172881886554, 5.0]
# 1

# curl -X POST localhost:8080/predict -d '{"data": [56887.0, -0.0754834663888726, 1.8123545842275102, -2.5669808101696203, 3.124319110867031, -1.62853157024518, -0.805895445766318, -2.236984407382579, 1.01935326231828, -2.45125125188341, -2.019373365934702, 2.991421924993211, -1.9409590671956645, -2.11550315600957, -1.802834475317419, 0.280108069299552, -1.952416410433839, -1.8082765194756663, -1.997969244031534, -0.440434552920779, 0.338598140549314, 0.7943724518977819, 0.27047123229786607, -0.143624140755259, 0.0135659145316466, 0.634203128800614, 0.213693187250942, 0.3339816451473099, 0.2749172881886554, 5.0]}' -H 'Content-Type: application/json'

# curl -X POST localhost:5000/predict -d '{"data": [26899.0, -4.263979957375013, 2.901188080680856, -3.7646449731967673, 3.124319110867031, -2.6429012689627394, -2.5177651329422983, -2.236984407382579, 1.1275019172451173, -2.504517212462476, -2.019373365934702, 2.991421924993211, -1.9409590671956645, 0.461807829323489, -1.802834475317419, -0.0228148529460228, -1.952416410433839, -1.8082765194756663, -1.997969244031534, 1.10435473489394, 0.6502217079234472, 0.8079413701109316, -1.57905510076487, -0.6258812915555879, 0.13456529188962, 1.3528964721899515, -0.22267085685559398, 0.3339816451473099, 0.2749172881886554, 99.99]}' -H 'Content-Type: application/json'

# curl -X POST http://127.0.0.1:5000/predict -d '{"data": [26899.0, -4.263979957375013, 2.901188080680856, -3.7646449731967673, 3.124319110867031, -2.6429012689627394, -2.5177651329422983, -2.236984407382579, 1.1275019172451173, -2.504517212462476, -2.019373365934702, 2.991421924993211, -1.9409590671956645, 0.461807829323489, -1.802834475317419, -0.0228148529460228, -1.952416410433839, -1.8082765194756663, -1.997969244031534, 1.10435473489394, 0.6502217079234472, 0.8079413701109316, -1.57905510076487, -0.6258812915555879, 0.13456529188962, 1.3528964721899515, -0.22267085685559398, 0.3339816451473099, 0.2749172881886554, 99.99]}' -H 'Content-Type: application/json'