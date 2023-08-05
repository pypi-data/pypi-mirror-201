import json
import validators

from ._odata_filter import _compose_select
from .guardpoint_dataclasses import Card, Cardholder
from .guardpoint_error import GuardPointError


class CardsAPI:
    def get_cards(self, count=False):
        url = "/odata/API_Cards"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        if count:
            url += "?$count=true&$top=0"

        code, json_body = self.gp_json_query("GET", headers=headers, url=url)

        if code != 200:
            if isinstance(json_body, dict):
                if 'error' in json_body:
                    raise GuardPointError(json_body['error'])

        if not isinstance(json_body, dict):
            raise GuardPointError("Badly formatted response.")
        if 'value' not in json_body:
            raise GuardPointError("Badly formatted response.")
        if not isinstance(json_body['value'], list):
            raise GuardPointError("Badly formatted response.")

        if count:
            return json_body['@odata.count']

        cards = []
        for x in json_body['value']:
            cards.append(Card(x))
        return cards

    def delete_card(self, card: Card):
        if not validators.uuid(card.uid):
            raise ValueError(f'Malformed Card UID {card.uid}')

        url = "/odata/API_Cards"
        url_query_params = "(" + card.uid + ")"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        code, json_body = self.gp_json_query("DELETE", headers=headers, url=(url + url_query_params))

        if code != 204:  # HTTP NO_CONTENT
            try:
                if 'error' in json_body:
                    raise GuardPointError(json_body['error'])
                else:
                    raise GuardPointError(str(code))
            except Exception:
                raise GuardPointError(str(code))

        return True

    def update_card(self, card: Card):
        if not validators.uuid(card.uid):
            raise ValueError(f'Malformed Card UID {card.uid}')

        url = "/odata/API_Cards"
        url_query_params = f"({card.uid})"

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            # 'IgnoreNonEditable': ''
        }

        ch = card.dict(changed_only=True)

        code, json_body = self.gp_json_query("PATCH", headers=headers, url=(url + url_query_params), json_body=ch)

        if code != 204:  # HTTP NO_CONTENT
            if 'error' in json_body:
                raise GuardPointError(json_body['error'])
            elif 'message' in json_body:
                raise GuardPointError(json_body['message'])
            else:
                raise GuardPointError(str(code))

        return True

    def new_card(self, card: Card):
        url = "/odata/API_Cards"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        body = card.dict(editable_only=True)

        code, json_body = self.gp_json_query("POST", headers=headers, url=url, json_body=body)

        if code == 201:  # HTTP CREATED
            return Card(json_body)
        else:
            if "errorMessages" in json_body:
                raise GuardPointError(json_body["errorMessages"][0]["other"])
            elif "message" in json_body:
                raise GuardPointError(json_body['message'])
            else:
                raise GuardPointError(str(code))

    def get_card(self, card_uid: str):
        url = "/odata/API_Cards"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        url_query_params = f"({card_uid})"

        code, json_body = self.gp_json_query("GET", headers=headers, url=(url + url_query_params))

        if code != 200:
            if isinstance(json_body, dict):
                if 'error' in json_body:
                    raise GuardPointError(json_body['error'])
            else:
                raise GuardPointError(str(code))

        # Check response body is formatted as expected
        if not isinstance(json_body, dict):
            raise GuardPointError("Badly formatted response.")
        if 'value' not in json_body:
            raise GuardPointError("Badly formatted response.")

        return Card(json_body['value'])

    def get_cardholder_by_card_code(self, card_code):
        url = "/odata/API_Cards"
        filter_str = f"?$filter=cardcode%20eq%20'{card_code}'%20and%20status%20eq%20'Used'%20&"
        url_query_params = f"{filter_str}" \
                           f"$expand=cardholder(" \
                           "$expand=securityGroup($select=name)," \
                           "cardholderType($select=typeName)," \
                           "cards," \
                           "cardholderPersonalDetail," \
                           "cardholderCustomizedField," \
                           "securityGroup," \
                           "insideArea)" \

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        code, json_body = self.gp_json_query("GET", headers=headers, url=(url + url_query_params))

        if code != 200:
            if isinstance(json_body, dict):
                if 'error' in json_body:
                    raise GuardPointError(json_body['error'])

        if not isinstance(json_body, dict):
            raise GuardPointError("Badly formatted response.")
        if 'value' not in json_body:
            raise GuardPointError("Badly formatted response.")
        if not isinstance(json_body['value'], list):
            raise GuardPointError("Badly formatted response.")

        card_holders = []
        for x in json_body['value']:
            if 'cardholder' in x:
                card_holders.append(Cardholder(x['cardholder']))

        if len(card_holders) > 0:
            return card_holders[0]
        else:
            raise GuardPointError("No Cardholder Found")
