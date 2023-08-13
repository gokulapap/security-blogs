import os
import sys
import telebot
import random

def main():
    telegram_token = sys.argv[1]
    chat_id = sys.argv[2]

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
        message = 'Blogs you need to read Today :\n\n' + '\n\n'.join(processed_lines)
        bot.send_message(chat_id, message)
    else:
        bot = telebot.TeleBot(telegram_token)
        bot.send_message(chat_id, "⚠️ NO MORE ARTICLES IN THE QUEUE, ADD THE BLOG LINKS IN THE QUEUE ⚠️", disable_web_page_preview=True)

if __name__ == '__main__':
    main()
