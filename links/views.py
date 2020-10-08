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
)

from rest_framework.views import APIView


class StartEventAPIView(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        channel = slack_message.get("text")  # channel from '/start' command text
        print("Slack message received: ", slack_message)

        check_res = check_channel_sign(channel=channel)
        if check_res is None:
            print("check_res is None, starting listen...")
            bot_resp_text = start_channel_listen(channel)
        else:
            Channel.objects.filter(channel_id=channel).update(
                channel_id=channel, listen=True
            )
            bot_resp_text = "Listening restored!"

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
