import functools
from pathlib import Path
from typing import Optional

from iolanta.iolanta import Iolanta
from iolanta.namespaces import IOLANTA
from iolanta_jinja2.macros import template_render
from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files


class IolantaPlugin(BasePlugin):   # type: ignore
    """Integrate MkDocs + iolanta."""

    iolanta: Iolanta

    def on_files(    # type: ignore
        self,
        files: Files,
        *,
        config: MkDocsConfig,
    ) -> Optional[Files]:
        """Construct the local iolanta instance and load files."""
        self.iolanta.add(source=Path(config.docs_dir))

    def on_config(self, config: MkDocsConfig) -> Optional[Config]:
        """Expose configuration & template variables."""
        self.iolanta = Iolanta()

        config.extra['iolanta'] = self.iolanta
        config.extra['render'] = functools.partial(
            template_render,
            iolanta=self.iolanta,
            environments=[IOLANTA.html],
        )
        return config
