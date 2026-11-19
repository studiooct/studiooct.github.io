"""맨 위 페이지(index.html) 냥아치 칸들의 글(네 언어). 2026-11-18 대표님 승인 시안(IljjangNyang art/concepts/homepage-mock-1118.png).

소식(NEWS)은 갈아 끼우기 쉬운 칸이다. 새 소식이 생기면 NEWS 맨 앞에 한 줄 더하고 오래된 것을 지운다(두 칸만 보인다).
  예: 다음 빌드가 스토어에 나온 뒤 "환영 보따리" 소식으로 바꾼다. 빌드가 켜지기 전엔 넣지 않는다.
공식 채널(CHANNELS)은 주소가 None 이면 단추를 그리지 않는다.
숫자 네 칸은 nyang_more.NX 의 stats 를 같이 쓴다. 쿠폰 칸 글은 coupon_nyang.C 의 title·intro 를 같이 쓴다.
"""

# (화면 그림 이름, 제목, 한 줄). 그림은 img/nyang/store/{언어}/{이름}.webp
SHOTS = {
    "ko": [("1-fight", "골목 싸움", "가만히 둬도 알아서 싸우고, 누르면 냥펀치가 더 나가요."),
           ("2-boss", "지역 대장", "지역마다 이름 있는 대장을 패서 이겨야 그 구역을 접수해요."),
           ("4-turf", "한국·대만 지도", "한국 여덟 지역을 지나 상자 속에서 잠든 채 대만까지 가요."),
           ("5-crew", "동료", "한국 다섯, 대만 다섯. 셋까지 데리고 다니며 함께 싸워요.")],
    "en": [("1-fight", "Alley fights", "Your cat fights on its own. Tap to throw extra cat punches."),
           ("2-boss", "Regional bosses", "Every area has a big-name boss. Beat them up to claim the turf."),
           ("4-turf", "Korea & Taiwan map", "Cross eight regions of Korea, then nap in a box all the way to Taiwan."),
           ("5-crew", "Crew", "Five from Korea, five from Taiwan. Take up to three into battle.")],
    "ja": [("1-fight", "路地裏バトル", "放っておいても勝手に戦う。タップすれば猫パンチをさらにお見舞い！"),
           ("2-boss", "各地のボス", "エリアごとに名の知れたボスが待っている。ぶっ倒せばそこは自分の縄張り！"),
           ("4-turf", "韓国・台湾マップ", "韓国の8つのエリアを巡ったら、箱の中で寝たまま台湾へ。"),
           ("5-crew", "仲間", "韓国の5匹と台湾の5匹。3匹まで連れて一緒に戦えます。")],
    "zh-tw": [("1-fight", "巷口開打", "放著也會自動開打，點一下還能多揮幾記貓拳。"),
              ("2-boss", "地區老大", "每個地區都有個響噹噹的老大，打趴牠才能拿下那一區的地盤。"),
              ("4-turf", "韓國與台灣地圖", "走完韓國八個地區後，在箱子裡睡著，一路被送到台灣。"),
              ("5-crew", "夥伴", "韓國五位、台灣五位，最多帶三位一起並肩作戰。")],
}

# (아이콘 img/nyang/ic-*.png, 주소(언어판 안 상대), 제목, 한 줄)
NEWS = {
    "ko": [("bundle", "nyangachi/", "1.2.0 출시 기념 환영 보따리", "7일 동안 무료 뽑기권 1,113장을 받아요. 서울 1-10을 깨면 열려요."),
           ("claw", "nyangachi/", "장비 대개편", "장비가 일곱 등급으로 바뀌고, 착용 장비 등급에 따라 오오라가 생겨요."),
           ("flag", "nyangachi/", "1.1.0 대만 편", "타이베이부터 가오슝까지 다섯 곳 150스테이지와 새 동료 다섯이 생겼어요."),
           ("trophy", None, "게임 센터 순위표", "1.1.1 업데이트로 최고 스테이지와 주간 레이드 순위를 게임 센터에서 겨뤄요.")],
    "en": [("bundle", "nyangachi/", "1.2.0: Launch Welcome Bundles", "1,113 free Pull Tickets over 7 days. Clear Seoul 1-10 to unlock."),
           ("claw", "nyangachi/", "Gear overhaul", "Gear has 7 grades. Rare gear or better gives your cat an aura."),
           ("flag", "nyangachi/", "1.1.0: Taiwan Chapter", "Five places from Taipei to Kaohsiung, 150 stages and five new crew members."),
           ("trophy", None, "Game Center leaderboards", "New in 1.1.1: compete for the top spots in Highest Stage and Weekly Raid on Game Center.")],
    "ja": [("bundle", "nyangachi/", "1.2.0 リリース記念ウェルカム風呂敷", "7日間でガチャ券1,113枚プレゼント。ソウル1-10クリアで解放。"),
           ("claw", "nyangachi/", "装備リニューアル", "装備が7つの等級に分かれ、身につけた装備の等級に応じてネコがオーラをまといます。"),
           ("flag", "nyangachi/", "1.1.0 台湾編", "台北から高雄まで、5つのエリアに150ステージ！新しい仲間も5匹登場。"),
           ("trophy", None, "Game Centerランキング", "1.1.1アップデートで、最高ステージと週間レイドの順位をGame Centerで競えるようになりました。")],
    "zh-tw": [("bundle", "nyangachi/", "1.2.0 上市紀念歡迎包袱", "7 天免費送 1,113 張轉蛋券，通關首爾 1-10 後解鎖。"),
              ("claw", "nyangachi/", "裝備大改版", "裝備改為七個等級，貓咪會依照身上裝備的等級散發氣場。"),
              ("flag", "nyangachi/", "1.1.0 台灣篇", "從台北到高雄共五個地方、150 個關卡，還有五位新夥伴。"),
              ("trophy", None, "Game Center 排行榜", "1.1.1 更新後，可以在 Game Center 比拚最高關卡和每週突襲排名。")],
}

CHANNELS = [  # (아이콘 글자, 주소, {언어: 이름})
    ("N", "https://game.naver.com/lounge/nyangachi/", {"ko": "네이버 게임 라운지", "en": "NAVER Game Lounge", "ja": "NAVER Game Lounge", "zh-tw": "NAVER Game Lounge"}),
    ("X", "https://x.com/nyangachi_game", {"ko": "X", "en": "X", "ja": "X", "zh-tw": "X"}),
    ("▶", "https://www.youtube.com/@nyangachi_game", {"ko": "유튜브", "en": "YouTube", "ja": "YouTube", "zh-tw": "YouTube"}),
]

H = {
    "ko": dict(shots_h="이런 게임이에요", news_h="소식", ch_h="공식 채널"),
    "en": dict(shots_h="What's the game like?", news_h="News", ch_h="Official channels"),
    "ja": dict(shots_h="どんなゲーム？", news_h="お知らせ", ch_h="公式チャンネル"),
    "zh-tw": dict(shots_h="遊戲特色", news_h="最新消息", ch_h="官方頻道"),
}
