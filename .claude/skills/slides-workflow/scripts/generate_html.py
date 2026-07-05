#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


COURSES_TEXT_ROOT = Path(
    os.environ.get(
        "COURSES_TEXT_ROOT",
        str(Path.home() / "Documents/products/courses/library/texts"),
    )
)


@dataclass(frozen=True)
class CourseConfig:
    course: str
    prefix: str
    package: str
    target_dir: str
    source_subdirs: tuple[str, ...]
    list_rel_y: int = 1200
    version: str = "2602"


COURSES: dict[str, CourseConfig] = {
    "gai": CourseConfig(
        course="gai",
        prefix="gai",
        package="gai-slide-drafts",
        target_dir="5gai",
        source_subdirs=("slide-drafts", "cases", "course-planning", "mindmaps", "materials"),
        list_rel_y=800,
    ),
    "cciot": CourseConfig(
        course="cciot",
        prefix="cciot",
        package="cciot-slide-drafts",
        target_dir="2cciot",
        source_subdirs=("slide-drafts", "mindmaps", "textbook-drafts", "integrated-drafts"),
    ),
    "dbpa": CourseConfig(
        course="dbpa",
        prefix="dbpa",
        package="dbpa-slide-drafts",
        target_dir="1dbpa",
        source_subdirs=("slide-drafts", "course-planning", "mindmaps", "textbook-drafts"),
    ),
    "ita": CourseConfig(
        course="ita",
        prefix="ita",
        package="ita-slide-drafts",
        target_dir="6ita",
        source_subdirs=("slide-drafts", "course-planning", "mindmaps", "cases", "tasks", "supporting-notes"),
    ),
    "pmi": CourseConfig(
        course="pmi",
        prefix="pmi",
        package="pmi-slide-drafts",
        target_dir="10pmi",
        source_subdirs=("slide-drafts", "course-planning", "mindmaps", "layout-data", "materials"),
    ),
    "itpm": CourseConfig(
        course="itpm",
        prefix="itpm",
        package="itpm-slide-drafts",
        target_dir="3itpm",
        source_subdirs=("slide-drafts",),
    ),
    "il": CourseConfig(
        course="il",
        prefix="il",
        package="il-slide-drafts",
        target_dir="8il",
        source_subdirs=("slide-drafts", "course-planning", "supporting-notes", "textbook-drafts"),
    ),
    "fiit": CourseConfig(
        course="fiit",
        prefix="fiit",
        package="fiit-slide-drafts",
        target_dir="9fiit",
        source_subdirs=("slide-drafts", "course-planning", "mindmaps"),
    ),
}


def project_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "AGENTS.md").exists() and (parent / "sh").exists():
            return parent
    return Path.cwd().resolve()


def infer_course_from_path(path: Path) -> str | None:
    resolved = path.resolve()
    for part in resolved.parts:
        if part.endswith("-slide-drafts"):
            return part.removesuffix("-slide-drafts")

    stem = path.stem
    prefix = stem.split("-", 1)[0].lower()
    if prefix in COURSES:
        return prefix
    if prefix.startswith("g") and prefix[1:] in COURSES:
        return prefix[1:]

    cwd_name = Path.cwd().resolve().name
    for course, config in COURSES.items():
        if cwd_name == config.target_dir:
            return course
    return None


def resolve_markdown_path(raw_input: str, course: str | None) -> tuple[Path, CourseConfig]:
    name = raw_input.strip()
    if not name:
        raise SystemExit("No markdown file provided.")
    if not name.endswith(".md"):
        name += ".md"

    direct = Path(name).expanduser()
    if direct.is_file():
        inferred = course or infer_course_from_path(direct)
        if inferred not in COURSES:
            raise SystemExit(f"Cannot infer course for {direct}; pass --course.")
        return direct.resolve(), COURSES[inferred]

    if course is None:
        inferred = infer_course_from_path(Path(name))
        if inferred in COURSES:
            course = inferred
    if course not in COURSES:
        raise SystemExit(f"Unknown course; pass --course. Known: {', '.join(sorted(COURSES))}")

    config = COURSES[course]
    package = COURSES_TEXT_ROOT / config.package
    for subdir in config.source_subdirs:
        candidate = package / subdir / Path(name).name
        if candidate.is_file():
            return candidate.resolve(), config
    raise SystemExit(f"Markdown not found in {package}: {name}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_chapter_section(markdown_file: Path) -> tuple[str, str, str, str]:
    lines = [line.strip() for line in read_text(markdown_file).splitlines() if line.strip()]
    if not lines:
        raise SystemExit(f"{markdown_file} must contain a title line.")

    chapter = lines[0]
    section = lines[1] if len(lines) > 1 and re.match(r"^\d+\.\d+\s+", lines[1]) else chapter
    filename_match = re.search(r"(\d+)-(\d+)", markdown_file.stem)

    try:
        chapter_number = chapter.split(".", 1)[0] if "." in chapter else filename_match.group(1)
        if "." in section and section != chapter:
            section_number = section.split(".", 1)[1].split(" ", 1)[0]
        else:
            section_number = filename_match.group(2)
    except (AttributeError, IndexError) as exc:
        raise SystemExit(f"Cannot parse chapter/section numbers from {markdown_file}.") from exc

    return chapter, section, chapter_number, section_number


class HTMLGenerator:
    def __init__(self, markdown_file: Path, html_file: Path, config: CourseConfig):
        self.markdown_file = markdown_file
        self.html_file = html_file
        self.config = config
        root = project_root()
        target = root / config.target_dir
        header_candidates = [target / "header.html", root / "sh/header.html"]
        header_path = next((candidate for candidate in header_candidates if candidate.is_file()), None)
        footer_path = root / "sh/footer.html"
        if header_path is None:
            searched = ", ".join(str(candidate) for candidate in header_candidates)
            raise SystemExit(f"Missing course/shared header; searched: {searched}")
        if not footer_path.is_file():
            raise SystemExit(f"Missing shared footer: {footer_path}")

        self.header = read_text(header_path)
        self.footer = read_text(footer_path)
        self.div_blocks: list[str] = []
        self.div_id_counter = 1
        self.header_processed = False
        self.section: str | None = None
        self.chapter_number: str | None = None
        self.section_number: str | None = None
        self.nav_questions = ""

    @staticmethod
    def get_div_id(div_block: str) -> str | None:
        match = re.search(r'id\s*=\s*"([^"]*)"', div_block)
        return match.group(1) if match else None

    @staticmethod
    def identify_block_type(block: str) -> str:
        lines = [line for line in block.split("\n") if line.strip()]
        if not lines:
            return "unknown"
        if lines[0].startswith("### "):
            return "list"
        if lines[0].startswith("!["):
            return "image_with_title" if len(lines) > 1 and lines[1].startswith("#### ") else "image"
        if block.startswith("    "):
            return "code"
        if lines[0].startswith("$$") and lines[-1].endswith("$$"):
            return "equation"
        return "unknown"

    def process_div_block(self, block: str) -> None:
        block_type = self.identify_block_type(block)
        if block_type == "list":
            self.process_list(block)
        elif block_type == "image_with_title":
            self.process_image_with_title(block)
        elif block_type == "image":
            self.process_image(block)
        elif block_type == "code":
            self.process_code(block)
        elif block_type == "equation":
            self.process_equation(block)
        elif block_type == "unknown":
            print("Unknown block type", file=sys.stderr)

    def process_header(self) -> None:
        chapter, section, chapter_number, section_number = parse_chapter_section(self.markdown_file)
        self.section = section
        self.chapter_number = chapter_number
        self.section_number = section_number
        section_heading = "" if section == chapter else f'        <h3 style="text-align: center">{section}</h3>\n'
        self.div_blocks.append(f'''    <div
    id         = "c{chapter_number}{section_number}t"
    class      = "step"
    data-x     = "0"
    data-y     = "0"
    data-z     = "0"
    data-scale = "5">

    <!-- 修改标题 -->
        <h2>{chapter}</h2>
{section_heading}        <p class="footnote">
            <inlinecode style="font-size: 16px">
            Powered by
            </inlinecode>
                <a href="https://github.com/impress/impress.js/">
                    <inlinecode style="font-size: 16px">
                    impress.js
                    </inlinecode>
                    <img class="icon" src="../favicon.png" style="width:10px;height:10px;">
                </a>
                <br/>
                <inlinecode style="font-size: 16px">
                    Ver. {self.config.version}
                </inlinecode>
            </inlinecode>
        </p>

    </div>
        ''')

    def append_content_div(self, current_div_id: str, class_name: str, rel_y: int, content: str) -> None:
        last_div_id = self.get_div_id(self.div_blocks[-1]) if self.div_blocks else None
        self.div_blocks.append(f'''
    <div
    id            = "{current_div_id}"
    class         = "{class_name}"
    data-rel-to   = "{last_div_id if last_div_id is not None else 'empty'}"
    data-rel-x    = "0"
    data-rel-y    = "{rel_y}"
    data-rel-z    = "0"
    data-rotate-y = "0"
    data-scale    = "2">

{content}

    </div>
''')
        self.div_id_counter += 1

    def process_list(self, block: str) -> None:
        lines = block.split("\n")
        title = lines[0]
        list_items = [line for line in lines[1:] if line.strip()]
        content = "\n".join([title, "", *list_items])
        self.append_content_div(f"a{self.div_id_counter}", "step markdown", self.config.list_rel_y, content)

    def process_image(self, block: str) -> None:
        image_link = block.split("\n")[0]
        self.append_content_div(f"a{self.div_id_counter}", "step markdown", 0, image_link)

    def process_image_with_title(self, block: str) -> None:
        lines = block.split("\n")
        image_link = lines[0]
        image_title = "\n".join(line for line in lines[1:] if line.strip())
        self.append_content_div(f"a{self.div_id_counter}", "step markdown", 0, f"{image_link}\n{image_title}")

    def process_equation(self, block: str) -> None:
        content = "\n".join(line for line in block.split("\n") if line.strip())
        self.append_content_div(f"a{self.div_id_counter}", "step", self.config.list_rel_y, content)

    def process_code(self, block: str) -> None:
        content = "\n".join(line for line in block.split("\n")[1:] if line.strip())
        self.append_content_div(f"a{self.div_id_counter}", "step markdown", self.config.list_rel_y, content)

    def process_navigation_and_questions(self) -> None:
        if self.chapter_number is None or self.section_number is None or self.section is None:
            raise SystemExit("Cannot build navigation before title page.")
        chapter_number_0 = f"{int(self.chapter_number):02d}"
        prefix = self.config.prefix
        self.nav_questions = f'''
    <div
    id            = "mm{self.chapter_number}{self.section_number}"
    class         = "step"
    data-rel-to   = "c{self.chapter_number}{self.section_number}t"
    data-rel-x    = "0"
    data-rel-y    = "-2000"
    data-rotate-y = "0"
    data-rotate   = "0"
    data-scale    = "1"
    style         = "width: 92vw; height: 92vh; display: flex; justify-content: center; align-items: center;">

    <iframe
    src           = "img/c{chapter_number_0}/mindmap-{self.chapter_number}-{self.section_number}.html"
    style         = "width: 100%; height: 100%; border: none;"
    allowfullscreen>
    </iframe>

    </div>

<!-- 本节问题 -->

    <div
    id            = "c{self.chapter_number}{self.section_number}q"
    class         = "step markdown"
    data-rel-to   = "c{self.chapter_number}{self.section_number}t"
    data-rel-x    = "0"
    data-rel-y    = "-800"
    data-z        = "500"
    data-rotate-x = "77"
    data-rotate-y = "0"
    data-rotate-z = "180"
    data-scale    = "2">

### {self.section}

-
-

----

[ {self.section}]({prefix}-{self.chapter_number}-{self.section_number}.html#/overview)
[| 练习 |]({prefix}-exec.html)
[ {self.section}]({prefix}-{self.chapter_number}-{self.section_number}.html#/overview)

    </div>
'''

    def generate_html(self) -> Path:
        markdown_lines = self.markdown_file.read_text(encoding="utf-8").splitlines(keepends=True)
        block: list[str] = []
        for line in markdown_lines:
            if line == "\n":
                if not self.header_processed:
                    self.process_header()
                    self.header_processed = True
                else:
                    self.process_div_block("".join(block))
                block = []
            else:
                block.append(line)

        if block:
            self.process_div_block("".join(block))

        if not self.header_processed:
            self.process_header()
        self.process_navigation_and_questions()
        self.div_blocks.append(self.nav_questions)

        self.html_file.parent.mkdir(parents=True, exist_ok=True)
        self.html_file.write_text(self.header + "\n" + "".join(self.div_blocks) + "\n" + self.footer, encoding="utf-8")
        return self.html_file


def default_output_path(markdown_file: Path, config: CourseConfig) -> Path:
    return project_root() / config.target_dir / f"{markdown_file.stem}.html"


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate impress.js HTML from a course markdown source.")
    parser.add_argument("markdown", nargs="?", help="Markdown file path or filename within the course source package.")
    parser.add_argument("--course", choices=sorted(COURSES), help="Course key used to resolve package-local filenames.")
    parser.add_argument("-o", "--output", help="Explicit output HTML path. Defaults to the configured target course directory.")
    return parser


def main(argv: list[str] | None = None, default_course: str | None = None) -> None:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    raw = args.markdown or input("Input the Markdown filename please:")
    markdown_file, config = resolve_markdown_path(raw, args.course or default_course)
    output = Path(args.output).expanduser() if args.output else default_output_path(markdown_file, config)
    generated = HTMLGenerator(markdown_file, output, config).generate_html()
    print(f"Generated {generated}")


if __name__ == "__main__":
    main()
