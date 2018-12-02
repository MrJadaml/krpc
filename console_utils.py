def status_console(conn):
    canvas = conn.ui.stock_canvas

    # Get the size of the game window in pixels
    screen_size = canvas.rect_transform.size

    # Add a panel to contain the UI elements
    panel = canvas.add_panel()

    # Position the panel on the left of the screen
    rect = panel.rect_transform
    rect.size = (400,200)
    rect.position = (210-(screen_size[0]/2), 200)

    # Settings for text size in the panel on screen
    text = panel.add_text("Countdown")
    text.rect_transform.position = (0,-20)
    text.color = (1,1,1)
    text.size = 18
