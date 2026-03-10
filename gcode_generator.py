"""
Converts vector paths to gcode using pen_config settings

Input:
    paths — list of paths, where each path is a list of (x, y) tuples (mm).
             Each path is drawn as a continuous stroke (pen down).
             The pen lifts between paths.

Usage:
    from gcode_generator import generate_gcode
    generate_gcode(paths)           # writes to config output_filename
    gcode = generate_gcode(paths, return_string=True)
"""

from pen_config import CONFIG


def generate_gcode(paths, return_string=False, output_file=None):
    """
    Convert a list of vector paths to gcode.

    Args:
        paths:         Iterable of paths. Each path is an iterable of (x, y) tuples in mm.
        return_string: If True, return the gcode as a string instead of writing to a file.
        output_file:   Override the output filename from config.

    Returns:
        gcode string if return_string=True, else None.
    """
    lines = []

    def cmd(s):
        lines.append(s)

    # --- Start block ---
    for c in CONFIG['start_commands']:
        cmd(c)

    pen_up   = CONFIG['pen_up']
    pen_down = CONFIG['pen_down']
    fr_draw  = CONFIG['feed_rate_draw']
    fr_travel = CONFIG['feed_rate_travel']
    fr_init  = CONFIG['feed_rate_initial']

    # Initial travel to first point at slow feed to avoid step loss
    first_move_done = False

    for path in paths:
        points = list(path)
        if not points:
            continue

        x0, y0 = points[0]

        if not first_move_done:
            # Slow first travel from home
            cmd(f'G0 X{x0:.3f} Y{y0:.3f} F{fr_init}')
            first_move_done = True
        else:
            # Fast travel between strokes
            cmd(pen_up)
            cmd(f'G0 X{x0:.3f} Y{y0:.3f} F{fr_travel}')

        cmd(pen_down)

        # Draw the path
        for x, y in points:
            cmd(f'G1 X{x:.3f} Y{y:.3f} F{fr_draw}')

    # --- End block: pen up and home ---
    cmd(pen_up)
    cmd('G0 X0 Y0')

    gcode = '\n'.join(lines) + '\n'

    if return_string:
        return gcode

    filename = output_file or CONFIG['output_filename']
    with open(filename, 'w') as f:
        f.write(gcode)
    print(f'Written {len(lines)} lines to {filename}')


# --- Example / test ---
if __name__ == '__main__':
    # Draw a simple square and a diagonal cross
    square = [(10, 10), (50, 10), (50, 50), (10, 50), (10, 10)]
    cross  = [(10, 10), (50, 50), (30, 30), (50, 10), (10, 50)]

    generate_gcode([square, cross])
