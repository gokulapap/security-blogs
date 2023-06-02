import os
import sys
import telebot

def main():
    telegram_token = sys.argv[1]
    chat_id = sys.argv[2]

    # Read queue.md file
    queue_file_path = os.path.join(os.getcwd(), 'queue.md')
    with open(queue_file_path, 'r') as queue_file:
        lines = queue_file.readlines()

    # Get the first 5 lines and process them
    lines_to_process = lines[:5]
    processed_lines = []

    for line in lines_to_process:
        line_parts = line.strip().split(', ')
        if len(line_parts) == 2:
            link, category = line_parts
            category_folder = os.path.join(os.getcwd(), category)

            # Check if the category folder exists, otherwise create it
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)

            # Save the line to links.md in the category folder
            links_file_path = os.path.join(category_folder, 'links.md')
            with open(links_file_path, 'a') as links_file:
                links_file.write(f'{line}\n')

            processed_lines.append(line)

    # Remove the processed lines from the queue.md file
    with open(queue_file_path, 'w') as queue_file:
        queue_file.writelines(lines[5:])

    # Alert via Telegram bot
    if processed_lines:
        bot = telebot.TeleBot(telegram_token)
        message = 'Blogs you need to read Today :\n\n' + '\n'.join(processed_lines)
        bot.send_message(chat_id, message)
    else:
        bot = telebot.TeleBot(telegram_token)
        bot.send_message(chat_id, "⚠️ NO MORE ARTICLES IN THE QUEUE, ADD THE BLOG LINKS IN THE QUEUE ⚠️")

if __name__ == '__main__':
    main()
