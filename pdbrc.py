import pdb


class Config(pdb.DefaultConfig):
    sticky_by_default = True

    # KDY: 44 is the default current line color. My terminal doesn't display it well
    # so I'm using gray here instead
    current_line_color = 40
