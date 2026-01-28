import time
import random
from pathlib import Path
from PIL import Image, ImageDraw

OUT_DIR = Path("/srv/ftp/images/incoming")
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1024, 1024
SLEEP_SECONDS = 30


def generate_nonsense(path: Path):
    img = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(img)

    # Random rectangles
    for _ in range(random.randint(20, 80)):
        x1 = random.randint(0, WIDTH)
        y1 = random.randint(0, HEIGHT)
        x2 = random.randint(x1, WIDTH)
        y2 = random.randint(y1, HEIGHT)
        color = tuple(random.randint(0, 255) for _ in range(3))
        draw.rectangle([x1, y1, x2, y2], fill=color)

    # Random lines
    for _ in range(random.randint(10, 40)):
        draw.line(
            [
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
            ],
            fill=tuple(random.randint(0, 255) for _ in range(3)),
            width=random.randint(1, 6),
        )

    img.save(path)


if __name__ == '__main__':
    counter = 0
    while True:
        filename = OUT_DIR / f"raw_{counter:06d}.png"
        generate_nonsense(filename)
        print(f"[+] Generated {filename}")
        counter += 1
        time.sleep(SLEEP_SECONDS)



