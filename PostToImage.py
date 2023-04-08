import praw
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import textwrap


# create a Reddit instance
reddit = praw.Reddit(
    client_id="vnYa7jPGv1AW513cHv0V4Q",
    client_secret="9wTztNolLjdww3GNtiivhbpazWWsbw",
    user_agent="RedditToVideo",
)

# calculate the time filter for the past week
past_week = datetime.utcnow() - timedelta(weeks=1)

# get the top posts from the Ask subreddit for the past week
top_ask_posts = reddit.subreddit("Ask").top("week", limit=2)

# set the font and font size for the image text
font_path = "C:\\Windows\\Fonts\\Arial.ttf"
font_title = ImageFont.truetype(font_path, size=30)
font_body = ImageFont.truetype(font_path, size=24)
font_comment = ImageFont.truetype(font_path, size=18)

# set the image size and color
image_size = (1920, 1080)
image_color = (255, 255, 255)

# create an empty list to store the post images
images_list = []

# iterate through the top posts and generate the images
for post in top_ask_posts:
    # create a new image with the specified size and color
    image = Image.new("RGB", image_size, image_color)
    draw = ImageDraw.Draw(image)

    # wrap the title text and draw it on the upper part of the image
    title_text = post.title
    title_text_wrapped = textwrap.fill(title_text, width=50)
    title_width, title_height = draw.textsize(title_text_wrapped, font=font_title)
    title_position = ((image_size[0] - title_width) / 2, 50)
    draw.multiline_text(title_position, title_text_wrapped, fill=(0, 0, 0), font=font_title, align='center')

    # wrap the body text and draw it on the middle part of the image
    body_text = post.selftext
    body_text_wrapped = textwrap.fill(body_text, width=50)
    body_width, body_height = draw.textsize(body_text_wrapped, font=font_body)
    body_position = ((image_size[0] - body_width) / 2, 200)
    draw.multiline_text(body_position, body_text_wrapped, fill=(0, 0, 0), font=font_body, align='center')

    # draw the top comments on the bottom part of the image
    comments_list = post.comments[:2]
    comments_position = (50, 600)
    for comment in comments_list:
        if comment.author.name != "AutoModerator":
            comment_text = f"{comment.author.name}: {comment.body}"
            comment_text_wrapped = textwrap.fill(comment_text, width=50)
            comment_width, comment_height = draw.textsize(comment_text_wrapped, font=font_comment)
            comment_position = ((image_size[0] - comment_width) / 2, comments_position[1])
            draw.multiline_text(comment_position, comment_text_wrapped, fill=(0, 0, 0), font=font_comment, align='center')
            comments_position = (comments_position[0], comments_position[1] + comment_height + 20)

    # append the image to the list
    images_list.append(image)

# save the images to disk
for i, image in enumerate(images_list):
    image.save(f"post_{i+1}.png")
