from twelvelabs import TwelveLabs


API_KEY = 'tlk_3S704BN3DPGHXA2M6201F17FBQR5'

client = TwelveLabs(api_key=API_KEY)
engines = client.engine.list()
print(engines)
