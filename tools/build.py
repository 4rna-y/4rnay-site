"""経歴サイトのページを書き出す。デザインは Figma の MyPage をもとにしている。

使い方: リポジトリの直下で python3 -I tools/build.py .

内容(名前、制作物、経歴)はこのファイルの定数にある。見た目は style.css、動きは site.js にある。
書き出すもの: index.html、works/<制作物>.html
"""
import html
import os
import re
import sys

OUT = sys.argv[1]

NAME = "Kyota Ikuyama"
GITHUB = "https://github.com/4rna-y"

# (slug, 名前, 絵文字, 説明, リポジトリ)
# 紹介動画は videos/<slug>.mp4、その最初の画面は posters/<slug>.jpg に置く
WORKS = [
    ("gasho", "Gasho", "🙏", "複数のマシンの Claude Code を、1 画面で動かす",
     "https://github.com/4rtofl/Gasho"),
    ("bobert", "Bobert", "🤖", "使った人が自分の API キーで払う、Discord の AI Bot",
     "https://github.com/4rtofl/Bobert"),
    ("dopagakix", "Dopagakix", "🎥", "AI の作業結果を、ショート動画にまとめる",
     "https://github.com/4rtofl/Dopagakix"),
    ("awakeverify", "AwakeVerify", "👀", "動画教材を見ている人の眠気を推定して、動画を止める",
     "https://github.com/4rna-y/AwakeVerify"),
]

# (アイコン, 役割, 始まり, 終わり, 所属, 所属の言語)
# 終わりが None なら期間を出さず、"" なら続いている("2026 09 -")
CAREER = [
    ("university", "University", "2024-04", None,
     "International Professional University of Technology in Tokyo", "en"),
    ("briefcase", "Internship", "2025-10", "2026-01", "株式会社ベースメントファクトリープロダクション", None),
    ("briefcase", "Internship", "2026-08", "2026-09", "丸紅株式会社 バリュークリエイションオフィス", None),
    ("briefcase", "Freelancer", "2026-09", "", "Digital Experts株式会社", None),
    ("briefcase", "Internship", "2026-10", "2026-11", "株式会社ベースメントファクトリープロダクション", None),
]

e = html.escape

# 途中で改行させない語
NO_BREAK = ["Claude Code", "AI Bot"]
# 英字や数字と、そのあとに続く和文(助詞など)のあいだの空白
LATIN_THEN_JAPANESE = re.compile(r"(?<=[A-Za-z0-9]) (?=[぀-ヿ㐀-鿿])")


def ja(text):
    for words in NO_BREAK:
        text = text.replace(words, words.replace(" ", " "))
    # 「1 画面」「AI の」のように、和文が行頭に来て前の語と離れないようにする
    text = LATIN_THEN_JAPANESE.sub(" ", text)
    # 狭い画面では、長い会社名を「株式会社」のあとで改行できるようにする。
    # <wbr> は nowrap でも改行されてしまうので、幅のない空白(U+200B)を使う
    return e(re.sub(r"株式会社(?=\S)", "株式会社​", text))


def ym(value):
    return value.replace("-", " ")


def when_html(start, end):
    text = f'<time datetime="{start}">{ym(start)}</time>'
    if end is None:
        return text
    if end == "":
        return text + " -"
    return text + f' - <time datetime="{end}">{ym(end)}</time>'


def icon(prefix, name, size, cls="icon"):
    return f'<img class="{cls}" src="{prefix}assets/icons/{name}.svg" width="{size}" height="{size}" alt="">'


def github_icon(prefix):
    return f'<span class="gh"><img class="icon" src="{prefix}assets/icons/github.svg" width="29" height="32" alt=""></span>'


def head(title, prefix):
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{e(title)}</title>
<script>
  // 保存した設定があればそれを、なければ OS の設定を使う
  (function () {{
    var saved = null;
    try {{ saved = localStorage.getItem("theme"); }} catch (e) {{}}
    var dark = saved ? saved === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    document.documentElement.dataset.theme = dark ? "dark" : "light";
  }})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400&amp;family=Noto+Sans+JP:wght@400&amp;display=swap">
<link rel="stylesheet" href="{prefix}style.css">
</head>
<body>
<div class="topbar">
  <button class="theme" type="button" aria-pressed="false" aria-label="ダークモード" title="ダークモード">
    {icon(prefix, "moon", 48, "icon to-dark")}
    {icon(prefix, "sun", 48, "icon to-light")}
  </button>
</div>
"""


def foot(prefix):
    return f"""<script src="{prefix}site.js"></script>
</body>
</html>
"""


def index_page():
    cards = "".join(f"""
      <li><a class="card tint-{slug}" href="works/{slug}.html">
        <span class="thumb"><span class="emoji" aria-hidden="true">{emoji}</span></span>
        <span class="label"><span>{e(name)}</span>{icon("", "chevron-right", 24)}</span>
      </a></li>""" for slug, name, emoji, _desc, _repo in WORKS)
    career = "".join(f"""
      <li>
        <div class="rail"><span class="badge">{icon("", kind, 48)}</span></div>
        <div class="what">
          <p class="role"><span class="title">{e(role)}</span> <span class="date">{when_html(start, end)}</span></p>
          <p class="org"{f' lang="{lang}"' if lang else ""}>{ja(org)}</p>
        </div>
      </li>""" for kind, role, start, end, org, lang in CAREER)
    return head(NAME, "") + f"""<main>
  <header class="profile">
    <div class="avatar"><img src="assets/avatar.jpg" width="120" height="120" alt=""></div>
    <div class="who">
      <h1>{e(NAME)}</h1>
      <button class="more" type="button" aria-expanded="false" aria-controls="links" aria-label="リンクを表示">{icon("", "chevron-right", 24)}</button>
      <ul class="links" id="links" hidden>
        <li><a href="{GITHUB}" aria-label="GitHub" title="GitHub">{github_icon("")}</a></li>
      </ul>
    </div>
  </header>
  <section class="projects" aria-labelledby="projects">
    <h2 id="projects">Projects.</h2>
    <ul class="cards">{cards}
    </ul>
  </section>
  <section class="career-section" aria-labelledby="career">
    <h2 id="career">Career.</h2>
    <ol class="career">{career}
    </ol>
    <div class="continues" aria-hidden="true"><span></span><span></span><span></span></div>
  </section>
</main>
""" + foot("")


def work_page(slug, name, desc, repo):
    prefix = "../"
    return head(f"{name} — {NAME}", prefix) + f"""<main>
  <a class="back" href="../index.html#projects">{icon(prefix, "chevron-right", 24)}<span>Projects.</span></a>
  <article class="work tint-{slug}">
    <div class="player">
      <video src="../videos/{slug}.mp4" poster="../posters/{slug}.jpg" controls muted loop playsinline preload="metadata" aria-label="{e(name)} の紹介動画"></video>
    </div>
    <div class="info">
      <h1>{e(name)}</h1>
      <p class="desc">{ja(desc)}</p>
      <a class="repo" href="{repo}" aria-label="{e(name)} の GitHub" title="GitHub">{github_icon(prefix)}</a>
    </div>
  </article>
</main>
""" + foot(prefix)


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", rel, len(text.encode("utf-8")), "bytes")


write("index.html", index_page())
for slug, name, _emoji, desc, repo in WORKS:
    write(f"works/{slug}.html", work_page(slug, name, desc, repo))
