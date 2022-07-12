import tekore as tk

def authorize():
 CLIENT_ID = "483c9c5153594b66b3816ec8a40777fd"
 CLIENT_SECRET = "36537ca720244c34a9172bd752a87e69"
 app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
 return tk.Spotify(app_token)
