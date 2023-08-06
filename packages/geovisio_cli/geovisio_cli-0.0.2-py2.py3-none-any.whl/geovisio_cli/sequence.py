from pathlib import Path, PurePath
from dataclasses import dataclass, field
from typing import List, Optional
import requests
from rich import print
from rich.table import Table
from rich.markup import escape
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    BarColumn,
    MofNCompleteColumn,
)
from rich.panel import Panel
from rich.console import Group
from rich.live import Live
from geovisio_cli.exception import CliException
from geovisio_cli.auth import login
from geovisio_cli.model import Geovisio
from time import sleep
from datetime import timedelta


@dataclass
class Picture:
    path: str


@dataclass
class SequenceToUpload:
    title: str
    pictures: List[Picture] = field(default_factory=lambda: [])


@dataclass
class UploadError:
    position: int
    picture_path: str
    error: str
    status_code: int


@dataclass
class UploadedPicture:
    path: str
    location: str


@dataclass
class UploadReport:
    location: str
    uploaded_pictures: List[UploadedPicture] = field(default_factory=lambda: [])
    errors: List[UploadError] = field(default_factory=lambda: [])


@dataclass
class PictureStatus:
    status: str
    id: str


@dataclass
class InteriorOrientation:
    make: str
    model: str
    field_of_view: Optional[int]


@dataclass
class GeovisioSequence:
    id: str
    title: str
    producer: Optional[str]
    interior_orientation: List[InteriorOrientation] = field(default_factory=lambda: [])


@dataclass
class SequenceStatus:
    pictures: List[PictureStatus] = field(default_factory=lambda: [])

    def all_done(self):
        return self.nb_waiting() + self.nb_preparing() == 0

    def nb_ready(self):
        return sum((1 for p in self.pictures if p.status == "ready"))

    def nb_waiting(self):
        return sum((1 for p in self.pictures if p.status == "waiting-for-process"))

    def nb_preparing(self):
        return sum((1 for p in self.pictures if p.status.startswith("preparing")))

    def nb_broken(self):
        return sum((1 for p in self.pictures if p.status == "broken"))


def process(path: Path) -> SequenceToUpload:
    sequence = _read_sequence(path)
    _check_sequence(sequence)
    return sequence


def upload(path: Path, geovisio: Geovisio, wait: bool = False) -> UploadReport:
    # early test that the given url is correct
    _test_geovisio_url(geovisio.url)

    sequence = process(path)

    return _publish(sequence, geovisio, wait)


def _publish(
    sequence: SequenceToUpload, geovisio: Geovisio, wait: bool
) -> UploadReport:
    print(f'📂 Publishing "{sequence.title}"')

    data = {}
    if sequence.title:
        data["title"] = sequence.title

    with requests.session() as s:
        seq = s.post(f"{geovisio.url}/api/collections", data=data)
        if seq.status_code == 401:
            login(s, geovisio)
            seq = s.post(f"{geovisio.url}/api/collections", data=data)
        seq.raise_for_status()

        seq_location = seq.headers["Location"]
        print(f"✅ Created collection {seq_location}")
        report = UploadReport(location=seq_location)

        uploading_progress = Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            TextColumn("[{task.completed}/{task.total}]"),
        )
        current_pic_progress = Progress(
            TextColumn("📷 Processing [bold purple]{task.fields[file]}"),
            SpinnerColumn("simpleDots"),
        )
        error_progress = Progress(TextColumn("{task.description}"))

        last_error = Progress(
            TextColumn("🔎 Last error 🔎\n{task.description}"),
        )
        error_panel = Panel(Group(error_progress, last_error), title="Errors")
        uploading_task = uploading_progress.add_task(
            f"[green]🚀 Uploading pictures...",
            total=len(sequence.pictures),
        )
        current_pic_task = current_pic_progress.add_task("", file="")
        progress_group = Group(
            uploading_progress,
            current_pic_progress,
            error_panel,
        )
        error_task = error_progress.add_task("[green]No errors")
        last_error_task = last_error.add_task("", visible=False)
        with Live(progress_group):
            for i, p in enumerate(sequence.pictures, start=1):
                uploading_progress.advance(uploading_task)
                current_pic_progress.update(
                    current_pic_task, file=p.path.split("/")[-1]
                )
                picture_response = s.post(
                    f"{seq_location}/items",
                    files={"picture": open(p.path, "rb")},
                    data={"position": i},
                )
                if picture_response.status_code >= 400:
                    body = (
                        picture_response.json()
                        if picture_response.headers.get("Content-Type")
                        == "application/json"
                        else picture_response.text
                    )
                    report.errors.append(
                        UploadError(
                            position=i,
                            picture_path=p.path,
                            status_code=picture_response.status_code,
                            error=body,
                        )
                    )

                    error_progress.update(
                        error_task,
                        description=f"[bold red]{len(report.errors)} errors",
                    )
                    last_error.update(last_error_task, description=body, visible=True)
                else:
                    report.uploaded_pictures.append(
                        UploadedPicture(
                            path=p.path,
                            location=picture_response.headers["Location"],
                        )
                    )

        if not report.uploaded_pictures:
            print(
                f"[red]💥 All pictures upload of sequence {sequence.title} failed! 💥[/red]"
            )
        else:
            print(
                f"🎉 [bold green]{len(report.uploaded_pictures)}[/bold green] pictures uploaded"
            )
        if report.errors:
            print(f"[bold red]{len(report.errors)}[/bold red] pictures not uploaded:")
            for e in report.errors:
                msg = escape(e.error.replace("\n", "\\n"))
                print(f" - {e.picture_path} (status [bold]{e.status_code}[/]): {msg}")

        if wait:
            wait_for_sequence(seq_location)
        else:
            print(f"Note: You can follow the picture processing with the command:")
            from rich.syntax import Syntax

            print(f"[bold]geovisio collection-status --wait --location {seq_location}")
        return report


def _check_sequence(sequence: SequenceToUpload):
    if not sequence.pictures:
        raise CliException(f"No pictures to upload for sequence {sequence.title}")


def _sort_files(pictures: List[Picture]) -> List[Picture]:
    """Sorts pictures according to their file name

    Parameters
    ----------
    pictures : Picture[]
        List of pictures to sort

    Returns
    -------
    Picture[]
        List of pictures, sorted
    """

    # Try to sort based on numeric notation
    try:
        pictures.sort(key=lambda p: int(PurePath(p.path).stem))
    # Otherwise, sort as strings
    except:
        pictures.sort(key=lambda p: PurePath(p.path).stem)

    return pictures


def _read_sequence(path: Path) -> SequenceToUpload:
    if not path.is_dir():
        raise CliException(f"{path} is not a directory, cannot read pictures")

    s = SequenceToUpload(title=path.name)

    for f in path.iterdir():
        if not f.is_file():
            continue
        if f.suffix.lower() not in [".jpg", ".jpeg"]:
            continue
        s.pictures.append(Picture(path=str(f)))

    s.pictures = _sort_files(s.pictures)

    return s


def _test_geovisio_url(geovisio: str):
    full_url = f"{geovisio}/api/collections"
    try:
        r = requests.get(full_url)
    except requests.ConnectionError as e:
        raise CliException(f"Impossible to query geovisio base url:\n\t{e}")
    if r.status_code >= 400:
        raise CliException(f"Impossible to query geovisio: {r.status_code}:\n {r.text}")


def status(sequence_location: str) -> SequenceStatus:
    s = requests.get(f"{sequence_location}/geovisio_status")
    if s.status_code == 404:
        raise CliException(f"Sequence {sequence_location} not found")
    if s.status_code >= 400:
        raise CliException(
            f"Impossible to get sequence {sequence_location} status: {s.text}"
        )
    r = s.json()
    return SequenceStatus(
        pictures=[PictureStatus(id=p["id"], status=p["status"]) for p in r["items"]]
    )


def info(sequence_location: str) -> GeovisioSequence:
    s = requests.get(sequence_location)
    if s.status_code == 404:
        raise CliException(f"Sequence {sequence_location} not found")
    if s.status_code >= 400:
        raise CliException(
            f"Impossible to get sequence {sequence_location} status: {s.text}"
        )
    r = s.json()
    producer = next(
        (p["name"] for p in r.get("providers", []) if "producer" in p["roles"]), None
    )
    summary = r.get("summaries", {}).get("pers:interior_orientation", [])
    return GeovisioSequence(
        id=r["id"],
        title=r["title"],
        producer=producer,
        interior_orientation=[
            InteriorOrientation(
                make=s.get("make"),
                model=s.get("model"),
                field_of_view=s.get("field_of_view"),
            )
            for s in summary
        ],
    )


def display_sequence_status(sequence_location: str):
    seq_status = status(sequence_location)
    seq_info = info(sequence_location)

    s = f"Sequence [bold]{seq_info.title}[/bold]"
    if seq_info.producer is not None:
        s += f" produced by [bold]{seq_info.producer}[/bold]"
    s += " taken with"
    for i in seq_info.interior_orientation:
        s += f" [bold]{i.make} {i.model}[/bold]"
        if i.field_of_view:
            s += f" ({i.field_of_view}°)"

    print(s)
    table = Table()

    table.add_column("Total")
    table.add_column("Ready", style="green")
    table.add_column("Waiting", style="magenta")
    table.add_column("Preparing", style="magenta")
    table.add_column("Broken", style="red")

    table.add_row(
        f"{len(seq_status.pictures)}",
        f"{seq_status.nb_ready()}",
        f"{seq_status.nb_waiting()}",
        f"{seq_status.nb_preparing()}",
        f"{seq_status.nb_broken()}",
    )
    print(table)


def _print_final_sequence_status(sequence_status: SequenceStatus):
    nb_broken = sequence_status.nb_broken()
    nb_ready = sequence_status.nb_ready()
    if nb_ready == 0:
        print(f"[red]💥 No picture processed")
        return
    s = f"✅ {nb_ready} pictures processed"
    if nb_broken:
        s += f"([red]{nb_broken}[/red] cannot be processed)"
    print(s)


def wait_for_sequence(sequence_location: str, timeout: Optional[timedelta] = None):
    seq_status = status(sequence_location)
    if seq_status.all_done():
        _print_final_sequence_status(seq_status)
        return

    print("🔭 Waiting for pictures to be processed by geovisio")
    status_progress = Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        MofNCompleteColumn(),
        "•",
        TextColumn("{task.fields[processing]}"),
    )
    processing_task = status_progress.add_task(
        f"[green]⏳ Processing ...",
        total=1,
        processing="",
    )
    progress_group = Group(
        status_progress,
    )
    waiting_time = timedelta(seconds=2)
    elapsed = timedelta(0)

    with Live(progress_group):
        while True:
            # TODO: display some stats about those errors

            nb_preparing = seq_status.nb_preparing()
            nb_waiting = seq_status.nb_waiting()
            processing = f"{nb_preparing} picture{('s' if nb_preparing != 0 else '')} currently processed"
            status_progress.update(
                processing_task,
                total=len(seq_status.pictures),
                completed=seq_status.nb_ready(),
                processing=processing,
            )

            if nb_waiting + nb_preparing == 0:
                break

            elapsed += waiting_time
            if timeout is not None and elapsed > timeout:
                raise CliException(f"❌ Sequence not ready after {elapsed}, stoping")

            sleep(waiting_time.total_seconds())
            seq_status = status(sequence_location)

    _print_final_sequence_status(seq_status)
