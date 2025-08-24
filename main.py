from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from src.functions import KidexErrorException, KidexWarningException, get_find_results

class KidexExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument() or str()
        max_results = int(extension.preferences["max_results"])
        items = []

        try:
            data = get_find_results(query, limit=max_results)
            for entry in data:
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name='%s' % entry.basename,
                                                 description='At %s' % entry.path,
                                                 on_enter=ExtensionCustomAction({}, keep_app_open=True)))

        except KidexWarningException as e:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Warning: %s' % e,
            ))
        except KidexErrorException as e:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Error: %s' % e,
            ))

        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        actions = [
            ExtensionResultItem(
                name="Copy",
                on_enter=HideWindowAction()
            ),
        ]
        return RenderResultListAction(actions)


if __name__ == '__main__':
    KidexExtension().run()
