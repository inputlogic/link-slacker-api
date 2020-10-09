import threading

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListAPIView
from django.conf import settings
from datetime import datetime

from .models import URL, Channel
from .serializer import URLSerializer
from .utils import (
    get_links_from_msg,
    start_channel_listen,
    check_channel_sign,
    write_link_db,
    is_valid_channel
)

from rest_framework.views import APIView

'''
class StartEventAPIView(APIView):
    def post(self, request, *args, **kwargs):
        
        # get slack message data
        slack_message = request.data
        print("Slack message received: ", slack_message)
        
        # collect channel details from slack
        channel_id = slack_message.get("channel_id")
        channel_name = slack_message.get("channel_name")
        channel_text = slack_message.get("text")
        
        # fail if not all channel data is available
        if None in (channel_id, channel_name, channel_text):
            bot_resp_text = "Hmm, I couldn't find a channel to listen to. :thinking_face:"
            return Response(data=bot_resp_text, status=status.HTTP_200_OK)
        
        # fail if slack says channel isn't valid
        if not is_channel_valid(channel_text):
            bot_resp_text = "Strange, that channel doesn't seem to be valid. :thinking_face:"
            return Response(data=bot_resp_text, status=status.HTTP_200_OK)            

        # if channel isn't listening yet, make it listen
        if not is_channel_listening(channel=channel_id):
            print("Didn't find channel, or channel isn't listening yet. Setting listen = True on channel: ", channel_text)
            bot_resp_text = start_channel_listen(channel_text)
        else:
            Channel.objects.filter(channel_id=channel_id).update(
                channel_name=channe_name,
                channel_id=channel_id,
                channel_text=channel_text,
                listen=True
            )
            bot_resp_text = "Great idea! Listening for links on " + str(channel_text) + "."

        return Response(data=bot_resp_text, status=status.HTTP_200_OK)
'''

class StartEventAPIView(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        channel = slack_message.get("text")  # channel from '/start' command text

        check_res = check_channel_sign(channel=channel)
        if check_res is None:
            if is_valid_channel(channel):
                bot_resp_text = f"Listening for links on {channel}. :robot_face:"
                listen_starter_thread = threading.Thread(target=start_channel_listen, kwargs=dict(channel=channel))
                listen_starter_thread.start()
            else:
                bot_resp_text = f"Strange, {channel} doesn't seem to be valid. :thinking_face:"
        else:
            Channel.objects.filter(channel_id=channel).update(
                channel_id=channel, listen=True
            )
            bot_resp_text = f"Great idea! Listening for links on {channel}."

        return Response(data=bot_resp_text, status=status.HTTP_200_OK)


class StopEventAPIView(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        channel = slack_message.get("text")  # channel from '/stop' command text

        # TODO: check if channel doesnt exist in db
        Channel.objects.filter(channel_id=channel).update(
            channel_id=channel, listen=False
        )
        # self.bot_message("Channel listening stopped!")

        return Response(data="Channel listening stopped!", status=status.HTTP_200_OK)


class MessagesEventAPIView(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        if slack_message.get("token") != settings.VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if slack_message.get("type") == "url_verification":
            return Response(data=slack_message, status=status.HTTP_200_OK)

        #
        if "event" in slack_message:
            event_message = slack_message.get("event")
            msg_channel = event_message.get("channel")
            if check_channel_sign(channel=msg_channel):
                if (
                        event_message.get("subtype")
                        and event_message.get("subtype") == "message_changed"
                ):
                    # change old links to full new ones
                    changed_message = event_message.get("message")
                    links_data = get_links_from_msg(changed_message)
                    URL.objects.filter(
                        msg=changed_message.get("client_msg_id")
                    ).delete()
                    for link_data in links_data:
                        write_link_db(link_data)
                    return Response(status=status.HTTP_200_OK)

                # way other channels messages
                print("Some channel user msg ---", event_message)
                links = get_links_from_msg(event_message)
                if links:
                    for link in links:
                        write_link_db(link)

        return Response(status=status.HTTP_200_OK)


class URLListAPIView(ListAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
