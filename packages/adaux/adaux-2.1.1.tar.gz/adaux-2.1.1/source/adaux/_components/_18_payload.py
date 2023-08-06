# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
import collections
import copy
import dataclasses as dc
import importlib
import types
import typing as tp

from .._logging import logger
from .._proto_namespace import _ProtoNamespace
from .._yaml import yaml  # type: ignore
from ._05_project import ProjectMixin
from ._payload import DockerBuildPayload
from ._payload import DockerComposePayload
from ._payload import DockerRunPayload
from ._payload import Payload
from ._payload import PythonPayload
from ._payload import WithDependencyPayload


class PayloadMixin(ProjectMixin):
    @classmethod
    def __keys(cls) -> tp.Tuple[str, ...]:
        return ("docker_settings",) + tuple(cls.payload_types())

    @classmethod
    def payload_types(cls) -> tp.Dict[str, tp.Type[Payload]]:
        type_list: tp.List[tp.Type[Payload]] = [
            DockerBuildPayload,
            DockerRunPayload,
            PythonPayload,
            DockerComposePayload,
            WithDependencyPayload,  # must be at end for now
        ]
        return {x.flavor: x for x in type_list}

    @classmethod
    def level_map(cls) -> tp.Dict[str, int]:
        res = {}
        for flavor, val in cls.payload_types().items():
            res[flavor] = 0
            if val == WithDependencyPayload:
                res[flavor] = 1
        return res

    def templated(self) -> None:
        super().templated()
        self.auxcon.payload = _ProtoNamespace()

    def formatted(self) -> None:
        super().formatted()
        self._copy_keys_over(self.__keys(), "payload")
        for key in self.__keys():
            if key in ["docker_settings"]:
                continue  # handled by docker
            self._to_proto_ns("payload", key, iter_mapping=True)

        try:
            for val in self.auxf.payload.with_dependency.values():
                try:
                    if isinstance(val.deps, str):
                        val.deps = [val.deps]
                except KeyError:
                    pass
        except KeyError:
            pass

    def defaulted(self) -> None:
        super().defaulted()
        self.auxd.setdefault("payload", _ProtoNamespace())
        data = self.auxd.payload
        for key in self.__keys():
            if key in ["docker_settings"]:
                continue  # handled by docker
            data.setdefault(key, _ProtoNamespace())

        prefix = "build-"
        for payload_name, val in data.with_dependency.items():
            # param gets removed in enriched
            if payload_name.startswith(prefix):
                val.setdefault("deps", [])
            else:
                val.setdefault("deps", [f"{prefix}{payload_name}"])

            val.deps = val.deps or []
            val.setdefault("payload", payload_name)

    def enriched(self) -> None:
        super().enriched()
        data = self.auxe.payload

        self._add_absend_and_expand_variants(data)

        # helper parameter
        for flavor in self.payload_types():
            for payload_name, payload in data[flavor].items():
                payload.name = payload_name
                payload.flavor = flavor

        lookup_cfg: DoubleDict[_ProtoNamespace] = DoubleDict(self.level_map())
        for flavor in list(self.payload_types()):
            lookup_cfg.update(data[flavor], unique=True, flavor=flavor)

        for _, val in lookup_cfg.level("with_dependency").items():
            try:
                # we can specify the payload with flavor:name,
                # but if it is only name, the flavor will get deduced
                if ":" in val.payload:
                    pflv, pname = val.payload.split(":", 1)
                    # produce key error if not available
                    data[pflv][pname]  # pylint: disable=pointless-statement
                else:
                    payload_cfg = lookup_cfg[(val.payload, val.name, 1)]
                    val.payload = f"{payload_cfg.flavor}:{payload_cfg.name}"
            except KeyError as err:
                raise RuntimeError(
                    f"did not find matching payload for '{val.name}'. Ensure it exists or use the payload argument."
                ) from err

    def _add_absend_and_expand_variants(self, data: _ProtoNamespace) -> None:
        # resolve variants
        for flavor in self.payload_types():
            # we should only _add_if_absent after the lower levels
            # had a change to expand their variants
            if flavor == "with_dependency":
                for payload_name, val in data.with_dependency.items():
                    param = val.get("param", _ProtoNamespace())
                    for dep in val.deps:
                        self._add_if_absent(dep, param, data)

                    val.setdefault("payload", payload_name)
                    self._add_if_absent(val.payload, param, data)

            for service_name, val in list(data[flavor].items()):
                self._expand_variant(flavor, service_name, val)

        for payload_name, val in data.with_dependency.items():
            val.pop("param", _ProtoNamespace())

    def _add_if_absent(
        self,
        payload_name: str,
        param: _ProtoNamespace,
        data: _ProtoNamespace,
        after: tp.Optional[str] = None,
    ) -> None:
        # prevents having to write a service in docker_run,
        # docker_build, and in with_dependency
        check_flavors = [flv for flv, val in self.level_map().items() if val == 0]
        flavor = DockerRunPayload.flavor
        if payload_name.startswith("build-"):
            flavor = DockerBuildPayload.flavor

        if all(payload_name not in data[flv] for flv in check_flavors):
            val = _ProtoNamespace(param=copy.deepcopy(param))
            if after:
                data[flavor].insert_after(after, payload_name, val)
            else:
                data[flavor][payload_name] = val
            logger.info("added %s:%s automatically", flavor, payload_name)

    def _expand_variant(  # pylint: disable=too-many-arguments
        self,
        flavor: str,
        base_service_name: str,
        base_val: _ProtoNamespace,
        interfix: str = "",
        prefix_opts: tp.Optional[_ProtoNamespace] = None,
    ) -> None:
        data = self.auxe.payload
        base_variants = base_val.pop("variant", _ProtoNamespace())

        # sanatize base_variants
        base_variants = _ProtoNamespace(
            (interfix + key, val or _ProtoNamespace())
            for key, val in base_variants.items()
        )

        if not prefix_opts:
            # prefix opts allows us to reuse the settings of a
            # variant later again, i.e.
            # variant:
            #     -mr:
            #         bla: 1
            #     -39:
            #         version: "3.9"
            #         variant:
            #             -mr:
            #             # has automatically bla: 1
            prefix_opts = _ProtoNamespace(
                {interfix: base_val.get("param", _ProtoNamespace())}
            )

        # prepare the param object for the variants
        for fvariant, mod in base_variants.items():
            if interfix:
                variant = fvariant.split(interfix, 1)[1]
            else:
                variant = fvariant
            prefix_opts[fvariant] = copy.deepcopy(prefix_opts[interfix])
            if variant in prefix_opts and interfix != "":
                prefix_opts[fvariant].update(prefix_opts[variant])
                logger.info(
                    "%s -> applied %s %s variant options to %s variant",
                    base_service_name,
                    variant,
                    prefix_opts[variant],
                    fvariant,
                )
            prefix_opts[fvariant].update(mod)

        # create the variants
        for fvariant, mod in reversed(base_variants.items()):
            # do subvariants first
            subvariants = mod.pop("variant", _ProtoNamespace())
            base_val_mod = copy.deepcopy(base_val)
            base_val_mod.param = copy.deepcopy(prefix_opts[fvariant])
            base_val_mod.variant = subvariants
            self._expand_variant(
                flavor,
                base_service_name,
                base_val_mod,
                interfix=fvariant,
                prefix_opts=prefix_opts,
            )

            # then self and potential automatic payload
            val = copy.deepcopy(base_val)
            val.setdefault("param", _ProtoNamespace())
            val.param = prefix_opts[fvariant]
            val.param.pop("variant", None)

            if flavor == "with_dependency":
                param = val.param
                param.setdefault("docker_name", base_val.payload)
                param.image_name = self.auxe.project.slug + "-" + base_val.payload
                val.payload += fvariant
                self._add_if_absent(val.payload, param, data, base_service_name)
            if flavor == "python":
                val.setdefault("fct", base_service_name)

            # finally add it
            data[flavor].insert_after(
                base_service_name, base_service_name + fvariant, val
            )

    def hydrated(self) -> None:
        super().hydrated()
        # hydration
        lookup: DoubleDict[Payload] = DoubleDict(self.level_map())
        type_sel = self.payload_types()
        data = self.auxh.payload
        custom_ppyload = self._load_custom_ppyload()

        def create_payload(kwgs: _ProtoNamespace, flavor: str) -> Payload:
            kwgs.auxh = self.auxh
            if flavor == "python":
                kwgs.fct = PythonPayload.import_function(
                    kwgs.get("fct", kwgs.name), custom_ppyload
                )
            if flavor == "with_dependency":
                kwgs.deps = tuple(lookup[key] for key in kwgs.deps)
                assert all(isinstance(x, Payload) for x in kwgs.deps)
                kwgs.payload = lookup[kwgs.payload]
            try:  # see if it exists...
                res = lookup[kwgs.name]
                if res.flavor != flavor:
                    raise KeyError(kwgs.name)
            except KeyError:  # ...if not, create
                # remove helper variable
                kwgs.pop("flavor")
                res = type_sel[flavor](**kwgs)

            assert isinstance(res, Payload)
            lookup.update({key: res}, flavor=flavor, unique=True)
            return res

        for flavor in self.payload_types():
            for key, val in data[flavor].items():
                create_payload(val, flavor)
        data.lookup = lookup
        for val in lookup.level("with_dependency").values():
            val.hydrate()
        for val in lookup.level("docker_build").values():
            val.hydrate()

    def payload_run(self, *payloads: Payload, force: bool, dry: bool = False) -> bool:
        # pylint: disable=import-outside-toplevel
        from ._aux_ci import JobManager, CommonJob

        @dc.dataclass(frozen=True)
        class _PayloadJobImpl:
            payload: Payload
            force: bool

        @dc.dataclass(frozen=True)
        class PayloadJob(CommonJob, _PayloadJobImpl):
            def is_up_to_date(self, env: tp.Mapping[str, tp.Any]) -> bool:
                if self.force:
                    return False
                return self.payload.is_up_to_date()

            def script(self) -> None:
                self.payload.run(self.force)

            def is_included(self, env: tp.Mapping[str, tp.Any]) -> tp.Tuple[bool, str]:
                if isinstance(self.payload, DockerBuildPayload):
                    if self.payload.is_up_to_date() and not self.force:
                        return False, f"{self.payload.executor.tag} exists"
                    return True, f"missing {self.payload.executor.tag}"

                return super().is_included(env)

        jman = JobManager(env=dict(verbose=True))

        def demo(*pld: Payload) -> tp.List[PayloadJob]:
            jobs = []
            for pl in pld:
                if isinstance(pl, WithDependencyPayload):
                    parents = demo(*pl.deps)
                    name = pl.payload.name
                    if name in jman.jobs:
                        x = jman.jobs[name]
                    else:
                        x = jman.add_job(
                            PayloadJob,
                            payload=pl.payload,
                            force=force,
                            name=pl.payload.name,
                            parents=parents,
                        )
                    jobs.append(x)
                else:
                    name = pl.name
                    if name in jman.jobs:
                        x = jman.jobs[name]
                    else:
                        x = jman.add_job(
                            PayloadJob, payload=pl, force=force, name=pl.name
                        )
                    jobs.append(x)
            return jobs  # type: ignore

        demo(*payloads)

        if dry:
            jman.prune_unincluded(show=True)
        else:
            jman.run_pipeline()
            jman.show_result()

        if jman.has_failed_jobs():
            return False
        return True

    def _load_custom_ppyload(self) -> tp.Optional[types.ModuleType]:
        try:
            with self.preprend_to_sys_path(self.target / "custom/"):
                custom_ppyload = importlib.import_module("payload.python.functions")
                logger.info("custom python payloads found")
        except (ImportError, FileNotFoundError):
            custom_ppyload = None
            logger.info("custom python payloads NOT found")
        return custom_ppyload


X = tp.TypeVar("X")


@dc.dataclass
class DoubleDict(tp.Generic[X]):
    level_map: tp.Dict[str, int]
    level_dict: tp.Dict[int, tp.Dict[str, X]] = dc.field(
        default_factory=lambda: collections.defaultdict(dict)
    )

    def update(self, rhs: tp.Dict[str, X], flavor: str, unique: bool = False) -> None:
        level = self.level_map[flavor]
        if unique:
            lhs_keys = set(self.level_dict[level])
            rhs_keys = set(rhs)
            overlap = lhs_keys & rhs_keys
            if overlap:
                raise RuntimeError(f"keys {overlap} are not unique!")

        self.level_dict[level].update(rhs)

    def __getitem__(self, key_or_tuple: tp.Union[str, tp.Tuple[str, str, int]]) -> X:
        skip_level = -1  # -1: means nothing is skipped, first hit is returned
        if isinstance(key_or_tuple, tuple):
            key, reduce_match, skip_level = key_or_tuple
            assert ":" not in key
            assert ":" not in reduce_match
            if key != reduce_match:
                skip_level = -1
        else:
            key = key_or_tuple

        if ":" in key:
            flavor, key = key.split(":")
            level = self.level_map[flavor]
            return self.level_dict[level][key]

        for level in reversed(sorted(self.level_dict)):
            if key in self.level_dict[level]:
                if level != skip_level:
                    return self.level_dict[level][key]

        raise KeyError(key)

    def level(self, flavor: str) -> tp.Dict[str, X]:
        level = self.level_map[flavor]
        return self.level_dict[level]


def repr_double_dict(
    representer: tp.Any, data: tp.Any  # pylint: disable=unused-argument
) -> tp.Any:
    return representer.represent_str("n/a")


yaml.representer.add_representer(DoubleDict, repr_double_dict)
