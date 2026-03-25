from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# コーポレートカラー
COLOR_MAIN    = RGBColor(0x00, 0x33, 0x8D)   # #00338D KPMG Blue
COLOR_MED     = RGBColor(0x00, 0x5E, 0xB8)   # #005EB8 Medium Blue
COLOR_LIGHT   = RGBColor(0x00, 0x91, 0xDA)   # #0091DA Light Blue
COLOR_PURPLE  = RGBColor(0x48, 0x36, 0x98)   # #483698 Purple
COLOR_TEAL    = RGBColor(0x00, 0xA3, 0xA1)   # #00A3A1 Teal
COLOR_WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_DARK    = RGBColor(0x1A, 0x1A, 0x2E)
COLOR_GRAY    = RGBColor(0xF4, 0xF6, 0xF9)
COLOR_GRAY2   = RGBColor(0x6B, 0x7B, 0x8D)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]  # 完全ブランク

# ──────────────────────────────────────────────────────────
# ユーティリティ
# ──────────────────────────────────────────────────────────
def add_rect(slide, l, t, w, h, fill_color, line_color=None, line_width=None):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        if line_width:
            shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()
    return shape

def add_text_box(slide, l, t, w, h, text, font_size, color,
                 bold=False, align=PP_ALIGN.LEFT, wrap=True):
    txBox = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txBox.word_wrap = wrap
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = "Meiryo"
    return txBox

def add_para(tf, text, font_size, color, bold=False, align=PP_ALIGN.LEFT, space_before=0):
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = "Meiryo"
    return p

# ──────────────────────────────────────────────────────────
# スライド1：タイトル
# ──────────────────────────────────────────────────────────
slide1 = prs.slides.add_slide(blank_layout)

# 背景：濃紺
add_rect(slide1, 0, 0, 13.33, 7.5, COLOR_MAIN)

# 左側アクセントバー（ティール）
add_rect(slide1, 0, 0, 0.5, 7.5, COLOR_TEAL)

# 右下装飾（ライトブルー半透明風）
add_rect(slide1, 9.5, 5.0, 3.83, 2.5, COLOR_MED)

# 右下装飾2
add_rect(slide1, 10.5, 5.8, 2.83, 1.7, COLOR_LIGHT)

# 会社名（左上）
add_text_box(slide1, 0.8, 0.4, 8, 0.5,
             "つなぐ会計事務所", 13, COLOR_TEAL, bold=True)

# タイトル（大）
txBox = slide1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(10), Inches(2.5))
txBox.word_wrap = True
tf = txBox.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.LEFT
r = p.add_run()
r.text = "公認会計士と税理士"
r.font.size = Pt(54)
r.font.color.rgb = COLOR_WHITE
r.font.bold = True
r.font.name = "Meiryo"
add_para(tf, "どう違うの？", 42, COLOR_LIGHT, bold=False)

# サブタイトル
add_text_box(slide1, 0.8, 4.6, 9, 0.5,
             "― 専門家の役割をわかりやすく解説します ―", 15, COLOR_GRAY2,
             align=PP_ALIGN.LEFT)

# 日付・資料種別
add_text_box(slide1, 0.8, 6.8, 8, 0.4,
             "お客様向け説明資料  ／  つなぐ会計事務所", 11, COLOR_GRAY2)

# ──────────────────────────────────────────────────────────
# スライド2：比較表
# ──────────────────────────────────────────────────────────
slide2 = prs.slides.add_slide(blank_layout)

# 背景：白
add_rect(slide2, 0, 0, 13.33, 7.5, COLOR_WHITE)

# ヘッダー帯
add_rect(slide2, 0, 0, 13.33, 1.1, COLOR_MAIN)
# ヘッダー左アクセント
add_rect(slide2, 0, 0, 0.35, 1.1, COLOR_TEAL)

add_text_box(slide2, 0.6, 0.25, 12, 0.65,
             "公認会計士と税理士　資格・業務の比較", 22, COLOR_WHITE, bold=True)

# ──── 列ヘッダー ────
COL_L  = 0.3   # 項目列
COL_C  = 4.6   # 公認会計士列
COL_R  = 9.0   # 税理士列
COL_W  = 4.1
ROW_START = 1.35
ROW_H  = 0.78

# 列ヘッダー背景
add_rect(slide2, COL_C - 0.1, ROW_START, COL_W + 0.1, 0.58, COLOR_MED)
add_rect(slide2, COL_R - 0.1, ROW_START, COL_W + 0.1, 0.58, COLOR_PURPLE)

add_text_box(slide2, COL_C, ROW_START + 0.05, COL_W, 0.5,
             "公認会計士（CPA）", 16, COLOR_WHITE, bold=True, align=PP_ALIGN.CENTER)
add_text_box(slide2, COL_R, ROW_START + 0.05, COL_W, 0.5,
             "税理士（Tax Accountant）", 16, COLOR_WHITE, bold=True, align=PP_ALIGN.CENTER)

# 項目列ヘッダー
add_text_box(slide2, COL_L, ROW_START + 0.08, 4.0, 0.5,
             "比較項目", 14, COLOR_MAIN, bold=True)

# ──── テーブル行データ ────
rows = [
    ("主な業務",
     "監査・会計・税務・経営\nコンサルティングなど",
     "税務申告・税務相談・\n記帳代行など"),
    ("独占業務",
     "財務諸表の監査\n（上場企業等への法定監査）",
     "税務代理・税務書類作成\n（個人・法人の確定申告等）"),
    ("試験難易度",
     "国家最難関レベル\n合格率 約10〜11%",
     "難関国家資格\n合格率 約15〜20%"),
    ("主な活躍場所",
     "監査法人・大企業・金融機関\nコンサルファームなど",
     "税理士事務所・会計事務所\n中小企業・個人事業主など"),
    ("費用感",
     "比較的高め\n（大企業・上場企業向け）",
     "費用がわかりやすい\n（中小企業・個人向け）"),
]

for i, (label, cpa_text, tax_text) in enumerate(rows):
    y = ROW_START + 0.58 + i * ROW_H + 0.1
    bg_color = COLOR_GRAY if i % 2 == 0 else COLOR_WHITE

    # 行背景
    add_rect(slide2, COL_L - 0.1, y - 0.05, 12.8, ROW_H - 0.05, bg_color)

    # 左区切り線（ティール）
    add_rect(slide2, COL_C - 0.12, y - 0.05, 0.05, ROW_H - 0.05, COLOR_LIGHT)
    add_rect(slide2, COL_R - 0.12, y - 0.05, 0.05, ROW_H - 0.05, COLOR_LIGHT)

    # テキスト
    add_text_box(slide2, COL_L, y, 4.0, ROW_H, label, 13, COLOR_MAIN, bold=True)
    add_text_box(slide2, COL_C, y, COL_W, ROW_H, cpa_text, 12, COLOR_DARK)
    add_text_box(slide2, COL_R, y, COL_W, ROW_H, tax_text, 12, COLOR_DARK)

# フッター
add_rect(slide2, 0, 7.15, 13.33, 0.35, COLOR_MAIN)
add_text_box(slide2, 0.3, 7.18, 12, 0.3,
             "つなぐ会計事務所", 10, COLOR_LIGHT)

# ──────────────────────────────────────────────────────────
# スライド3：どちらに相談すべきか
# ──────────────────────────────────────────────────────────
slide3 = prs.slides.add_slide(blank_layout)

add_rect(slide3, 0, 0, 13.33, 7.5, COLOR_WHITE)
add_rect(slide3, 0, 0, 13.33, 1.1, COLOR_MAIN)
add_rect(slide3, 0, 0, 0.35, 1.1, COLOR_TEAL)

add_text_box(slide3, 0.6, 0.25, 12, 0.65,
             "どちらに相談すればいい？　― シーン別ガイド ―", 22, COLOR_WHITE, bold=True)

# ─ 左パネル：公認会計士 ─
add_rect(slide3, 0.3, 1.25, 5.9, 5.4, COLOR_MED)
add_rect(slide3, 0.3, 1.25, 5.9, 0.6, RGBColor(0x00, 0x28, 0x6B))  # ダーク帯

add_text_box(slide3, 0.5, 1.32, 5.5, 0.5,
             "公認会計士に相談", 17, COLOR_WHITE, bold=True)

cpa_items = [
    "上場準備・IPOを目指している",
    "金融機関からの監査証明が必要",
    "M&A・企業買収の財務デューデリジェンス",
    "内部統制・コーポレートガバナンスの整備",
    "大規模な資金調達を検討している",
]
y = 2.05
for item in cpa_items:
    # 丸アイコン
    add_rect(slide3, 0.45, y + 0.07, 0.18, 0.18, COLOR_TEAL)
    add_text_box(slide3, 0.72, y, 5.2, 0.42, item, 13, COLOR_WHITE)
    y += 0.46

add_text_box(slide3, 0.45, 4.85, 5.4, 0.65,
             "→ 大企業・上場企業・金融機関との取引が\n　　多いケースに強みがあります",
             11, RGBColor(0xCC, 0xE5, 0xFF))

# ─ 右パネル：税理士 ─
add_rect(slide3, 6.9, 1.25, 5.9, 5.4, COLOR_PURPLE)
add_rect(slide3, 6.9, 1.25, 5.9, 0.6, RGBColor(0x33, 0x28, 0x70))

add_text_box(slide3, 7.1, 1.32, 5.5, 0.5,
             "税理士に相談", 17, COLOR_WHITE, bold=True)

tax_items = [
    "毎年の確定申告・法人税申告をお願いしたい",
    "節税対策・税務相談をしたい",
    "会社設立・起業時の税務手続き",
    "記帳代行・経理のアウトソーシング",
    "相続税・贈与税の申告をしたい",
]
y = 2.05
for item in tax_items:
    add_rect(slide3, 7.05, y + 0.07, 0.18, 0.18, COLOR_TEAL)
    add_text_box(slide3, 7.32, y, 5.2, 0.42, item, 13, COLOR_WHITE)
    y += 0.46

add_text_box(slide3, 7.05, 4.85, 5.4, 0.65,
             "→ 中小企業・個人事業主・フリーランスの\n　　身近な税務パートナーとして活躍します",
             11, RGBColor(0xD9, 0xD0, 0xFF))

# 中央区切り
add_text_box(slide3, 6.35, 3.2, 0.7, 1.0, "VS", 26, COLOR_MAIN, bold=True, align=PP_ALIGN.CENTER)

# 注釈ボックス
add_rect(slide3, 0.3, 6.75, 12.5, 0.45, RGBColor(0xE8, 0xF0, 0xFE))
add_text_box(slide3, 0.5, 6.78, 12.2, 0.38,
             "※ つなぐ会計事務所では、公認会計士・税理士双方の視点からお客様に最適なサポートをご提供します。お気軽にご相談ください。",
             10, COLOR_MAIN)

# フッター
add_rect(slide3, 0, 7.15, 13.33, 0.35, COLOR_MAIN)
add_text_box(slide3, 0.3, 7.18, 12, 0.3,
             "つなぐ会計事務所", 10, COLOR_LIGHT)

# ──────────────────────────────────────────────────────────
# 保存
# ──────────────────────────────────────────────────────────
output_path = "/home/user/my_Cash/公認会計士と税理士の違い_つなぐ会計事務所.pptx"
prs.save(output_path)
print(f"保存完了: {output_path}")
