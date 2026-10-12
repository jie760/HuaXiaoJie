def simulate_ball(h0,total_time):
    v = 0.0
    g = 9.8
    h = h0
    dt = 0.01
    rebound_factor = 0.8
    time_list=[]
    height_list=[]
    steps = int(total_time/dt)
    for i in range(steps):
        t = i*dt
        time_list.append(t)
        height_list.append(h)
        v = v-g*dt
        h = h+v*dt
        if h <= 0:
            h=0
            v=-rebound_factor*v
    return time_list,height_list
time_list,height_list=simulate_ball(10, 5)
print(f"模拟结束，总采集数据点：{len(time_list)}")
print(f"time_list 前五个数据：{time_list[:5]}")
print(f"height_list 前五个数据：{height_list[:5]}")
print(f"最后一刻高度：{height_list[-1]:.4f}米")



