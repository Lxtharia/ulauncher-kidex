from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from src.functions import IndexEntry, KidexErrorException, KidexWarningException, get_find_results


class KidexExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument() or str()
        binary_path = extension.preferences["path_to_binary"] or "kidex-client"
        # TODO: Don't query, if the query string is empty
        max_results = int(extension.preferences["max_results"])
        items = []

        try:
            data = get_find_results(query, limit=max_results, command=binary_path)
            for entry in data:
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name='%s' % entry.basename,
                                                 description='At %s' % entry.path,
                                                 on_enter=ExtensionCustomAction(entry, keep_app_open=True)))

        except KidexWarningException as e:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=('Warning: %s' % e.name),
                description=str(e.desc),
            ))

        except KidexErrorException as e:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=('Error: %s' % e.name),
                description=str(e.desc),
            ))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        entry: IndexEntry = event.get_data()

        actions = [
            ExtensionSmallResultItem(
                name="Open",
                on_enter=OpenAction(entry.path)
            ),
            ExtensionSmallResultItem(
                name="Copy Full Path",
                on_enter=CopyToClipboardAction(entry.path)
                ),
        ]

        if entry.type == "directory":
            actions += [
            ]
        else:
            actions += [
                ExtensionSmallResultItem(
                    name="Open parent directory",
                    on_enter=OpenAction(entry.parent_dir)
                ),
            ]
        return RenderResultListAction(actions)


if __name__ == '__main__':
    KidexExtension().run()
