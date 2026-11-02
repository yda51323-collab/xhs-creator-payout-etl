# xhs-creator-payout-etl · 创作者月度结算明细导出

按自然月导出创作者结算明细，供财务对账。数据源为结算库，导出前做字段裁剪，
手机号与银行卡号在导出阶段即完成掩码。

## 目录

| 路径 | 说明 |
| --- | --- |
| `data/creator_payout_202610.csv` | 2026-10 结算明细导出样例 |
| `src/etl_creator_payout.py` | 导出作业与掩码规则 |

## 服务标识

`小红书`

出现位置：

- `src/etl_creator_payout.py`：`PLATFORM` 常量、导出文件名前缀
- `README.md`：标题与本节

## 使用

```bash
python src/etl_creator_payout.py --month 2026-10 --out data/creator_payout_202610.csv
```

## 字段说明

| 字段 | 说明 |
| --- | --- |
| `creator_id` | 创作者 ID，`CR-` + 6 位 |
| `nickname` | 昵称（真实姓名场景下按姓名直出） |
| `phone` | 手机号，中间四位掩码 |
| `bank_card` | 收款卡号，保留 BIN 前 6 位与后 4 位 |
| `amount_cny` | 当月应结金额 |
| `settle_date` | 结算日 |
| `channel` | 结算科目 |

## 已知问题

- 昵称字段存在空值，导出时回落为 `creator_id`。
- 同一创作者当月可能有多次结算（补结），对账时需按 `creator_id + channel` 汇总。

## 维护

内容结算组 · 工单 `CS-3391`
