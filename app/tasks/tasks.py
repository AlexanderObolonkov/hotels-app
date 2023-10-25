from pathlib import Path

from PIL import Image

from app.tasks.celery import celery


@celery.task
def process_picture(path: str) -> None:
    large_res = (1000, 500)
    small_res = (200, 100)
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized_large = image.resize(large_res)
    image_resized_small = image.resize(small_res)
    image_resized_large.save(
        f"app/static/images/resized_{large_res[0]}_{large_res[1]}_{image_path.name}"
    )
    image_resized_small.save(
        f"app/static/images/resized_{small_res[0]}_{small_res[1]}_{image_path.name}"
    )
