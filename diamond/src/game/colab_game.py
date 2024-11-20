from typing import Tuple, Union

import numpy as np
from PIL import Image

from csgo.action_processing import CSGOAction
from .dataset_env import DatasetEnv
from .play_env import PlayEnv


class ColabGame:
	def __init__(
		self,
		play_env: Union[PlayEnv, DatasetEnv],
		size: Tuple[int, int],
		mouse_multiplier: int,
		fps: int,
		verbose: bool,
	) -> None:
		self.env = play_env
		self.height, self.width = size
		self.mouse_multiplier = mouse_multiplier
		self.fps = fps
		self.verbose = verbose

		self.env.print_controls()
		print("\nControls:\n")
		print(" m  : switch control (human/replay)") # Not for main as Game can use either PlayEnv or DatasetEnv
		print(" .  : pause/unpause")
		print(" e  : step-by-step (when paused)")
		print(" ⏎  : reset env")
		print("Esc : quit")
		print("\n")
		input("Press enter to start")

	def run(self) -> None:


		header_height = 150 if self.verbose else 0
		header_width = 540
		font_size = 16
		screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		pygame.mouse.set_visible(False)
		pygame.event.set_grab(True)
		clock = pygame.time.Clock()
		font = pygame.font.SysFont("mono", font_size)
		x_center, y_center = screen.get_rect().center
		x_header = x_center - header_width // 2
		y_header = y_center - self.height // 2 - header_height - 10
		header_rect = pygame.Rect(x_header, y_header, header_width, header_height)

		def clear_header():
			pygame.draw.rect(screen, pygame.Color("black"), header_rect)
			pygame.draw.rect(screen, pygame.Color("white"), header_rect, 1)

		def draw_text(text, idx_line, idx_column, num_cols):
			x_pos = 5 + idx_column * int(header_width // num_cols)
			y_pos = 5 + idx_line * font_size
			assert (0 <= x_pos <= header_width) and (0 <= y_pos <= header_height)
			screen.blit(font.render(text, True, pygame.Color("white")), (x_header + x_pos, y_header + y_pos))

		def draw_obs(obs, obs_low_res=None):
			assert obs.ndim == 4 and obs.size(0) == 1
			img = Image.fromarray(obs[0].add(1).div(2).mul(255).byte().permute(1, 2, 0).cpu().numpy())
			pygame_image = np.array(img.resize((self.width, self.height), resample=Image.BICUBIC)).transpose((1, 0, 2))
			surface = pygame.surfarray.make_surface(pygame_image)
			screen.blit(surface, (x_center - self.width // 2, y_center - self.height // 2))

			if obs_low_res is not None:
				assert obs_low_res.ndim == 4 and obs_low_res.size(0) == 1
				img = Image.fromarray(obs_low_res[0].add(1).div(2).mul(255).byte().permute(1, 2, 0).cpu().numpy())
				h = self.height * obs_low_res.size(2) // obs.size(2)
				w = self.width * obs_low_res.size(3) // obs.size(3)
				pygame_image = np.array(img.resize((w, h), resample=Image.BICUBIC)).transpose((1, 0, 2))
				surface = pygame.surfarray.make_surface(pygame_image)
				screen.blit(surface, (x_header + header_width - w - 5, y_header + 5 + font_size))
				# screen.blit(surface, (x_center - w // 2, y_center + self.height // 2))

		def reset():
			nonlocal obs, info, do_reset, ep_return, ep_length, keys_pressed, l_click, r_click, steering_value
			obs, info = self.env.reset()
			pygame.event.clear()
			do_reset = False
			ep_return = 0
			ep_length = 0
			keys_pressed = []
			steering_value = 0.0
			l_click = r_click = False
		
		steering_value = 0.0
		obs, info, do_reset, ep_return, ep_length, keys_pressed, l_click, r_click = (None,) * 8

		if do_reset:
			reset()
		do_wait = False
		should_stop = False


		csgo_action = CSGOAction(steering_value)
		next_obs, rew, end, trunc, info = self.env.step(csgo_action)

		draw_obs(next_obs)
		if end or trunc:
			reset()

		else:
			obs = next_obs
