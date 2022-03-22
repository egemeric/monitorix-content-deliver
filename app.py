import json
import io
from flask import Flask, request, make_response, send_file
from controller.requestbot import PageBot
from system.cron import Cron
app = Flask(__name__)
mbot = PageBot(
    "http://10.1.1.2:8080/monitorix-cgi/monitorix.cgi?mode=localhost&graph=all&when=1day&color=black")
mbot2 = PageBot(
    "http://10.1.1.21:8080/monitorix-cgi/monitorix.cgi?mode=localhost&graph=all&when=1day&color=black")


mbotcron = Cron(mbot,60*30)
mbot2cron = Cron(mbot2,60*10)
mbotcron.start()
mbot2cron.start()


@app.route('/getImage', methods=['GET'])
def getimage():
    ImageSrc = request.args.get('src')
    if(mbot.IMAGES.get(ImageSrc)):
        return send_file(io.BytesIO(mbot.IMAGES[ImageSrc]), 'image/'+ImageSrc.split(".")[-1])
    else:
        return app.response_class(
            response=json.dumps({"err": "NOT FOUND"}),
            content_type="application/json",
            status=404,
        )


@app.route('/getMonitorixImages/', methods=['GET'])
def getimages():
    if mbot.is_alive() is not True:
        return app.response_class(
            response=json.dumps({'stats-imgs': list(mbot.IMAGES.keys())}),
            content_type='application/json',
            status=200,
        )
    else:
        return app.response_class(
            response=json.dumps({'stats-imgs': 'fetching'}),
            content_type='application/json',
            status=200,
        )


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=False, host='0.0.0.0', port='8888')
