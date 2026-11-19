#!/usr/bin/env python3
"""Studio Oct 홈페이지 만들기 도구.

    python3 tools/build.py

만드는 것 (네 언어: 한국어 / en / ja / zh-tw):
  index.html              스튜디오 첫 화면 (게임 두 개)
  nyangachi/index.html    냥아치 키우기 소개
  startup/index.html      스타트업 키우기 소개 (예전 첫 화면 본문을 그대로 옮기고 머리·꼬리만 새것)

옛 스타트업 문서(privacy / faq / press-kit / probability / support, 네 언어)는 본문을 그대로 두고 머리·꼬리만 새것으로 바꾼다(build_startup_doc).
글을 고치려면 아래 T 표를 고치고 다시 돌린다. 언어를 더하려면 LANGS 와 T 에 한 칸씩 더한다.
결과물은 그냥 HTML 이라 GitHub Pages 에 그대로 올라간다.
"""
import html
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://studiooct.github.io/"
STARTUP_SRC = os.path.join(ROOT, "tools", "startup_src")  # 예전 첫 화면(스타트업 키우기 소개) 원본. 옛 저장소 커밋 8f8677a 의 {언어}index.html 을 2026-11-19 저장소 교체 때 옮겨 둠
PLAY_STARTUP = "https://play.google.com/store/apps/details?id=com.ceogame.app&utm_source=homepage&utm_medium=referral&utm_campaign=studio_home_{c}&utm_content={where}"
MAIL = "contact.studiooct@gmail.com"

# 언어: (주소 앞부분, html lang, hreflang, og:locale, 이름, 스타트업 화면 그림 폴더)
LANGS = {
    "ko": ("", "ko", "ko", "ko_KR", "한국어", "st1-ko"),
    "en": ("en/", "en", "en", "en_US", "English", "st1-en"),
    "ja": ("ja/", "ja", "ja", "ja_JP", "日本語", "st1-ja"),
    "zh-tw": ("zh-tw/", "zh-Hant", "zh-Hant", "zh_TW", "繁體中文", "st1-zh-tw"),
}

T = {
    "ko": dict(
        skip="본문으로 건너뛰기", lang_label="언어", nav_contact="문의",
        startup="스타트업 키우기", startup_full="스타트업 키우기: 고시원에서 상장까지", nyang="냥아치 키우기", nyang_nav="냥아치 키우기", f_about="소개",
        home_title="스튜디오 옥트 Studio Oct — 스타트업 키우기 · 냥아치 키우기",
        home_desc="스튜디오 옥트는 방치형 모바일 게임을 만드는 1인 게임 스튜디오예요. 스타트업 키우기: 고시원에서 상장까지, 냥아치 키우기를 만들어요.",
        kick="STUDIO OCT · 1인 게임 스튜디오",
        h1="잠깐 봐도 즐겁고,<br>자리를 비워도 자라는 게임",
        lead="스튜디오 옥트는 귀여운 방치형 모바일 게임을 만들어요.",
        live="출시", soon="출시 준비 중",
        startup_tile="고시원에서 상장까지, 한 주씩 키우는 회사",
        nyang_tile="골목부터 세계까지, 동네를 접수하는 길고양이",
        games_h="게임",
        startup_lead="비서 고양이와 함께, 한 주씩 키우는 나의 작은 회사.",
        startup_sub="고시원 한 칸에서 시작해 직원을 뽑고 제품을 만들며 상장까지 회사를 키우는 모바일 방치형 경영 시뮬레이션 게임이에요. 비서 고양이와 한 주씩 일을 정하고, 자리를 비운 동안에도 수익이 쌓여요.",
        startup_meta="무료 · Android · 한국어 English 日本語 繁體中文",
        get_play="Google Play에서 받기", more="자세히 보기",
        nyang_lead="귀여운 턱시도 길고양이가 동네를 한 구역씩 접수해요.",
        nyang_sub="골목 동물들과 싸워 돈을 벌고, 까마귀 상점에서 강해지고, 보스를 이겨 다음 동네로 가는 세로 화면 방치형 게임이에요.",
        nyang_meta="iOS · 출시",
        play_soon="Google Play 출시 준비 중",
        about_k="스튜디오 소개", about_h="혼자 만드는 작은 게임 스튜디오",
        about_p=["스튜디오 옥트(Studio Oct)는 서울에 있는 1인 게임 스튜디오예요. 기획과 개발, 운영을 한 사람이 맡고 있어요.",
                 "바쁜 하루 사이에 잠깐 열어도 재미있고, 닫아 두어도 조금씩 자라 있는 방치형 게임을 만들어요."],
        contact_k="문의", contact_h="궁금한 점은 메일로 보내 주세요",
        c_mail_h="문의 메일", c_mail_p="게임 문의, 제휴, 취재 요청 모두 여기로 보내 주세요.",
        c_sup_h="고객 지원", c_sup_p="결제, 계정, 오류 문의 방법을 안내해요.", c_sup_a="문의 안내 보기",
        c_pol_h="개인정보처리방침", c_pol_p="게임이 다루는 정보와 지우는 방법을 설명해요.", c_pol_a="방침 보기",
        f_privacy="개인정보처리방침", f_support="문의", f_faq="자주 묻는 질문", f_press="보도자료실", f_prob="확률 안내",
        biz="스튜디오옥트(Studio Oct) · 대표 홍은총 · 사업자등록번호 844-57-01010<br>서울특별시 중구 동호로14길 19, 3층 368호(신당동, 고마운빌딩) · " + MAIL,
        n_title="냥아치 키우기 — 골목부터 세계까지, 길고양이 방치형 게임",
        n_desc="냥아치 키우기는 귀여운 턱시도 길고양이가 동네를 한 구역씩 접수하는 방치형 모바일 게임이에요. 앱스토어에서 무료로 받을 수 있고, Google Play 출시도 준비하고 있어요.",
        n_tag="골목부터 세계까지",
        n_feat_k="게임 소개", n_feat_h="우리 동네는 내가 접수한다옹",
        n_feats=[("seoul", "싸워서 벌고, 보스를 꺾어요", "골목 동물들과 싸워 돈을 벌어요. 충분히 강해지면 보스에게 도전해 다음 스테이지로 가요."),
                 ("shop", "까마귀 상점에서 강해져요", "반짝이는 건 다 받는 까마귀 상점에서 발톱과 체력, 장비를 키워요."),
                 ("crew", "동료를 모아 자릿세를 받아요", "접수한 구역에서는 자릿세가 쌓여요. 동료를 파견하면 자리를 비운 동안에도 더 많이 모여요."),
                 ("taebaek", "서울 골목에서 태백 산골까지", "도심 골목에서 시작해 시골 들판을 지나 산골까지 가요. 지역마다 이름 있는 보스가 기다려요.")],
        music_on="음악 켜기", music_off="음악 끄기", n_shots_h="게임 화면", n_shots_note="화면은 업데이트로 달라질 수 있어요.",
        n_news_h="출시 소식", n_news_p="2026년 11월 13일 앱스토어에 나왔어요. Google Play 출시는 준비하고 있어요. 궁금한 점은 메일로 보내 주세요.",
        s_title_suffix="",
    ),
    "en": dict(
        skip="Skip to content", lang_label="Language", nav_contact="Contact",
        startup="Grow My Startup", startup_full="Grow My Startup", nyang="Kitty Kingpin: Idle Alley Cat", nyang_nav="Kitty Kingpin", f_about="About",
        home_title="Studio Oct — Grow My Startup · Kitty Kingpin: Idle Alley Cat",
        home_desc="Studio Oct is a solo game studio making idle mobile games: Grow My Startup and Kitty Kingpin: Idle Alley Cat.",
        kick="STUDIO OCT · SOLO GAME STUDIO",
        h1="Fun in a quick peek,<br>still growing while you're away",
        lead="Studio Oct makes cute idle games for mobile.",
        live="Out now", soon="Coming soon",
        startup_tile="Grow a tiny company one week at a time",
        nyang_tile="An alley cat taking over the neighborhood",
        games_h="Games",
        startup_lead="Grow a tiny company one week at a time, with a cat for a secretary.",
        startup_sub="Grow My Startup is a free idle business game for Android. Hire staff, build products and plan each week with a cat for a secretary, from one tiny room to an IPO.",
        startup_meta="Free · Android · 한국어 English 日本語 繁體中文",
        get_play="Get it on Google Play", more="Learn more",
        nyang_lead="A cute tuxedo alley cat takes over the neighborhood, one block at a time.",
        nyang_sub="Fight neighborhood animals for coins, power up at the Crow Shop, and beat the boss to reach the next neighborhood. An idle game in portrait mode.",
        nyang_meta="iOS · Out now",
        play_soon="Coming soon to Google Play",
        about_k="About", about_h="A small studio run by one person",
        about_p=["Studio Oct is a solo game studio based in Seoul. One person handles design, development and operations.",
                 "We make idle games that are fun to open for a minute on a busy day, and that have grown a little by the time you come back."],
        contact_k="Contact", contact_h="Questions? Send us an email",
        c_mail_h="Email", c_mail_p="Game questions, partnerships and press requests all go here.",
        c_sup_h="Support", c_sup_p="How to reach us about purchases, accounts and bugs.", c_sup_a="Support page",
        c_pol_h="Privacy policy", c_pol_p="What data the game handles and how to delete it.", c_pol_a="Read the policy",
        f_privacy="Privacy policy", f_support="Support", f_faq="FAQ", f_press="Press kit", f_prob="Probabilities",
        biz="Studio Oct (스튜디오옥트) · Representative: Eunchong Hong · Business registration no. 844-57-01010<br>3F #368, 19 Dongho-ro 14-gil, Jung-gu, Seoul, Republic of Korea · " + MAIL,
        n_title="Kitty Kingpin: Idle Alley Cat — From the back alleys to the whole world",
        n_desc="Kitty Kingpin: Idle Alley Cat is an idle mobile game where a cute tuxedo street cat takes over the neighborhood one block at a time. Free on the App Store, with Google Play coming soon.",
        n_tag="From the back alleys to the whole world",
        n_feat_k="About the game", n_feat_h="This neighborhood is mine now!",
        n_feats=[("seoul", "Fight, earn, beat the boss", "Fight the local animals to earn coins. Once you are strong enough, challenge the boss and move to the next stage."),
                 ("shop", "Power up at the Crow Shop", "The Crow Shop takes anything shiny. Trade your coins for sharper claws, more health, and better gear."),
                 ("crew", "Build your crew, collect turf dues", "The neighborhoods you take over earn you dues. Send out your crew to collect even more while you're away."),
                 ("taebaek", "From city alleys to the mountains", "Start in a downtown alley, cross the countryside and climb into the mountains. A named boss waits in every region.")],
        music_on="Music on", music_off="Music off", n_shots_h="Screens", n_shots_note="Screens may change with updates. Shown in Korean.",
        n_news_h="Launch news", n_news_p="Out on the App Store since November 13, 2026. A Google Play version is on the way. Questions are welcome by email.",
    ),
    "ja": dict(
        skip="本文へスキップ", lang_label="言語", nav_contact="お問い合わせ",
        startup="こつこつ社長", startup_full="こつこつ社長", nyang="にゃんピラ育成", nyang_nav="にゃんピラ育成", f_about="紹介",
        home_title="Studio Oct — こつこつ社長・にゃんピラ育成",
        home_desc="Studio Octは放置系スマホゲームを作る個人ゲームスタジオです。「こつこつ社長」と「にゃんピラ育成」を開発しています。",
        kick="STUDIO OCT · 個人ゲームスタジオ",
        h1="ちょっと覗くだけで楽しく、<br>離れていても育つゲーム",
        lead="Studio Octは、かわいい放置系スマホゲームを作っています。",
        live="配信中", soon="配信準備中",
        startup_tile="小さな部屋から上場まで、一週間ずつ育てる会社",
        nyang_tile="路地裏から世界へ、ナワバリを広げる野良猫",
        games_h="ゲーム",
        startup_lead="猫の秘書と、一週間ずつ育てる小さな会社。",
        startup_sub="こつこつ社長は、小さな部屋から始めて社員を雇い、アプリを作り、上場まで会社を育てるスマホの放置系・会社経営ゲームです。猫の秘書と毎週の仕事を決め、離れている間も収益が貯まります。",
        startup_meta="無料 · Android · 한국어 English 日本語 繁體中文",
        get_play="Google Playでダウンロード", more="詳しく見る",
        nyang_lead="かわいいタキシード柄の野良猫が、町をひと区画ずつ縄張りにしていきます。",
        nyang_sub="路地裏の動物たちと戦ってお金を稼ぎ、カラスの店で強化しながら、ボスを倒して次の町へ進む縦画面の放置系ゲームです。",
        nyang_meta="iOS · 配信中",
        play_soon="Google Playで配信準備中",
        about_k="スタジオ紹介", about_h="ひとりで作る小さなゲームスタジオ",
        about_p=["Studio Oct（スタジオ・オクト）は、ソウルにある個人ゲームスタジオです。企画・開発・運営をひとりで担当しています。",
                 "忙しい一日の合間に少し開くだけで楽しく、閉じている間にも少しずつ育っている放置系ゲームを作っています。"],
        contact_k="お問い合わせ", contact_h="ご質問はメールでお送りください",
        c_mail_h="メール", c_mail_p="ゲームのご質問、提携、取材のご依頼はこちらへ。",
        c_sup_h="サポート", c_sup_p="購入・アカウント・不具合のお問い合わせ方法をご案内します。", c_sup_a="お問い合わせ案内",
        c_pol_h="プライバシーポリシー", c_pol_p="ゲームが扱う情報と削除方法を説明します。", c_pol_a="ポリシーを読む",
        f_privacy="プライバシーポリシー", f_support="お問い合わせ", f_faq="よくある質問", f_press="プレスキット", f_prob="確率表記",
        biz="Studio Oct（스튜디오옥트）· 代表：Eunchong Hong · 事業者登録番号 844-57-01010<br>3F #368, 19 Dongho-ro 14-gil, Jung-gu, Seoul, Republic of Korea · " + MAIL,
        n_title="にゃんピラ育成 — 路地裏から世界へ！野良猫の放置系ゲーム",
        n_desc="にゃんピラ育成は、かわいいタキシード柄の野良猫が町をひと区画ずつ縄張りにしていく放置系スマホゲームです。App Storeで無料配信中です。Google Play版も準備中です。",
        n_tag="路地裏から世界へ！",
        n_feat_k="ゲーム紹介", n_feat_h="この町はもらったニャ",
        n_feats=[("seoul", "戦って稼いで、ボスを倒す", "路地裏の動物たちと戦ってお金を稼ぎます。十分に強くなったらボスに挑み、次のステージへ進みましょう。"),
                 ("shop", "カラスの店で強くなる", "光るものなら何でも引き取るカラスの店で、ツメや体力、装備を強化できます。"),
                 ("crew", "仲間を集めてショバ代を稼ぐ", "縄張りにした区画にはショバ代が貯まります。仲間を派遣すれば、離れている間も効率よく集められます。"),
                 ("taebaek", "都会の路地裏から山奥まで", "都会の路地裏から始まり、田舎の野原を抜けて山奥へと進みます。各地域には、それぞれ名前のあるボスが待ち受けています。")],
        music_on="音楽オン", music_off="音楽オフ", n_shots_h="ゲーム画面", n_shots_note="画面はアップデートで変わる場合があります。画面は韓国語版です。",
        n_news_h="配信のお知らせ", n_news_p="2026年11月13日にApp Storeで配信を開始しました。Google Play版は準備中です。お問い合わせはメールでお送りください。",
    ),
    "zh-tw": dict(
        skip="跳到主要內容", lang_label="語言", nav_contact="聯絡我們",
        startup="小公司大老闆", startup_full="小公司大老闆", nyang="喵混混養成記", nyang_nav="喵混混養成記", f_about="介紹",
        home_title="Studio Oct — 小公司大老闆・喵混混養成記",
        home_desc="Studio Oct 是製作放置型手機遊戲的個人遊戲工作室，作品有《小公司大老闆》與《喵混混養成記》。",
        kick="STUDIO OCT · 個人遊戲工作室",
        h1="看一眼就有趣，<br>不在的時候也在成長的遊戲",
        lead="Studio Oct 製作可愛的放置型手機遊戲。",
        live="已上架", soon="即將推出",
        startup_tile="從小房間到上市，一週一週經營公司",
        nyang_tile="從巷口到全世界，搶地盤的街貓",
        games_h="遊戲",
        startup_lead="和貓咪秘書一起，一週一週經營我的小公司。",
        startup_sub="小公司大老闆是一款免費的放置模擬經營手遊。從一間小房間開始招募員工、開發產品，一路把公司帶到上市。和貓咪秘書每週安排工作，離開遊戲時收入也會累積。",
        startup_meta="免費 · Android · 한국어 English 日本語 繁體中文",
        get_play="前往Google Play下載", more="了解更多",
        nyang_lead="可愛的賓士街貓，逐區搶下地盤。",
        nyang_sub="和巷子裡的動物打架賺錢，到烏鴉商店變強，打倒頭目前往下一個地區。直式畫面的放置型遊戲。",
        nyang_meta="iOS · 已上架",
        play_soon="Google Play 即將推出",
        about_k="工作室介紹", about_h="一個人做的小小遊戲工作室",
        about_p=["Studio Oct 是位於首爾的個人遊戲工作室，企劃、開發與營運都由一個人負責。",
                 "我們製作忙碌的一天裡打開一下就有趣、關掉之後也會慢慢成長的放置型遊戲。"],
        contact_k="聯絡我們", contact_h="有問題歡迎來信",
        c_mail_h="電子郵件", c_mail_p="遊戲問題、合作與採訪邀約都請寄到這裡。",
        c_sup_h="客服支援", c_sup_p="說明付款、帳號與錯誤回報的聯絡方式。", c_sup_a="查看聯絡說明",
        c_pol_h="隱私權政策", c_pol_p="說明遊戲處理的資料與刪除方式。", c_pol_a="查看政策",
        f_privacy="隱私權政策", f_support="聯絡我們", f_faq="常見問題", f_press="媒體資料", f_prob="機率公告",
        biz="Studio Oct（스튜디오옥트）· 負責人：Eunchong Hong · 營業登記號碼 844-57-01010<br>3F #368, 19 Dongho-ro 14-gil, Jung-gu, Seoul, Republic of Korea · " + MAIL,
        n_title="喵混混養成記 — 從巷口到全世界的街貓放置型 RPG",
        n_desc="喵混混養成記是一款直式放置型手機遊戲，玩家將帶領可愛的賓士街貓，一區一區搶下地盤。現已在 App Store 免費上架，Google Play 版本也正在準備中。",
        n_tag="從巷口到全世界",
        n_feat_k="遊戲介紹", n_feat_h="這條街歸我了喵",
        n_feats=[("seoul", "打架賺錢，打倒頭目", "和巷子裡的動物打架賺錢。變強之後就挑戰頭目，前往下一關。"),
                 ("shop", "到烏鴉商店變強", "烏鴉什麼亮晶晶的東西都收。在烏鴉商店強化爪子、體力和裝備，讓自己變得更強。"),
                 ("crew", "召集夥伴，收地盤費", "搶下的地區會持續累積地盤費。派出夥伴，就算離線也能收取更多地盤費。"),
                 ("taebaek", "從都市巷弄到深山", "從市區巷弄出發，穿過鄉間田野，一路深入深山。每個地區都有各自的頭目等著你。")],
        music_on="開啟音樂", music_off="關閉音樂", n_shots_h="遊戲畫面", n_shots_note="畫面可能隨更新而有所不同。畫面為韓文版。",
        n_news_h="上架消息", n_news_p="已於 2026 年 11 月 13 日在 App Store 上架。Google Play 版本正在準備中。有任何問題都歡迎來信詢問。",
    ),
}

# ── 2차 개편에서 더한 글 ──
T2 = {
    "ko": dict(
        nav_games="게임", nav_studio="스튜디오", lang_short="KO",
        home_title="스튜디오 옥트 Studio Oct — 게임 스튜디오",
        home_desc="스튜디오 옥트는 한 사람이 운영하는 게임 스튜디오예요. 스타트업 키우기: 고시원에서 상장까지, 냥아치 키우기를 만들었어요.",
        h1="떠오른 게임을<br>만들어요",
        lead="스튜디오 옥트는 혼자서 뚝딱뚝딱 게임을 만드는 작은 스튜디오예요. 모바일이든 웹이든 PC든, 만들고 싶은 게임이 떠오르면 만들어서 내놓아요.",
        studio_h="스튜디오", studio_say="플랫폼과 장르를 가리지 않고, 아이디어가 게임이 될 때까지 하나씩 꾸준히 만들어요.",
        l_name="이름", v_name="스튜디오 옥트 (Studio Oct)", l_base="위치", v_base="서울", l_team="만드는 사람", v_team="1명", l_contact="문의",
        l_platform="플랫폼", l_genre="장르", l_status="상태",
        startup_genre="방치형 경영 시뮬레이션", nyang_genre="방치형 RPG",
        startup_state="출시 중", nyang_state="출시 중", l_policy="방침",
    ),
    "en": dict(
        nav_games="Games", nav_studio="Studio", lang_short="EN",
        home_title="Studio Oct — Game Studio",
        home_desc="Studio Oct is a one-person game studio, maker of Grow My Startup and Kitty Kingpin: Idle Alley Cat.",
        h1="We dream up games,<br>then bring them to life",
        lead="Studio Oct is a small, one-person studio that makes games from scratch. Mobile, web, or PC: when an idea for a game strikes, we make it and put it out there.",
        studio_h="Studio", studio_say="Any platform, any genre. We keep at it, one game at a time, until the idea becomes a game.",
        l_name="Name", v_name="Studio Oct (스튜디오 옥트)", l_base="Based in", v_base="Seoul, Korea", l_team="Team", v_team="One person", l_contact="Contact",
        l_platform="Platform", l_genre="Genre", l_status="Status",
        startup_genre="Idle business sim", nyang_genre="Idle RPG",
        startup_state="Out now", nyang_state="Out now", l_policy="Privacy",
    ),
    "ja": dict(
        nav_games="ゲーム", nav_studio="スタジオ", lang_short="JA",
        home_title="Studio Oct — ゲームスタジオ",
        home_desc="Studio Octは、ひとりで運営しているゲームスタジオです。「こつこつ社長」と「にゃんピラ育成」を開発しています。",
        h1="思いついたゲームを<br>形にするスタジオ",
        lead="Studio Octは、ひとりで運営しているゲームスタジオです。スマホ、ウェブ、PCなど、プラットフォームを問わず、作りたいゲームを作って公開しています。",
        studio_h="スタジオ", studio_say="プラットフォームもジャンルも問わず、アイデアをゲームにするまで、一つずつこつこつ作っています。",
        l_name="名称", v_name="Studio Oct（スタジオ・オクト）", l_base="所在地", v_base="ソウル（韓国）", l_team="メンバー", v_team="1人", l_contact="連絡先",
        l_platform="プラットフォーム", l_genre="ジャンル", l_status="状況",
        startup_genre="放置系・会社経営", nyang_genre="放置系RPG",
        startup_state="配信中", nyang_state="配信中", l_policy="ポリシー",
    ),
    "zh-tw": dict(
        nav_games="遊戲", nav_studio="工作室", lang_short="繁中",
        home_title="Studio Oct — 遊戲工作室",
        home_desc="Studio Oct 是一個人經營的遊戲工作室，作品有《小公司大老闆》與《喵混混養成記》。",
        h1="把想到的遊戲，<br>一款款做出來的工作室",
        lead="Studio Oct 是一間由一人經營的遊戲工作室。不論手機、網頁或 PC，只要有想做的遊戲，就會親手開發並推出。",
        studio_h="工作室", studio_say="不論平台或遊戲類型，都一款一款踏實地開發，直到點子真正變成遊戲。",
        l_name="名稱", v_name="Studio Oct", l_base="所在地", v_base="首爾（韓國）", l_team="成員", v_team="1 人", l_contact="聯絡",
        l_platform="平台", l_genre="類型", l_status="狀態",
        startup_genre="放置模擬經營", nyang_genre="放置型 RPG",
        startup_state="已上架", nyang_state="已上架", l_policy="政策",
    ),
}
for _k in T:
    T[_k].update(T2[_k])

# ── 3차(2026-11-17): 맨 위 페이지를 냥아치 키우기 중심으로. 1인 개발은 앞세우지 않는다. ──
T3 = {
    "ko": dict(
        home_title="스튜디오 옥트 Studio Oct — 냥아치 키우기",
        home_desc="스튜디오 옥트는 떠오른 게임을 만들어 내놓는 작은 게임 스튜디오예요. 귀여운 턱시도 길고양이가 동네를 접수하는 방치형 게임, 냥아치 키우기를 만들어요.",
        other_h="다른 게임",
        studio_p="떠오른 게임을 만들어 내놓는 작은 스튜디오예요. 모바일이든 웹이든 PC든, 장르를 가리지 않고 아이디어가 게임이 될 때까지 하나씩 꾸준히 만들어요.",
    ),
    "en": dict(
        home_title="Studio Oct — Kitty Kingpin: Idle Alley Cat",
        home_desc="Studio Oct is a small game studio that turns ideas into games and releases them. We make Kitty Kingpin: Idle Alley Cat, an idle game where a cute tuxedo alley cat takes over the neighborhood.",
        other_h="More games",
        studio_p="We're a small studio that turns ideas into games and releases them. Whether it's mobile, web, or PC, we keep building one game at a time, across all genres, until each idea comes to life.",
    ),
    "ja": dict(
        home_title="Studio Oct — にゃんピラ育成",
        home_desc="Studio Octは、思いついたゲームを形にして届ける小さなゲームスタジオです。かわいいタキシード柄の野良猫が町を縄張りにしていく放置系ゲーム「にゃんピラ育成」を開発しています。",
        other_h="ほかのゲーム",
        studio_p="思いついたゲームを形にして届ける小さなスタジオです。スマホでもWebでもPCでも、ジャンルを問わず、アイデアがゲームになるまで一つずつコツコツ作っています。",
    ),
    "zh-tw": dict(
        home_title="Studio Oct — 喵混混養成記",
        home_desc="Studio Oct 是一間把遊戲點子做出來並推出的小型遊戲工作室。我們正在製作《喵混混養成記》，這是一款讓可愛的賓士貓在街頭搶地盤的放置遊戲。",
        other_h="其他遊戲",
        studio_p="我們是把遊戲點子做出來並推出的小型工作室。不論是手機、網頁還是 PC，也不拘遊戲類型，都會一款一款踏實開發，直到點子變成真正的遊戲。",
    ),
}
for _k in T:
    T[_k].update(T3[_k])

# 게임 목록. 새 게임(모바일·웹·스팀 무엇이든)은 여기에 한 칸 더하고, T 에 <id>, <id>_genre, <id>_state, <id>_lead 글을 넣는다.
GAMES = [
    dict(id="startup", path="startup/", cover="img/v3/hero-building.webp", cover_size=(872, 1200), cover_class=" so-cover-startup",
         platform="Android", live=True, store=("Google Play", "play")),
    dict(id="nyang", path="nyangachi/", cover="img/nyang/icon.webp", cover_size=(512, 512), cover_class="",
         platform="iOS", live=True, store=("App Store", "appstore")),
]

e = html.escape


ROOT_DIR = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))


def rel(depth, path):
    """뿌리 기준 주소 path 를 depth 만큼 깊은 페이지에서 쓰는 상대 주소로."""
    return ("../" * depth + path) or "./"


def head_html(lang, page, depth):
    """page: '' | 'startup/' | 'nyangachi/' — 그 언어판 안에서의 주소."""
    t = T[lang]
    lp = LANGS[lang][0]
    home = rel(depth, lp)
    langs = "".join(
        '<a href="%s" hreflang="%s" lang="%s" title="%s"%s>%s</a>' % (
            rel(depth, v[0] + page), v[2], v[1], v[4], ' aria-current="page"' if k == lang else "", T[k]["lang_short"])
        for k, v in LANGS.items())
    return (
        '<header class="so-head"><div class="so-wrap so-head-row">\n'
        '  <a class="so-brand" href="%s">Studio Oct</a>\n'
        '  <nav class="so-nav" aria-label="menu"><a href="%s#games">%s</a><a href="%s#studio">%s</a></nav>\n'
        '  <nav class="so-langs" aria-label="%s">%s</nav>\n'
        '</div></header>' % (home, home, e(t["nav_games"]), home, e(t["nav_studio"]), e(t["lang_label"]), langs))


def foot_html(lang, depth):
    """꼬리: 게임마다 한 줄씩 그 게임의 문서를 모은다."""
    t = T[lang]
    lp = LANGS[lang][0]
    a = lambda p, label: '<a href="%s">%s</a>' % (rel(depth, lp + p), e(label))
    startup = [a("startup/", t["f_about"]), a("faq.html", t["f_faq"]), a("press-kit.html", t["f_press"]),
               a("probability.html", t["f_prob"]), a("privacy.html", t["f_privacy"]), a("support.html", t["f_support"])]
    nyang = [a("nyangachi/", t["f_about"])]
    if lang == "ko":  # 보도자료는 아직 한국어판만 있다
        nyang.append('<a href="%s">%s</a>' % (rel(depth, "nyangachi/press/"), e(t["f_press"])))
    from coupon_nyang import C as CP
    nyang += [a("nyangachi/coupon.html", CP[lang]["f_coupon"]), a("nyangachi/privacy.html", t["f_privacy"]), '<a href="mailto:%s">%s</a>' % (MAIL, e(t["f_support"]))]
    row = lambda name, links: '  <nav aria-label="%s"><b>%s</b>%s</nav>\n' % (e(name), e(name), "".join(links))
    return (
        '<footer class="so-foot"><div class="so-parade" aria-hidden="true"><div class="so-wrap">%s</div></div><div class="so-wrap">\n'
        '%s%s'
        '  <p>%s</p><p>© 2026 Studio Oct</p>\n'
        '</div></footer>' % (
            "".join('<img src="%s" alt="">' % rel(depth, "img/nyang/pal-crew%d.webp" % n) for n in (1, 2, 3, 4, 5)),
            row(t["nyang_nav"], nyang), row(t["startup"], startup), t["biz"]))


def page_head(lang, page, depth, title, desc, og_image, theme, extra=""):
    v = LANGS[lang]
    url = SITE + v[0] + page
    alts = "".join('<link rel="alternate" hreflang="%s" href="%s">\n' % (x[2], SITE + x[0] + page) for x in LANGS.values())
    alts += '<link rel="alternate" hreflang="x-default" href="%s">\n' % (SITE + "en/" + page)
    return f'''<!doctype html>
<html lang="{v[1]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Studio Oct">
<meta property="og:locale" content="{v[3]}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{theme}">
<link rel="icon" type="image/png" href="{rel(depth, 'img/cat.png')}">
<!-- i18n:hreflang -->
{alts}<!-- /i18n:hreflang -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
{cute_font(lang)}<link rel="stylesheet" href="{rel(depth, 'site.css')}">
{extra}</head>
<body class="so-page">
<a class="so-skip" href="#main">{e(T[lang]["skip"])}</a>
'''


def cute_font(lang):
    """제목용 둥근 글꼴. 한국어·영어는 게임과 같은 주아, 일본어는 둥근 고딕. 번체는 맞는 둥근 글꼴이 없어 기기 글꼴을 쓴다."""
    fam = {"ko": "Jua", "en": "Jua", "ja": "M+PLUS+Rounded+1c:wght@800"}.get(lang)
    if not fam:
        return ""
    return ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=%s&amp;display=swap">\n' % fam)


def play_startup(lang, where):
    return e(PLAY_STARTUP.format(c=lang.replace("-", "_"), where=where))


APPSTORE_CT = "https://apps.apple.com/app/apple-store/id6833861408?pt=129781558&ct=%s&mt=8"


def appstore(lang):
    """냥아치 키우기 앱스토어 주소. 캠페인 링크(ct=web)라 앱스토어 커넥트에서 홈페이지로 온 설치를 따로 본다.
    보는 사람의 나라 스토어로 열린다. 설명: IljjangNyang docs/marketing/CAMPAIGN_LINKS.md"""
    return APPSTORE_CT % "web"


def ic(depth, name):
    """게임 속 작은 아이콘."""
    return '<img class="so-ic" src="%s" width="88" height="88" alt="">' % rel(depth, "img/nyang/ic-%s.png" % name)


def state_html(t, g):
    return '<span class="so-state%s">%s</span>' % (" so-state-live" if g["live"] else "", e(t[g["id"] + "_state"]))


def build_home(lang):
    t = T[lang]
    v = LANGS[lang]
    d = 1 if v[0] else 0
    r = lambda p: rel(d, p)
    here = lambda p: rel(d, v[0] + p)
    ld = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","@id":"https://studiooct.github.io/#studio","name":"Studio Oct","alternateName":"스튜디오옥트","url":"https://studiooct.github.io/","email":"%s","sameAs":["https://x.com/Studio_Oct"]}
</script>
''' % MAIL
    items = ""
    others = [g for g in GAMES if g["id"] != "nyang"]  # 냥아치는 맨 위 배너로
    nyg = next(g for g in GAMES if g["id"] == "nyang")
    for i, g in enumerate(others):
        name = t["startup_full"] if g["id"] == "startup" else t[g["id"]]
        links = ""
        if g["store"]:
            links += '<a href="%s">%s ↗</a>' % (play_startup(lang, "home") if g["store"][1] == "play" else appstore(lang), g["store"][0])
        links += '<a href="%s">%s →</a>' % (here(g["path"]), e(t["more"]))
        items += f'''
      <li class="so-item">
        <a class="so-cover{g["cover_class"]}" href="{here(g["path"])}" tabindex="-1" aria-hidden="true"><img src="{r(g["cover"])}" width="{g["cover_size"][0]}" height="{g["cover_size"][1]}" alt=""></a>
        <span class="so-item-no">{i + 1:02d}</span>
        <h3><a href="{here(g["path"])}">{e(name)}</a></h3>
        <p class="so-item-meta">{e(t[g["id"] + "_genre"])}<br>{g["platform"]} · {state_html(t, g)}</p>
        <p class="so-item-desc">{e(t[g["id"] + "_lead"])}</p>
        <p class="so-links">{links}</p>
      </li>'''
    home_more = build_home_nyang(lang, d, r, here)
    out = page_head(lang, "", d, t["home_title"], t["home_desc"], "img/nyang/feature.webp", "#63BEFF", ld)
    out += head_html(lang, "", d) + f'''
<main id="main">
  <section id="games" class="so-ghero so-home-banner"><div class="so-wrap so-ghero-row">
    {nyang_play(lang, r, t)}
    <div>
      <h1>{e(t["nyang"])}</h1>
      <p class="so-tag">{e(t["n_tag"])}</p>
      <p class="so-sub">{e(t["nyang_lead"])}</p>
      <p>{state_html(t, nyg)} <a class="so-store" href="{appstore(lang)}">App Store ↗</a> <span class="so-store so-store-soon">Google Play · {e(t["soon"])}</span> <a class="so-store so-store-light" href="{here(nyg["path"])}">{e(t["more"])} →</a></p>
    </div>
  </div></section>
{home_more}
  <section id="more-games"><div class="so-wrap">
    <div class="so-bar"><h2>{ic(d, "coin")}{e(t["other_h"])}</h2><div class="so-pals" aria-hidden="true"><img class="so-px" src="{r("img/lp/hire-cat-a.png")}" width="114" height="114" alt=""></div></div>
    <ol class="so-shelf so-shelf-small">{items}
    </ol>
  </div></section>

  <section id="studio"><div class="so-wrap">
    <div class="so-bar"><h2>{ic(d, "bell")}{e(t["studio_h"])}</h2></div>
    <div class="so-split">
      <p>{e(t["studio_p"])}</p>
      <dl class="so-rows so-note-card">
        <div><dt>{ic(d, "stat_cute")}{e(t["l_name"])}</dt><dd>{e(t["v_name"])}</dd></div>
        <div><dt>{ic(d, "flag")}{e(t["l_base"])}</dt><dd>{e(t["v_base"])}</dd></div>
        <div><dt>{ic(d, "feather")}{e(t["l_contact"])}</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
        <div><dt>{ic(d, "box")}X</dt><dd><a href="https://x.com/Studio_Oct">@Studio_Oct</a></dd></div>
      </dl>
    </div>
  </div></section>
</main>

''' + foot_html(lang, d) + "\n</body>\n</html>\n"
    write(v[0] + "index.html", out)


def nyang_play(lang, r, t, music=True):
    """냥아치 세로 폰 플레이 영상(소리 없음, 반복) + 서울 배경음악 단추.
    언어판 영상이 있으면 그것(img/nyang/play-{언어}.mp4, 앱 미리보기 영상에서 사람 장면을 뺀 싸움 부분), 없으면 한국어 play.mp4."""
    import os
    suf = "" if lang == "ko" or not os.path.exists(os.path.join(ROOT_DIR, "img/nyang/play-%s.mp4" % lang)) else "-" + lang
    poster = "img/nyang/play-poster%s.webp" % suf
    art = (f'<video class="so-play" autoplay muted loop playsinline preload="metadata" width="390" height="838" '
           f'poster="{r(poster)}" aria-label="{e(t["nyang"])}">'
           f'<source src="{r("img/nyang/play%s.mp4" % suf)}" type="video/mp4"></video>')
    if music and os.path.exists(os.path.join(ROOT_DIR, "img/nyang/bgm-seoul.m4a")):
        # 게임 서울 배경음악. 브라우저가 소리 자동 재생을 막으므로 단추를 눌러야 나온다.
        art = (f'<div class="so-playbox">{art}'
               f'<audio id="so-bgm" loop preload="none" src="{r("img/nyang/bgm-seoul.m4a")}"></audio>'
               f'<button type="button" class="so-music" aria-pressed="false" data-on="{e(t["music_on"])}" data-off="{e(t["music_off"])}">'
               f'<span aria-hidden="true">♪</span> <b>{e(t["music_on"])}</b></button></div>'
               '<script>(function(){var b=document.querySelector(".so-music"),a=document.getElementById("so-bgm");if(!b||!a)return;a.volume=.5;'
               'function s(on){b.setAttribute("aria-pressed",on?"true":"false");b.querySelector("b").textContent=on?b.dataset.off:b.dataset.on;}'
               'b.addEventListener("click",function(){if(a.paused){a.play().then(function(){s(true)}).catch(function(){s(false)})}else{a.pause();s(false)}});})();</script>')
    return art


def build_home_nyang(lang, d, r, here):
    """맨 위 페이지의 냥아치 칸들: 숫자 네 칸, 게임 화면 네 장, 소식 두 칸 + 쿠폰, 공식 채널, 동료 열 마리 띠.
    글은 tools/home_nyang.py (소식은 거기서 갈아 끼운다)."""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from home_nyang import SHOTS, NEWS, CHANNELS, H
    from nyang_more import NX
    from coupon_nyang import C as CP
    h, x, cp = H[lang], NX[lang], CP[lang]
    stats = "".join(f'<li><b>{n}</b><span>{e(l)}</span></li>' for n, l in x["stats"])
    shots = "".join(
        f'<li><img src="{r("img/nyang/store/%s/%s.webp" % (lang, k))}" width="360" height="780" loading="lazy" alt=""><b>{e(tt)}</b><span>{e(p)}</span></li>'
        for k, tt, p in SHOTS[lang])
    def card(icon, href, tt, p, cls=""):
        inner = f'<img src="{r("img/nyang/ic-%s.png" % icon)}" width="88" height="88" alt=""><div><b>{e(tt)}</b><span>{e(p)}</span></div>'
        return (f'<li class="{cls}"><a href="{here(href)}">{inner}<i aria-hidden="true">›</i></a></li>' if href
                else f'<li class="{cls}"><div class="so-news-in">{inner}</div></li>')
    news = "".join(card(*n[:4]) for n in NEWS[lang][:2])
    news += card("gift", "nyangachi/coupon.html", cp["title"], cp["intro"], "so-news-coupon")
    chans = "".join(f'<li><a href="{u}" rel="me noopener"><span class="so-chan-ic" aria-hidden="true">{e(g)}</span>{e(names[lang])}<i aria-hidden="true">›</i></a></li>'
                    for g, u, names in CHANNELS if u)
    crew = "".join(f'<img src="{r("img/nyang/pal-crew%d.webp" % n)}" alt="" loading="lazy">' for n in range(1, 11))
    return f'''
  <section class="so-gap so-home-nyang"><div class="so-wrap">
    <ul class="so-stats">{stats}</ul>
    <div class="so-bar"><h2>{ic(d, "can")}{e(h["shots_h"])}</h2></div>
    <ul class="so-shots">{shots}</ul>
    <div class="so-bar"><h2>{ic(d, "bell")}{e(h["news_h"])}</h2></div>
    <ul class="so-news">{news}</ul>
    <div class="so-bar"><h2>{ic(d, "feather")}{e(h["ch_h"])}</h2></div>
    <ul class="so-chan">{chans}</ul>
    <div class="so-crewstrip" aria-hidden="true">{crew}</div>
  </div></section>
'''


def build_nyang(lang):
    t = T[lang]
    v = LANGS[lang]
    d = 2 if v[0] else 1
    r = lambda p: rel(d, p)
    here = lambda p: rel(d, v[0] + p)
    g = GAMES[1]
    ld = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":["VideoGame","MobileApplication"],"name":%s,"url":"%s","operatingSystem":"iOS","gamePlatform":"iOS","applicationCategory":"GameApplication","installUrl":"%s","author":{"@type":"Organization","name":"Studio Oct","url":"https://studiooct.github.io/"},"publisher":{"@type":"Organization","name":"Studio Oct","url":"https://studiooct.github.io/"},"description":%s}
</script>
''' % (jstr(t["nyang"]), SITE + v[0] + "nyangachi/", appstore(lang), jstr(t["n_desc"]))
    if lang == "ko":
        art = f'<img class="so-ghero-art" src="{r("img/nyang/feature.webp")}" width="1024" height="500" alt="{e(t["nyang"])}">'
    else:
        art = f'<img class="so-ghero-art so-ghero-art-icon" src="{r("img/nyang/icon.webp")}" width="512" height="512" alt="">'
    import os
    if os.path.exists(os.path.join(ROOT_DIR, "img/nyang/play.mp4")):
        art = nyang_play(lang, r, t)
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from nyang_more import NX, CREW_ART
    x = NX[lang]
    shot = lambda k: r("img/nyang/store/%s/%s.webp" % (lang, k))
    stats = "".join(f'<li><b>{n}</b><span>{e(l)}</span></li>' for n, l in x["stats"])
    crew = "".join(f'<li><img src="{r("img/nyang/pal-crew%d.webp" % n)}" alt="" loading="lazy"><b>{e(x["crew"][cid][0])}</b><span>{e(x["crew"][cid][1])}</span></li>' for cid, n in CREW_ART)
    duo = lambda k, h, body, flip="": (f'<div class="so-duo{flip}"><img src="{shot(k)}" width="360" height="780" loading="lazy" alt="">' +
                                       (f'<div><h3>{e(h)}</h3>' if h else '<div>') + f'{body}</div></div>')
    chips = lambda ns: "".join(f"<li>{e(n)}</li>" for n in ns)
    regions = (f"<p class='so-mini'>{e(x['land'][0])}</p><ul class='so-chips'>{chips(x['regions'])}</ul>"
               f"<p class='so-mini'>{e(x['land'][1])}</p><ul class='so-chips'>{chips(x['tw_regions'])}</ul>")
    tw_p = f"<p>{e(x['tw_p'])}</p>"
    # 대만 편(1.1.0): 번체 쪽은 대만 첫 장면 그림과 함께 따로, 다른 언어는 지역 칸 안에 한 문단으로
    tw_alone = lang == "zh-tw"
    tw_in_region = "" if tw_alone else f"<h3>{e(x['tw_h'])}</h3>{tw_p}"
    bosses = "".join(f"<li>{e(n)}</li>" for n in x["bosses"])
    vids = "".join(f'<li><video controls playsinline preload="none" width="1080" height="1920" poster="{r("nyangachi/press/files/thumb/" + k + ".webp")}" src="{r("nyangachi/press/files/video/" + k + ".mp4")}"></video><span>{e(c)}</span></li>' for k, c in x["videos"])
    more = f'''
  <section class="so-gap"><div class="so-wrap">
    <div class="so-bar"><h2>{ic(d, "stat_cute")}{e(x["stats_h"])}</h2></div>
    <ul class="so-stats">{stats}</ul>
    {duo("1-fight", x["human_h"], f"<p>{e(x['human_p'])}</p>")}
    {duo("4-turf", x["region_h"], f"<p>{e(x['region_p'])}</p>{regions}<p class='so-mini'>{e(x['bosses_l'])}</p><ul class='so-chips so-chips-boss'>{bosses}</ul>{tw_in_region}", " so-duo-flip")}
    {duo("tw-1", x["tw_h"], tw_p) if tw_alone else ""}
  </div></section>

  <section class="so-gap"><div class="so-wrap">
    <div class="so-bar"><h2>{ic(d, "stat_hp")}{e(x["crew_h"])}</h2><span>{len(CREW_ART)}</span></div>
    {duo("5-crew", "", f"<p>{e(x['crew_p'])}</p>")}
    <ul class="so-crew">{crew}</ul>
    {duo("7-raid", x["raid_h"], f"<p>{e(x['raid_p'])}</p><p class='so-mini'>{e(x['skins_l'])}: {e(x['skins'])}</p>")}
  </div></section>
'''
    after = f'''
  <section class="so-gap"><div class="so-wrap">
    <div class="so-bar"><h2>{ic(d, "bell")}{e(x["video_h"])}</h2><span>{len(x["videos"])}</span></div>
    <ul class="so-vids">{vids}</ul>{f'<p class="so-note">{e(x["video_note"])}</p>' if x["video_note"] else ""}
  </div></section>

  <section><div class="so-wrap">
    <div class="so-presscard">
      <img src="{r("img/nyang/pal-wave.webp")}" width="190" height="200" alt="">
      <div><h2>{e(x["press"])}{e(x["press_note"])}</h2><p>{e(x["presscard_p"])}</p>
      <p><a class="so-store" href="{r("nyangachi/press/")}">{e(x["presscard_a"])} →</a></p></div>
    </div>
  </div></section>
'''
    feats = "".join(
        f'\n      <li><img src="{r("img/nyang/shot-" + k + ".webp")}" width="390" height="780" loading="lazy" alt=""><span class="so-item-no">{i + 1:02d}</span><h3>{e(h)}</h3><p>{e(p)}</p></li>'
        for i, (k, h, p) in enumerate(t["n_feats"]))
    out = page_head(lang, "nyangachi/", d, t["n_title"], t["n_desc"], "img/nyang/feature.webp", "#63BEFF", ld)
    out += head_html(lang, "nyangachi/", d) + f'''
<main id="main">
  <section class="so-ghero"><div class="so-wrap so-ghero-row">
    {art}
    <div>
      <h1>{e(t["nyang"])}</h1>
      <p class="so-tag">{e(t["n_tag"])}</p>
      <p class="so-sub">{e(t["nyang_lead"])} {e(t["nyang_sub"])}</p>
      <p>{state_html(t, g)} <a class="so-store" href="{appstore(lang)}">App Store ↗</a> <a class="so-store so-store-light" href="{r("nyangachi/press/")}">{e(x["press"])}{e(x["press_note"])} →</a></p>
    </div>
  </div></section>

  <section class="so-gap"><div class="so-wrap">
    <div class="so-bar"><h2>{ic(d, "can")}{e(t["n_feat_k"])}</h2><div class="so-pals" aria-hidden="true"><img src="{r("img/nyang/pal-sit.webp")}" width="180" height="200" alt=""></div></div>
    <div class="so-split">
      <p>{e(t["n_feat_h"])}</p>
      <dl class="so-rows so-note-card">
        <div><dt>{ic(d, "box")}{e(t["l_platform"])}</dt><dd>{g["platform"]}</dd></div>
        <div><dt>{ic(d, "claw")}{e(t["l_genre"])}</dt><dd>{e(t["nyang_genre"])}</dd></div>
        <div><dt>{ic(d, "flag")}{e(t["l_status"])}</dt><dd>{e(t["n_news_p"])}</dd></div>
        <div><dt>{ic(d, "feather")}{e(t["l_contact"])}</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
        <div><dt>{ic(d, "bell")}{e(t["l_policy"])}</dt><dd><a href="privacy.html">{e(t["f_privacy"])}</a></dd></div>
      </dl>
    </div>
  </div></section>

{more}
  <section><div class="so-wrap">
    <div class="so-bar"><h2>{ic(d, "coin")}{e(t["n_shots_h"])}</h2><span>{len(t["n_feats"])}</span></div>
    <ol class="so-feats">{feats}
    </ol>
    <p class="so-note">{e(t["n_shots_note"])}</p>
  </div></section>
{after}
</main>

''' + foot_html(lang, d) + "\n</body>\n</html>\n"
    write(v[0] + "nyangachi/index.html", out)


def jstr(s):
    import json
    return json.dumps(s, ensure_ascii=False)


def build_startup(lang):
    """예전 첫 화면(스타트업 키우기 소개)을 startup/ 아래로 옮긴다. 본문은 그대로, 주소와 머리·꼬리만 바꾼다."""
    v = LANGS[lang]
    d = 2 if v[0] else 1
    with open(os.path.join(STARTUP_SRC, lang + ".html"), encoding="utf-8") as f:
        src = f.read()
    old_url = SITE + v[0]
    # 1) 상대 주소를 한 칸 더 깊게
    def deeper(m):
        attr, val = m.group(1), m.group(2)
        if re.match(r"(https?:|mailto:|#|data:|//)", val):
            return m.group(0)
        return '%s="../%s"' % (attr, val)
    out = re.sub(r'\b(href|src|poster)="([^"]*)"', deeper, src)
    # 2) 이 페이지 자신의 주소(canonical, og:url, hreflang, 게임 url)
    for x in LANGS.values():
        out = out.replace('hreflang="%s" href="%s"' % (x[2], SITE + x[0]), 'hreflang="%s" href="%sstartup/"' % (x[2], SITE + x[0]))
    out = out.replace('hreflang="x-default" href="%sen/"' % SITE, 'hreflang="x-default" href="%sen/startup/"' % SITE)
    out = out.replace('<link rel="canonical" href="%s">' % old_url, '<link rel="canonical" href="%sstartup/">' % old_url)
    out = out.replace('<meta property="og:url" content="%s">' % old_url, '<meta property="og:url" content="%sstartup/">' % old_url)
    out = out.replace('"url": "%s",\n  "operatingSystem"' % old_url, '"url": "%sstartup/",\n  "operatingSystem"' % old_url)
    # 3) 머리·꼬리·공통 스타일
    out = re.sub(r"<!-- i18n:langbar -->.*?<!-- /i18n:langbar -->\n", "", out, flags=re.S)
    out, n1 = re.subn(r'<header class="top">.*?</header>', lambda m: head_html(lang, "startup/", d), out, flags=re.S)
    out, n2 = re.subn(r'<footer class="foot">.*?</footer>', lambda m: foot_html(lang, d), out, flags=re.S)
    out, n3 = re.subn(r'(<link rel="stylesheet" href="[./]*lang\.css">)', lambda m: m.group(1) + '\n' + cute_font(lang) + '<link rel="stylesheet" href="%s">' % rel(d, "site.css"), out, count=1)
    assert (n1, n2, n3) == (1, 1, 1), (lang, n1, n2, n3)
    # 보도자료실·자주 묻는 질문·확률 안내로 가는 카드
    t = T[lang]
    card_p = {"ko": "게임 소개, 언어별 이름, 게임 화면을 한곳에 모았어요. 자주 묻는 질문과 확률 안내도 여기서 볼 수 있어요.",
              "en": "The game summary, its name in each language and screenshots, all in one place. The FAQ and probabilities are here too.",
              "ja": "ゲーム紹介、言語別のタイトル、ゲーム画面をまとめています。よくある質問と確率表記もこちらからどうぞ。",
              "zh-tw": "遊戲介紹、各語言名稱和遊戲畫面都整理在這裡。常見問題和機率公告也可以從這裡查看。"}[lang]
    card = (f'<section><div class="so-wrap"><div class="so-presscard"><img src="{rel(d, "img/lp/hire-cat-a.png")}" width="114" height="114" alt="" style="image-rendering:pixelated">'
            f'<div><h2>{e(t["f_press"])}</h2><p>{e(card_p)}</p>'
            f'<p><a class="so-store" href="{rel(d, v[0] + "press-kit.html")}">{e(t["f_press"])} →</a> '
            f'<a class="so-store so-store-light" href="{rel(d, v[0] + "faq.html")}">{e(t["f_faq"])}</a> '
            f'<a class="so-store so-store-light" href="{rel(d, v[0] + "probability.html")}">{e(t["f_prob"])}</a></p></div></div></div></section>\n')
    out, n4 = re.subn(r"</main>", lambda m: card + "</main>", out, count=1)
    assert n4 == 1
    write(v[0] + "startup/index.html", out)


# 옛 스타트업 문서(faq·press-kit·privacy·probability·support) 본문 원본은 tools/startup_src/docs/{언어}/ (옛 저장소 커밋 870dafa 에서 2026-11-19 옮겨 둠)
OLD_DOCS = ["faq.html", "press-kit.html", "privacy.html", "probability.html", "support.html"]


def build_startup_doc(lang, page):
    """옛 스타트업 키우기 문서의 머리·꼬리만 새것으로 바꾼다. 본문(방침·확률 글)은 한 글자도 건드리지 않는다.
    주소도 그대로다(스토어와 게임이 이 주소를 쓴다)."""
    v = LANGS[lang]
    d = 1 if v[0] else 0
    t = T[lang]
    with open(os.path.join(STARTUP_SRC, "docs", lang, page), encoding="utf-8") as f:
        src = f.read()
    out = re.sub(r"<!-- i18n:langbar -->.*?<!-- /i18n:langbar -->\n?", "", src, flags=re.S)
    out = re.sub(r'<nav class="lang-bar".*?</nav>\n?', "", out, flags=re.S)
    back = '<p class="so-doc-back so-old-back"><a href="%s">← %s</a></p>' % (rel(d, v[0] + "startup/"), e(t["startup"]))
    out, n1 = re.subn(r'<header class="(?:top|page-head)">.*?</header>', lambda m: head_html(lang, page, d), out, count=1, flags=re.S)
    out, n2 = re.subn(r'<footer class="foot">.*?</footer>', lambda m: foot_html(lang, d), out, count=1, flags=re.S)
    out, n3 = re.subn(r"<main>", lambda m: '<main id="main">' + back, out, count=1)
    out, n4 = re.subn(r'(<link rel="stylesheet" href="[./]*lang\.css">)', lambda m: m.group(1) + '\n' + cute_font(lang) + '<link rel="stylesheet" href="%s">' % rel(d, "site.css"), out, count=1)
    out, n5 = re.subn(r"<body([^>]*)>", lambda m: ('<body class="so-old %s">' % re.sub(r'.*class="([^"]*)".*', r"\1", m.group(1)) if "class=" in m.group(1) else '<body class="so-old">')
                      + '\n<a class="so-skip" href="#main">%s</a>' % e(t["skip"]), out, count=1)
    assert (n1, n2, n3, n4, n5) == (1, 1, 1, 1, 1), (lang, page, n1, n2, n3, n4, n5)
    write(v[0] + page, out)


def build_nyang_privacy(lang):
    """냥아치 키우기 방침 페이지. 글은 tools/privacy_nyang.py 에 있다."""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from privacy_nyang import P
    c = P[lang]
    t = T[lang]
    v = LANGS[lang]
    d = 2 if v[0] else 1
    page = "nyangachi/privacy.html"
    out = page_head(lang, page, d, c["title"] + " — Studio Oct", c["summary"][0], "img/nyang/feature.webp", "#FFFDF8")
    body = "".join("\n    <h2>%s</h2>%s" % (e(h), "".join("\n    <p>%s</p>" % p for p in ps)) for h, ps in c["sections"])
    tr = '\n    <p class="so-doc-note">%s</p>' % (c["translated"] % rel(d, page)) if c["translated"] else ""
    out += head_html(lang, page, d) + f'''
<main id="main"><div class="so-wrap so-doc">
    <p class="so-doc-back"><a href="{rel(d, v[0] + "nyangachi/")}">← {e(t["nyang"])}</a></p>
    <h1>{e(c["title"])}</h1>
    <p class="so-doc-date">{e(c["date"])}</p>{tr}{"".join('<p class="so-doc-note so-doc-change">%s</p>' % e(x) for x in c.get("change", []))}
    <p>{c["intro"]}</p>
    <p class="so-doc-note">{c["other"] % rel(d, v[0] + "privacy.html")}</p>
    <h2>{e(c["sum_h"])}</h2>
    <ul>{"".join("<li>%s</li>" % e(x) for x in c["summary"])}</ul>{body}
</div></main>

''' + foot_html(lang, d) + "\n</body>\n</html>\n"
    write(v[0] + page, out)
    # 기존 방침 맨 위에 안내 한 줄(이미 있으면 그대로 둔다). 기존 방침의 다른 글은 건드리지 않는다.
    old = os.path.join(ROOT, v[0] + "privacy.html")
    src = open(old, encoding="utf-8").read()
    if "<!-- nyangachi-notice -->" not in src:
        line = '<!-- nyangachi-notice --><p class="notice">%s</p>\n' % (c["notice"] % "nyangachi/privacy.html")
        assert src.count("<h1>") == 1
        with open(old, "w", encoding="utf-8") as f:
            f.write(src.replace("<h1>", line + "<h1>"))
        print("added notice to", v[0] + "privacy.html")


PRESS_SHOTS = [("1-fight", "골목 싸움"), ("2-boss", "지역 대장"), ("4-turf", "한국·대만 지도"),
               ("5-crew", "동료"), ("6-gacha", "장비·기술 뽑기"), ("7-raid", "주간 레이드"), ("8-away", "자리 비운 동안 모인 자릿세"), ("3-human", "골목 사람들")]
PRESS_VIDEOS = [("idea2-skills-ko", "기술 모음", 13), ("idea3-oneminute-ko", "1분 플레이", 60), ("hook-charm-ko", "골목 사람들", 17)]


def build_nyang_press():
    """냥아치 키우기 보도자료 쪽(한국어만). 파일은 nyangachi/press/files/ 에 있다.
    zip 은 손으로 만든다: nyangachi-press-ko.zip(아이콘·가로 그림·한국어 스크린샷·13·17초 영상·README-ko.txt),
    nyangachi-screens-{en,ja,zh-tw}.zip(언어별 스크린샷)."""
    lang, d, page = "ko", 2, "nyangachi/press/"
    t = T[lang]
    F = "files/"
    mb = lambda p: "%.0fMB" % (os.path.getsize(os.path.join(ROOT, page, p)) / 1e6) if os.path.getsize(os.path.join(ROOT, page, p)) >= 1e6 else "%.1fMB" % (os.path.getsize(os.path.join(ROOT, page, p)) / 1e6)
    title = "냥아치 키우기 보도자료 — Studio Oct"
    desc = "냥아치 키우기 보도자료와 그림·영상 내려받기. 서울 골목의 턱시도 고양이가 한국 여덟 지역을 접수하고, 상자에서 자다 깼더니 대만에 와 있는 세로 화면 방치형 RPG예요."
    out = page_head(lang, page, d, title, desc, "img/nyang/feature.webp", "#FFFDF8")
    out = re.sub(r"<!-- i18n:hreflang -->.*?<!-- /i18n:hreflang -->\n", "", out, flags=re.S)  # 한국어판만 있다
    head = head_html(lang, "nyangachi/", d).replace('href="../../nyangachi/" hreflang="ko"', 'href="./" hreflang="ko"')
    glance = [
        ("이름", "냥아치 키우기"),
        ("장르", "세로 화면 방치형 RPG"),
        ("만든 곳", "Studio Oct (서울)"),
        ("출시", "iOS 2026년 11월 13일 (한국·일본·대만·미국). 1.1.0 업데이트로 대만 편이 더해졌어요. 안드로이드는 준비 중이에요."),
        ("값", "무료. 인앱 구매와 보상형 광고(누를 때만 나와요, 배너·전면 광고 없음). 확률형 아이템이 있어요."),
        ("앱스토어", '<a href="%s">앱스토어에서 보기</a>' % e(APPSTORE_CT % "press")),
        ("문의", f'<a href="mailto:{MAIL}">{MAIL}</a>'),
    ]
    points = [
        ("동네 짐승은 패서 이겨요.", "비둘기·들개부터 반달곰까지, 한국과 대만에 실제로 사는 동물 약 90종이 상대와 대장으로 나와요. 대장은 직접 두들겨 패서 이겨야 그 구역을 접수해요."),
        ("한국 골목에서 대만까지.", "서울·경기·충청·전라·경상·부산·강원·태백 여덟 지역 240스테이지를 다 접수하면 상자 속에서 잠든 채 배에 실려 대만으로 가요. 타이베이·타이중·시뤄·타이난·가오슝 다섯 곳 150스테이지(1.1.0). 곳마다 그 땅의 동물과 대장이 나오고, 가오슝까지 끝내면 시뤄의 매 사부가 새 기술 \"비껴치기\"를 가르쳐 줘요."),
        ("광고는 원할 때만.", "보상형 광고만 있고 화면을 덮는 광고는 없어요. 뽑기 확률은 게임 안에서 바로 볼 수 있어요. 배경음악은 소리 파일 없이 악보를 계산해 만들어요."),
    ]
    more = [
        "가만히 둬도 알아서 싸우고, 화면을 누르면 냥펀치가 더 나가요. 상대는 무리로 몰려오고 큰 기술 한 방에 여러 마리가 날아가요.",
        "접수한 동네에서 자릿세가 쌓여요. 꺼 둔 동안에도 8시간치까지 모여요.",
        "동료 열. 한국의 치즈, 짹이, 도토리, 콩이, 삼색이와 대만의 란란, 루루, 뉴뉴, 스후, 허우. 셋은 데리고 다니고 나머지는 파견을 보내요.",
        "주간 레이드: 쓰러지지 않는 거대 보스 \"집채 황소\"를 때려 넣은 피해로 한 주 순위를 겨뤄요.",
        "스킨: 턱시도, 치즈, 봄베이, 노르웨이숲, 페르시안.",
    ]
    shots = "".join(
        f'\n      <li><a href="{F}ko/{k}.png"><img src="{F}thumb/{k}.webp" width="360" height="780" loading="lazy" alt="{e(c)} 화면"></a><span>{e(c)}</span></li>'
        for k, c in PRESS_SHOTS)
    vids = "".join(
        f'\n      <li><video controls playsinline preload="none" width="1080" height="1920" poster="{F}thumb/{k}.webp" src="{F}video/{k}.mp4"></video>'
        f'<span>{e(c)} · {s}초 · <a href="{F}video/{k}.mp4" download>내려받기 ({mb(F + "video/" + k + ".mp4")})</a></span></li>'
        for k, c, s in PRESS_VIDEOS)
    others = " · ".join(f'<a href="{F}nyangachi-screens-{l}.zip" download>{n} ({mb(F + "nyangachi-screens-" + l + ".zip")})</a>'
                        for l, n in (("en", "영어"), ("ja", "일본어"), ("zh-tw", "번체 중국어")))
    out += head + f'''
<main id="main"><div class="so-wrap so-doc so-press">
    <p class="so-doc-back"><a href="../">← {e(t["nyang"])}</a></p>
    <h1>냥아치 키우기 보도자료</h1>
    <p class="so-doc-date">자료 기준: 1.1.0 대만 편</p>
    <p>서울 골목의 턱시도 고양이 "냥아치"가 동네 짐승들을 제압하며 한국 여덟 지역을 접수하고, 상자에서 자다 깼더니 대만에 와 있는 방치형 RPG예요.</p>
    <p class="so-press-all"><a class="so-press-btn" href="{F}nyangachi-press-ko.zip" download>한 번에 내려받기 (zip, {mb(F + "nyangachi-press-ko.zip")})</a></p>
    <p class="so-doc-note">아이콘, 가로 대표 그림, 한국어 스크린샷 8장, 13초·17초 영상, 이 쪽의 글이 들어 있어요. 60초 영상은 아래에서 따로 받아 주세요. 기사와 소개 글에 자유롭게 쓰셔도 돼요.</p>

    <h2>한눈에</h2>
    <dl class="so-rows so-note-card">{"".join(f"<div><dt>{e(k)}</dt><dd>{v if k in ('앱스토어', '문의') else e(v)}</dd></div>" for k, v in glance)}</dl>

    <h2>기자가 쓸 만한 점 세 가지</h2>
    <ol>{"".join(f"<li><b>{e(h)}</b> {e(p)}</li>" for h, p in points)}</ol>

    <h2>그 밖의 내용</h2>
    <ul>{"".join(f"<li>{e(x)}</li>" for x in more)}</ul>

    <h2>그림</h2>
    <ul class="so-press-art">
      <li><a href="{F}icon-1024.png"><img src="{F}thumb/icon.webp" width="256" height="256" alt="앱 아이콘"></a><span>앱 아이콘 1024×1024 · <a href="{F}icon-1024.png" download>PNG ({mb(F + "icon-1024.png")})</a></span></li>
      <li class="so-press-wide"><a href="{F}header-3840x1646.png"><img src="{F}thumb/header.webp" width="1200" height="514" loading="lazy" alt="가로 대표 그림"></a><span>가로 대표 그림 3840×1646 · <a href="{F}header-3840x1646.png" download>PNG ({mb(F + "header-3840x1646.png")})</a></span></li>
    </ul>

    <h2>스크린샷 (한국어, 1290×2796)</h2>
    <p class="so-doc-note">그림을 누르면 원본 PNG가 열려요.</p>
    <ol class="so-press-shots">{shots}
    </ol>
    <p>다른 언어 스크린샷 묶음: {others}</p>

    <h2>대만 편 (1.1.0)</h2>
    <ul class="so-press-art so-press-tw">
      <li><a href="{F}tw/shot1-tw-1290x2796.png"><img src="{F}thumb/tw-1.webp" width="360" height="780" loading="lazy" alt="대만 편 번체 첫 스크린샷"></a><span>번체 첫 스크린샷 1290×2796 · <a href="{F}tw/shot1-tw-1290x2796.png" download>PNG ({mb(F + "tw/shot1-tw-1290x2796.png")})</a></span></li>
      <li><video controls playsinline preload="none" width="1920" height="1280" poster="{F}thumb/search-tw.webp" src="{F}tw/search-tw-1920x1280-zh-TW.mp4"></video><span>대만 앱스토어 검색 결과 영상 1920×1280 · <a href="{F}tw/search-tw-1920x1280-zh-TW.mp4" download>MP4 ({mb(F + "tw/search-tw-1920x1280-zh-TW.mp4")})</a></span></li>
    </ul>

    <h2>영상 (세로 1080×1920)</h2>
    <ul class="so-press-vids">{vids}
    </ul>
</div></main>

''' + foot_html(lang, d) + "\n</body>\n</html>\n"
    write(page + "index.html", out)


COUPON_DB = "https://firestore.googleapis.com/v1/projects/nyangachi-studiooct/databases/(default)/documents"


def build_nyang_coupon(lang):
    """웹 쿠폰 페이지(아이폰은 앱 안에서 코드를 못 넣는다). 글은 tools/coupon_nyang.py 에 있다.
    로그인 없이 redeem/{회원 번호}/codes/{코드} = {t: 서버 시각} 하나를 만든다. 없는·지난·이미 쓴 코드는 서버 규칙이 거절한다."""
    import json
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from coupon_nyang import C
    c = C[lang]
    t = T[lang]
    v = LANGS[lang]
    d = 2 if v[0] else 1
    page = "nyangachi/coupon.html"
    out = page_head(lang, page, d, c["title"] + " — " + t["nyang"], c["desc"].format(game=t["nyang"]), "img/nyang/feature.webp", "#FFFDF8")
    msg = json.dumps({k: c[k] for k in ("bad_id", "bad_code", "ok", "used", "fail", "net", "busy", "go")}, ensure_ascii=False)
    out += head_html(lang, page, d) + f'''
<main id="main"><div class="so-wrap so-doc so-coupon">
    <p class="so-doc-back"><a href="{rel(d, v[0] + "nyangachi/")}">← {e(t["nyang"])}</a></p>
    <h1>{e(c["title"])}</h1>
    <p>{e(c["intro"])}</p>
    <form id="cp" novalidate>
      <label for="cp-id">{e(c["id_l"])}</label>
      <input id="cp-id" name="id" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" maxlength="64" required>
      <label for="cp-code">{e(c["code_l"])}</label>
      <input id="cp-code" name="code" autocomplete="off" autocapitalize="characters" autocorrect="off" spellcheck="false" maxlength="16" placeholder="{e(c["code_ph"])}" required>
      <button class="so-press-btn" type="submit">{e(c["go"])}</button>
      <p id="cp-msg" class="so-coupon-msg" role="status" aria-live="polite"></p>
    </form>
    <h2>{e(c["how_h"])}</h2>
    <ol>{"".join("<li>%s</li>" % e(x) for x in c["how"])}</ol>
    <ul class="so-doc-note">{"".join("<li>%s</li>" % e(x) for x in c["notes"])}</ul>
</div></main>
<script>
(function () {{
  var DB = {json.dumps(COUPON_DB)}, M = {msg};
  var f = document.getElementById("cp"), idIn = document.getElementById("cp-id"), codeIn = document.getElementById("cp-code"),
      out = document.getElementById("cp-msg"), btn = f.querySelector("button");
  try {{ idIn.value = localStorage.getItem("nyang_member") || ""; }} catch (x) {{}}
  function say(text, kind) {{ out.textContent = text; out.className = "so-coupon-msg" + (kind ? " is-" + kind : ""); }}
  f.addEventListener("submit", function (ev) {{
    ev.preventDefault();
    var id = idIn.value.replace(/\\s+/g, ""), code = codeIn.value.replace(/\\s+/g, "").toUpperCase();
    if (!/^[A-Za-z0-9]{{20,40}}$/.test(id)) {{ say(M.bad_id, "bad"); idIn.focus(); return; }}
    if (!/^[A-Z0-9]{{4,16}}$/.test(code)) {{ say(M.bad_code, "bad"); codeIn.focus(); return; }}
    idIn.value = id; codeIn.value = code;
    try {{ localStorage.setItem("nyang_member", id); }} catch (x) {{}}
    var name = DB.replace("https://firestore.googleapis.com/v1/", "") + "/redeem/" + id + "/codes/" + code;
    var body = {{ writes: [{{ update: {{ name: name, fields: {{}} }}, currentDocument: {{ exists: false }},
      updateTransforms: [{{ fieldPath: "t", setToServerValue: "REQUEST_TIME" }}] }}] }};
    btn.disabled = true; btn.textContent = M.busy; say("");
    fetch(DB + ":commit", {{ method: "POST", headers: {{ "Content-Type": "application/json" }}, body: JSON.stringify(body) }})
      .then(function (r) {{
        if (r.ok) {{ say(M.ok, "ok"); codeIn.value = ""; return; }}
        return r.json().catch(function () {{ return {{}}; }}).then(function (j) {{
          var st = (j && j.error && j.error.status) || "";
          if (r.status === 409 || st === "ALREADY_EXISTS") say(M.used, "bad");
          else if (r.status === 400 || r.status === 403 || r.status === 404) say(M.fail, "bad");
          else say(M.net, "bad");
        }});
      }}, function () {{ say(M.net, "bad"); }})
      .then(function () {{ btn.disabled = false; btn.textContent = M.go; }});
  }});
}})();
</script>

''' + foot_html(lang, d) + "\n</body>\n</html>\n"
    write(v[0] + page, out)


def build_sitemap():
    pages = ["", "startup/", "nyangachi/", "nyangachi/privacy.html", "nyangachi/coupon.html", "faq.html", "press-kit.html", "privacy.html", "probability.html", "support.html"]
    urls = sorted([SITE + v[0] + p for v in LANGS.values() for p in pages] + [SITE + "nyangachi/press/"])
    body = "".join("  <url>\n    <loc>%s</loc>\n  </url>\n" % u for u in urls)
    write("sitemap.xml", "<?xml version='1.0' encoding='utf-8'?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n%s</urlset>" % body)


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", path)


if __name__ == "__main__":
    for lang in LANGS:
        build_home(lang)
        build_nyang(lang)
        build_startup(lang)
        for page in OLD_DOCS:
            build_startup_doc(lang, page)
        build_nyang_privacy(lang)
        build_nyang_coupon(lang)
    build_nyang_press()
    build_sitemap()
