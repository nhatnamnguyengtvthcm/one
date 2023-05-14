from django.core.management.base import BaseCommand

from one.masterdata.uom.models import UOM


class Command(BaseCommand):
    help = "Create UOM objects"
    uom_data = {
        "CREATIVE": [
            {"code": "UOM_PIECE", "name": "Sản phẩm"},
            {"code": "UOM_SECTION", "name": "Buổi"},

            {"code": "UOM_WORD", "name": "Chữ"},

            {"code": "UOM_POST_LOWER_300", "name": "Bài dưới 300 chữ", "base_uom": "UOM_WORD"},
            {"code": "UOM_POST_301_500", "name": "Bài 301 - 500 chữ", "base_uom": "UOM_WORD"},
            {"code": "UOM_POST_501_700", "name": "Bài 501 - 700 chữ", "base_uom": "UOM_WORD"},
            {"code": "UOM_POST_701_900", "name": "Bài 701 - 900 chữ", "base_uom": "UOM_WORD"},
            {"code": "UOM_POST_901_1000", "name": "Bài 901 - 1000 chữ", "base_uom": "UOM_WORD"},
            {"code": "UOM_POST_1001_3000", "name": "Bài 1001 - 3000 chữ", "base_uom": "UOM_WORD"},
            {"code": "UOM_POST_UPPER_3000", "name": "Bài trên 3000 chữ", "base_uom": "UOM_WORD"},

            # {"code": "UOM_PACK_5_POST_LOWER_300", "name": "5 Bài dưới 300 chữ", "base_uom": "UOM_POST_LOWER_300"},
            # {"code": "UOM_PACK_5_POST_301_500", "name": "5 Bài 301 - 500 chữ", "base_uom": "UOM_POST_301_500"},
            # {"code": "UOM_PACK_5_POST_501_700", "name": "5 Bài 501 - 700 chữ", "base_uom": "UOM_POST_501_700"},
            # {"code": "UOM_PACK_5_POST_701_900", "name": "5 Bài 701 - 900 chữ", "base_uom": "UOM_POST_701_900"},
            # {"code": "UOM_PACK_5_POST_901_1000", "name": "5 Bài 901 - 1000 chữ", "base_uom": "UOM_POST_901_1000"},
            # {"code": "UOM_PACK_5_POST_1001_3000", "name": "5 Bài 1001 - 3000 chữ", "base_uom": "UOM_POST_1001_3000"},
            # {"code": "UOM_PACK_5_POST_UPPER_3000", "name": "5 Bài trên 3000 chữ", "base_uom": "UOM_POST_UPPER_3000"},
            #
            # {"code": "UOM_PACK_10_POST_LOWER_300", "name": "10 Bài dưới 300 chữ", "base_uom": "UOM_POST_LOWER_300"},
            # {"code": "UOM_PACK_10_POST_301_500", "name": "10 Bài 301 - 500 chữ", "base_uom": "UOM_POST_301_500"},
            # {"code": "UOM_PACK_10_POST_501_700", "name": "10 Bài 501 - 700 chữ", "base_uom": "UOM_POST_501_700"},
            # {"code": "UOM_PACK_10_POST_701_900", "name": "10 Bài 701 - 900 chữ", "base_uom": "UOM_POST_701_900"},
            # {"code": "UOM_PACK_10_POST_901_1000", "name": "10 Bài 901 - 1000 chữ", "base_uom": "UOM_POST_901_1000"},
            # {"code": "UOM_PACK_10_POST_1001_3000", "name": "10 Bài 1001 - 3000 chữ", "base_uom": "UOM_POST_1001_3000"},
            # {"code": "UOM_PACK_10_POST_UPPER_3000", "name": "10 Bài trên 3000 chữ", "base_uom": "UOM_POST_UPPER_3000"},

            {"code": "UOM_SECOND", "name": "Giây"},

            {"code": "UOM_SCRIPT_30_45", "name": "Kịch bản 30-45s", "base_uom": "UOM_SECOND"},
            {"code": "UOM_SCRIPT_60", "name": "Kịch bản 60s", "base_uom": "UOM_SECOND"},
            {"code": "UOM_SCRIPT_120", "name": "Kịch bản 120s", "base_uom": "UOM_SECOND"},
            {"code": "UOM_SCRIPT_180", "name": "Kịch bản 180s", "base_uom": "UOM_SECOND"},

            # {"code": "UOM_PACK_5_SCRIPT_30_45", "name": "5 Kịch bản 30-45s", "base_uom": "UOM_SCRIPT_30_45"},
            # {"code": "UOM_PACK_5_SCRIPT_60", "name": "5 Kịch bản 60s", "base_uom": "UOM_SCRIPT_60"},
            # {"code": "UOM_PACK_5_SCRIPT_120", "name": "5 Kịch bản 120s", "base_uom": "UOM_SCRIPT_120"},
            # {"code": "UOM_PACK_5_SCRIPT_180", "name": "5 Kịch bản 180s", "base_uom": "UOM_SCRIPT_180"},
            #
            # {"code": "UOM_PACK_10_SCRIPT_30_45", "name": "10 Kịch bản 30-45s", "base_uom": "UOM_SCRIPT_30_45"},
            # {"code": "UOM_PACK_10_SCRIPT_60", "name": "10 Kịch bản 60s", "base_uom": "UOM_SCRIPT_60"},
            # {"code": "UOM_PACK_10_SCRIPT_120", "name": "10 Kịch bản 120s", "base_uom": "UOM_SCRIPT_120"},
            # {"code": "UOM_PACK_10_SCRIPT_180", "name": "10 Kịch bản 180s", "base_uom": "UOM_SCRIPT_180"},
        ],
    }

    def add_arguments(self, parser):
        parser.add_argument("business_type", choices=["CREATIVE"], help="Business Type", default="creative")

    def handle(self, *args, **options):
        uom_data = self.uom_data["CREATIVE"]
        business_type = options.get("business_type", None)
        if business_type:
            uom_data = self.uom_data[business_type.upper()]
        for uom in uom_data:
            UOM.objects.update_or_create(code=uom["code"], name=uom["name"])
        for uom in uom_data:
            uom_obj = UOM.objects.get(code=uom["code"])
            if uom.get("base_uom", None):
                base_uom = UOM.objects.get(code=uom["base_uom"])
                uom_obj.base_uom = base_uom
                uom_obj.save()
        self.stdout.write(self.style.SUCCESS("Successfully created UOM objects."))
