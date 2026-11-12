"""Fixed option sets, taken from 'Eupepsia Timeless Collection Prices, Sizes, Colors.xlsx'.
Prices in USD. Edit here when the line sheet changes.
`type` groups garments for the order form; `variant` distinguishes styles within a type (None when a type has one style)."""

from __future__ import annotations

from enum import Enum


class Fabric(str, Enum):
    COTTON = "cotton"  # 100% Combed Cotton, Maurice Brassard
    WOOL = "wool"      # 100% Extra Fine Merino, Zegna Baruffa Cashwool


class Size(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
    ONE = "One Size"


class Status(str, Enum):
    # Declaration order is the workflow order; sorting by status follows it (see STATUS_RANK).
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


STATUS_RANK = {s.value: i for i, s in enumerate(Status)}


class Style(str, Enum):
    # cotton
    CT_TOP_25_SS = "HBS-CT-T25S"
    CT_TUNIC_30_SS = "HBS-CT-TC30S"
    CT_TUNIC_30_LS = "HBS-CT-TC30L"
    CT_TUNIC_ALINE_30_LS = "HBS-CT-TCA30L"
    CT_DRESS_37_SS = "HBS-CT-D37S"
    CT_DRESS_ALINE_37_LS = "HBS-CT-A37L"
    CT_CARDIGAN_31 = "HBS-CT-C31"
    CT_CARDIGAN_38 = "HBS-CT-C38"
    CT_HOODIE = "HBS-CT-HOOD"
    CT_PANTS_WIDE = "HBS-CT-PANW"
    CT_PANTS_JOGGER = "HBS-CT-PANJ"
    CT_SHAWL_JERSEY_LONG = "HBS-CT-SHJL"
    CT_SHAWL_JERSEY_SHORT = "HBS-CT-SHJS"
    CT_SHAWL_BIRDSEYE_LONG = "HBS-CT-SHBL"
    CT_SHAWL_BIRDSEYE_SHORT = "HBS-CT-SHBS"
    # wool
    WL_TUNIC_30_LS = "HBS-WL-TC30L"
    WL_TUNIC_ALINE_30_LS = "HBS-WL-TCA30L"
    WL_DRESS_37_LS = "HBS-WL-D37L"
    WL_DRESS_ALINE_37_LS = "HBS-WL-A37L"
    WL_CARDIGAN_31 = "HBS-WL-C31"
    WL_HOODIE = "HBS-WL-HOOD"
    WL_PANTS_WIDE = "HBS-WL-PANW"
    WL_PANTS_JOGGER = "HBS-WL-PANJ"
    WL_SHAWL_JERSEY = "HBS-WL-SHJ"
    WL_BEANIE = "HBS-WL-B"


GARMENT_SIZES = [Size.XS, Size.S, Size.M, Size.L, Size.XL, Size.XXL]
UNI_SIZE = [Size.ONE]

# length: body length from the line sheet; shawls are length × width from the size guide. None where unknown.
PRODUCTS: dict[Style, dict] = {
    Style.CT_TOP_25_SS: dict(type="Top", variant="Short sleeve", length='25"', name="Top, straight — short sleeve", fabric=Fabric.COTTON, sizes=GARMENT_SIZES, price=170),
    Style.CT_TUNIC_30_SS: dict(type="Tunic", variant="Straight, short sleeve", length='30"', name="Tunic, straight — short sleeve", fabric=Fabric.COTTON, sizes=GARMENT_SIZES, price=188),
    Style.CT_TUNIC_30_LS: dict(type="Tunic", variant="Straight, long sleeve", length='30"', name="Tunic, straight — long sleeve", fabric=Fabric.COTTON, sizes=GARMENT_SIZES, price=197),
    Style.CT_TUNIC_ALINE_30_LS: dict(type="Tunic", variant="A-line, long sleeve", length='30"', name="Tunic, A-line — long sleeve", fabric=Fabric.COTTON, sizes=GARMENT_SIZES, price=206),
    Style.CT_DRESS_37_SS: dict(type="Dress", variant="Straight, short sleeve", length='37"', name="Dress, straight — short sleeve", fabric=Fabric.COTTON, sizes=GARMENT_SIZES, price=233),
    Style.CT_DRESS_ALINE_37_LS: dict(type="Dress", variant="A-line, long sleeve", length='37"', name="Dress, A-line — long sleeve", fabric=Fabric.COTTON, sizes=GARMENT_SIZES, price=242),
    Style.CT_CARDIGAN_31: dict(type="Cardigan", variant=None, length='31"', name="Cardigan", fabric=Fabric.COTTON, sizes=GARMENT_SIZES, price=206),
    Style.CT_CARDIGAN_38: dict(type="Cardigan", variant=None, length='38"', name="Cardigan", fabric=Fabric.COTTON, sizes=GARMENT_SIZES, price=242),
    Style.CT_HOODIE: dict(type="Hoodie", variant=None, length=None, name="Hoodie", fabric=Fabric.COTTON, sizes=GARMENT_SIZES, price=260),
    Style.CT_PANTS_WIDE: dict(type="Pants", variant="Wide leg", length=None, name="Pants, wide leg", fabric=Fabric.COTTON, sizes=GARMENT_SIZES, price=224),
    Style.CT_PANTS_JOGGER: dict(type="Pants", variant="Jogger", length=None, name="Pants, jogger", fabric=Fabric.COTTON, sizes=GARMENT_SIZES, price=224),
    Style.CT_SHAWL_JERSEY_LONG: dict(type="Shawl", variant="Jersey, long", length='106 × 38"', name="Shawl, jersey — long", fabric=Fabric.COTTON, sizes=UNI_SIZE, price=296),
    Style.CT_SHAWL_JERSEY_SHORT: dict(type="Shawl", variant="Jersey, short", length='80 × 35"', name="Shawl, jersey — short", fabric=Fabric.COTTON, sizes=UNI_SIZE, price=197),
    Style.CT_SHAWL_BIRDSEYE_LONG: dict(type="Shawl", variant="Bird's eye, long", length='106 × 38"', name="Shawl, bird's eye — long", fabric=Fabric.COTTON, sizes=UNI_SIZE, price=296),
    Style.CT_SHAWL_BIRDSEYE_SHORT: dict(type="Shawl", variant="Bird's eye, short", length='80 × 35"', name="Shawl, bird's eye — short", fabric=Fabric.COTTON, sizes=UNI_SIZE, price=197),
    Style.WL_TUNIC_30_LS: dict(type="Tunic", variant="Straight, long sleeve", length='30"', name="Tunic, straight — long sleeve", fabric=Fabric.WOOL, sizes=GARMENT_SIZES, price=278),
    Style.WL_TUNIC_ALINE_30_LS: dict(type="Tunic", variant="A-line, long sleeve", length='30"', name="Tunic, A-line — long sleeve", fabric=Fabric.WOOL, sizes=GARMENT_SIZES, price=278),
    Style.WL_DRESS_37_LS: dict(type="Dress", variant="Straight, long sleeve", length='37"', name="Dress, straight — long sleeve", fabric=Fabric.WOOL, sizes=GARMENT_SIZES, price=305),
    Style.WL_DRESS_ALINE_37_LS: dict(type="Dress", variant="A-line, long sleeve", length='37"', name="Dress, A-line — long sleeve", fabric=Fabric.WOOL, sizes=GARMENT_SIZES, price=314),
    Style.WL_CARDIGAN_31: dict(type="Cardigan", variant=None, length='31"', name="Cardigan", fabric=Fabric.WOOL, sizes=GARMENT_SIZES, price=251),
    Style.WL_HOODIE: dict(type="Hoodie", variant=None, length=None, name="Hoodie", fabric=Fabric.WOOL, sizes=GARMENT_SIZES, price=278),
    Style.WL_PANTS_WIDE: dict(type="Pants", variant="Wide leg", length=None, name="Pants, wide leg", fabric=Fabric.WOOL, sizes=GARMENT_SIZES, price=260),
    Style.WL_PANTS_JOGGER: dict(type="Pants", variant="Jogger", length=None, name="Pants, jogger", fabric=Fabric.WOOL, sizes=GARMENT_SIZES, price=260),
    Style.WL_SHAWL_JERSEY: dict(type="Shawl", variant="Jersey", length='80 × 35"', name="Shawl, jersey", fabric=Fabric.WOOL, sizes=UNI_SIZE, price=287),
    Style.WL_BEANIE: dict(type="Beanie", variant=None, length=None, name="Beanie", fabric=Fabric.WOOL, sizes=UNI_SIZE, price=71),
}


class CottonColour(str, Enum):
    """value = Maurice Brassard code"""
    PALE_ROSE = "C1768"
    MAGENTA = "5214"
    LILAC = "1507"
    PALE_GREEN = "1831"
    BLUE = "4272"
    EMERALD = "5506"
    PEACOCK = "4616"
    TURQUOISE = "1510"
    AQUAMARINE = "5206"
    SIERRA = "1391"
    MEDIUM_BROWN = "1313"


class WoolColour(str, Enum):
    """value = six-digit Zegna Baruffa mill code"""
    TANGIBLE_BEIGE = "029293"
    M_LEGNO_CH = "420938"
    M_AZZUR_MB = "421225"
    GLICINE = "029277"
    MALVA = "028775"
    AVIO_CH_1 = "027047"
    AVIO_CH_2 = "028384"
    OCEANO = "029278"
    BLU_ELETTRICO = "028780"
    ROYAL_MED = "118206"
    AVIAZIONE_SC = "028156"
    VERDE_SC = "156277"
    SALVIA_CH = "028776"
    SALVIA = "029271"
    ACCIAIO = "028995"
    LAGO = "029779"
    VERDE_BOSCO = "028125"
    NERO_70 = "099070"
    M_TABACCO = "442841"
    M_NOCE_SC = "441316"
    CAROTA = "028772"
    MATTONE = "029274"
    ROSSO = "008768"
    BORDO_MED = "000527"
    VINACCIA = "028332"
    AZALEA = "029777"


COLOURS: dict[Fabric, type[Enum]] = {Fabric.COTTON: CottonColour, Fabric.WOOL: WoolColour}

# Swatch approximations sampled from the mill colour cards (screen only; match to a physical card).
COLOUR_HEX: dict[str, str] = {
    "C1768": "#CDA5A2",
    "5214": "#8B3E6B",
    "1507": "#9A808E",
    "1831": "#9AC7AD",
    "4272": "#5674C8",
    "5506": "#469264",
    "4616": "#3B8698",
    "1510": "#529F8B",
    "5206": "#387E75",
    "1391": "#7D5733",
    "1313": "#5F3F23",
    "029293": "#EDE7CB",
    "420938": "#D1C0A9",
    "421225": "#829CBB",
    "029277": "#BBA5C3",
    "028775": "#9A8A93",
    "027047": "#687F8A",
    "028384": "#425C7B",
    "029278": "#065D81",
    "028780": "#0E2460",
    "118206": "#151D3F",
    "028156": "#3D4B55",
    "156277": "#1A2425",
    "028776": "#949E9B",
    "029271": "#7D827D",
    "028995": "#6C706F",
    "029779": "#5A6565",
    "028125": "#232823",
    "099070": "#0C1115",
    "442841": "#705F50",
    "441316": "#564D44",
    "028772": "#B02E13",
    "029274": "#7D2B2D",
    "008768": "#88041A",
    "000527": "#481320",
    "028332": "#4D3745",
    "029777": "#612849",
}


def colour_label(member: Enum) -> str:
    return member.name.replace("_", " ").title()


def styles_matching(type: str | None = None, fabric: str | None = None) -> list[str]:
    """Style codes for a garment type and/or fabric (both optional)."""
    return [
        s.value for s, p in PRODUCTS.items()
        if (type is None or p["type"] == type) and (fabric is None or p["fabric"].value == fabric)
    ]


def catalogue_json() -> dict:
    """Everything the order form needs to render its dropdowns."""
    return {
        "products": [
            {"style": s.value, "name": p["name"], "type": p["type"], "variant": p["variant"], "length": p["length"],
             "fabric": p["fabric"].value, "sizes": [z.value for z in p["sizes"]], "price": p["price"]}
            for s, p in PRODUCTS.items()
        ],
        "colours": {
            f.value: [{"code": c.value, "name": colour_label(c), "hex": COLOUR_HEX[c.value]} for c in enum]
            for f, enum in COLOURS.items()
        },
        "statuses": [s.value for s in Status],
    }
