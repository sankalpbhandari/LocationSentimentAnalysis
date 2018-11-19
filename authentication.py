class Authentication:
    def __init__(self):
        self.consumer_key = ""
        self.consumer_secret = ""
        self.access_token = ""
        self.access_token_secret = ""
        self.google_key = ""

    def get_consumer_key(self):
        return self.consumer_key

    def get_consumer_secret(self):
        return self.consumer_secret

    def get_access_token_secret(self):
        return self.access_token_secret

    def get_access_token(self):
        return self.access_token

    def get_google_key(self):
        return self.google_key

