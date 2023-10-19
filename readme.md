# **YappaThilda**
### An elevenlabs TTS bot with built in twitch integration

---

Elevate your chat tts by using the limitless speech possibility provided by elevenlabs.
Comes with direct twitch integration and obs integration.

**If you enjoy this software, please credit [LucyCecidit](https://www.twitch.tv/lucycecidit)**


for any direct questions or concerns feel free to join the discord server.


[![Join our Discord server!](https://invidget.switchblade.xyz/4ahvUxhcab)](http://discord.gg/4ahvUxhcab)

---

**Requirements**

- [Elevenlabs](https://elevenlabs.io/) account set up 
(this is not required though you will be rate limited)
  - Disclaimer: To make full usage of elevenlabs posibilities you will need a subscription.
- a twitch account :)
- obs move transition (https://obsproject.com/forum/resources/move.913/)

---

**Setup process**

##### Twitch & elevenlabs


Inside your config folder, there will be a file
named ``config.json.example``; rename this file to ``config.json`` and fill 
in all the required information.

your auth token can be found here: https://twitchtokengenerator.com/

your twitch channel id can be found here: https://streamscharts.com/tools/convert-username

Your APIKey for [elevenlabs](https://elevenlabs.io/) can be found in your profile section.

---

##### OBS

Inside OBS, you will need to make a scene for your tts bot to have the two images
(one for opening mouth and one for closing). This scene name should be similar to ``source_name``
inside your ``config.json`` file.

Once this is done you will need to make another scene, the name will have to be similar to ``scene_name``
inside your ``config.json`` file. Add your prior made scene into this one as a source and hide it by default.

After this, go to your audio settings inside OBS and assign an unused audio source to ``desktop audio 2``;
Then scroll down to advanced and assign your default audio source to ``monitoring device``.

- To find out what other audio device you can add to your config file, please use the ``discover_audio_devices`` executable


Go to the advanced audio properties in obs by clicking on the burger icon on one of your audio sources in the audio mixer.

If it is difficult to follow this [video](https://www.youtube.com/watch?v=u0XXNotHMEA) (excluding the parts about bikubot) Might be of use!
Between 2:25 and 5:20 is of use to you.


Make sure to open up the OBS websocket, this can be found in [tools]>[websocket server settings]
Also please make sure you used the correct data in your config file.

---

**Development setup process**

Python 3.11.6 is used for development. pip requirements are listed in requirements.txt
To create an executable, use ``auto-py-to-exe`` in your terminal of choice