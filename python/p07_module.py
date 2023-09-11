#python 에는 많은 내장 모듈이 있다
import math
pt1, pt2 = [ -150, -100 ], [ 150, 300 ]
distance = math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)
print(f'두 점 {pt1} 과 {pt2} 사이의 거리는 {distance:.2f} 이다')
