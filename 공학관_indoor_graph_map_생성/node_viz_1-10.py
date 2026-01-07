import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json
import numpy as np
import os
import matplotlib.font_manager as fm

# 사용자 설정
PIXELS_PER_METER = 9667.01 / 152.8  # ≈ 63.25
FLOOR_IMAGE_PATH = "downscaling_images/3F_10-1.jpeg"
LOAD_PATH = "graph_map_with_guides.json"
FLOOR_NAME = "3F"

plt.rcParams['toolbar'] = 'toolbar2'
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 그래프 데이터
state = {
    "nodes": [],
    "edges": [],
    "markers": [],
    "guide_lines": {"horizontal": [], "vertical": []}
}

undo_stack = []
node_id_counter = 1
node_positions = {}
edge_start_node = None
current_mode = "node"

# 픽셀 <-> 미터 변환
def pixel_to_meter(x, y):
    return [x / PIXELS_PER_METER, y / PIXELS_PER_METER]

def meter_to_pixel(mx, my):
    # return [mx * PIXELS_PER_METER, my * PIXELS_PER_METER]
    return [int(mx * PIXELS_PER_METER * 0.1), int(my * PIXELS_PER_METER * 0.1)]

# 그리기 함수
def redraw():
    # 확대/이동 상태 저장
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    ax.clear()
    ax.imshow(img, origin='upper', zorder=-1)
        
    node_positions.clear()
    for node in state['nodes']:
        mx, my, _ = node['position']
        x, y = meter_to_pixel(mx, my)
        node_positions[node['id']] = (x, y)
        ax.plot(x, y, 'ro')
        ax.text(x + 10, y + 10, node['id'], color='red', fontsize=8)
    for edge in state['edges']:
        x1, y1 = node_positions[edge['start']]
        x2, y2 = node_positions[edge['end']]
        ax.plot([x1, x2], [y1, y2], 'b--')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    for y in state['guide_lines']['horizontal']:
        x0, x1 = ax.get_xlim()
        ax.plot([x0, x1], [y, y], color='gray', linestyle='--', zorder=0)
    for x in state['guide_lines']['vertical']:
        ax.axvline(x, color='gray', linestyle='--', zorder=0)
        # 확대/이동 상태 복원
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    for marker in state['markers']:
        mx, my, _ = marker['position']
        x, y = meter_to_pixel(mx, my)
        ax.plot(x, y, 'ms', markersize=10)  # 마젠타 색상의 사각형 마커 표시
        ax.text(x + 10, y + 10, marker['id'], color='magenta', fontsize=8)

    fig.canvas.draw()


def load_json():
    global node_id_counter
    if os.path.exists(LOAD_PATH):
        with open(LOAD_PATH, 'r') as f:
            data = json.load(f)
            state["nodes"] = data.get("nodes", [])
            state["edges"] = data.get("edges", [])
            state["markers"] = data.get("markers", [])
            state["guide_lines"] = data.get("guide_lines", {"horizontal": [], "vertical": []})
            node_id_counter = len(state["nodes"]) + 1
        print("📂 이전 저장 내용 불러옴")
        redraw()

# 시작
if not os.path.exists(FLOOR_IMAGE_PATH):
    print(f"이미지 파일이 없습니다: {FLOOR_IMAGE_PATH}")
    exit()

img = mpimg.imread(FLOOR_IMAGE_PATH)
fig, ax = plt.subplots(figsize=(12, 8))
ax.imshow(img, origin='upper')
load_json()
plt.tight_layout()
plt.show()
