from os import environ
from EXAM import create_app

app = create_app()

import os

port = int(os.environ.get("PORT", 5050)) 

if __name__ == '__main__':
   
   app.run(debug=True, port=port, host='0.0.0.0')

    # app.run(debug=True, host='0.0.0.0:5000')

# if __name__ == '__main__':
#     HOST = environ.get('SERVER_HOST', 'localhost')
#     try:
#         PORT = int(environ.get('SERVER_PORT', '5555'))
#     except ValueError:
#         PORT = 5555
#     app.run(HOST, PORT,debug=True)
#     print("server started")
