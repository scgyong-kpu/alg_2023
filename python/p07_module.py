#python 에는 많은 내장 모듈이 있다
import math
pt1, pt2 = [ -150, -100 ], [ 150, 300 ]
distance = math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)
print(f'두 점 {pt1} 과 {pt2} 사이의 거리는 {distance:.2f} 이다')

# 두 점이 이루는 각도를 구하려면 atan(y/x) 을 사용해야 한다
# 하지만 부호도 신경써야 하므로 atan2(y, x) 를 쓰면 알아서 해 준다
angle_radian = math.atan2((pt2[1]-pt1[1]), (pt2[0]-pt1[0]))

# Computer Graphics 는 대부분 radian 단위를 사용한다. 사람이 이해할 때는 Degree 가 편할때가 많다
angle_degree = 180 * angle_radian / math.pi

print(f'두 점 사이의 선이 만드는 각도는 Radian 으로는 {angle_radian:.2f}, Degree 로는 {angle_degree:.2f}° 이다')
