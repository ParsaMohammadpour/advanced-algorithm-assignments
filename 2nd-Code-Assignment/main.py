import numpy as np
import math
import cv2
import pandas as pd

# Some colors
cyan_color = (255, 255, 0)
cadet_blue_color = (160, 158, 95)
dark_cyan_color = (139, 139, 255)
light_steel_blue_color = (222, 196, 176)
medium_aqua_marin_color = (170, 205, 102)
spring_green_color = (0, 255, 127)
sky_blue_color = (235, 206, 135)
crimson_color = (60, 20, 220)
magneta_color = (255, 0, 255)
fire_brick_color = (34, 34, 178)
gold_color = (0, 215, 255)

def generate_random_numbers(n: int = 100, height_bound: tuple[int, int] = (20, 680),
                            width_bound: tuple[int, int] = (20, 1180)) -> np.array:
    np.random.seed()
    x = np.random.randint(width_bound[0], width_bound[1], n)
    y = np.random.randint(height_bound[0], height_bound[1], n)
    return [tuple(x) for x in zip(x, y)]

def generate_base_image(points: list[tuple[int]], height: int = 700, width: int = 1200,
                        color: tuple[int] = sky_blue_color) -> np.array:
    # we use zeros function, this makes a black image
    img = np.zeros((height, width, 3), np.uint8)
    for p in points:
        cv2.circle(img, (int(p[0]), int(p[1])), 7, color, -1)
    return img

def get_most_left_point(points: np.array):
    return min(points, key=lambda x: x[0])

def get_vector_size(vector: tuple[float, float]) -> float:
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

def convert_points_to_vector(start: tuple[float, float], end: tuple[float, float]) -> tuple[float, float]:
    return end[0] - start[0], end[1] - start[1]

def calculate_vector_dot_product(vector1, vector2) -> float:
    return vector1[0] * vector2[0] + vector1[1] * vector2[1]

def calculate_vector_cosin(vector1, vector2) -> float:
    dot_product = calculate_vector_dot_product(vector1, vector2)
    size1, size2 = get_vector_size(vector1), get_vector_size(vector2)
    if size1 == 0 or size2 == 0: return 1
    return dot_product / (size1 * size2)

def calculate_point_cosin(coordinator: tuple[float, float], new_point: tuple[float, float],
                          pre_node: tuple[float, float]) -> float:
    vector1 = convert_points_to_vector(coordinator, pre_node)
    vector2 = convert_points_to_vector(coordinator, new_point)
    return calculate_vector_cosin(vector1, vector2)

def get_next_left_most(points: np.array, coordinator: tuple[float, float], pre: tuple[float, float] = None) -> tuple[
    float, float]:
    if pre is None: pre = coordinator[0], coordinator[1] - 0.001
    return min(points, key=lambda x: calculate_point_cosin(coordinator, x, pre))

def image_new_circle(img, point: tuple[float], passed_point_color: tuple[int],
                     current_point_color: tuple[int], step: int) -> np.array:
    temp_img = cv2.circle(img.copy(), point, 14, current_point_color, -1)
    cv2.imwrite(f'results\\image-{step}.png', temp_img)
    img = cv2.circle(img, point, 7, passed_point_color, -1)
    return img

def get_points_in_order(points: list[tuple[int]], height: int = 700, width: int = 1200,
                        base_point_color: tuple[int] = sky_blue_color,
                        passed_point_color: tuple[int] = spring_green_color,
                        current_point_color: tuple[int] = crimson_color, line_color: tuple[int] = gold_color) -> list[
    tuple[int, int]]:
    img = generate_base_image(points, height, width, base_point_color)
    if len(points) < 3: raise ValueError("Not enough points")
    res = []
    first_node = get_most_left_point(points)
    step = 1
    img = image_new_circle(img, first_node, passed_point_color, current_point_color, step)
    res.append(first_node)
    pre_node = first_node
    curr_node = get_next_left_most(points, first_node)
    while curr_node != first_node:
        step += 1
        res.append(curr_node)
        img = cv2.line(img, curr_node, pre_node, line_color, 2)
        img = image_new_circle(img, curr_node, passed_point_color, current_point_color, step)
        new_curr = get_next_left_most(points, curr_node, pre_node)
        pre_node = curr_node
        curr_node = new_curr
    img = cv2.line(img, first_node, pre_node, line_color, 2)
    cv2.imwrite(f'results\\final-image.png', img)
    return img

def save_points(points: np.array):
    df = pd.DataFrame(points, columns=['x', 'y'])
    df.to_csv('results\\points.csv', index=False)

if __name__ == '__main__':
    points = generate_random_numbers(200) # generating random points
    save_points(points) # saving points in .csv file
    image = get_points_in_order(points) # running algorithm and getting final output image
    cv2.imshow('img', image) # showing image
    cv2.waitKey(0)
    cv2.destroyAllWindows()
