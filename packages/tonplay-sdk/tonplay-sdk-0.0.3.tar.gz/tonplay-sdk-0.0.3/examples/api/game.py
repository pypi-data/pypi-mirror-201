import uuid

from examples.utils.prepare_env import get_api_key
from tonplay.methods import TonPlayApi

client = TonPlayApi(api_key=get_api_key())

payout_id = str(uuid.uuid4())
print(
    client.make_payout_request(payout_id)
)