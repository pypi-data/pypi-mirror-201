import io
from types import TracebackType
from typing import Any, List, Optional, Type, Union
from typing_extensions import Self
from tqdm import tqdm
from io import SEEK_CUR, SEEK_END, SEEK_SET

SeekMode = Union[type(SEEK_SET), type(SEEK_CUR), type(SEEK_END)]


class StreamProgressWrapper(io.IOBase):
    def __init__(
        self, stream: io.IOBase, *, desc: str = "", expected_size=None, guess_size=True
    ):
        self.stream = stream
        self.size = None
        self.desc = desc

        if expected_size is not None:
            self.size = expected_size
        elif guess_size and self.stream.seekable():
            pos = stream.tell()
            stream.seek(0, SEEK_END)
            self.size = stream.tell()
            stream.seek(pos, SEEK_SET)
        else:
            pass

        self.progress_bar = tqdm(total=self.size, desc=desc)

    def __enter__(self) -> Self:
        self.stream.__enter__()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Any:
        return self.stream.__exit__(exc_type, exc_val, exc_tb)

    def close(self) -> None:
        self.stream.close()

    @property
    def closed(self) -> bool:
        return self.stream.closed

    def read(self, hint=-1):
        data = self.stream.read(hint)
        self.progress_bar.update(len(data))
        return data

    def readline(self, size: Optional[int] = None):
        data = self.stream.readline(size)
        self.progress_bar.update(len(data))
        return data

    def readlines(self, hint: Optional[int] = None) -> List:
        lines = self.stream.readlines(hint)
        num_data = sum([len(line) for line in lines])
        self.progress_bar.update(num_data)
        return lines

    def seek(self, offset: int, whence: SeekMode = SEEK_SET) -> int:
        pos = self.stream.seek(offset, whence)
        self.progress_bar.n = pos
        return pos

    def tell(self) -> int:
        return self.stream.tell()
