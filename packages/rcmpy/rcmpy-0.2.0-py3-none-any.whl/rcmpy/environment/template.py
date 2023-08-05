"""
An environment extension for working with template files.
"""

# third-party
from datazen.templates import environment
from jinja2 import FileSystemLoader

# internal
from rcmpy.environment.base import BaseEnvironment


class TemplateEnvironment(BaseEnvironment):
    """
    A class implementing template management for this package's runtime
    environment.
    """

    def _init_loaded(self) -> None:
        """Called during initialization if a valid configuration is loaded."""

        super()._init_loaded()

        if not hasattr(self, "jinja"):
            template_root = self.state.directory.joinpath("templates")

            template_dirs = [
                x
                for x in [
                    template_root.joinpath(self.state.variant),
                    template_root.joinpath("common"),
                ]
                if x.is_dir()
            ]

            # Prefer variant templates, if the variant template-directory
            # exists.
            self.jinja = environment(
                loader=FileSystemLoader(
                    template_dirs,
                    followlinks=True,
                )
            )

            # Tasks to do:
            # - split into two kinds of files, literal files and actual jinja
            #   templates (check for .j2 extension)
            # - find the full, absolute paths of the template objects
            # - add the template dirs to the template file-info cache
            # - use vcorelib file-info cache to figure out which templates are
            #   new or changed (log this?)
            for template in self.jinja.list_templates():
                print(template)
