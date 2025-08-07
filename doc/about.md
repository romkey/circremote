# About This Project

I've been wanting a tool like `circremote` for quite a while. I have CircuitPython devices which are long running but which occasionally I'd like to run a diagnostic on, without overwriting the code already installed on it. I also often bring up new sensors or test hardware using CircuitPython - I've run an I2C scanner countless times and always end up copying and pasting the code. `circremote` allows me to run code on the device without disturbing whatever is installed on it, and lets me very conveniently reuse code across devices and time. It lets me focus on managing the code rather than the device.

While I wanted a tool like this I was also busy and didn't feel like writing it. I'm a competent Python programmer but idiomatic Python isn't intuitive to me yet and while I'm enthusiastic about Python (and particularly CircuitPython) I'm not skilled enough to call myself a Pythonista.

And being a developer, I fundamentally want to do more with less.

Like many experienced developers, I've tried using LLMs to write code. My first results were poor, to put it kindly. The LLMs were not well trained in the areas I was working in. I asked for an ESP32 program and they hallucinated Adafruit libraries that didn't exist. The code didn't even compile. But the rate at which LLMs are improving is incredible. What was difficult for an LLM a few months ago it may now do flawlessly.

A friend was very excited about [Cursor](https://cursor.com/), so I decided that I'd try it out. The results were suprisingly good. My first go at it never got Web Workflow's websocket support in Python working but many other functions worked well. I'm more proficient in Ruby so I had Cursor rewrite `circremote` in Ruby, and it got websockets with the Web Workflow right on the first try. So I continued to iterate on the design in Ruby but the idea of telling the CircuitPython community that they needed to install Ruby in order to run `circremote` felt absurd. So I asked Cursor to rewrite it in Python again and it worked! Even the websocket support for Web Workflow.

This has been such a positive experience that it's really shifted my view on using an LLM to write code.

It also leaves me very concerned about maintenance. Fundamentally I designed this code but I didn't write it. I don't know it very well. I've gone down some rabbit holes with Cursor trying to correct bugs... and generally it's been okay but sometimes it goes down a dead end and builds up more and more cruft in the code with failed attempts... unwinding that can be tedious and difficult. Good git hygiene helps a lot but it's still too easy to end up with some twisted code from misugided attempts to fix things which never pan out.

I'm happy to say that almost all of the code and text in `circremote` was written by Cursor under my guidance. I've tweaked  the code directly here and there (mostly in some of the commands where Cursor was really not having a good time, and in parts of the text like this chunk and other places where there were nuances and useful information that Cursor just didn't get a grip on.
	- john romkey
