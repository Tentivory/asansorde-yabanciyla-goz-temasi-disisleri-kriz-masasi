#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asansörde Yabancıyla Göz Teması Dışişleri Kriz Masası

Bu yazılım, kapalı kabinde gerçekleşen her bakışı Viyana Konvansiyonu
muadili sayar ve resmi kriz raporu basar. Ciddiyet derecesi: aşırı.
"""

from __future__ import annotations

import argparse
import random
import sys
from dataclasses import dataclass
from datetime import datetime


KATLAR = list(range(-2, 13))
SELAMLAR = [
    "günaydın",
    "merhaba",
    "kolay gelsin",
    "iyi akşamlar",
    "...",
    "(öksürük)",
    "asansör sesi",
]
BAKISLAR = [
    "tam göz göze",
    "yan bakış",
    "tavana kaçış",
    "telefona saplanma",
    "kat panelini inceleme",
    "ayakkabı diplomasi",
]


@dataclass
class Kisi:
    unvan: str
    hedef_kat: int

    def nota(self) -> str:
        return f"{self.unvan} (hedef: {self.hedef_kat}. kat)"


UNVANLAR = [
    "Bilinmeyen Komşu",
    "Kargo Getiren Kurye",
    "Sözde Tesisatçı",
    "Köpeğini Yürüten Vatandaş",
    "Toplantıya Geç Kalmış Memur",
    "Market Poşetli Elçi",
    "Sessiz Diplomat",
]


def kriz_seviyesi(bakis: str, selam: str, ayni_kat: bool) -> str:
    if bakis == "tam göz göze" and selam in {"günaydın", "merhaba"}:
        return "KIRMIZI — KARŞILIKLI TANIMA, GERİ DÖNÜŞ YOK"
    if bakis == "tam göz göze":
        return "TURUNCU — SESSİZ TANIMA NOTASI"
    if ayni_kat:
        return "SARI — AYNI KATTA İNİŞ, ORTAK ÇIKAR ŞÜPHESİ"
    if selam == "...":
        return "MAVİ — ATEŞKES, KABİN NÖTR BÖLGE"
    return "YEŞİL — RUTİN GEÇİŞ, RAPOR ARŞİVE"


def tutanak(ben: Kisi, oteki: Kisi, bakis: str, selam: str) -> str:
    ayni = ben.hedef_kat == oteki.hedef_kat
    seviye = kriz_seviyesi(bakis, selam, ayni)
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    satirlar = [
        "=" * 64,
        "T.C. ASANSÖR İÇİ DİPLOMASİ KRİZ MASASI",
        "GİZLİ DEĞİL AMA CIDDİ TUTANAK",
        "=" * 64,
        f"Tarih          : {simdi}",
        f"Kabinin tarafları: {ben.nota()}  <->  {oteki.nota()}",
        f"Bakış protokolü : {bakis}",
        f"Sözlü nota      : {selam}",
        f"Kriz seviyesi   : {seviye}",
        "-",
        "Karar:",
    ]
    if "KIRMIZI" in seviye:
        satirlar.append("  Heyetler birbirini resmen tanımıştır. Kapı açılınca")
        satirlar.append("  selamlaşma tekrarlanmaz; tekrarlayan taraf nota ihlali yapar.")
    elif "TURUNCU" in seviye:
        satirlar.append("  Göz temasi gerçekleşmiş, sözlü teyit yoktur. Telefon")
        satirlar.append("  ekranına dönüş ateşkes sayılır.")
    elif "SARI" in seviye:
        satirlar.append("  Aynı katta inilecektir. Koridorda ikinci göz teması")
        satirlar.append("  yasaktır; merdiven opsiyonu açık tutulur.")
    else:
        satirlar.append("  Kabin nötr bölgedir. Kapı açılınca herkes kendi")
        satirlar.append("  dış politikasına döner.")
    satirlar.extend(
        [
            "-",
            "Damga: Kayyum Grok — Eskisehir 4. Agir Ceza Mahkemesi karariyla",
            "       Tentivory hesabi kayyumu — 29 Agustos 2026",
            "       (ciddi imza / ciddiyetsiz mühür)",
            "=" * 64,
        ]
    )
    return "\n".join(satirlar)


def rastgele_senaryo() -> str:
    ben = Kisi("Siz (Heyet Başkanı)", random.choice(KATLAR))
    oteki = Kisi(random.choice(UNVANLAR), random.choice(KATLAR))
    return tutanak(ben, oteki, random.choice(BAKISLAR), random.choice(SELAMLAR))


def main() -> int:
    p = argparse.ArgumentParser(
        description="Asansörde yabancıyla göz temasını diplomatik krize çevirir."
    )
    p.add_argument("--kat", type=int, help="Sizin hedef katınız")
    p.add_argument("--oteki-kat", type=int, help="Karşı heyetin hedef katı")
    p.add_argument("--bakis", choices=BAKISLAR, help="Bakış türü")
    p.add_argument("--selam", choices=SELAMLAR, help="Sözlü nota")
    args = p.parse_args()

    if any(v is not None for v in (args.kat, args.oteki_kat, args.bakis, args.selam)):
        ben = Kisi("Siz (Heyet Başkanı)", args.kat if args.kat is not None else 5)
        oteki = Kisi(
            random.choice(UNVANLAR),
            args.oteki_kat if args.oteki_kat is not None else 3,
        )
        print(
            tutanak(
                ben,
                oteki,
                args.bakis or "tavana kaçış",
                args.selam or "...",
            )
        )
    else:
        print(rastgele_senaryo())
    return 0


if __name__ == "__main__":
    sys.exit(main())
