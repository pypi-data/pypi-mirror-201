from lxml import etree, objectify

from gdshoplib.apps.platforms.base import Platform
from gdshoplib.core.settings import ProductSettings
from gdshoplib.packages.feed import Feed
from gdshoplib.services.notion.database import Database


class YandexMarketManager(Platform, Feed):
    KEY = "YM"

    def get_categories(self):
        categories = Database(ProductSettings().CATEGORY_DB).pages()
        return [(i.id, i.title) for i in categories]

    def get_shop(self):
        shop = objectify.Element("shop")

        shop.name = self.feed_settings.SHOP_NAME
        shop.company = self.feed_settings.COMPANY_NAME
        shop.url = self.feed_settings.SHOP_URL

        currencies = objectify.Element("currencies")
        currency = etree.Element("currency")
        currency.attrib["id"] = "RUB"
        currency.attrib["rate"] = "1"
        objectify.deannotate(currency, cleanup_namespaces=True, xsi_nil=True)
        objectify.deannotate(currencies, cleanup_namespaces=True, xsi_nil=True)
        currencies.append(currency)
        shop.currencies = currencies

        categories = objectify.Element("categories")
        for ind, k in enumerate(
            ["Все товары", "Спорт и отдых", "Конный спорт"], start=1
        ):
            category = etree.Element("category")
            category.attrib["id"] = str(ind)
            if ind - 1 != 0:
                category.attrib["parentId"] = str(ind - 1)
            category.text = k
            categories.append(category)

        for _id, name in self.get_categories():
            category = etree.Element("category")
            category.attrib["id"] = _id
            category.attrib["parentId"] = "3"
            category.text = name
            objectify.deannotate(category, cleanup_namespaces=True, xsi_nil=True)
            categories.append(category)

        shop.categories = categories
        objectify.deannotate(shop, cleanup_namespaces=True, xsi_nil=True)

        return shop

    def get_offer(self, product):
        appt = objectify.Element("offer")
        appt.attrib["id"] = product.sku
        appt.count = product.quantity
        if product.quantity == 0:
            appt.attrib["type"] = "on.demand"

        appt.currencyId = "RUB"
        appt.price = product.price.now
        if self.get_old_price(product):
            appt.oldprice = self.get_old_price(product)

        for image in product.images:
            appt.addattr("picture", self.get_media_url(image))

        appt.name = product.name
        appt.description = product.description.generate(self)
        appt.vendor = product.brand.title
        appt.categoryId = product.categories[0].id
        # appt.vendorCode = ""
        # appt.vat = "VAT_20"
        # appt.model = ""
        # appt.shipmentoptions = ""

        # param

        # appt.barcode = ""
        # appt.dimensions = ""
        # appt.weight = ""
        # appt.country_of_origin = ""
        # appt.vendorCode = ""
        # appt.url = ""

        objectify.deannotate(appt, cleanup_namespaces=True, xsi_nil=True)
        return appt
