#! /usr/bin/env python
"""Creation of a github-page for the review as part of the data operations"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import zope.interface
from dataclasses_jsonschema import JsonSchemaMixin

import colrev.env.package_manager
import colrev.env.utils
import colrev.record
import colrev.ui_cli.cli_colors as colors

if False:  # pylint: disable=using-constant-test
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        import colrev.ops.data
        import git


@zope.interface.implementer(colrev.env.package_manager.DataPackageEndpointInterface)
@dataclass
class GithubPages(JsonSchemaMixin):
    """Export the literature review into a Github Page"""

    ci_supported: bool = False

    @dataclass
    class GHPagesSettings(colrev.env.package_manager.DefaultSettings, JsonSchemaMixin):
        """Settings for GithubPages"""

        endpoint: str
        version: str
        auto_push: bool

        _details = {
            "auto_push": {
                "tooltip": "Indicates whether the Github Pages branch "
                "should be pushed automatically"
            },
        }

    GH_PAGES_BRANCH_NAME = "gh-pages"

    settings_class = GHPagesSettings

    def __init__(
        self,
        *,
        data_operation: colrev.ops.data.Data,
        settings: dict,
    ) -> None:
        # Set default values (if necessary)
        if "version" not in settings:
            settings["version"] = "0.1.0"
        if "auto_push" not in settings:
            settings["auto_push"] = True

        self.settings = self.settings_class.load_settings(data=settings)
        self.review_manager = data_operation.review_manager

    def get_default_setup(self) -> dict:
        """Get the default setup"""
        github_pages_endpoint_details = {
            "endpoint": "colrev.github_pages",
            "version": "0.1",
            "auto_push": True,
        }

        return github_pages_endpoint_details

    def __setup_github_pages_branch(
        self, *, data_operation: colrev.ops.data.Data, git_repo: git.Repo
    ) -> None:
        # if branch does not exist: create and add index.html
        data_operation.review_manager.logger.info("Setup github pages")
        git_repo.create_head(self.GH_PAGES_BRANCH_NAME)
        git_repo.git.checkout(self.GH_PAGES_BRANCH_NAME)
        title = "Manuscript template"
        readme_file = data_operation.review_manager.readme
        if readme_file.is_file():
            with open(readme_file, encoding="utf-8") as file:
                title = file.readline()
                title = title.replace("# ", "").replace("\n", "")
                title = '"' + title + '"'
        git_repo.git.rm("-rf", Path("."))

        gitignore_file = Path(".gitignore")
        git_repo.git.checkout("HEAD", "--", gitignore_file)
        with gitignore_file.open("a", encoding="utf-8") as file:
            file.write("status.yaml\n")
        data_operation.review_manager.dataset.add_changes(path=gitignore_file)

        colrev.env.utils.retrieve_package_file(
            template_file=Path("template/github_pages/index.html"),
            target=Path("index.html"),
        )
        data_operation.review_manager.dataset.add_changes(path=Path("index.html"))
        colrev.env.utils.retrieve_package_file(
            template_file=Path("template/github_pages/_config.yml"),
            target=Path("_config.yml"),
        )
        colrev.env.utils.inplace_change(
            filename=Path("_config.yml"),
            old_string="{{project_title}}",
            new_string=title,
        )
        data_operation.review_manager.dataset.add_changes(path=Path("_config.yml"))
        colrev.env.utils.retrieve_package_file(
            template_file=Path("template/github_pages/about.md"),
            target=Path("about.md"),
        )
        data_operation.review_manager.dataset.add_changes(path=Path("about.md"))

    def __update_data(
        self, *, data_operation: colrev.ops.data.Data, silent_mode: bool
    ) -> None:
        if not silent_mode:
            data_operation.review_manager.logger.info("Update data on github pages")
        records = data_operation.review_manager.dataset.load_records_dict()

        # pylint: disable=duplicate-code
        included_records = {
            r["ID"]: r
            for r in records.values()
            if r["colrev_status"]
            in [
                colrev.record.RecordState.rev_synthesized,
                colrev.record.RecordState.rev_included,
            ]
        }
        data_file = Path("data.bib")
        data_operation.review_manager.dataset.save_records_dict_to_file(
            records=included_records, save_path=data_file
        )
        data_operation.review_manager.dataset.add_changes(path=data_file)

        data_operation.review_manager.create_commit(msg="Update sample")

    def __push_branch(
        self,
        *,
        data_operation: colrev.ops.data.Data,
        git_repo: git.Repo,
        silent_mode: bool,
    ) -> None:
        if not silent_mode:
            data_operation.review_manager.logger.info("Push to github pages")
        if "origin" in git_repo.remotes:
            if "origin/gh-pages" in [r.name for r in git_repo.remotes.origin.refs]:
                git_repo.git.push("origin", self.GH_PAGES_BRANCH_NAME, "--no-verify")
            else:
                git_repo.git.push(
                    "--set-upstream",
                    "origin",
                    self.GH_PAGES_BRANCH_NAME,
                    "--no-verify",
                )

            username, project = (
                git_repo.remotes.origin.url.replace("https://github.com/", "")
                .replace(".git", "")
                .split("/")
            )
            if not silent_mode:
                data_operation.review_manager.logger.info(
                    f"Data available at: https://{username}.github.io/{project}/"
                )
        else:
            if not silent_mode:
                data_operation.review_manager.logger.info("No remotes specified")

    def __check_gh_pages_setup(self, *, git_repo: git.Repo) -> None:
        username, project = (
            git_repo.remotes.origin.url.replace("https://github.com/", "")
            .replace(".git", "")
            .split("/")
        )
        gh_page_link = f"https://{username}.github.io/{project}/"
        if gh_page_link not in (self.review_manager.path / Path("readme.md")).read_text(
            encoding="utf-8"
        ):
            print(
                f"{colors.ORANGE}The Github page is not yet linked in the readme.md file.\n"
                "To make it easier to access the page, add the following to the readme.md file:\n"
                f"\n    [Github page]({gh_page_link}){colors.END}\n"
            )

    def update_data(
        self,
        data_operation: colrev.ops.data.Data,
        records: dict,  # pylint: disable=unused-argument
        synthesized_record_status_matrix: dict,  # pylint: disable=unused-argument
        silent_mode: bool,
    ) -> None:
        """Update the data/github pages"""

        if data_operation.review_manager.in_ci_environment():
            data_operation.review_manager.logger.error(
                "Running in CI environment. Skipping github-pages generation."
            )
            return

        if data_operation.review_manager.dataset.has_changes():
            data_operation.review_manager.logger.error(
                "Cannot update github pages because there are uncommited changes."
            )
            return

        git_repo = data_operation.review_manager.dataset.get_repo()
        active_branch = git_repo.active_branch

        if self.GH_PAGES_BRANCH_NAME not in [h.name for h in git_repo.heads]:
            self.__setup_github_pages_branch(
                data_operation=data_operation, git_repo=git_repo
            )

        self.__check_gh_pages_setup(git_repo=git_repo)
        git_repo.git.checkout(self.GH_PAGES_BRANCH_NAME)

        self.__update_data(data_operation=data_operation, silent_mode=silent_mode)

        if self.settings.auto_push:
            self.__push_branch(
                data_operation=data_operation,
                git_repo=git_repo,
                silent_mode=silent_mode,
            )

        git_repo.git.checkout(active_branch)

    def update_record_status_matrix(
        self,
        data_operation: colrev.ops.data.Data,  # pylint: disable=unused-argument
        synthesized_record_status_matrix: dict,
        endpoint_identifier: str,
    ) -> None:
        """Update the record_status_matrix"""

        # Note : automatically set all to True / synthesized
        for syn_id in synthesized_record_status_matrix:
            synthesized_record_status_matrix[syn_id][endpoint_identifier] = True

    def get_advice(
        self,
        review_manager: colrev.review_manager.ReviewManager,
    ) -> dict:
        """Get advice on the next steps (for display in the colrev status)"""

        data_endpoint = "Data operation [github pages data endpoint]: "

        advice = {"msg": f"{data_endpoint}", "detailed_msg": "TODO"}
        if "NA" == review_manager.dataset.get_remote_url():
            advice["msg"] += (
                "\n    - To make the repository available on Github pages, "
                + "push it to a Github repository\nhttps://github.com/new"
            )
        else:
            advice[
                "msg"
            ] += "\n    - The page is updated automatically (gh-pages branch)"

        return advice


if __name__ == "__main__":
    pass
