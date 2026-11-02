#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创作者月度结算明细导出。

导出阶段完成字段裁剪与掩码：手机号保留前三后四，银行卡保留 BIN 前六位与后四位。
"""
import argparse
import csv
import sys

PLATFORM = "小红书"
FILE_PREFIX = "creator_payout_"
EXPORT_FIELDS = ("creator_id", "nickname", "phone", "bank_card",
                 "amount_cny", "settle_date", "channel")


def mask_phone(v):
    v = str(v or "")
    if len(v) < 8:
        return v
    return v[:3] + "****" + v[-4:]


def mask_card(v):
    digits = "".join(ch for ch in str(v or "") if ch.isdigit())
    if len(digits) < 12:
        return v
    return "%s %s** **** **%s" % (digits[:4], digits[4:6], digits[-2:])


def transform(row):
    out = dict(row)
    out["phone"] = mask_phone(row.get("phone"))
    out["bank_card"] = mask_card(row.get("bank_card"))
    out["nickname"] = row.get("nickname") or row.get("creator_id")
    return out


def export(rows, out_path):
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=EXPORT_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: transform(r).get(k, "") for k in EXPORT_FIELDS})
    print("platform=%s rows=%d out=%s" % (PLATFORM, len(rows), out_path))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    src = "%s%s.csv" % (FILE_PREFIX, args.month.replace("-", ""))
    with open(src, encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    export(rows, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
