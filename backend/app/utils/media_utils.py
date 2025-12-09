import exifread
import ffmpeg
import os
from PIL import Image, UnidentifiedImageError
from typing import Dict

class MediaUtils:
	@staticmethod
	async def extract_metadata(file_path: str) -> Dict:
		"""Извлечение метаданных для изображений и видео"""
		metadata = {}
		ext = os.path.splitext(file_path)[1].lower()

		try:
			# Обработка изображений
			if ext in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
				with Image.open(file_path) as img:
					metadata.update({
						"width": img.width,
						"height": img.height,
						"format": img.format
					})

				# EXIF данные только для JPEG
				if ext in ('.jpg', '.jpeg'):
					with open(file_path, 'rb') as f:
						tags = exifread.process_file(f, details=False)
						if tags:
							metadata["exif"] = {
								tag: str(value)
								for tag, value in tags.items()
								if tag not in ('JPEGThumbnail', 'TIFFThumbnail')
							}

			# Обработка SVG (упрощенная)
			elif ext == '.svg':
				metadata.update({"type": "vector"})

			# Обработка видео
			elif ext in ('.mp4', '.mov', '.avi', '.mkv', '.webm'):
				probe = ffmpeg.probe(file_path)
				video_stream = next(
					(stream for stream in probe['streams'] 
					 if stream['codec_type'] == 'video'), None
				)
				audio_stream = next(
					(stream for stream in probe['streams'] 
					 if stream['codec_type'] == 'audio'), None
				)

				if video_stream:
					metadata.update({
						"width": int(video_stream.get('width', 0)),
						"height": int(video_stream.get('height', 0)),
						"duration": float(video_stream.get('duration', 0)),
						"codec": video_stream.get('codec_name')
					})

				if audio_stream:
					metadata["audio"] = {
						"codec": audio_stream.get('codec_name'),
						"channels": audio_stream.get('channels')
					}

		except UnidentifiedImageError:
			pass  # Не удалось определить изображение
		except Exception as e:
			print(f"Metadata extraction error: {str(e)}")

		return metadata

	@staticmethod
	async def generate_thumbnail(
		input_path: str,
		output_path: str,
		size: tuple = (300, 300)
	) -> bool:
		"""Генерация превью для изображений и видео"""
		try:
			ext = os.path.splitext(input_path)[1].lower()

			# Для изображений
			if ext in ('.jpg', '.jpeg', '.png', '.webp'):
				with Image.open(input_path) as img:
					img.thumbnail(size)
					img.save(output_path)
				return True

			# Для видео (первый кадр)
			elif ext in ('.mp4', '.mov', '.avi'):
				(
					ffmpeg.input(input_path, ss='00:00:01')
					.filter('scale', size[0], -1)
					.output(output_path, vframes=1)
					.run(capture_stdout=True, capture_stderr=True)
				)
				return True

		except Exception as e:
			print(f"Thumbnail generation failed: {str(e)}")
			return False
