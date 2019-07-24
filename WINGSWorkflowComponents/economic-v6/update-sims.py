#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Economic Model."""

import os
import csv
import sys
from pathlib import Path


def _generate_sim_price(p, sim_price):
    i = Path(p)
    o = Path("simprice.csv")

    with i.open("r") as r, o.open("w") as w:
        r = csv.reader(r)
        w = csv.writer(w)

        for c, p in r:
            if c == "":
                w.writerow((c, p))
            else:
                p = float(p)
                w.writerow((c, round(p + (p * sim_price), 2)))

    return o


def _generate_sim_production_cost(pc, sim_production_c1, sim_production_c2):
    i = Path(pc)
    o = Path("simproductioncost.csv")

    with i.open("r") as r, o.open("w") as w:
        r = csv.reader(r)
        w = csv.writer(w)

        for c, c1, c2 in r:
            if c == "":
                w.writerow((c, c1, c2))
            else:
                c1 = float(c1)
                c2 = float(c2)

                w.writerow(
                    (
                        c,
                        round(c1 + (c1 * sim_production_c1), 2),
                        round(c2 + (c2 * sim_production_c2), 2),
                    )
                )

    return o


def _main():
    base_p = sys.argv[1]
    base_c = sys.argv[2]

    a_p = float(sys.argv[3]) / 100
    a_c1 = float(sys.argv[4]) / 100
    a_c2 = float(sys.argv[5]) / 100

    _generate_sim_price(base_p, a_p)
    _generate_sim_production_cost(base_c, a_c1, a_c2)


if __name__ == "__main__":
    _main()

