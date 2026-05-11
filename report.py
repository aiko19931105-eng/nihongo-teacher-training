import anthropic
import requests
import os
from datetime import datetime

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
team_webhook = os.environ["DISCORD_WEBHOOK_URL"]
personal_webhook = os.environ["DISCORD_PERSONAL_WEBHOOK_URL"]

context = """
あなたはAikoさんの日本語教師養成講座プロジェクトチームです。
- Aikoさんはパリ在住、インスタ2.6万フォロワー
- 5月末に講座募集予定（目標20〜30人、30万円以上）
- 現金残高250万、毎月固定費160万
- ペルソナ：30〜40代、海外移住したい、収入不安な女性
- 集客はインスタ100%（@aiko.paris）
- 今月やること：共感投稿3本、コンサル生インタビューライブ
"""

team_members = [
    ("とんこつ", "マーケター担当", "今日のインスタ投稿アイデアを箇条書き3点のみで完結に答えてください。"),
    ("わさび", "コンテンツ担当", "講座資料の改善アイデアを箇条書き3点のみで完結に答えてください。"),
]

personal_members = [
    ("ごま", "リーダー・戦略担当", "今日の最優先タスクを箇条書き3点のみで完結に答えてください。現金残高250万、固定費月160万を踏まえて。"),
    ("からし", "反対意見担当", "今の計画のリスクを箇条書き3点のみで完結に答えてください。財務状況も踏まえて率直に。"),
]

def send_to_discord(webhook, messages):
    full_message = "\n".join(messages)
    chunks = [full_message[i:i+1900] for i in range(0, len(full_message), 1900)]
    for chunk in chunks:
        requests.post(webhook, json={"content": chunk})

def generate_report(members):
    messages = []
    for name, role, prompt in members:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": context + "\nあなたは" + name + "（" + role + "）です。" + prompt
                }
            ]
        )
        text = response.content[0].text
        messages.append("\n## " + name + " (" + role + ")\n" + text + "\n")
    return messages

date_str = datetime.now().strftime("%Y年%m月%d日")

team_messages = ["# Aikoチーム定期報告 " + date_str + "\n"]
team_messages += generate_report(team_members)
send_to_discord(team_webhook, team_messages)

personal_messages = ["# Aikoさんへの経営レポート " + date_str + "\n"]
personal_messages += generate_report(personal_members)
send_to_discord(personal_webhook, personal_messages)

print("Discord送信完了！")
