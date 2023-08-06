import pykeepass


class Credentials:

    def __init__(self, filename, password=None, keyfile=None) -> None:
        self._kdbx = pykeepass.PyKeePass(filename, password, keyfile)

    def __len__(self) -> int:
        return len(self._kdbx.entries)

    def __contains__(self, title: str) -> bool:
        if self._kdbx.find_entries(title=title, first=True):
            return True
        return False

    def __iter__(self):
        return iter(self._kdbx.entries)

    def __getitem__(self, title: str) -> pykeepass.entry.Entry:
        item = self._kdbx.find_entries(
            title=title,
            first=True)
        return item

    def get(self, title: str) -> pykeepass.entry.Entry:
        item = self.__getitem__(title)
        return item if item else None

    def add(self, title, username, password) -> pykeepass.entry.Entry:
        try:
            res = self._kdbx.add_entry(
                self._kdbx.root_group, title, username, password)
        except Exception as e:
            res = None
            if 'already exists' in str(e):
                raise ValueError(
                    'Entry "{}" already exists in the root group'.format(
                        title))
            else:
                raise e
        self._kdbx.save()
        return res

    def delete(self, title):
        item = self.__getitem__(title)
        if item:
            item.delete()
            self._kdbx.save()
