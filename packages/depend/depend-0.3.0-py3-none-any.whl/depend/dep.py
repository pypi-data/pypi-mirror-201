from __future__ import annotations

from dataclasses import dataclass, field

from packaging.specifiers import SpecifierSet

from depend.helper import constraints_to_string, fix_constraint


@dataclass(unsafe_hash=True)
class Dep:
    language: str
    name: str
    _constraints: str = field(compare=False, hash=False)
    constraints: tuple[SpecifierSet] = field(init=False, default_factory=tuple)

    def __post_init__(self):
        self.constraints = fix_constraint(self.language, self.name, self._constraints)

    def __repr__(self):
        constraints = constraints_to_string(self.constraints)
        return f"Dep({self.language!r}, {self.name!r}, {constraints!r})"


@dataclass(unsafe_hash=True)
class RustDep(Dep):
    features: list[str] = field(default_factory=list, hash=False)


@dataclass(unsafe_hash=True)
class ResolvedDep:
    language: str
    name: str
    version: str
    dep: Dep
    _constraints: tuple[SpecifierSet] = field(repr=False, compare=False, hash=False)

    @classmethod
    def from_dep(cls, dep: Dep, version: str) -> ResolvedDep:
        return cls(dep.language, dep.name, version, dep, dep.constraints)
