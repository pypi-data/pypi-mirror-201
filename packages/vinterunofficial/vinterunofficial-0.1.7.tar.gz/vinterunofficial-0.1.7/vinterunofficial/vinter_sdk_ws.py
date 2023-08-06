import websocket
from .utils import VinterUrl

class VinterAPIWS:
    def __init__(self, symbol, token, asset_type, on_message, on_error, on_close, on_open):
        '''The function takes in a symbol, token, asset type, and four callback functions. It then creates
        a websocket connection to the url for the symbol and asset type.
        
        Parameters
        ----------
        symbol
            The symbol you want to subscribe to.
        token
            Your API token.
        asset_type
            The asset type of the symbol.
        on_message
            This is the callback function that will be called when a message is received from the server.
        on_error
            This is a callback function that will be called when an error occurs.
        on_close
            A function that will be called when the websocket is closed.
        on_open
            This is a callback function that will be called when the connection is opened.
        
        '''
        self.ws = None
        self.symbol = symbol
        self.token = token
        self.asset_type = asset_type
        self.url = self.get_ws_url() + "/?token=" + self.token
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close
        self.on_open = on_open

    def get_ws_url(self):
        '''It takes the asset type and symbol and returns the websocket url
        
        Returns
        -------
            The websocket url for the asset type and symbol.
        
        '''
        return VinterUrl.websocket_url(self.asset_type, self.symbol)

    def open(self):
        '''The function opens a websocket connection to the url specified in the constructor
        
        '''
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open,
        )
        self.ws.run_forever()

    def close(self):
        '''The function closes the websocket connection
        
        '''
        self.ws.close()

