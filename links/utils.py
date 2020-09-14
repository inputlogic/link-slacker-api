from rest_framework.response import Response
from slack.errors import SlackApiError
import slack

from .models import URL, Channel
from .serializer import URLSerializer
from .settings import BOT_USER_ACCESS_TOKEN

client = slack.WebClient(token=BOT_USER_ACCESS_TOKEN)


def get_links_from_msg(message):
    # get links from attachments
    # if no attachments -> get links from "blocks"
    links_attach, links_elems = delete_duplicates(
        get_links_from_attachs(message), get_links_from_elems(message)
    )
    return links_attach + links_elems


def get_links_from_elems(message):
    links = []
    if (
        "blocks" in message
        and "elements" in message["blocks"][0]
        and "elements" in message["blocks"][0]["elements"][0]
    ):
        msg_elements = message["blocks"][0]["elements"][0]["elements"]
        urls = [elem.get("url") for elem in msg_elements if elem.get("type") == "link"]
        for url in urls:
            link_data = dict(link=url, msg=message.get("client_msg_id"),)
            links.append(link_data)
    return links


def get_links_from_attachs(message):
    links = []
    if "attachments" in message:
        msg_attachs = message.get("attachments")
        for attach in msg_attachs:
            link_title = attach.get("title")
            link_url = attach.get("title_link")
            link_desc = attach.get("text")
            link_image = attach.get("image_url")
            link_msg_id = message.get("client_msg_id")
            if not link_image:
                link_image = attach.get("service_icon")
            link_data = dict(
                title=link_title,
                link=link_url,
                description=link_desc,
                image=link_image,
                msg=link_msg_id,
            )
            links.append(link_data)
    return links


def delete_duplicates(links_attach, links_elems):
    for link1 in links_attach:
        for index, link2 in enumerate(links_elems):
            if link1.get("msg") == link2.get("msg"):
                links_elems.pop(index)
    return links_attach, links_elems


def start_channel_listen(channel):
    if is_valid_channel(client, channel):
        history = get_channel_history(client, channel=channel)
        if history:
            print("History was received!")

            # getting from channel history links data for db
            for msg in history:
                links = get_links_from_msg(msg)
                if links is None:
                    continue
                else:
                    for link in links:
                        write_link_db(link)

            # write channel listening to db
            Channel.objects.create(channel_id=channel, listen=True)

        return f"Bot now listen <@{channel}> :robot_face:"
    else:
        return f"Sorry, <@{channel}> was not found!"


def check_channel_sign(channel):
    channel = Channel.objects.filter(channel_id=channel).first()
    if channel is None:
        return None
    return channel.listen


def get_channel_history(client, channel):
    history_resp = client.conversations_history(channel=channel)
    history_arr = history_resp.get("messages")
    history = history_arr[:-1]
    return history


def write_link_db(link_data):
    serializer = URLSerializer(data=link_data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


def is_valid_channel(client, channel):
    try:
        client.conversations_info(channel=channel)
        return True
    except SlackApiError:
        return False
