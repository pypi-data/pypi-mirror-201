.. image:: asc.png

``ascvid`` is an ASCII video player with quite exact results. It is mostly advised to be used under Linux, but it should work on other OS too.
Here is a little showcase of what it can do: 

.. image:: rick.gif

It requires a Truecolor terminal to work like that. If you are using a more stupid terminal, the graphics will look less realistic. The produced graphics aren't blinking as in other ASCII video players, however, the videos might lag a bit if your terminal is zoomed out.
``ascvid`` also supports audio! It's a true video player.

Installation
============

.. code-block:: console
   
   python3 -m pip install ascvid

CLI Options
===========

.. code-block:: console
        
    Usage: ascvid [OPTIONS] FILE

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
