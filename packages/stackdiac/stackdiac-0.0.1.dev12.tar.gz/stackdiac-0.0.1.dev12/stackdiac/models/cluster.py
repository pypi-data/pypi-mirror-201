
import os
from urllib.parse import urlparse
from pydantic import BaseModel, parse_obj_as
import logging
from typing import Any
from deepmerge import always_merger

import yaml
from stackdiac.models.backend import Backend

from stackdiac.models.operation import Operation

from .stack import Stack

logger = logging.getLogger(__name__)

class ClusterStack(BaseModel):
    name: str | None = None
    src: str | None = None
    vars: dict[str, Any] = {}
    stack: Stack | None = None
    override: dict[str, Any] = {}
    backend: Backend | None = None
    operations: Any = {}
    
    class Config:
        arbitrary_types_allowed = True
        exclude = ["stack"]

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}:{self.name}>"

    def build(self, cluster, **kwargs):

        from stackdiac.stackd import sd

        if self.src is None:
            self.src = self.name

        # src is url with repo in scheme
        parsed_src = urlparse(self.src)
        if not parsed_src.scheme:
            parsed_src = urlparse(f"root:{self.src}") # add root repo
        if len(self.src.split("/")) == 1:
            parsed_src = urlparse(f"{parsed_src.scheme}:stack/{self.src}") # add stack dir

        repo = sd.conf.repos[parsed_src.scheme]

        if self.src.endswith(".yaml"):
            path = os.path.join(repo.repo_dir, parsed_src.path.lstrip("/"))           
        else:
            path = os.path.join(repo.repo_dir, parsed_src.path.lstrip("/"), "stack.yaml")
            

        url = parsed_src.geturl()
        logger.info(f"{self} building stack {self.name} in {cluster.name} {url} <- {path}")
        sdd = yaml.safe_load(open(path).read())
        sdd["name"] = sdd.get("name", self.name)
        
        
        if self.override:
            sdd = always_merger.merge(sdd, self.override)

        self.stack = parse_obj_as(Stack, sdd)
        logger.debug(f"{self} stack: {self.stack}")
        self.stack.build(cluster_stack=self, cluster=cluster, **kwargs)
        cluster.built_stacks[self.name] = self.stack

class Cluster(BaseModel):
    name: str
    vars: dict[str, Any] = {}    
    stacks: dict[str, ClusterStack] = {}
    built_stacks: dict[str, Stack] = {}
    backend: Backend | None = None
    

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        for sname, s in self.stacks.items():
            # s.cluster = self
            s.name = sname


    def build(self, stack="all", **kwargs):
        if stack == "all":
            for s in self.stacks.values():
                s.build(cluster=self, **kwargs)
        else:
            s = self.stacks[stack]
            s.build(cluster=self, **kwargs)
        

from stackdiac.api import app as api_app


@api_app.get("/clusters/", operation_id="get_clusters", response_model=list[Cluster])
async def _api_get_clusters() -> list[Cluster]:    
    from stackdiac.stackd import Stackd
    sd = Stackd()
    sd.configure()
    logger.debug(f"get_clusters: {sd.clusters['data'].dict()}")
    return list(sd.clusters.values())

@api_app.get("/build/{cluster_name}", operation_id="build_cluster", response_model=Cluster)
async def build_cluster(cluster_name:str) -> Cluster:
    """
    cluster.stacks will setup while bulding
    """
    from stackdiac.stackd import Stackd
    sd = Stackd()
    sd.configure()
    cluster = sd.clusters[cluster_name]
    cluster.build()    
    return cluster