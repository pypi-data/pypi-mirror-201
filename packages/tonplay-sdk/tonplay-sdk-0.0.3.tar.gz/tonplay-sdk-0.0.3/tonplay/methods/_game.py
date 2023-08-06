

def make_payout_request(self, payout_id):
    """
        Make payout request

        POST /gamecenter/v1/payout

        How it works:

        Your project has own built-in wallet inside TONPLAY.
        Your project need to have 'payout-verify-endpoint' inside TONPLAY platform that must return
        { amount: float, address: str } by requested payout_id

        You can make auto-withdraw from built-in wallet over API request by next logic:

        - create withdraw request in your database per each user
        - pass ID of this request into our API (this method)
        - TONPLAY will make verify request on your verify URL for check is this valid withdraw or not
        - if your API answer is OK than TONPLAY will send requested TON amount to selected address

        Args:
            payout_id (str) : payout_id from your system in any format
    """

    url_path = f"/gamecenter/v1/payout"
    payload = {"payoutId": payout_id}
    return self.send_request("POST", url_path, payload=payload)
