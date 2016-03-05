import textwrap
import config
import color


def Message(new_msg, color=color.white):
    new_msg_lines = textwrap.wrap(new_msg, config.message_width)

    for line in new_msg_lines:
        if len(config.game_msgs) == config.message_height:
            del config.game_msgs[0]

        config.game_msgs.append((line, color))
