# **YappaThilda**
### A twitch elevenlabs TTS integration,

---

A twitch integration programme connected with elevenlabs to deliver
custom voice tts to your own stream

**If you enjoy this software, please credit [LucyCecidit](https://www.twitch.tv/lucycecidit)**

---

**Requirements**

- [Elevenlabs](https://elevenlabs.io/) account set up 
(this is not required though you will be rate limited)
- a twitch account :)
- obs move transition (https://obsproject.com/forum/resources/move.913/)

---

**Setup process**

Inside your config folder, there will be a file
named config.json.example; rename this file to config.json and fill 
in all the required information.

your twitch channel id and auth token can be found here: https://twitchtokengenerator.com/

Your APIKey for [elevenlabs](https://elevenlabs.io/) can be found in your profile section.

On the OBS side you can follow this [video](https://www.youtube.com/watch?v=u0XXNotHMEA) (excluding the parts about bikubot)

Make sure to open up the OBS websocket, this can be found in [tools]>[websocket server settings]
Also please make sure you used the correct data in your config file.

---

**Development setup process**

Python 3.11.6 is used for development. pip requirements are listed in requirements.txt
To create an executable, use ``auto-py-to-exe`` in your terminal of choice