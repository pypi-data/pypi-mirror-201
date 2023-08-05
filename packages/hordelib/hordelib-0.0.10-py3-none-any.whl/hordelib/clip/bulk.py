import hashlib
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Literal, Union

import numpy as np
from PIL import Image
from tqdm import tqdm

from hordelib import disable_progress
from hordelib.cache import Cache
from hordelib.clip.image import ImageEmbed
from hordelib.model_manager.clip import ClipModelManager
from loguru import logger


class BulkImageEmbedder:
    def __init__(self):
        self.model_manager = None
        self.model_name = None
        self.image_embed = None
        self.cache_image = None
        self.executor = ThreadPoolExecutor(max_workers=4)

    def __call__(
        self,
        model_name: Literal["ViT-L/14", "ViT-H-14"] = "ViT-L/14",
        input_directory: str = "input",
    ):
        """
        :param model_name: Name of model to use
        :param input_directory: Directory to read input from
        """
        self.model_name = model_name
        self.model_manager = ClipModelManager()
        self.cache_image = Cache(
            self.model_name, cache_parentname="embeds", cache_subname="image"
        )
        self.model_manager.load(self.model_name)
        self.image_embed = ImageEmbed(
            self.model_manager.loaded_models[self.model_name], self.cache_image
        )
        self._prepare_from_directory(input_directory=input_directory)

    def insert(self, image, input_directory):
        pil_image = Image.open(f"{input_directory}/{image}.webp").convert("RGB")
        pil_hash = hashlib.sha256(pil_image.tobytes()).hexdigest()
        # hash = hashlib.sha256(open(f"{input_directory}/{image}.webp", "rb").read()).hexdigest()
        self.cache_image.add_sqlite_row(file=image, pil_hash=pil_hash, hash=None)

    def _prepare_from_directory(self, input_directory: str):
        """
        :param input_directory: Directory to read input from
        """
        logger.info(f"Reading from {input_directory}")
        directory_list = self.cache_image.list_dir(input_directory)
        logger.info(f"Found {len(directory_list)} files. Filtering...")
        filtered_list = self.cache_image.filter_list(directory_list)
        logger.info(f"Found {len(filtered_list)} files to embed.")
        for image in tqdm(filtered_list, disable=disable_progress.active):
            self.insert(image, input_directory)
