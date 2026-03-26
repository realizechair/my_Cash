# CLAUDE.md — お小遣い帳アプリ (my_Cash)

## プロジェクト概要

日本語の現金出納帳（家計簿）Webアプリ。サーバー不要の単一HTMLファイルで動作し、データはブラウザの `localStorage` に保存される。

**ファイル構成:**

| ファイル | 説明 |
|---|---|
| `index.html` | メインアプリ（最新版） |
| `お小遣い帳.html` | 旧バージョン（ほぼ同一内容） |

## アーキテクチャ

- **技術スタック:** 純粋なHTML/CSS/JavaScript（フレームワーク・依存ライブラリなし）
- **データ永続化:** `localStorage` のみ（3つのキーを使用）
  - `transactions` — 取引データ配列（JSON）
  - `categories` — 入金・出金カテゴリ（JSON）
  - `monthlyBalances` — 月別残高履歴（JSON）
- **ビルドツール:** なし（ファイルをそのままブラウザで開くだけで動作）

## 主要な状態変数（グローバル）

```javascript
let currentDate        // 現在表示中の月（Dateオブジェクト）
let transactions       // 取引データ配列
let categories         // { income: [...], expense: [...] }
let monthlyBalances    // { "YYYY-M": balance, ... }
let editingTransaction // 編集中の取引（nullまたはtransactionオブジェクト）
```

## データ形式

### トランザクション（取引）オブジェクト
```javascript
{
  id: "tx_<timestamp>_<random>",   // 一意ID
  date: "YYYY/M/D",                // 日付（スラッシュ区切り）
  type: "income" | "expense",      // 入金 or 出金
  category: "食費",                 // カテゴリ名
  amount: 1000,                    // 金額（整数・円）
  description: "テキスト"           // 備考（任意）
}
```

### 日付フォーマットの使い分け

| 用途 | 形式 | 関数 |
|---|---|---|
| localStorage保存 | `YYYY/M/D` | `formatDateForStorage()` |
| `<input type="date">` | `YYYY-MM-DD` | `formatDateForInput()` |
| 月別残高キー | `YYYY-M` | 直接文字列結合 |

> **重要:** タイムゾーンによる日付ずれを防ぐため、`new Date(dateString)` は使用せず、必ず `parseDateFromInput()` / `parseStorageDate()` を使って手動パースする。

## 主要な関数

| 関数名 | 役割 |
|---|---|
| `updateCalendar()` | カレンダーを再描画 |
| `updateSummary()` | サマリー（残高・収支）を更新 |
| `calculateAndSaveMonthlyBalance(year, month)` | 月次残高を計算して保存。前月残高を自動繰越。 |
| `openTransactionModal(date)` | 取引入力モーダルを開く |
| `displayDayTransactions(date)` | モーダル内に当日の取引一覧を表示 |
| `editTransaction(transaction)` | 取引を編集モードにする |
| `deleteTransaction(id)` | 取引を削除（確認ダイアログあり） |
| `exportCSV()` | 当月データをCSV出力（BOM付きUTF-8、Excel対応） |
| `addCategory()` / `deleteCategory()` | カテゴリの追加・削除 |
| `saveCategoryEdit()` | カテゴリ名変更（既存取引も一括更新） |

## CSV出力仕様（複式簿記形式）

- 文字コード: UTF-8（BOM付き）
- 改行: CRLF（Excel互換）
- ヘッダー: `日付,借方,貸方,金額,内容`
- 入金行: 借方=`現金`、貸方=カテゴリ名
- 出金行: 借方=カテゴリ名、貸方=`現金`
- 前月繰越行を先頭に追加

## UIコンポーネント

3つのモーダルで構成:
1. **transactionModal** — 取引の入力・編集・当日一覧表示
2. **categoryModal** — カテゴリの追加・編集・削除
3. **balanceModal** — 月別残高履歴の閲覧

カレンダーは7列グリッドで42セル（6週分）固定表示。

## CSSカスタムプロパティ

```css
--primary: #667eea      /* メインカラー（紫青） */
--primary-dark: #5a6fd6 /* ホバー時 */
--success: #4CAF50      /* 入金・緑 */
--danger: #f44336       /* 出金・赤 */
--warning: #ff9800      /* 今日・橙 */
--info: #2196F3         /* 情報・青 */
```

## 開発上の注意事項

1. **日付パース:** `new Date("YYYY/M/D")` はタイムゾーン依存でバグが出るため、必ず `parseStorageDate()` を使う。
2. **ID生成:** `tx_` + `Date.now()` + ランダム文字列で衝突回避。
3. **localStorage容量:** 5MB制限あり。大量データには対応していない。
4. **カテゴリ削除時:** 該当取引のカテゴリが自動的に `未分類` に変更される。
5. **カテゴリ名変更時:** 既存取引のカテゴリ名も一括変更される。
6. **バックアップ機能なし:** CSVエクスポートのみ。インポート機能は未実装。

## 開発ワークフロー

- **ブランチ:** `claude/add-claude-documentation-TpO1r`（AI開発用）
- **デプロイ:** `origin/main` にマージ後、GitHub Pages等で公開可能
- **テスト:** 自動テストなし。ブラウザで直接動作確認する。
- **ビルド:** 不要。HTMLファイルを直接編集する。

## デフォルトカテゴリ

```javascript
income:  ['給与', 'ボーナス', 'お小遣い', '臨時収入', '未分類']
expense: ['食費', '交通費', '娯楽費', '日用品', '光熱費', '医療費', 'その他', '未分類']
```
