import cv2
import time
from ultralytics import YOLO

if __name__ == '__main__':
    # 1. 加载你刚刚训练好的模型
    # 注意路径中的 train-2，要和你 runs/detect 里面的文件夹名字对应上
    model = YOLO("../runs/detect/train-2/weights/best.pt")

    # 2. 打开电脑摄像头 (0 代表默认摄像头)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头！请检查摄像头是否被其他程序占用。")
        exit()

    print("摄像头已开启，按键盘上的 'q' 键退出推理。")

    while True:
        # 读取一帧画面
        ret, frame = cap.read()
        if not ret:
            print("无法读取画面，退出。")
            break

        # 3. 让 YOLO 进行实时推理
        results = model(frame, stream=True, verbose=False)

        # 4. 将识别框和类别画在画面上
        for r in results:
            annotated_frame = r.plot()

        # 5. 显示画面
        cv2.imshow("YOLO Real-time Inference", annotated_frame)

        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # 5. 检测按键（注意：先把waitKey的结果存到key变量里）
        key = cv2.waitKey(1) & 0xFF

        # 按 'q' 退出
        if key == ord('q'):
            print("已退出推理。")
            break

        # 按 's' 保存当前截图
        elif key == ord('s'):
            filename = f"result_{int(time.time())}.jpg"
            cv2.imwrite(filename, annotated_frame)
            print(f"✅ 识别结果已保存为：{filename}")

        # 🌟 核心优化：如果点击了窗口右上角的 X，自动退出，防止卡死
        if cv2.getWindowProperty("YOLO Real-time Inference", cv2.WND_PROP_VISIBLE) < 1:
            print("窗口已关闭，程序退出。")
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
    print("推理已停止。")