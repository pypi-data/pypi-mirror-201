# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
import os
import typing as tp

from .._logging import logger
from .._proto_namespace import _ProtoNamespace
from .._util import ApiRequestCommunicator
from ._03_meta import MetaMixin
from ._18_payload import PayloadMixin


class CiMixin(PayloadMixin, MetaMixin):
    # pylint: disable=unused-private-member
    @classmethod
    def __keys(cls) -> tp.Tuple[str, ...]:
        return ("mechanism", "docker_image", "runner", "trigger", "use_adaux_img")

    def templated(self) -> None:
        super().templated()
        self.auxcon.ci = _ProtoNamespace(trigger=_ProtoNamespace())
        data = self.auxcon.ci.trigger
        data["+push"] = {
            "-openmr": {
                "-release": {"pre-commit": None, "pytest": None},
                "+release": {
                    "+gitlab": {
                        "gitlab-release": None,
                        "pkg-gitlab": None,
                        "pkg-pypi": None,
                    }
                },
            }
        }
        data["+mr"] = {
            "+draft": {
                "pre-commit": None,
                "pytest": None,
            },
            "-draft": {
                "pre-commit-all": None,
                "-vip": {
                    "pytest-mr": None,
                },
                "+vip": {
                    "pytest-cov-mr": None,
                },
            },
            "+release": {
                "check-release-notes": None,
            },
        }

    def demodata(self) -> None:
        super().demodata()
        self.auxcon.ci.runner = "dind-cached"
        self.auxcon.ci.mechanism = "mixed"

    def formatted(self) -> None:
        super().formatted()
        self._copy_keys_over(self.__keys(), "ci")

        for key in ["trigger"]:
            self._to_proto_ns("ci", key, iter_mapping=True)

    def defaulted(self) -> None:
        super().defaulted()
        self.auxd.setdefault("ci", _ProtoNamespace())
        data = self.auxd.ci

        data.setdefault("mechanism", "monolith")
        data.setdefault("runner", "normal")
        data.setdefault("docker_image", self.versions.ci_docker_image)
        data.setdefault("trigger", _ProtoNamespace())
        data.setdefault("use_adaux_img", True)
        assert data.trigger is not None
        assert data.mechanism in ["monolith"]
        assert data.runner in ["dind-cached", "normal"]

    # def update_to_template(self, tpl: _ProtoNamespace, full: _ProtoNamespace) -> None:
    #     super().update_to_template(tpl, full)

    #     data = self.auxd.ci.stages
    #     for key, stage in data.items():
    #         old = list(stage)
    #         new = list(tpl.ci.stages.get(key, {}))

    #         last_idx = 0
    #         for name, job in full.ci.stages.get(key, {}).items():
    #             if name in new and name not in old:
    #                 data.jobs.insert(last_idx + 1, job)
    #                 stage[name] = job
    #                 old.insert(last_idx + 1, name)
    #                 self._print(f"ci.jobs: added {name}", fg="green")
    #             elif name in old and name not in new:
    #                 del stage[name]
    #                 old.remove(name)
    #                 self._print(f"ci.jobs: removed {name}", fg="red")
    #             if name in old and name in new:
    #                 last_idx = old.index(name)

    def enriched(self) -> None:
        super().enriched()
        data = self.auxe.ci

        rule_used = _ProtoNamespace(
            mr=False,
            web=False,
            pipeline=False,
            schedule=False,
        )
        for reason in self._get_trigger_combos():
            for key in ["push", "push_no_mr"] + list(rule_used):
                if key in ["push", "push_no_mr"]:
                    if "+push" in reason:
                        rule_used.setdefault("push", False)
                        rule_used.setdefault("push_no_mr", True)
                        if "-openmr" not in reason:
                            rule_used["push_no_mr"] &= False
                            rule_used["push"] |= True
                else:
                    rule_used[key] |= f"+{key}" in reason

        data.used_rules = [key for key, val in rule_used.items() if val]

    # infuse shorthands
    # shorthand = dict(push=["push-no-mr", "mr"])
    # default_rules: tp.Dict[str, tp.List[str]] = {
    #     "rules": shorthand["push"] + ["web", "pipeline"],
    # }
    # for key in ["rules", "build-rules", "run-rules"]:
    #     res = []
    #     for rule in copy.deepcopy(val[key]):
    #         if rule in shorthand:
    #             val[key].remove(rule)
    #             res += shorthand[rule]
    #         else:
    #             res += [rule]
    #     if not val["rules"]:
    #         res = res or default_rules[key]
    #     val[key] = res

    # diff = set(val.keys()) - set(valid_opts_keys)
    # if diff:
    # raise RuntimeError(f"invalid options: {diff}")

    # data.setdefault("mechanism", "monolith")
    # data.setdefault("runner", "normal")
    # data.setdefault("docker_image", self.versions.ci_docker_image)
    # assert data.mechanism in ["monolith", "gitlab", "mixed"]
    # assert data.runner in ["dind-cached", "normal"]
    # yield auxcone

    def run_ci(self, trigger_str: str, dry: bool = False) -> int:
        if trigger_str == "gitlab":
            triggers = self._triggers_from_gitlab_ci()
        else:
            triggers = self._triggers_from_str(trigger_str)

        # get the payload_names
        payload_names = self._get_payload_names(triggers)

        self._print(f"triggers: {', '.join(triggers)}", fg="cyan")

        if not payload_names:
            self._print("no payloads selected", fg="yellow")
            return 0
        payloads = [self.auxh.payload.lookup[x] for x in payload_names]
        success = self.payload_run(*payloads, force=False, dry=dry)
        if success:
            if "+draft" in triggers:
                return 42
            return 0
        return 1

    def _triggers_from_gitlab_ci(self) -> tp.Sequence[str]:
        triggers = []

        def env(key: str) -> str:
            return os.environ.get(key, "")

        gitlab2adaux = {
            "push": "+push",
            "merge_request_event": "+mr",
            "web": "+web",
            "pipeline": "+pipeline",
            "schedule": "+schedule",
        }
        source_trigger = gitlab2adaux[env("CI_PIPELINE_SOURCE")]
        triggers.append(source_trigger)

        if env("CI_COMMIT_TAG") != "":
            assert source_trigger == "+push"
            source_trigger = "+tag"
        if env("CI_OPEN_MERGE_REQUESTS") != "":
            triggers.append("+openmr")
            # we dont care abound env("CI_OPEN_MERGE_REQUESTS") in push
            # draft is only an option for mr lines

        mr_iid = env("CI_MERGE_REQUEST_IID")
        if mr_iid != "":
            try:
                resp = self.get_mr_status(mr_iid)
                if resp["draft"]:
                    triggers.append("+draft")
                    logger.info("merge request %s is a draft", mr_iid)
                else:
                    logger.info("merge request %s is NOT a draft", mr_iid)
            except RuntimeError as err:
                self._print(
                    f"could not access gitlab api for checking mr draft ({err.args[0]})",
                    fg="red",
                )

        if source_trigger == "+push":
            branch = env("CI_COMMIT_BRANCH")
        elif source_trigger == "+mr":
            branch = env("CI_MERGE_REQUEST_TARGET_BRANCH_NAME")

        gitlab = self.auxh.gitlab
        if branch in gitlab.vip_branches:
            triggers.append("+vip")
        if branch == gitlab.default_branch:
            triggers.append("+default")
        if branch == gitlab.release_branch:
            triggers.append("+release")

        branch_trigger = f"+{branch}"
        if branch_trigger not in triggers:
            triggers.append(branch_trigger)

        triggers.append("+gitlab")
        return triggers

    def get_mr_status(self, mr_iid: str) -> tp.Dict[str, tp.Any]:
        coord = [
            "projects",
            os.environ["CI_PROJECT_ID"],
            "merge_requests",
            mr_iid,
        ]
        api = ApiRequestCommunicator()
        token = os.environ["GITLAB_READ_API"]
        api.headers = {"PRIVATE-TOKEN": token}
        api.base_url = "https://" + os.environ["CI_SERVER_HOST"]
        return api.api_request(*coord)  # type: ignore

    def _triggers_from_str(self, trigger_str: str) -> tp.Sequence[str]:
        if trigger_str[0] not in "+-":
            trigger_str = f"+{trigger_str}"

        triggers = []
        old = 0
        for i, char in enumerate(trigger_str):
            if char in "+-":
                triggers.append(trigger_str[old:i])
                old = i
        triggers.append(trigger_str[old:])
        waste = triggers.pop(0)
        assert waste == ""
        return triggers

    def _get_payload_names(self, triggers: tp.Sequence[str]) -> tp.Sequence[str]:
        res = []
        for payload_name, reason in self._get_payload_names_and_reason(triggers):
            logger.info("%s included due to %s", payload_name, "".join(reason))
            res.append(payload_name)
        return res

    def _get_payload_names_and_reason(
        self, triggers: tp.Sequence[str], collect_all: bool = False
    ) -> tp.Sequence[tp.Tuple[str, tp.Tuple[str, ...]]]:
        payload_names_reason = []
        data = self.auxe.ci.trigger

        def dig(data: _ProtoNamespace, reason: tp.Tuple[str, ...]) -> None:
            for key, val in data.items():
                if key.startswith("-"):
                    pos_key = key.replace("-", "+")
                    if pos_key not in triggers or collect_all:
                        dig(val, reason + (key,))
                elif key.startswith("+"):
                    if key in triggers or collect_all:
                        dig(val, reason + (key,))
                else:
                    payload_names_reason.append((key, reason))

        dig(data, tuple())

        return payload_names_reason

    def _get_trigger_combos(self) -> tp.Sequence[tp.Tuple[str, ...]]:
        reasons = set()
        for _, reason in self._get_payload_names_and_reason([], collect_all=True):
            reasons.add(reason)
        return list(reasons)

    def bake(self) -> None:  # pylint: disable=too-many-branches,too-many-locals
        super().bake()
        data = self.auxe.ci
        base_files = ["00-main.yml", "01-rules.yml"]
        assert data.mechanism == "monolith"

        for filename in base_files:
            self.bake_file(f"CI/{filename}")
