import cv2
import numpy as np

#%%
def interpolate_points(p1, p2, num_points):
    t_values = np.linspace(0, 1, num_points)
    points = []

    for t in t_values:
        x = p1[0] * (1 - t) + p2[0] * t
        y = p1[1] * (1 - t) + p2[1] * t
        points.append((x, y))

    return points

def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def find_grid_point(np_cnt,hdivide=8,vdivide=4) :
    
    
    _divide = vdivide + 1
    _hdivide = hdivide + 1
    
    rect = cv2.minAreaRect(np_cnt)
    # print(rect)
    box = cv2.boxPoints(rect)
    # print(box)
    
    # draw red circle center area
    # _box = np.int0(box) # 좌표값을 정수형으로 변환
    # cv2.circle(_seg_img, (int(rect[0][0]), int(rect[0][1])), 3, (0, 0, 255), -1)
    # cv2.drawContours(_seg_img, [_box], 0, (0,255,0), 1)
    
    p1, p2, p3, p4 = box
    
    
    if distance(p1, p2) < distance(p1, p3): 
        _line1 = interpolate_points(p1, p2, _divide)
        _line2 = interpolate_points(p4, p3, _divide)
    else:
        _line1 = interpolate_points(p1, p3, _divide)
        _line2 = interpolate_points(p2, p4, _divide)
        
    
    _lines = np.array([  ( _line1[i],_line2[i]) for i in range(_divide)  ])
    
    #draw line
    line_points = [ interpolate_points(line[0], line[1], _hdivide) for line in _lines]
        # _points =  interpolate_points(line[0], line[1], 9)
        
        # for point in _points:
        #     point_int = tuple(np.int0(point))
            # cv2.circle(_seg_img, point_int, 1, (255, 0, 0), -1)
    return rect,box,_lines,line_points

    #draw center line
    # point1_int = tuple(np.int0(_lines[2][0]))
    # point2_int = tuple(np.int0(_lines[2][1]))
    
    # cv2.line(_seg_img, point1_int, point2_int, (255, 0, 255), 2)
    
    # draw bbox
    # _bbox = result.boxes[_index]        
    # print(_bbox)
    # x1, y1, x2, y2 = _bbox.xyxy[0]
    # cv2.rectangle(_seg_img,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0),2)
