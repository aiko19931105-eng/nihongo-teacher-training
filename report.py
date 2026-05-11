import anthropic
import requests
import os
from datetime import datetime

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

context = """
あなたはAikoさんの日本語教師養成講座プロジェクトチームです。
- Aikoさんはパリ在住、インスタ2.6万フォロワー
- 5月末に講座募集予定（目標20〜30人、30万円以上）
- 現金残高250万、毎月固定費160万
- ペルソナ：30〜40代、海外移住したい、収入不安な女性
- 集客はインスタ100%（@aiko.paris）
- 今月やること：共感投稿3本、コンサル生インタビューライブ
"""

members = [
    ("ごま", "リーダー・戦略担当", "今日の最優先タスクと売上に直結する戦略的アドバイスを1つ提案してください。"),
    ("とんこつ", "マーケター担当", "今日のインスタ投稿案またはストーリーズのアイデアを1つ具体的に提案してください。"),
    ("わさび", "コンテンツ担当", "講座資料や教材の改善アイデアを1つ提案してください。"),
    ("からし", "反対意見担当", "今の計画で見落としているリスクや甘い部分を1つ指摘してください。"),
]

messages = ["# Aikoチーム定期報告\n"]
messages.append(datetime.now().strftime("%Y年%m月%d日") + "\n")

for name, role, prompt in members:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": context + "\nあなたは" + name + "（" + role + "）です。" + prompt
            }
        ]
    )
    text = response.content[0].text
    messages.append("\n## " + name + " (" + role + ")\n" + text + "\n")

full_message = "\n".join(messages)

chunks = [full_message[i:i+1900] for i in range(0, len(full_message), 1900)]
for chunk in chunks:
    requests.post(webhook_url, json={"content": chunk})

print("Discordに送信完了！")
