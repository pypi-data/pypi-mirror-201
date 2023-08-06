# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
import typing as tp

from .._parser import Jinja2Parser
from .._parser import YamlParser
from .._proto_namespace import _ProtoNamespace
from ._03_meta import MetaMixin
from ._05_project import ProjectMixin
from ._06_dependency import DependencyMixin
from ._18_payload import PayloadMixin


class DockerMixin(PayloadMixin, DependencyMixin, ProjectMixin, MetaMixin):
    @classmethod
    def __keys(cls) -> tp.Tuple[str, ...]:
        return ("base_match", "platform", "compose_version")

    def templated(self) -> None:
        super().templated()
        data = self.auxcon.payload

        if self.is_enabled("pre-commit"):
            data.setdefault("with_dependency", _ProtoNamespace())
            run = "pre-commit"
            build = f"build-{run}"
            data.with_dependency[run] = dict(
                deps=[build], variant={"-all": dict(cmd="--all")}
            )
            data.with_dependency[build] = dict(deps=["build-python-deps"])

        if self.is_enabled("pytest"):
            data.setdefault("with_dependency", _ProtoNamespace())
            run = "pytest"
            build = f"build-{run}"
            data.with_dependency[build] = dict(deps=["build-python-deps"])
            data.with_dependency[run] = dict(deps=[build])
            if self.is_enabled("coverage"):
                data.with_dependency[run]["variant"] = {
                    "-mr": {"marker": ""},
                    "-cov": dict(coverage=95, variant={"-mr": None}),
                }

        if self.is_enabled("docs"):
            data.setdefault("with_dependency", _ProtoNamespace())
            data.with_dependency["docs"] = dict(param=dict(extra_req="docs"))

        if self.is_enabled("gitlab"):
            data.setdefault("docker_run", _ProtoNamespace())
            data.setdefault("python", _ProtoNamespace())
            data.docker_run["gitlab-release-run"] = _ProtoNamespace()
            data.python["gitlab-release"] = _ProtoNamespace()
            data.docker_run["pkg-gitlab"] = _ProtoNamespace()

    def demodata(self) -> None:
        super().demodata()
        data = self.auxcon.payload
        data.docker_settings = _ProtoNamespace(platform="amd64")

    def update_to_template(self, tpl: _ProtoNamespace, full: _ProtoNamespace) -> None:
        super().update_to_template(tpl, full)

        for flavor in ["docker_build", "docker_run", "with_dependency"]:
            if flavor not in self.auxf.payload:
                continue
            if flavor not in tpl.payload:
                continue
            data = self.auxf.payload[flavor]
            old = list(data)
            new = list(tpl.payload[flavor])
            last_idx = 0
            for name, payload in full.payload[flavor].items():
                if name in new and name not in old:
                    data[name] = payload
                    old.insert(last_idx + 1, name)
                    self._print(f"payload.{flavor}: added {name}", fg="green")
                elif name in old and name not in new:
                    del data[name]
                    old.remove(name)
                    self._print(f"payload.{flavor}: removed {name}", fg="red")
                if name in old and name in new:
                    last_idx = old.index(name)

    def formatted(self) -> None:
        super().formatted()
        self._copy_keys_over(self.__keys(), "payload", "docker_settings")
        self._to_proto_ns("payload", "docker_settings")
        self._to_proto_ns("payload", "docker_settings", "base_match", iter_mapping=True)

    def defaulted(self) -> None:
        super().defaulted()
        payload_data = self.auxd.payload
        payload_data.setdefault("docker_settings", _ProtoNamespace())
        data = payload_data.docker_settings
        data.setdefault("base_match", _ProtoNamespace())
        data.setdefault("platform", None)
        data.setdefault("compose_version", self.versions.docker_compose_file)

    def enriched(self) -> None:
        super().enriched()
        data = self.auxe.payload.docker_settings
        data.project_dir = "../.."
        data.source_dir = f"../../{self.auxe.project.source_dir}"
        self._docker_build_enrich()
        self._docker_run_enrich()

    def _docker_build_enrich(self) -> None:
        extra_req_default = {
            "python-deps": ["default"],
            "pytest": ["test"],
            "pre-commit": ["test", "dev"],
            "pytest-standalone": ["default", "test"],
            "docs": ["docs"],
            "ansible-deploy": ["deploy"],
        }
        deps = self.auxe.dependencies
        data = self.auxe.payload
        prefix = "build-"
        for key, payload_cfg in data.docker_build.items():
            assert key.startswith(prefix)
            name = key[len(prefix) :]
            payload_cfg.setdefault("param", _ProtoNamespace())
            param = payload_cfg.param
            if "extra_req" in param and isinstance(param.extra_req, str):
                param.extra_req = [param.extra_req]

            param.setdefault("pip_req", [])
            param.setdefault("script", [])
            param.setdefault("base", None)
            self._adjust_base_on_match_entry(param, self.auxe)

            param.setdefault("apt_req", {})

            self._set_name_and_version(param, name)

            if "mode" in param:
                supported = ["django", "django+nginx"]
                if param.mode not in supported:
                    raise RuntimeError(
                        f"mode {param.mode} is not supported {supported}"
                    )

            # branch matching and dep settings
            fallback = extra_req_default.get(param.docker_name, [])
            needed = param.get("extra_req", fallback)
            param.pip_req = self._unique_sum(
                param.pip_req, *[deps.get(x, []) for x in needed]
            )
            param.apt_req = self._unique_sum_dict(
                param.apt_req, *[deps.get(x + "_apt", {}) for x in needed]
            )
            param.script = self._sum(
                param.script, *[deps.get(x + "_script", []) for x in needed]
            )
            assert all('"' not in x for x in param.pip_req)

            if self.is_enabled("pip"):
                self.branch_match_and_cred_passing(param, self.auxe)  # type: ignore

    def _docker_run_enrich(self) -> None:
        data = self.auxe.payload
        for key, payload_cfg in data.docker_run.items():
            payload_cfg.setdefault("param", _ProtoNamespace())
            param = payload_cfg.param

            res = []
            if "assets" in param:
                if isinstance(param.assets, str):
                    param.assets = [param.assets]

                for x in param.assets:
                    shortname = x.rsplit("/", 1)[1]
                    url = "$CI_API_V4_URL/projects/$CI_PROJECT_ID/packages/generic/" + x
                    res.append(
                        r"{\"name\":\"" + shortname + r"\",\"url\":\"" + url + r"\"}"
                    )
            param.assets = res
            self._set_name_and_version(param, key)
            param.setdefault("services", [param.service_name])

    def _set_name_and_version(self, param: _ProtoNamespace, name: str) -> None:
        slug = self.auxe.project.slug
        param.service_name = name
        if param.service_name == slug:
            raise RuntimeError(
                f"service name should not be identical to project slug '{slug}'"
            )

        param.setdefault("image_name", f"{slug}-{param.service_name}")

        param.setdefault("docker_name", name)
        param.setdefault("version", self.auxe.project.minimal_version)
        if not isinstance(param.version, str):
            raise RuntimeError(
                f"please specity the version '{param.version}' in {name} as a string"
            )
        param.setdefault("version_slug", param.version.replace(".", ""))

    def _adjust_base_on_match_entry(
        self,
        opts: _ProtoNamespace,
        auxe: _ProtoNamespace,
    ) -> None:
        base_match = auxe.payload.docker_settings.base_match
        if opts.base is None:
            return
        image, tag = opts.base.rsplit(":", 1)
        if image not in base_match:
            return
        fallback = base_match[image].fallback
        var = (
            f'{image.upper().replace("/", "_").replace(".", "_").replace("-", "_")}_TAG'
        )
        skip = [auxe.gitlab.release_branch]

        # changing this order affects the jinja2 files!
        opts.base_match = [(image, var, skip, fallback, tag)]

        opts.base = f"{image}:${var}"

    def bake(self) -> None:  # pylint: disable=too-many-branches
        super().bake()
        data = self.auxe.payload
        settings = self.auxe.payload.docker_settings

        config = _ProtoNamespace(
            [("version", settings.compose_version), ("services", {})]
        )

        # pylint: disable=too-many-nested-blocks
        for val in data.docker_run.values():
            self._bake_docker_compose_file(val, config)

        for val in data.docker_build.values():
            self._bake_docker_build_file(val)
            self._bake_docker_compose_file(val, config)

        dest = self.target / "docker/compose.yml"
        written = YamlParser.write(config, dest)
        if written:
            self._print(f"baked {dest}", fg="green")

        # self._add_compositions(config)

    def _bake_docker_build_file(self, payload: _ProtoNamespace) -> None:
        """
        Return true if the file was a custom one.
        """
        opts = payload.param
        try:
            self.bake_file(
                f"docker/services/{opts.docker_name}/Dockerfile",
                f"docker/{opts.service_name}.dockerfile",
                opts=opts,
            )
            return
        except FileNotFoundError:  # then it must be custom
            pass

        self.bake_file(
            f"docker/{opts.docker_name}.dockerfile",
            f"docker/{opts.service_name}.dockerfile",
            custom=True,
            opts=opts,
        )

    def _bake_docker_compose_file(
        self, payload: _ProtoNamespace, config: _ProtoNamespace
    ) -> None:
        opts = payload.param
        src_dir = self.root / f"docker/services/{opts.docker_name}"
        srcj = src_dir / "docker-compose.yml.jinja2"
        custom_srcj = self.target_custom / "docker/compose.yml.jinja2"
        custom_src = self.target_custom / "docker/compose.yml"

        if srcj.exists():
            with Jinja2Parser.render_to_tmp(srcj, aux=self.auxe, opts=opts) as src:
                part = YamlParser.read(src).services
                self._update_config(payload, part, config)
                return
        elif custom_srcj.exists():
            with Jinja2Parser.render_to_tmp(
                custom_srcj, aux=self.auxe, opts=opts
            ) as src:
                custom_config = YamlParser.read(src)
        else:
            if not custom_src.exists():
                raise RuntimeError(
                    f"{custom_src} not found! Needed by {opts.docker_name}."
                )
            custom_config = YamlParser.read(custom_src)

        if list(custom_config.keys()) != ["services"]:
            raise RuntimeError(
                "only services can be defined in custom docker-compose.yml."
            )
        part = custom_config.services
        self._update_config(payload, part, config)

    def _update_config(
        self, payload: _ProtoNamespace, part: _ProtoNamespace, config: _ProtoNamespace
    ) -> None:
        for service_name, val in part.items():
            for key in list(val):
                if payload.flavor == "docker_build":
                    if key not in ["build", "image"]:
                        del val[key]
                elif payload.flavor == "docker_run":
                    if key in ["build"]:
                        del val[key]
                else:
                    raise NotImplementedError(payload.flavor)
            config["services"].setdefault(service_name, val)
            config["services"][service_name].update(val)

    # def _add_compositions(self, compose_all_config: _ProtoNamespace) -> None:
    #     data = self.auxe.docker
    #     for comp_name, comp in data.get("compositions", {}).items():
    #         # check validity and set defaults
    #         valid_keys = {"pre_build", "pre_script", "services", "overwrite"}
    #         invalid_keys = set(comp.keys()) - valid_keys
    #         if invalid_keys:
    #             raise RuntimeError(
    #                 f"invalid keys {invalid_keys} in composition '{comp_name}'. "
    #                 f"Valid key are {valid_keys}."
    #             )
    #         for key in valid_keys:
    #             comp.setdefault(key, [])
    #         comp.name = comp_name
    #         prefix = self.auxe.project.slug
    #         comp.services = [f"{prefix}-{key}" for key in comp.services]
    #         comp.pre_build = [f"{prefix}-{key}" for key in comp.pre_build]
    #         og_overwrite = comp.overwrite
    #         comp.overwrite = [f"../custom/docker/{key}" for key in comp.overwrite]
    #         for overwrite, file in zip(og_overwrite, comp.overwrite):
    #             search = (self.target / "docker" / file).resolve()
    #             if not search.exists():
    #                 raise RuntimeError(
    #                     f"overwrite file '{overwrite}' does not exist at '{search.relative_to(self.target.resolve().parent)}'"
    #                 )

    #         # docker-compose file
    #         config = copy.deepcopy(compose_all_config)
    #         config.services = {
    #             key: val
    #             for key, val in compose_all_config.services.items()
    #             if key in comp.services
    #         }
    #         config.setdefault("networks", {})
    #         config["networks"][f"{comp.name}-network"] = {}

    #         for val in config.services.values():
    #             val.setdefault("networks", [])
    #             val["networks"].append(f"{comp.name}-network")
    #         comp.compose_filename = f"{comp.name}-compose.yml"
    #         dest = self.target / f"docker/{comp.compose_filename}"
    #         written = YamlParser.write(config, dest)
    #         if written:
    #             self._print(f"baked {dest}", fg="green")

    #         # helper bash file
    #         self.bake_file(
    #             "docker/comp-helper.sh", f"docker/{comp.name}-compose.sh", comp=comp
    #         )

    @staticmethod
    def _unique_sum(*args: tp.List[str]) -> tp.List[str]:
        res = []
        for part in args:
            for x in part:
                if x not in res:
                    res.append(x)
        return res

    @staticmethod
    def _unique_sum_dict(
        *args: tp.Dict[str, tp.List[str]]
    ) -> tp.Dict[str, tp.List[str]]:
        res: tp.Dict[str, tp.List[str]] = {}
        for part in args:
            for key, val in part.items():
                res.setdefault(key, [])
                for x in val:
                    if x not in res[key]:
                        res[key].append(x)

        return res

    @staticmethod
    def _sum(*args: tp.List[str]) -> tp.List[str]:
        res = []
        for part in args:
            for x in part:
                res.append(x)
        return res
