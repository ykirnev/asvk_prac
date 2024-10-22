def walk2d():
    xy = 0, 0
    yield xy
    while True:
        xy_new =(yield xy)
        xy = xy[0] + xy_new(0), xy[1] + xy_new[1]

