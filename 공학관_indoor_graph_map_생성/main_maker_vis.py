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
FLOOR_IMAGE_PATH = "images/floorplan_page3.png"
SAVE_PATH = "graph_map_with_guides.json"
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
    return [mx * PIXELS_PER_METER, my * PIXELS_PER_METER]

# 가이드라인 스냅
def snap_to_guide(x, y, threshold=10):
    snap_x, snap_y = x, y
    matched_x = [gx for gx in state["guide_lines"]["vertical"] if abs(x - gx) < threshold]
    matched_y = [gy for gy in state["guide_lines"]["horizontal"] if abs(y - gy) < threshold]
    if matched_x:
        snap_x = matched_x[0]
    if matched_y:
        snap_y = matched_y[0]
    return snap_x, snap_y

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

# 클릭 처리
def onclick(event):
    if fig.canvas.manager.toolbar.mode != '' or event.button != 1 or event.inaxes != ax:
        return

    global node_id_counter, edge_start_node
    x, y = float(event.xdata), float(event.ydata)
    x, y = snap_to_guide(x, y)

    if current_mode == "node":
        node_id = f"N{node_id_counter}"
        node_id_counter += 1
        state["nodes"].append({
            "id": node_id,
            "position": pixel_to_meter(x, y) + [0],
            "floor": FLOOR_NAME,
            "type": "unknown",
            "name": "",
            "landmark": None
        })
        undo_stack.append({"type": "node", "data": node_id})
        redraw()

    elif current_mode == "edge":
        clicked_node = find_nearest_node(x, y)
        if clicked_node:
            if edge_start_node is None:
                edge_start_node = clicked_node
                print(f"[Edge] 시작 노드 선택: {clicked_node}")
                x0, y0 = node_positions[clicked_node]
                ax.plot(x0, y0, 'go', markersize=10)
                fig.canvas.draw()
            else:
                if clicked_node != edge_start_node:
                    x1, y1 = node_positions[edge_start_node]
                    x2, y2 = node_positions[clicked_node]
                    length = float(np.hypot(x2 - x1, y2 - y1) / PIXELS_PER_METER)
                    state["edges"].append({
                        "start": edge_start_node,
                        "end": clicked_node,
                        "length": round(length, 2),
                        "directionality": "bidirectional"
                    })
                    undo_stack.append({"type": "edge"})
                edge_start_node = None
                redraw()

# 가장 가까운 노드
def find_nearest_node(x, y, threshold=30):
    min_dist = threshold
    closest_node = None
    for node_id, (nx, ny) in node_positions.items():
        dist = np.hypot(x - nx, y - ny)
        if dist < min_dist:
            min_dist = dist
            closest_node = node_id
    return closest_node

# 저장 및 불러오기
def save_json():
    with open(SAVE_PATH, 'w') as f:
        json.dump(state, f, indent=2)
    print(f"✅ 저장 완료: {SAVE_PATH}")

def load_json():
    global node_id_counter
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, 'r') as f:
            data = json.load(f)
            state["nodes"] = data.get("nodes", [])
            state["edges"] = data.get("edges", [])
            state["markers"] = data.get("markers", [])
            state["guide_lines"] = data.get("guide_lines", {"horizontal": [], "vertical": []})
            node_id_counter = len(state["nodes"]) + 1
        print("📂 이전 저장 내용 불러옴")
        redraw()

# 키 입력 처리
def onkey(event):
    global current_mode
    print(f"[키 입력 감지] key={event.key}")
    if event.key == 'n':
        current_mode = "node"
    elif event.key == 'e':
        current_mode = "edge"
    elif event.key == 'h':
        y = last_mouse_xy[1]
        if y is not None:
            state["guide_lines"]["horizontal"].append(y)
            undo_stack.append({"type": "guide", "data": ("horizontal", y)})
            redraw()
    elif event.key == 'v':
        x = last_mouse_xy[0]
        if x is not None:
            state["guide_lines"]["vertical"].append(x)
            undo_stack.append({"type": "guide", "data": ("vertical", x)})
            redraw()
    elif event.key == 's':
        save_json()
    elif event.key == 'l':
        load_json()
    elif event.key == 'z':
        if undo_stack:
            last = undo_stack.pop()
            if last['type'] == 'node':
                node_id = last['data']
                state['nodes'] = [n for n in state['nodes'] if n['id'] != node_id]
            elif last['type'] == 'edge':
                if state['edges']:
                    state['edges'].pop()
            elif last['type'] == 'guide':
                axis, val = last['data']
                state['guide_lines'][axis].remove(val)
            redraw()
        else:
            print("[실행 취소] 스택 비어 있음")

# 마우스 위치 기억용 변수
last_mouse_xy = [None, None]

# 마우스 이동 시 좌표 저장
def onmotion(event):
    if event.inaxes == ax and event.xdata is not None and event.ydata is not None:
        last_mouse_xy[0] = float(event.xdata)
        last_mouse_xy[1] = float(event.ydata)

# 시작
if not os.path.exists(FLOOR_IMAGE_PATH):
    print(f"이미지 파일이 없습니다: {FLOOR_IMAGE_PATH}")
    exit()

img = mpimg.imread(FLOOR_IMAGE_PATH)
fig, ax = plt.subplots(figsize=(12, 8))
ax.imshow(img, origin='upper')
ax.set_title("[n] 노드 | [e] 엣지 | [h/v] 가이드 | [z] 되돌리기 | [s/l] 저장/불러오기")
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', onkey)
fig.canvas.mpl_connect('motion_notify_event', onmotion)
load_json()
plt.tight_layout()
plt.show()
