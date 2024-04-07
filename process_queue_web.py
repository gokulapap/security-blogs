import os
import sys
import telebot
import random
import requests

def send_slack_alert(webhook_url, message):
    payload = {
        "text": message
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("Slack alert sent successfully")
    else:
        print("Failed to send Slack alert")

def main():
    telegram_token = sys.argv[1]
    chat_id = sys.argv[2]
    chat_ids = ['1214546863','1309362123', '1338786380', '1551270031', '5733169306', '1452475940', '5589889222', '803127855', '1048207326', '766621469', '703153391','1153543502','1081075130','1966029855', '1915797756', '1186054020', '1008678344', '574311101', '1380636569', '2033286410', '5093483274', '991707921', '5964575914', '912247136', '857929726']
    slack_webhook_url = sys.argv[3]

    # Read queue.md file
    queue_file_path = os.path.join(os.getcwd(), 'a_queue.md')
    with open(queue_file_path, 'r') as queue_file:
        lines = queue_file.readlines()

    # Choose 5 random lines to process
    num_lines_to_process = min(5, len(lines))  # Ensure we don't select more lines than available
    random_lines_indices = random.sample(range(len(lines)), num_lines_to_process)
    lines_to_process = [lines[i] for i in random_lines_indices]
    processed_lines = []

    for line in lines_to_process:
        line_parts = line.strip().split(', ')
        if len(line_parts) == 2:
            link, category = line_parts
            category_folder = os.path.join(os.getcwd(), 'web-security', category)  # Modified folder path

            t = line.split(" ")
            line = t[1].strip(",") + "\n[{}]".format(t[2])
            line = link.lstrip("- ") + f"\n[{category}]"

            # Check if the category folder exists, otherwise create it
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)

            # Save the line to links.md in the category folder
            links_file_path = os.path.join(category_folder, 'links.md')
            with open(links_file_path, 'a') as links_file:
                t = link.lstrip("- ")
                links_file.write(f'- {t}\n')

            processed_lines.append(line)

    # Remove the processed lines from the queue.md file
    with open(queue_file_path, 'w') as queue_file:
        queue_file.writelines([line for i, line in enumerate(lines) if i not in random_lines_indices])

    # Alert via Telegram bot
    if processed_lines:
        bot = telebot.TeleBot(telegram_token)
        message = '📙 Blogs you need to read Today 📙\n\n✅ ' + '\n\n✅ '.join(processed_lines)
        for sid in chat_ids:
            try:
                bot.send_message(sid, message)
            except:
                print("[-] Error for ", sid, "\n")
        # Alert via Slack webhook
        message_slack = '📙 Blogs you need to read Today 📙\n\n✅ ' + '\n\n✅ '.join(processed_lines)
        send_slack_alert(slack_webhook_url, message_slack)
    else:
        bot = telebot.TeleBot(telegram_token)
        bot.send_message(chat_id, "⚠️ NO MORE ARTICLES IN THE QUEUE, ADD THE BLOG LINKS IN THE QUEUE ⚠️", disable_web_page_preview=True)
        send_slack_alert(slack_webhook_url, "⚠️ NO MORE ARTICLES IN THE QUEUE, ADD THE BLOG LINKS IN THE QUEUE ⚠️")
        
if __name__ == '__main__':
    main()
