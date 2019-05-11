from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
from build_dashboard.views import BuildbotView, BuildListView
from build_dashboard import logger

def draw_screen(model, loop, update_secs=5):
    screen = Screen.open()
    scenes = []
    scenes.append(Scene([BuildbotView(screen, model)], -1, name="BuildbotView"))
    scenes.append(Scene([BuildListView(screen, model)], -1, name="BuildListView"))
    screen.set_scenes(scenes)

    while True:
        try:
            loop.run_until_complete(model.update())
            screen.force_update()
            screen.draw_next_frame(repeat=True)
            screen.wait_for_input(0.05)
        except RuntimeError as e:
            logger.debug(e)
            break
        except ResizeScreenError as e:
            logger.debug(e)
            break
        except KeyboardInterrupt as e:
            logger.debug(e)
            break
    screen.close()
