import setuptools

setuptools.setup(name="ascvid",version="1.0.0",description="ASCII Video player.", long_description=
                 """
.. image:: https://raw.githubusercontent.com/jenca-adam/ascvid/main/asc.png

``ascvid`` is an ASCII video player with quite exact results. It is mostly advised to be used under Linux, but it might work on other OS too.
Here is a little showcase of what it can do: 

.. image:: https://raw.githubusercontent.com/jenca-adam/ascvid/main/rick.gif

It requires a Truecolor terminal to work like this. If you are on a stupider terminal, the results will look less realistic.The produced graphics aren't blinking as in other ASCII video players, however, the videos might lag a bit if your terminal is zoomed out.
``ascvid`` also supports audio! It's a true video player.

Installation
============

.. code-block:: console
   
   python3 -m pip install ascvid

Then you can just run ``ascvid`` and you're good to go.

CLI Options
===========
*NOTE :: --no-truecolor option lags like my brain, so if you are on a stupid terminal, you are better off using --no-color in ASCII mode.*
.. code-block:: console
    
    Usage: python -m ascvid [OPTIONS] FILE

    Options:
      -H, --hide-cursor   Hide the cursor while playing the video
      -A, --no-audio      Don't play audio stream
      -f, --fps TEXT      Number of FPS the video's supposed to run at. If None,
                          it's determined from the video. If "max", ascvid will
                          try its best to keep the video from lagging
      -c, --char TEXT     Character to be used while rendering the video frames
      -C, --no-color      Don't color output
      -a, --ascii         Use multiple ASCII characters. Best to be used with
                          --no-truecolor
      -T, --no-truecolor  Reduces color palette. Use this flag on more stupid
                          terminals (windows).
      -F, --fast          Toggles off resizing each frame individually, rather
                          resizes the entire video. Use this if the video is
                          lagging too much.
      --help              Show this message and exit.
    """,
                 install_requires=["pillow","moviepy","cursor","numpy","click"],
                 packages=["ascvid"],
                 classifiers=["Development Status :: 4 - Beta","Environment :: Console","Intended Audience :: End Users/Desktop","License :: OSI Approved :: GNU General Public License v3 (GPLv3)","Operating System :: OS Independent","Programming Language :: Python :: 3.10","Topic :: Multimedia :: Video :: Display"],keywords="Video,ASCII,Terminal",author="Adam Jenca",author_email="jenca.a@gjh.sk",url="https://github.com/jenca-adam/ascvid",entry_points={"console_scripts":["ascvid = ascvid.cli:main"]})






