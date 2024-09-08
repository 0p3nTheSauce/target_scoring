import cv2
import numpy as np
from ideal_scoreboard import ideal_centred_ellipses
from lines_to_points import ellipses_to_points, visualise_points

ellipses,centre, img = ideal_centred_ellipses(x=700, y=700)
for ellipse in ellipses:
  print(ellipse)
ellipse_pnts = ellipses_to_points(ellipses)
visualise_points(ellipse_pnts, title="Ideal Ellipses", show=True)
