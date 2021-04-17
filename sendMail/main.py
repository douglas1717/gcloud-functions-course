from flask import abort, jsonify, make_response

def send_mail(request):

    request_json = request.get_json(silent=True)
    parameters = ('sender', 'receiver','subject','message')

    if request.method == "OPTIONS":
        headers = {'Access-Control-Allow-Origin':'*',
         'Access-Control-Allow-Methods': 'POST',
         'Access-Control-Allow-Headers': 'Content-Type',
         'Access-Control-Max-Age': '3600'}
        return '', 204, headers

    headers = {'Access-Control-Allow-Origin':'*'}
    if request.method != "POST":
        abort(404)

    bearer_token = request.headers.get("Authorization").split()[1]
    security_acess_token = "757f7645c4e09d2824ed7f8bc2d9e5e1"
    if bearer_token != security_acess_token:
        abort(401)

    if request_json and all(k in request_json for k in parameters):
        sender = request_json['sender']
        receiver = request_json['receiver']
        subject = request_json['subject']
        message = request_json['message']
    else:
        abort(400)

    return_data = {'subject': subject, 'code': 'SUCCESS'}
    return return_data, 200, headers #make_response(jsonify(return_data), 200)