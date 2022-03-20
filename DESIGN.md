## Touchscreen <--> Main Communication

### Requirements

1. Touchscreen input must be non-blocking
2. Touchscreen should feel responsive - meaning, visual changes on the screen are instant, LED effects happen within one or two frames

### Design

Right now, `main.py` uses precision timer, which is basically a fancy way to `sleep` for the correct amount of time (i.e. framerate minus processing time for the `loop()` function). However, while python is sleeping, it can't do anything.

This was a problem for trying to listen to audio input, which got out-of-sync when only reading from it every 25ms. To solve that, I moved the audio input processing to a separate thread; see `modules/audio_input/runner.py` for code.

Adding a thread did not seem to impact performance or memory usage.

I think we can follow the same Threading strategy for running the touchscreen code.

### Shared State

Say we have a file `modules/touchscreen/runner.py` which runs some process to display the touchscreen interface. That process should output to STDOUT in a format that's easy for us to parse. One message per line.

Shared state should be:

`fingerMessageQueue = []`

An array of finger messages with the properties
```
{
  fingerId: int
  action: int (0 for press, 1 for move, 2 for release)
  x: int
  y: int
}
```

`actionMessageQueue = []`

An array of messages of the format
```
[
  functionName,
  ...params
]
```

ex. say we want to adjust the brightness via a slider; would queue up the message `["setBrightness", 0.5]`

### Shared Coordinates

The main program needs to know the coordinates of touchscreen objects to understand what's currently being touched and where.

The touchscreen needs to know the coordinates so it knows where to place the objects, and knows how to change the display (for active vs inactive effects).

These coordinates should be shared somehow - through some data file that both processes load.

### Main program responsibilities

- Translate finger messages into the correct filters
- Discard any "old" finger messages
- Run any actions
