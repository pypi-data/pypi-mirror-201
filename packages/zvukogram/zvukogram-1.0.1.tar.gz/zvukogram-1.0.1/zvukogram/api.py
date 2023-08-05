from .models import Audio, Voice
from .exceptions import ZvukoGramError, raise_for_status

from typing import Dict, Optional
from aiohttp import ClientSession


class ZvukoGram(object):
    """
    Base class for ZvukoGram API
    """

    voices = None
    API_URL = 'https://zvukogram.com/index.php?r=api/%s'

    def __init__(self, token: str, email: str, session: Optional[ClientSession]=None):

        self.token = token
        self.email = email

        self.session = session or ClientSession()


    @raise_for_status
    async def _request(self, endpoint: str, method: str='POST', **kwargs) -> dict:
        """
        Make a request to ZvukoGram API

        :param str endpoint: API endpoint
        :return dict: API response
        """

        async with self.session.request(
            method,
            self.API_URL % endpoint,
            data={
                'token': self.token,
                'email': self.email,
                **{
                    key: value 
                    for key, value in kwargs.items()
                    if value is not None
                },
            },
        ) as response:

            return await response.json(content_type=None)


    async def get_voices(self, no_cache: bool=False) -> Dict[str, Voice]:
        """
        Get list of available voices

        :param bool no_cache: Do not use cache
        :return list[Voice]: Voices list
        """

        if self.voices and not no_cache:

            return self.voices

        response = await self._request('voices')
        self.voices = {
            language: [Voice(**voice) for voice in voices]
            for language, voices in response.items()
        }

        return self.voices


    async def tts(
        self, 
        voice: str, 
        text: str, 
        format: str='mp3', 
        speed: Optional[float]=None, 
        pitch: Optional[int]=None, 
        emotion: Optional[str]=None,
    ) -> Audio:
        """
        Text-to-speech

        :param str voice: Voice name
        :param str text: Text to convert to speech
        :param str format: Audio format
        :param float speed: Speed of speech
        :param float pitch: Pitch of speech
        :return Audio: Audio model
        """

        if len(text) > 300:

            raise ZvukoGramError('Max text length in tts-short is 300 characters')

        response = await self._request(
            'text', voice=voice, text=text, format=format, 
            speed=speed, pitch=pitch, emotion=emotion,
        )
        return Audio(**response)


    async def tts_long(
        self, 
        voice: str, 
        text: str, 
        format: str='mp3', 
        speed: Optional[float]=None, 
        pitch: Optional[int]=None, 
        emotion: Optional[str]=None,
    ) -> Audio:
        """
        Text-to-speech

        :param str voice: Voice name
        :param str text: Text to convert to speech
        :param str format: Audio format
        :param float speed: Speed of speech
        :param float pitch: Pitch of speech
        :return AudioProgress: Audio model
        """

        response = await self._request(
            'longtext', voice=voice, text=text, format=format, 
            speed=speed, pitch=pitch, emotion=emotion,
        )
        return Audio(**response)


    async def check_progress(self, id: int) -> Audio:
        """
        Text-to-speech

        :param int id: Audio process ID
        :return AudioProgress: Audio model
        """

        response = await self._request('result', id=id)
        return Audio(**response)
