import random
import string
import requests
import csv
from datetime import datetime, timedelta
from pydantic import HttpUrl
from common import settings as s
from common import pyd_models as pyd


def random_ipv4():
    return "{}.{}.{}.{}".format(
        str(random.randint(0, 256)),
        str(random.randint(0, 256)),
        str(random.randint(0, 256)),
        str(random.randint(0, 256)),
    )


def random_datetime():
    min_date = datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0)
    max_date = datetime.now()
    delta = max_date - min_date
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return min_date + timedelta(seconds=random_second)


def random_hex():
    return random.choice(string.digits + "ABCDEF")


def random_example_ipv6():
    return "2001:DB8::{}{}{}{}".format(
        random_hex(), random_hex(), random_hex(), random_hex()
    )


def get_fqdn_from_url(url: pyd.Url):
    fqdn = url.url.split("//")[1].split("/")[0]
    return fqdn


def random_tld():
    with open("common/top200_tlds.csv", "r") as file:
        reader = csv.reader(file)
        tld_dist = [(row[0], int(row[1])) for row in reader]
        tlds, dist = map(list, zip(*tld_dist))

    return random.choices(population=tlds, weights=dist, k=1)[0]


def get_random_fqdn():
    return "www." + random_sld() + "." + random_tld()


def generate_random_url(fqdn=None) -> pyd.Url:
    applied_fqdn = get_random_fqdn() if fqdn is None else fqdn
    return pyd.Url(
        url="http://{}/{}{}".format(
            applied_fqdn, get_random_german_text(), get_random_web_filename()
        ),
        fqdn=applied_fqdn,
        url_pagerank=random_pagerank(),
        url_discovery_date=datetime.now(),
    )


def get_random_existing_url(session: requests.Session, fqdn: str = None) -> pyd.Url:
    if fqdn is None:
        random_url = session.get(s.websch_random_urls_endpoint).json()

    else:
        random_url = session.get(
            "{}?fqdn={}".format(s.websch_random_urls_endpoint, fqdn)
        ).json()

    if len(random_url["url_list"]) == 0:
        new_url = generate_random_url()
        random_url["url_list"].append(dict(url=new_url.url, fqdn=new_url.fqdn))

    return pyd.Url(
        url=random_url["url_list"][0]["url"], fqdn=random_url["url_list"][0]["fqdn"]
    )


def get_similar_url(url: pyd.Url) -> pyd.Url:
    fqdn = get_fqdn_from_url(url)
    return generate_random_url(fqdn=fqdn)


def get_random_web_filename():
    file = random.choice(["/index", "/home", "/impressum", "/contact"])
    extension = random.choice([".php", ".html", ".aspx", "", "/"])
    return file + extension


def random_sld():
    first_char = random.choice(string.ascii_lowercase)
    random_allowed_characters = string.ascii_lowercase + "0123456789-"
    last_char = random.choice(random_allowed_characters[:-1])
    sld = (
        first_char
        + "".join(
            random.choice(random_allowed_characters)
            for _ in range(random.randint(8, 15) - 1)
        )
        + last_char
    )
    return sld


def get_random_german_text(length: int = None):
    chars = [
        "e",
        "n",
        "i",
        "s",
        "r",
        "a",
        "t",
        "d",
        "h",
        "u",
        "l",
        "c",
        "g",
        "m",
        "o",
    ]
    distribution = [
        0.1740,
        0.0978,
        0.0755,
        0.0758,
        0.0700,
        0.0651,
        0.0615,
        0.0508,
        0.0476,
        0.0435,
        0.0344,
        0.0306,
        0.0301,
        0.0253,
        0.0251,
    ]

    if length is None:
        length = random.randint(10, 16)

    return "".join(random.choices(population=chars, weights=distribution, k=length))


def random_pagerank(rank: int = random.randint(0, 60000000000)):
    if rank <= 10:
        random_pagerank = random.uniform(8.0, 10.0)
    elif rank <= 100:
        random_pagerank = random.uniform(4.0, 8.0)
    elif rank <= 1000:
        random_pagerank = random.uniform(2.0, 4.0)
    elif rank <= 10000:
        random_pagerank = random.uniform(1.0, 2.0)
    elif rank <= 100000:
        random_pagerank = random.uniform(0.2, 1.0)
    elif rank <= 1000000:
        random_pagerank = random.uniform(0.01, 0.2)
    elif rank <= 10000000:
        random_pagerank = random.uniform(0.001, 0.01)
    elif rank <= 100000000:
        random_pagerank = random.uniform(0.0001, 0.001)
    elif rank <= 1000000000:
        random_pagerank = random.uniform(0.00001, 0.0001)
    else:
        random_pagerank = random.uniform(0.0, 0.00001)

    return random_pagerank


def random_crawl_delay():
    crawl_delays = [
        None,
        1,
        2,
        3,
        5,
        10,
        15,
        20,
        30,
        45,
        50,
        60,
        120,
        200,
        300,
        600,
        1000,
    ]
    distibution = [
        0.80000,
        0.00800,
        0.00450,
        0.00450,
        0.01950,
        0.05400,
        0.00450,
        0.01900,
        0.01500,
        0.00800,
        0.00100,
        0.01800,
        0.00800,
        0.00450,
        0.00300,
        0.00150,
        0.00080,
    ]

    return random.choices(population=crawl_delays, weights=distibution)[0]
