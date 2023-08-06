## ascii_gif

#### Example

```python
    from ascii_gif import AsciiGif

    file_name = 'test.gif'
    width = 80
    AsciiGif(file_name).output()
```

#### Available Options to constructor
```
    frame_delay - Delay between frames in GIF while rendering to terminal
    fit_terminal - Ignores width, takes the entire terminal size
    chars - specify chars for ASCII text (fat characters gives better results)
    loop_gif - you know what it is :p (ctrl + c to end)
```