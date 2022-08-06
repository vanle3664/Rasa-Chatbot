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
import pandas as pd

from sqlalchemy import true

product_data = pd.read_csv("./product.csv")


def product_avail(id, color):
    for i in range(0, product_data.shape[0]):
        p = product_data.iloc[i]
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
                    print(color)
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
                    mess = "Bên em hiện tại đang hết màu " + color + \
                        ", anh/chị có thể cân nhắc màu khác ạ!"

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
                    for i in range(0, product_data.shape[0]):
                        p = product_data.iloc[i]
                        if p["id"] == prod_id:
                            mess = p["name"] + "-" + p["id"] + \
                                " bên em đang bán chỉ " + str(p["price"])

        dispatcher.utter_message(text=mess)
        return []


class ActionSize(Action):

    def name(self) -> Text:
        return "action_size"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message["entities"]
        print(entities)

        if entities != []:
            height = 0
            weight = 0
            for e in entities:
                if e["entity"] == "height":
                    height = float(e["value"])
                    print(height)
                else:
                    weight = int(e["value"])
            if weight == 0 or height == 0:
                mess = "Chưa nhận được thông tin của anh chị, vui lòng kiểm tra và nhập lại giùm shop ạ!"
            elif height < 1.55 and weight < 50:
                mess = "Size S sẽ phù hợp nhất với anh/chị ạ!"
            elif height < 1.67 and weight < 60:
                mess = "Size M sẽ phù hợp nhất với anh/chị ạ!"
            else:
                mess = "Size L sẽ phù hợp nhất với anh/chị ạ!"
        else:
            mess = "Bên shop có đủ các size S M L cho các mẫu. Anh chị muốn tư vấn cụ thể cho shop xin cân nặng và chiều cao ạ! (Ví dụ: cao 1.65 nặng 47)"

        dispatcher.utter_message(text=mess)

        return []


class ActionReceiveInfo(Action):

    def name(self) -> Text:
        return "action_receive_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message["entities"]
        print(entities)
        print("NO")

        mess = "Anh/chị nhập giùm shop tên và số điện thoại ạ!"

        if entities != None:
            name = ""
            phone = ""
            for e in entities:
                if e["entity"] == "customer_name":
                    name = e["value"]
                    print(name)
                else:
                    phone = e["value"]
            if phone == "" or name == "":
                mess = "Shop chưa nhận được thông tin của anh chị, vui lòng kiểm tra và nhập lại giùm shop tên và số điện thoại ạ!"
            else:
                mess = "Cảm ơn anh/chị " + name + \
                    " đã đặt hàng, shop sẽ gọi lại chốt đơn chậm nhất là trong ngày mai! Anh/chị để ý điện thoại giùm shop nhé!"

        dispatcher.utter_message(text=mess)

        return []
