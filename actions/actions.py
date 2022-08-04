# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
from html import entities

from sqlalchemy import true
product = [{"id": "mk1", "name": "áo trái tim", "color": "xanh", "stock": 0, "price": "150 000"},
           {"id": "mk1", "name": "áo trái tim", "color": "đỏ", "stock": 2, "price": "150 000"},
           {"id": "mk1", "name": "áo trái tim", "color": "tím", "stock": 2, "price": "150 000"},
           {"id": "mk1", "name": "áo trái tim", "color": "vàng", "stock": 2, "price": "150 000"},
           {"id": "mk2", "name": "áo cô gái", "color": "xanh", "stock": 2, "price": "150 000"},
           {"id": "mk2", "name": "áo cô gái", "color": "đỏ", "stock": 2, "price": "150 000"},
           {"id": "mk2", "name": "áo cô gái", "color": "tím", "stock": 2, "price": "150 000"},
           {"id": "mk2", "name": "áo cô gái", "color": "vàng", "stock": 2, "price": "150 000"},
           {"id": "mk3", "name": "áo bọt biển", "color": "xanh", "stock": 2, "price": "150 000"},
           {"id": "mk3", "name": "áo bọt biển", "color": "đỏ", "stock": 0, "price": "150 000"},
           {"id": "mk3", "name": "áo bọt biển", "color": "tím", "stock": 0, "price": "150 000"},
           {"id": "mk3", "name": "áo bọt biển", "color": "vàng", "stock": 0, "price": "150 000"},
           {"id": "mk4", "name": "áo cây dừa", "color": "xanh", "stock": 9, "price": "150 000"},
           {"id": "mk4", "name": "áo cây dừa", "color": "đỏ", "stock": 7, "price": "150 000"},
           {"id": "mk4", "name": "áo cây dừa", "color": "tím", "stock": 0, "price": "150 000"},
           {"id": "mk4", "name": "áo cây dừa", "color": "vàng", "stock": 0, "price": "150 000"},
           ]
def product_avail(id, color):
    for p in product:
        if p["id"] == id and p["color"] == color:
            if p["stock"] > 0:
                return 1
            else:
                return 0


class ActionColorAsk(Action):

    def name(self) -> Text:
        return "action_color"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message["entities"]
        print(entities)

        mess = "Các sản phẩm bên em có đủ màu xanh, đỏ, tím, vàng. Để biết chi tiết cho từng mẫu, anh/chị cho em xin mã sản phẩm và màu sắc ạ!"
        if entities != None:
            color = ""
            prod_id = ""
            for e in entities:
                if e["entity"] == "color":
                    color = e["value"]
                    print (color)
                else:
                    prod_id = e["value"]
                    
                # if color == None:
                #     mess = "Bên em có đủ màu xanh, đỏ, tím, vàng ạ!"
                # if color in ["đỏ", "tím", "xanh"]:
                #     mess = "Bên em còn màu " + color + " nhé ạ!"
                # if color == "vàng":
                #     mess = "Bên em hiện tại đang hết màu vàng, anh/chị có thể cân nhắc màu khác ạ!"
            if prod_id == "" or color == "": 
                mess = "Mã sản phẩm hoặc màu sắc không có, anh/chị kiểm tra lại giùm shop ạ!"
            else:   
                res = product_avail(prod_id, color)
                if res == 1:
                    mess = "Bên em còn màu " + color + " nhé ạ!"
                else:
                    mess = "Bên em hiện tại đang hết màu " + color +", anh/chị có thể cân nhắc màu khác ạ!"

        dispatcher.utter_message(text=mess)
        return []


class ActionPrice(Action):

    def name(self) -> Text:
        return "action_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message["entities"]
        print(entities)

        mess = "Giá áo bên shop rẻ nhất thị trường chỉ từ 100k đến 300k. Anh chị muốn biết giá cụ thể cho từng sản phẩm vui lòng cho shop mã sản phẩm nhé ạ!"
        if entities != None:
            for e in entities:
                if e["entity"] == "product_id":
                    prod_id = e["value"]
                    for p in product:
                        if p["id"] == prod_id:
                            mess = p["name"] + "-" + p["id"] + " bên em đang bán chỉ " + p["price"]
                    

        dispatcher.utter_message(text=mess)
        return []