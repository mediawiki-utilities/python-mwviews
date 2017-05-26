import urllib.parse


class PageViewCount:
    __slots__ = ('project', 'page_name', 'views', 'bytes_returned')

    def __init__(self, project, page_name, views, bytes_returned):
        self.project = str(project)
        self.page_name = str(page_name)
        self.views = int(views)
        self.bytes_returned = int(bytes_returned)

    @classmethod
    def from_line(cls, line):
        line_split_on_spaces = line.strip().split(" ")

        views = line_split_on_spaces[-2]
        del(line_split_on_spaces[-2])

        bytes_returned = line_split_on_spaces[-1]
        del(line_split_on_spaces[-1])

        project = line_split_on_spaces[0]
        del(line_split_on_spaces[0])
        
        page_name = " ".join(line_split_on_spaces)
        page_name = urllib.parse.unquote(page_name).split("#")[0]  # No anchors

        return cls(project, page_name, int(views), int(bytes_returned))

    def to_line(self):
        return " ".join([self.project, self.page_name,
                         str(self.views), str(self.bytes_returned)])

    def __lt__(self, other):
        return (self.project, self.page_name) < \
               (other.project, other.page_name)
