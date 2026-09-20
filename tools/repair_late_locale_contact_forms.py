#!/usr/bin/env python3
"""Restore localized quote forms on the five remaining late locale pages."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FORM_RE = re.compile(r'(<form class="contact-form"(?:\s|>).*?</form>)', re.DOTALL)
SUCCESS_RE = re.compile(r'(<p id="formSuccess" class="form-success" hidden>).*?(</p>)', re.DOTALL)
MAIN_END = "</main>"

COPY = {
    "be": {
        "Pošalji upit": "Адправіць запыт",
        "Ime": "Імя",
        "Kompanija": "Кампанія",
        "Email": "Электронная пошта",
        "Država": "Краіна",
        "Proizvod": "Прадукт",
        "Količina": "Колькасць",
        "Odredišna luka": "Порт прызначэння",
        "Poruka": "Паведамленне",
        "Please include size, micron rating, flow rate, packaging, logo and certificates needed.":
            "Пазначце памер, мікроннасць, расход, упакоўку, лагатып і патрэбныя сертыфікаты.",
        "success": "Дзякуй. Ваш запыт быў паспяхова адпраўлены ў Yuchen Water. Наш інжынер па продажах звяжацца з вамі як мага хутчэй.",
    },
    "ga": {
        "Pošalji upit": "Seol fiosrúchán",
        "Ime": "Ainm",
        "Kompanija": "Cuideachta",
        "Email": "Ríomhphost",
        "Država": "Tír",
        "Proizvod": "Táirge",
        "Količina": "Cainníocht",
        "Odredišna luka": "Calafort cinn scríbe",
        "Poruka": "Teachtaireacht",
        "Please include size, micron rating, flow rate, packaging, logo and certificates needed.":
            "Cuir méid, rátáil micron, ráta sreafa, pacáistiú, lógó agus deimhnithe san áireamh.",
        "success": "Go raibh maith agat. Seoladh d’fhiosrúchán chuig Yuchen Water. Rachaidh ár n-innealtóir díolacháin i dteagmháil leat chomh luath agus is féidir.",
    },
    "lb": {
        "Pošalji upit": "Ufro schécken",
        "Ime": "Numm",
        "Kompanija": "Firma",
        "Email": "E-Mail",
        "Država": "Land",
        "Proizvod": "Produkt",
        "Količina": "Quantitéit",
        "Odredišna luka": "Destinatiounshafen",
        "Poruka": "Noriicht",
        "Please include size, micron rating, flow rate, packaging, logo and certificates needed.":
            "Gitt Gréisst, Mikronwäert, Duerchfloss, Verpakung, Logo an néideg Zertifikater un.",
        "success": "Merci. Är Ufro gouf erfollegräich un Yuchen Water geschéckt. Eise Verkafsingenieur kontaktéiert Iech sou séier wéi méiglech.",
    },
    "mk": {
        "Pošalji upit": "Испрати барање",
        "Ime": "Име",
        "Kompanija": "Компанија",
        "Email": "Е-пошта",
        "Država": "Земја",
        "Proizvod": "Производ",
        "Količina": "Количина",
        "Odredišna luka": "Одредишно пристаниште",
        "Poruka": "Порака",
        "Please include size, micron rating, flow rate, packaging, logo and certificates needed.":
            "Наведете големина, микронска вредност, проток, пакување, лого и потребни сертификати.",
        "success": "Ви благодариме. Вашето барање беше успешно испратено до Yuchen Water. Нашиот продажен инженер ќе ве контактира што е можно поскоро.",
    },
    "mt": {
        "Pošalji upit": "Ibgħat mistoqsija",
        "Ime": "Isem",
        "Kompanija": "Kumpanija",
        "Email": "Email",
        "Država": "Pajjiż",
        "Proizvod": "Prodott",
        "Količina": "Kwantità",
        "Odredišna luka": "Port tad-destinazzjoni",
        "Poruka": "Messaġġ",
        "Please include size, micron rating, flow rate, packaging, logo and certificates needed.":
            "Inkludi d-daqs, il-grad mikron, ir-rata tal-fluss, l-ippakkjar, il-logo u ċ-ċertifikati meħtieġa.",
        "success": "Grazzi. Il-mistoqsija tiegħek intbagħtet b’suċċess lil Yuchen Water. L-inġinier tal-bejgħ tagħna se jikkuntattjak kemm jista’ jkun malajr.",
    },
}


def localized_form(template: str, locale: str) -> str:
    form = template.replace("-cnr", f"-{locale}")
    form = form.replace("/cnr/contact.html", f"/{locale}/contact.html")
    form = form.replace('value="cnr" data-submitted-language',
                        f'value="{locale}" data-submitted-language')
    copy = COPY[locale]
    for source, replacement in copy.items():
        if source != "success":
            form = form.replace(source, replacement)
    success = copy["success"] + " WhatsApp: +86-19908311885 · Email: expresswater025@gmail.com"
    form, count = SUCCESS_RE.subn(r"\1" + success + r"\2", form)
    if count != 1:
        raise ValueError(f"{locale}: expected one success message")
    return form


def transform(target: str, form: str) -> str:
    if FORM_RE.search(target):
        return target
    if target.count(MAIN_END) != 1:
        raise ValueError("contact page must contain exactly one main end tag")
    section = '<section class="tx-section"><div class="tx-container">' + form + "</div></section>"
    return target.replace(MAIN_END, section + MAIN_END)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    source = (args.site_root / "cnr" / "contact.html").read_text(encoding="utf-8")
    match = FORM_RE.search(source)
    if match is None:
        raise ValueError("reviewed CNR contact form is missing")
    template = match.group(1)

    changed_count = 0
    for locale in COPY:
        path = args.site_root / locale / "contact.html"
        target = path.read_text(encoding="utf-8")
        repaired = transform(target, localized_form(template, locale))
        changed = repaired != target
        if args.apply and changed:
            path.write_text(repaired, encoding="utf-8")
        changed_count += int(changed)
        print(f"locale={locale} forms={len(FORM_RE.findall(repaired))} changed={str(changed).lower()} applied={str(args.apply and changed).lower()}")
    print(f"locales={len(COPY)} changed={changed_count} apply={str(args.apply).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
