from flask import Response, Flask, stream_with_context

app = Flask(__name__)

@app.route('/jsonp/<int:size>')
def jsonp(size):
    def _genrate_file(size):
        yield "1"
        yield "\0" * (size-1)
    return Response(stream_with_context(_genrate_file(size)))

if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=8888, host="0.0.0.0")
