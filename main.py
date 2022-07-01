from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
import animego


class AnimeGoExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        searchKeyword = event.get_argument()
        if not searchKeyword:
            return

        return RenderResultListAction(animego.search(searchKeyword))


if __name__ == "__main__":
    AnimeGoExtension().run()
